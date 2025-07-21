import subprocess
import os
import modules.misc.utils as utils
import modules.misc.global_vars as global_vars
from modules.misc.enums import OpenModes

WRITE_PATH: str = os.path.join(global_vars.SCRIPT_TEMP, "hwid.cmd")
SCRIPT_PATH: str = "https://gist.githubusercontent.com/PowerPCFan/0129696cb0f4716d1ace148ac0772e78/raw/57c4af12c4b72441f6c54d1fd723199281914651/hwid.cmd"

def run():
    # download the MAS script (use download_large_file even though it's not too large just for simplicity)
    utils.download_large_file(
        url=SCRIPT_PATH,
        destination=WRITE_PATH
    )
    
    # read contents
    with open(file=WRITE_PATH, mode=OpenModes.READ.value, encoding='utf-8') as f:
        content = f.read()

    # the following lines ensure that it's CRLF and not LF. the script doesn't function when it has LF endings.
    content = content.replace('\r\n', '\n')  # convert CRLF to LF
    content = content.replace('\r', '\n')  # convert CR to LF
    content = content.replace('\n', '\r\n')  # now that everything is LF, convert all LF endings to CRLF

    # overwrite downloaded script with new CRLF contents
    with open(file=WRITE_PATH, mode=OpenModes.WRITE.value, encoding='utf-8') as f:
        f.write(content)
        print(f"debug: wrote to {WRITE_PATH}")
    
    print("Starting Massgrave script...")
    
    subprocess.run(
        args=[
            "powershell.exe",
            "-Command",
            f'Start-Process -Verb runAs -FilePath "cmd.exe" -ArgumentList "/k cd /d `\"%USERPROFILE%\\AppData\\Local\\Temp`\" && `\"{WRITE_PATH}`\""'
        ]
    )
