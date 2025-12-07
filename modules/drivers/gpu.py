import os
import requests
import subprocess
import time
import modules.misc.utils as utils
import modules.drivers.nvidia_gpu_drivers as nvidia_drivers
import modules.misc.global_vars as global_vars
import urllib.parse
from modules.color.ansi_codes import RED, RESET, CYAN, GREEN, YELLOW


class GPUDrivers:
    def __init__(self) -> None:
        self.driver_download_path: str = utils.ensure_dir_exists(
            os.path.join(global_vars.SCRIPT_TEMP, "drivers", "gpu"))

        self.amd_driver_download_path: str = utils.ensure_dir_exists(
            os.path.join(self.driver_download_path, "amd")
        )
        self.intel_arc_driver_download_path: str = utils.ensure_dir_exists(
            os.path.join(self.driver_download_path, "intel_arc")
        )
        self.nvidia_driver_download_path: str = utils.ensure_dir_exists(
            os.path.join(self.driver_download_path, "nvidia")
        )

        self.amd_driver_download_link: str = ""
        try:
            link: str = requests.get("https://raw.githubusercontent.com/nunodxxd/AMD-Software-Adrenalin/refs/heads/main/configs/config.json").json()["driver_links"]["stable"]  # noqa: E501
            hostname: str | None = urllib.parse.urlparse(link).hostname
            if hostname is not None and hostname.endswith("amd.com"):
                self.amd_driver_download_link = link
            else:
                raise ValueError("non-AMD domain detected, falling back to version 25.6.1 due to malware risk with non AMD domain")  # i know this line won't be printed but i figured i'd still describe what's happening  # noqa: E501
        except Exception:
            self.amd_driver_download_link = "https://drivers.amd.com/drivers/installer/25.10/whql/amd-software-adrenalin-edition-25.6.1-minimalsetup-250602_web.exe"  # noqa: E501

        self.intel_driver_download_link: str = requests.get("https://raw.githubusercontent.com/PowerPCFan/Intel-Arc-GPU-Drivers/refs/heads/main/configs/link.txt").text.strip()  # noqa: E501

    def install_nvidia_drivers(self):
        print(f"{CYAN}Nvidia GPU detected.{RESET}")
        print("A window will pop up asking you to select your GPU, OS, language, and the driver you'd like to install.")

        result = nvidia_drivers.main()

        if result is None:
            print(f"{YELLOW}Warning: No driver was selected. Skipping Nvidia driver installation...{RESET}")
        else:
            name: str | None = result.get("name")
            version: str | None = result.get("version")
            download_link: str | None = result.get("download_url")

            if download_link:
                print(f"{CYAN}Installing {name if name else 'Nvidia GPU Driver'} version {version if version else 'unknown'}...{RESET}")  # noqa: E501

                nvidia_driver = os.path.join(self.nvidia_driver_download_path, "setup.exe")

                utils.download_large_file(
                    url=download_link,
                    destination=nvidia_driver,
                    timeout=10
                )

                print(f"{GREEN}Nvidia GPU drivers successfully downloaded.{RESET}")

                if os.path.exists(nvidia_driver):
                    output = subprocess.run([nvidia_driver])

                    if output.returncode == 0:
                        print(f"{GREEN}Nvidia GPU drivers installed successfully.{RESET}")
                    else:
                        print(f"{YELLOW}Warning: The Nvidia GPU driver installer closed with exit code {output.returncode}. This may indicate that something went wrong.{RESET}")  # noqa: E501
                else:
                    print(f"{RED}Error: Nvidia driver installer not found at {nvidia_driver}.{RESET}")
            else:
                print(f"{RED}Error: Download link not found for selected driver. Skipping Nvidia driver installation...{RESET}")  # noqa: E501

    def install_amd_drivers(self):
        print(f"{CYAN}AMD GPU detected. Drivers downloading and installing...{RESET}")

        amd_drivers = os.path.join(self.amd_driver_download_path, "setup.exe")

        utils.download_large_file(
            url=self.amd_driver_download_link,
            destination=amd_drivers,
            headers={
                "Referer": "https://www.amd.com/en/support/download/drivers.html"
            },
            timeout=10
        )

        print(f"{GREEN}AMD GPU drivers successfully downloaded.{RESET}")

        if os.path.exists(amd_drivers):
            output = subprocess.run([amd_drivers])

            if output.returncode == 0:
                while utils.process_is_running("amdsoftwareinstaller.exe"):
                    time.sleep(5)

                print(f"{GREEN}AMD GPU drivers installed successfully.{RESET}")
            else:
                print(f"{YELLOW}Warning: The AMD GPU driver installer closed with nonzero exit code {output.returncode}. This may indicate that something went wrong.{RESET}")  # noqa: E501
        else:
            print(f"{RED}Error: AMD driver installer not found at {amd_drivers}.{RESET}")

    def install_intel_arc_drivers(self):
        print(f"{CYAN}Intel Arc GPU detected. Drivers downloading and installing...{RESET}")

        intel_drivers = os.path.join(self.intel_arc_driver_download_path, "setup.exe")

        utils.download_large_file(
            url=self.intel_driver_download_link,
            destination=intel_drivers,
            timeout=10
        )

        print(f"{GREEN}Intel Arc GPU drivers successfully downloaded.{RESET}")

        if os.path.exists(intel_drivers):
            output = subprocess.run([intel_drivers])

            if output.returncode == 0:
                print(f"{GREEN}Intel Arc GPU drivers installed successfully.{RESET}")
            else:
                print(f"{YELLOW}Warning: The Intel Arc GPU driver installer closed with exit code {output.returncode}. This may indicate that something went wrong.{RESET}")  # noqa: E501
        else:
            print(f"{RED}Error: Intel Arc driver installer not found at {intel_drivers}.{RESET}")


def install_gpu_drivers():
    gpu = global_vars.GPU.lower()
    drivers = GPUDrivers()

    if "geforce" in gpu or "nvidia" in gpu:
        drivers.install_nvidia_drivers()
    elif "amd" in gpu or "radeon" in gpu:
        drivers.install_amd_drivers()
    elif "intel" in gpu and "arc" in gpu:
        drivers.install_intel_arc_drivers()
    else:
        response = utils.detection_error(
            title="GPU Detection Error",
            resizable=False,
            message="Error detecting GPU.\nWhat brand is your GPU?",
            names=["AMD", "Nvidia", "Intel Arc", "Other"]
        )

        if response is not None:
            response = response.lower()

        # Act on responses.
        if response == "amd":
            drivers.install_amd_drivers()
        elif response == "nvidia":
            drivers.install_nvidia_drivers()
        elif response == "intelarc":
            drivers.install_intel_arc_drivers()
        elif response == "other":
            print("You selected \"Other\", which means your GPU is currently unsupported. Please download the appropriate drivers manually.")  # noqa: E501
            time.sleep(5)
        else:
            print(f"{RED}There was an error collecting your response. Continuing without installing GPU drivers...{RESET}")  # noqa: E501
            time.sleep(5)
