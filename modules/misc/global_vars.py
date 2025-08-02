import tempfile
import os
import wmi

# pylance REALLY hates this
import clr  # type: ignore
import System  # type: ignore



# Variables for this file
computer = wmi.WMI()
environment = System.Environment



# Windows environment variables
TEMP: str = tempfile.gettempdir()
WINDIR: str = os.getenv("WINDIR", r"C:\Windows")
SYSTEM32: str = os.path.join(WINDIR, "System32")
PROGRAMFILES: str = os.getenv("ProgramFiles", os.getenv("ProgramW6432", r"C:\Program Files"))
PROGRAMFILES_X86: str = os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")
USERPROFILE: str = os.getenv("USERPROFILE", os.path.expanduser("~"))



# Script variables
SCRIPT_TEMP: str = tempfile.mkdtemp()  # temporary directory for script files

WINDOWS_OS_VERSION: str = computer.Win32_OperatingSystem()[0].Caption

OS_IS_64BIT: bool = environment.Is64BitOperatingSystem

BOARD: str = computer.Win32_BaseBoard()[0].Product
MANUFACTURER: str = computer.Win32_BaseBoard()[0].Manufacturer
FULL_MOTHERBOARD_NAME: str = f"{MANUFACTURER} {BOARD}"

GPU: str = "Unknown"
for video_controller in computer.Win32_VideoController():
    if video_controller.Status == "OK" and video_controller.Availability == 3:
        GPU = video_controller.Name

CPU: str = computer.Win32_Processor()[0].Name



# Winget variables
WINGET_PARAMS: str = "--accept-package-agreements --accept-source-agreements --silent"
