import sys
import netchecker
import modules.misc.utils as utils
from modules.color.ansi_codes import RESET, RED, GREEN


def test_internet():
    has_internet = netchecker.has_internet(ping_count=2)
    has_dns = netchecker.has_dns()

    if not has_internet:
        utils.clear_screen()
        print(f"{RED}{'=' * 56}{RESET}")
        print("          Failure: Internet Connection Test Failed.          ")
        print("Please make sure that you have a working internet connection.")
        print(f"{RED}{'=' * 56}{RESET}")
        input(f"{GREEN}\nPress any key to exit...{RESET}")
        sys.exit(1)

    if not has_dns:
        utils.clear_screen()
        print(f"{RED}{'=' * 56}{RESET}")
        print("               Failure: DNS Resolution Failed.               ")
        print("Please make sure that you have a working internet connection.")
        print(f"{RED}{'=' * 56}{RESET}")
        input(f"{GREEN}\nPress any key to exit...{RESET}")
        sys.exit(1)
