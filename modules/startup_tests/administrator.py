import ctypes
import subprocess
import sys
import os
import modules.misc.utils as utils
from modules.color.ansi_codes import RESET, RED, GREEN


def relaunch_as_admin():
    subprocess.run([
        "powershell.exe",
        "-Command",
        f"Start-Process powershell.exe -ArgumentList '-NoExit', '-Command', '\"{sys.executable}\" \"{os.path.abspath(sys.argv[0])}\"' -Verb RunAs"  # noqa: E501
    ])

    sys.exit(0)


def exit_script_with_code_1():
    sys.exit(1)


def test_admin_privileges():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        utils.clear_screen()

        failure_message = "Failure: Current permissions inadequate: Script not running as administrator."
        border = f"{RED}{'=' * len(failure_message)}{RESET}"

        print(border)
        print(f"{RED}{failure_message}{RESET}")
        print(border)

        print("")
        print("Please select an action:")
        print(f"    {GREEN}[R]{RESET} Relaunch as administrator")
        print(f"    {RED}[E]{RESET} Exit")

        print("\n>>> ", end="", flush=True)

        utils.get_user_choice2(
            options={
                "R": relaunch_as_admin,
                "E": exit_script_with_code_1
            },
            default=exit_script_with_code_1
        )
