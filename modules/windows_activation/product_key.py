import subprocess
from modules.color.ansi_codes import RESET, RED, GREEN, YELLOW

def activate(key: str):
    if key is not None:
        try:
            print("Activating Windows using product key...")
            
            # I could do this in Python with the win32com or wmi module, but it's easier to just not
            output = subprocess.run(
                args=[
                    "powershell.exe",
                    "-Command",
                    f"$sv = Get-CimInstance -ClassName \"SoftwareLicensingService\";$sp = @{{ClassName = 'SoftwareLicensingProduct'; Filter = \"ApplicationId='55c92734-d682-4d71-983e-d6ec3f16059f' AND PartialProductKey IS NOT NULL\"}};$p = Get-CimInstance @sp;$sv | Invoke-CimMethod -MethodName InstallProductKey -Arguments @{{ ProductKey = \"{key}\" }}|Out-Null;$p | Invoke-CimMethod -MethodName Activate|Out-Null;$sv | Invoke-CimMethod -MethodName RefreshLicenseStatus|Out-Null"
                ],
                check=True,
                capture_output=True,
                text=True
            )
            
            # this is the most terrible way to check for errors but honestly who cares, it works
            if "error" in output.stderr.lower() or "error" in output.stdout.lower():
                raise Exception("Unknown Error")
            
            print(f"{GREEN}Success! Windows was activated using your product key.{RESET}")
        except Exception as e:
            print(f"{RED}Error: There was an issue activating Windows: {e} {RESET}")
    else:
        print(f"{YELLOW}No activation key was provided. Skipping activation...{RESET}")
