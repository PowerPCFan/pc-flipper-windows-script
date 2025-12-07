import subprocess
import os
import modules.misc.global_vars as global_vars
import modules.misc.utils as utils
from modules.color.ansi_codes import RESET, RED
from packaging.version import parse as parse_version


class WingetTools:
    def __init__(self) -> None:
        self.PACKAGES_DIR = utils.ensure_dir_exists(
            os.path.join(global_vars.SCRIPT_TEMP, "packages")
        )
        self.WINUI_URL = "https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.8.6/Microsoft.UI.Xaml.2.8.x64.appx"  # noqa: E501
        self.WINUI_MIN_VERSION_STRING = "8.2310.30001.0"
        self.WINUI_MIN_VERSION = parse_version(self.WINUI_MIN_VERSION_STRING)

    def install_winui_2_8(self):
        """
        Installs/updates WinUI 2.8 to the minimum required version.
        """

        version_architecture_lines: list[str] = (
            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    'Get-AppxPackage -Name "Microsoft.UI.Xaml.2.8" | Select-Object Version, Architecture',
                ],
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .splitlines()
        )

        parsed_versions: list[str] = []

        for line in version_architecture_lines:
            parts = line.split()

            if len(parts) == 2:
                ver_str, arch = parts

                if arch.lower() == "x64":
                    try:
                        parse_version(ver_str)
                        parsed_versions.append(ver_str)
                    except Exception:
                        pass

        installed_version = (
            max(parsed_versions, key=parse_version) if parsed_versions else None
        )

        if (
            installed_version is None
            or parse_version(installed_version) < self.WINUI_MIN_VERSION
        ):
            # current version is outdated or winui 2.8 is not installed whatsoever

            local_path = os.path.join(self.PACKAGES_DIR, "Microsoft_UI_Xaml_2_8.appx")
            utils.download_large_file(url=self.WINUI_URL, destination=local_path)

            try:
                install = subprocess.run(
                    ["powershell", "-Command", f'Add-AppxPackage "{local_path}"'],
                    check=True,
                )

                if install.returncode != 0:
                    # raise exception on non-zero exit code just in case check=True doesnt catch it
                    raise Exception("Process exited with a non-zero exit code.")
            except Exception as e:
                print(f"{RED}Error installing WinUI 2.8: {e}{RESET}")
                return

    def fix_winget(self):
        subprocess.run(["winget", "source", "remove", "-n", '"winget"'])

        subprocess.run([
            "winget",
            "source",
            "add",
            "-n",
            '"winget"',
            "-a",
            '"https://cdn.winget.microsoft.com/cache"',
        ])

    def install_winget(self):
        try:
            url = "https://aka.ms/getwinget"
            file_path = os.path.join(self.PACKAGES_DIR, "winget_installer.msixbundle")

            utils.download_large_file(url=url, destination=file_path, chunk_size=8192)

            subprocess.run(
                args=[
                    "powershell.exe",
                    "-Command",
                    f'$filePath = "{file_path}"; Add-AppxPackage $filePath',
                ],
                check=True,
            )
        except Exception as e:
            print(f"{RED}Error installing WinGet: {e}{RESET}")

    def test_winget(self) -> dict[str, str | bool]:
        try:
            result = subprocess.run(
                [
                    "winget",
                    "search",
                    "notepad",
                    "--source",
                    "winget",
                ],  # winget search notepad --source winget
                check=False,  # we do not want errors to be automatically raised by subprocess.run
                capture_output=True,
                text=True,
            )

            winget_error: str = result.stderr + result.stdout

            is_winget_source_bug = (
                "0x8a15000f" in winget_error
                and "Data required by the source is missing" in winget_error
            )

            return {
                "Success": result.returncode == 0,
                "WingetSourceBug": is_winget_source_bug,
                "ErrorMessage": winget_error.strip(),
            }

        except Exception as e:
            return {
                "Success": False,
                "WingetSourceBug": False,
                "ErrorMessage": f"An unexpected error occurred while testing WinGet functionality: {e}",
            }


class Winget:
    def install(self, id: str, params: str | None = None) -> bool:
        """
        Installs a package using winget.

        :param id: The ID of the package to install.
        :param params: Additional parameters for the installation command.
        :return: True if the installation was successful, False otherwise.
        :raises subprocess.CalledProcessError: If the installation command fails.
        """

        cmd = ["winget", "install", "--id", id]

        if params is not None:
            cmd.extend(params.split())

        try:
            result = subprocess.run(
                cmd,
                check=True,
                # capture_output=True,
                # text=True
            )

            if result.returncode != 0:
                raise Exception(
                    f"The command {''.join(cmd)} exited with a non-zero status code."
                )

            return (
                result.returncode == 0
            )  # True if the exit code is 0 (successful install)

        except subprocess.CalledProcessError as e:
            print(e.stderr)
            return False
        except Exception as e:
            print(f"{RED}An error occurred while trying to install {id}: {e}")
            return False
