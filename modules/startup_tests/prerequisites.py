import subprocess
from modules.winget import Winget, WingetTools
from modules.color.ansi_codes import RESET, RED, GREEN, CYAN, YELLOW
from packaging.version import parse as parse_version

# global class instances
winget = Winget()
winget_tools = WingetTools()


class WingetNotInstalledError(Exception):
    pass


def _winget_installed_and_winget_version() -> tuple[bool, str | None]:
    try:
        output = subprocess.run(["winget", "--version"], check=True, capture_output=True, text=True)

        if output.returncode != 0:
            raise Exception("Process exited with a non-zero exit code.")

        return True, output.stdout.strip()
    except Exception:
        return False, None


def _winget_outdated(version: str) -> bool:
    winget_version = parse_version(version)
    min_version = parse_version("1.6")  # consider <1.6 "outdated"

    return winget_version < min_version


def check_prerequisites() -> None:
    # WinGet
    try:
        winget_installed, winget_version = _winget_installed_and_winget_version()

        if not winget_installed or winget_version is None:
            raise WingetNotInstalledError()

        print(f"{GREEN}WinGet is already installed.{RESET}")

        if _winget_outdated(winget_version):
            print(f"{YELLOW}WinGet version {winget_version} is outdated. Installing latest version...{RESET}")
            print(f"{CYAN}This can take a while. Please be patient.{RESET}")
            try:
                winget_tools.install_winget()
                print(f"{GREEN}WinGet updated successfully.{RESET}")
            except Exception as e:
                print(f"{RED}Error updating WinGet: {e}{RESET}")
        else:
            print(f"{GREEN}WinGet version {winget_version} is sufficient.{RESET}")

    except WingetNotInstalledError:
        print(f"{YELLOW}WinGet not installed. Installing WinGet...{RESET}")
        try:
            winget_tools.install_winget()
            print(f"{GREEN}WinGet installed successfully.{RESET}")
        except Exception as e:
            print(f"{RED}Error installing WinGet: {e}{RESET}")

    print("Checking WinGet functionality...")
    test_result = winget_tools.test_winget()

    # WinGet working normally - exit early
    if test_result["Success"]:
        print(f"{GREEN}WinGet is functioning correctly.{RESET}")
        return

    # Check for the specific error we know how to fix
    if test_result["WingetSourceBug"]:
        print("Known Error Detected! Running first fix...")
        winget_tools.fix_winget()
        print(f"{GREEN}Fix applied. Testing WinGet...{RESET}")

        test_result = winget_tools.test_winget()
        if test_result["Success"]:
            print(f"{GREEN}Fix was successful!{RESET}")
            return

        # If first fix failed, try the second fix
        if test_result["WingetSourceBug"]:
            print("Error detected again. Applying alternative fix...")
            winget_tools.install_winget()
            print(f"{GREEN}Alternative fix applied. Testing WinGet...{RESET}")

            test_result = winget_tools.test_winget()

            if test_result["Success"]:
                print(f"{GREEN}Alternative fix was successful!{RESET}")
                return

            # If second fix also failed
            if test_result["WingetSourceBug"]:
                print(f"{RED}All repair attempts failed. Apps may not install properly.{RESET}")
                return

        print(f"{RED}Unexpected error after repair attempt: {test_result['ErrorMessage']}{RESET}")
        return
    else:
        print(f"{RED}Unknown WinGet error occurred: {test_result['ErrorMessage']}{RESET}")
