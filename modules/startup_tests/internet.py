# import sys
# import socket
# import subprocess
# import modules.misc.utils as utils
# from modules.color.ansi_codes import RESET, RED, GREEN


# def has_network(ips, count=1):
#     for ip in ips:
#         try:
#             result = subprocess.run(
#                 ['ping', '-n', str(count), ip],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL
#             )
#             if result.returncode == 0:
#                 return True
#         except Exception:
#             continue
#     return False


# def has_dns(domains):
#     for domain in domains:
#         try:
#             socket.gethostbyname(domain)
#             return True
#         except socket.gaierror:
#             continue
#     return False


# def test_internet():
#     MY_IPS = [
#         "8.8.8.8",
#         "1.1.1.1",
#         "9.9.9.9",
#         # "8.8.4.4",
#         # "1.0.0.1"
#     ]

#     MY_DOMAINS = [
#         "www.github.com",
#         "www.google.com",
#         "www.cloudflare.com",
#         # "www.microsoft.com"
#     ]

#     if not has_network(ips=MY_IPS, count=2):
#         utils.clear_screen()
#         print(f"{RED}{'=' * 56}{RESET}")
#         print("        Failure: Internet Connection Test Failed.       ")
#         print("Please make sure that you are connected to the Internet.")
#         print(f"{RED}{'=' * 56}{RESET}")
#         input(f"{GREEN}\nPress any key to exit...{RESET}")
#         sys.exit(1)

#     if not has_dns(domains=MY_DOMAINS):
#         utils.clear_screen()
#         print(f"{RED}{'=' * 56}{RESET}")
#         print("             Failure: DNS Resolution Failed.            ")
#         print("Please make sure that you are connected to the Internet.")
#         print(f"{RED}{'=' * 56}{RESET}")
#         input(f"{GREEN}\nPress any key to exit...{RESET}")
#         sys.exit(1)

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
