# import os
import re as regexp
import subprocess
# import modules.misc.global_vars as global_vars
from modules.winget import Winget, WingetTools
from modules.color.ansi_codes import RESET, RED, GREEN, CYAN, YELLOW

winget = Winget()

def check_prerequisites():
    # WinGet
    try:
        output = subprocess.run(["winget", "--version"], check=True, capture_output=True, text=True)
        
        winget_version = output.stdout.strip().strip("\n")
        
        # if this prints then that means the try-except wasnt triggered so winget must be installed
        print(f"{GREEN}WinGet is already installed.{RESET}")

        regex = r"v(\d+)\.(\d+)"
        match: regexp.Match[str] | None = regexp.match(regex, output.stdout)
        
        # Check if version is less than 1.6
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            
            if major < 1 or (major == 1 and minor < 6):
                print(f"{YELLOW}WinGet version {winget_version} is outdated. Installing latest version...{RESET}")
                print(f"{CYAN}This can take a while. Please be patient.{RESET}")
                try:
                    WingetTools().install_winget()
                    print(f"{GREEN}WinGet updated successfully.{RESET}")
                except Exception as e:
                    print(f"{RED}Error updating WinGet: {e}{RESET}")
            else:
                print(f"{GREEN}WinGet version {winget_version} is sufficient.{RESET}")
        else:
            print(f"{YELLOW}Could not determine WinGet version from output: {winget_version}{RESET}")
    except Exception:
        print(f"{YELLOW}WinGet not installed. Installing WinGet...{RESET}")
        try:
            WingetTools().install_winget()
            print(f"{GREEN}WinGet installed successfully.{RESET}")
        except Exception as e:
            print(f"{RED}Error installing WinGet: {e}{RESET}")

    print("Checking WinGet functionality...")
    test_result = WingetTools().test_winget()

    # WinGet working normally - exit early
    if test_result["Success"]:
        print(f"{GREEN}WinGet is functioning correctly.{RESET}")
        return

    # Check for the specific error we know how to fix
    if test_result["WingetSourceBug"]:
        print("Known Error Detected! Running first fix...")
        WingetTools().fix_winget()
        print(f"{GREEN}Fix applied. Testing WinGet...{RESET}")

        test_result = WingetTools().test_winget()
        if test_result["Success"]:
            print(f"{GREEN}Fix was successful!{RESET}")
            return
        
        # If first fix failed, try the second fix
        if test_result["WingetSourceBug"]:
            print("Error detected again. Applying alternative fix...")
            WingetTools().install_winget()
            print(f"{GREEN}Alternative fix applied. Testing WinGet...{RESET}")

            test_result = WingetTools().test_winget()
            
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

    # cURL
    # commented out because curl isnt needed anymore
    
    # if os.path.exists(os.path.join(global_vars.SYSTEM32, "curl.exe")):
    #     print(f"{GREEN}cURL is already installed.{RESET}")
    # else:
    #     print(f"{YELLOW}cURL is not installed. Installing...{RESET}")
    #     try:
    #         winget.install(id="cURL.cURL", params=global_vars.WINGET_PARAMS)
    #         print(f"{GREEN}cURL installed successfully.{RESET}")
    #     except Exception as e:
    #         print(f"{RED}Error installing cURL: {e}{RESET}")
