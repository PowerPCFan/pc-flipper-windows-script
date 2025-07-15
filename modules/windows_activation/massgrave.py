import subprocess
import os
import modules.misc.global_vars as global_vars
from modules.misc.enums import OpenModes

def run():
    # read the contents of the MAS script
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hwid.cmd"), OpenModes.READ.value, encoding="utf-8") as f:
        content = f.read()

    # the following lines ensure that it's CRLF and not LF. the script doesn't function when it has LF endings.
    content = content.replace('\r\n', '\n')  # convert CRLF to LF
    content = content.replace('\r', '\n')  # convert CR to LF
    content = content.replace('\n', '\r\n')  # now that everything is LF, convert all LF endings to CRLF

    write_path = os.path.join(global_vars.SCRIPT_TEMP, "hwid.cmd")
    
    # write new CRLF contents
    with open(file=write_path, mode=OpenModes.WRITE.value, encoding='utf-8') as f:
        f.write(content)
    
    print("Starting Massgrave script...")
    
    subprocess.run(
        args=[
            "powershell.exe",
            "-Command",
            f'Start-Process -Verb runAs -FilePath "cmd.exe" -ArgumentList "/k cd /d `\"%USERPROFILE%\\AppData\\Local\\Temp`\" && `\"{write_path}`\" /HWID"'
        ]
    )
