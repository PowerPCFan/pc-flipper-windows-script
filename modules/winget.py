import subprocess
import os
import modules.misc.global_vars as global_vars
import modules.misc.utils as utils
from modules.color.ansi_codes import RESET, RED


class WingetTools:
    def fix_winget(self):
        subprocess.run([
            "winget", 
            "source", 
            "remove", 
            "-n", 
            '"winget"'
        ])
        
        subprocess.run([
            "winget", 
            "source", 
            "add", 
            "-n", 
            '"winget"',
            "-a", 
            '"https://cdn.winget.microsoft.com/cache"'
        ])

    def install_winget(self):
        try:
            url = "https://aka.ms/getwinget"
            path = utils.ensure_dir_exists(os.path.join(global_vars.SCRIPT_TEMP, "packages"))
            file_path = os.path.join(path, "winget_installer.msixbundle")

            utils.download_large_file(url=url, destination=file_path, chunk_size=8192)
            
            subprocess.run(
                args=[
                    "powershell.exe",
                    "-Command",
                    f'$filePath = "{file_path}"; Add-AppxPackage $filePath'
                ],
                check=True
            )
        except Exception as e:
            print(f"{RED}Error installing Winget: {e}{RESET}")
            
    def test_winget(self) -> dict:
        # original powershell function:

        #     $wingetError = winget search notepad --source winget 2>&1
        #     $isSuccess = $LASTEXITCODE -eq 0
        #     $isWingetSourceBug = ($wingetError -match "0x8a15000f" -and $wingetError -match "Data required by the source is missing")
            
        #     return @{
        #         Success = $isSuccess
        #         WingetSourceBug = $isWingetSourceBug
        #         ErrorMessage = $wingetError
        #     }
        
        try:
            result = subprocess.run(
                ["winget", "search", "notepad", "--source", "winget"],  # winget search notepad --source winget
                check=False,  # we do not want errors to be automatically raised by subprocess.run
                capture_output=True,
                text=True
            )
            
            winget_error = result.stderr + result.stdout
            
            is_success = result.returncode == 0
            
            is_winget_source_bug = (
                "0x8a15000f" in winget_error and
                "Data required by the source is missing" in winget_error
            )

            return {
                "Success": is_success,
                "WingetSourceBug": is_winget_source_bug,
                "ErrorMessage": winget_error.strip()
            }

        except Exception as e:
            return {
                "Success": False,
                "WingetSourceBug": False,
                "ErrorMessage": f"An unexpected error occurred while testing WinGet functionality: {e}"
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
                raise Exception(f"The command {''.join(cmd)} exited with a non-zero status code.")

            return result.returncode == 0  # True if the exit code is 0 (successful install)
        
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            return False
        except Exception as e:
            print(f"{RED}An error occurred while trying to install {id}: {e}")
            return False
