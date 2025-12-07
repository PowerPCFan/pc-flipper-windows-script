import os
import requests
import subprocess
import time
import modules.misc.utils as utils
import modules.misc.global_vars as global_vars
from modules.color.ansi_codes import RED, RESET, CYAN, GREEN, YELLOW


class ChipsetDrivers:
    def __init__(self) -> None:
        self.driver_download_path: str = utils.ensure_dir_exists(os.path.join(global_vars.SCRIPT_TEMP, "drivers", "chipset"))  # noqa: E501

        self.amd_driver_download_path: str = utils.ensure_dir_exists(os.path.join(self.driver_download_path, "amd"))
        self.intel_driver_download_path: str = utils.ensure_dir_exists(os.path.join(self.driver_download_path, "intel"))

        self.amd_driver_download_link: str = requests.get("https://raw.githubusercontent.com/notFoxils/AMD-Chipset-Drivers/refs/heads/main/configs/link.txt").text.strip()  # noqa: E501
        self.intel_driver_download_link: str = "https://downloadmirror.intel.com/843223/SetupChipset.exe"

    def install_amd_drivers(self):
        print(f"{CYAN}AMD CPU detected. Chipset drivers downloading and installing...{RESET}")

        driver_path = os.path.join(self.amd_driver_download_path, "chipset_amd.exe")

        utils.download_large_file(
            url=self.amd_driver_download_link,
            destination=driver_path,
            headers={
                "Referer": "https://www.amd.com/en/support/download/drivers.html"
            },
            timeout=10
        )

        print(f"{GREEN}AMD chipset drivers successfully downloaded. Starting installer...{RESET}")
        if os.path.exists(driver_path):
            output = subprocess.run([driver_path])

            if output.returncode == 0:
                while utils.process_is_running("chipset_amd.exe") or utils.process_is_running("amd_chipset_drivers.exe") or utils.process_is_running("Setup.exe"):  # noqa: E501
                    time.sleep(5)

                print(f"{GREEN}AMD chipset drivers installed successfully.{RESET}")
            else:
                print(f"{YELLOW}Warning: The AMD chipset driver installer closed with exit code {output.returncode}. This may indicate that something went wrong.{RESET}")  # noqa: E501
        else:
            print(f"{RED}Error: AMD chipset driver installer not found at {driver_path}.{RESET}")

    def install_intel_drivers(self):
        print(f"{CYAN}Intel CPU detected. Chipset drivers downloading and installing...{RESET}")

        driver_path = os.path.join(self.intel_driver_download_path, "chipset_intel.exe")

        utils.download_large_file(
            url=self.intel_driver_download_link,
            destination=driver_path,
            timeout=10
        )

        print(f"{GREEN}Intel chipset drivers successfully downloaded. Starting installer...{RESET}")
        if os.path.exists(driver_path):
            output = subprocess.run([driver_path])

            if output.returncode == 3010:
                print(f"{GREEN}Intel chipset drivers installed successfully. A reboot is required for proper functionality.{RESET}")  # noqa: E501
            elif output.returncode == 0:
                print(f"{GREEN}Intel chipset drivers installed successfully.{RESET}")
            else:
                print(f"{YELLOW}Warning: The Intel chipset driver installer closed with exit code {output.returncode}. This may indicate that something went wrong.{RESET}")  # noqa: E501
        else:
            print(f"{RED}Error: Intel chipset driver installer not found at {driver_path}.{RESET}")


def install_chipset_drivers():
    cpu = global_vars.CPU.lower()
    drivers = ChipsetDrivers()

    if "amd" in cpu:
        drivers.install_amd_drivers()
    elif "intel" in cpu:
        drivers.install_intel_drivers()
    else:
        response = utils.detection_error(
            title="Chipset Detection Error",
            resizable=False,
            message="Error detecting chipset.\nWhat brand is your CPU?",
            names=["AMD", "Intel", "Other"]
        )

        response = response.lower() if response is not None else response

        if response == "amd":
            drivers.install_amd_drivers()
        elif response == "intel":
            drivers.install_intel_drivers()
        elif response == "other":
            print("You selected \"Other\", which means your CPU is currently unsupported. Please download the appropriate chipset drivers manually.")  # noqa: E501
            time.sleep(5)
        else:
            print(f"{RED}There was an error collecting your response. Continuing without installing chipset drivers...{RESET}")  # noqa: E501
            time.sleep(5)
