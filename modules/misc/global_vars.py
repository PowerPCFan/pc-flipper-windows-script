import tempfile
import os
import netchecker
import wmi
import socket
import platformdirs
import psutil
import platform
import pathlib
from collections import Counter


# Variables for this file
computer = wmi.WMI()

Win32_ComputerSystem = computer.Win32_ComputerSystem()[0]
Win32_OperatingSystem = computer.Win32_OperatingSystem()[0]
Win32_BaseBoard = computer.Win32_BaseBoard()[0]
Win32_Processor = computer.Win32_Processor()[0]
# Win32_LogicalDisk = computer.Win32_LogicalDisk()[0]


# Operating System
OS: str = "Unknown"
match platform.system().lower():
    case "windows":
        OS = "Windows"
    case "linux":
        OS = "Linux"
    case "darwin":
        OS = "MacOS"


# Windows environment variables
TEMP: str = tempfile.gettempdir()
WINDIR: str = os.getenv("WINDIR", r"C:\Windows")
SYSTEM32: str = os.path.join(WINDIR, "System32")
PROGRAMFILES: str = os.getenv("ProgramFiles", os.getenv("ProgramW6432", r"C:\Program Files"))
PROGRAMFILES_X86: str = os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")
USERPROFILE: str = os.getenv("USERPROFILE", os.path.expanduser("~"))


# Current user and system variables/information
# i'm using the following because using `~/Desktop` isn't reliable due to OneDrive, different languages, etc
CURRENT_USER_DESKTOP: str = platformdirs.user_desktop_dir()
PC_NAME: str = str(Win32_ComputerSystem.Name)
INSTALL_TIME: str = str(Win32_OperatingSystem.InstallDate)
WINDOWS_OS_VERSION: str = str(Win32_OperatingSystem.Caption)
LOCAL_IP: str = socket.gethostbyname(socket.gethostname())


# Script variables
SCRIPT_TEMP: str = tempfile.mkdtemp()  # temporary directory for script files
SCRIPT_TEMP_PATH: pathlib.Path = pathlib.Path(SCRIPT_TEMP)

OS_IS_64BIT: bool = platform.machine().lower().endswith("64")

_motherboard_model: str = str(Win32_BaseBoard.Product)
_motherboard_manufacturer: str = str(Win32_BaseBoard.Manufacturer)
FULL_MOTHERBOARD_NAME: str = f"{_motherboard_manufacturer} {_motherboard_model}"

GPU: str = "Unknown"
for video_controller in computer.Win32_VideoController():
    if video_controller.Status == "OK" and video_controller.Availability == 3:
        GPU = str(video_controller.Name)

CPU: str = str(Win32_Processor.Name)

RAM: str = f"{str(round(psutil.virtual_memory().total / (1024 ** 3), 2))} GB"

DDR_TYPES = {20: "DDR", 21: "DDR2", 24: "DDR3", 26: "DDR4", 34: "DDR5", 35: "DDR5"}
ram_strings_raw = []

for ram in computer.Win32_PhysicalMemory():
    _ram_stick_parts = []

    if _ram_stick_brand := ram.Manufacturer.strip() if ram.Manufacturer else "":
        _ram_stick_parts.append(_ram_stick_brand)

    _ram_stick_parts.append(f"{int(ram.Capacity) // (1024**3)}GB")
    _ram_stick_parts.append(f"{DDR_TYPES.get(
        (ram.MemoryType if ram.MemoryType and ram.MemoryType != 0 else ram.SMBIOSMemoryType),
        "DDR?"
    )}-{ram.Speed or "????"}MHz")

    ram_strings_raw.append(" ".join(_ram_stick_parts))

counted = Counter(ram_strings_raw)

ram_strings = []
for ram_str, qty in counted.items():
    if qty > 1:
        ram_strings.append(f"{ram_str} x{qty}")
    else:
        ram_strings.append(ram_str)

RAM_STICKS = "; ".join(ram_strings)

# disabled since not working for some reason
# STORAGE: str = f"{(int(Win32_LogicalDisk.Size) / (1024**3)):.2f} GB"
STORAGE: str = "unknown"


# Winget variables
WINGET_PARAMS: str = "--accept-package-agreements --accept-source-agreements --silent"


def get_public_ip(default: str = "127.0.0.1") -> str:
    return netchecker.get_public_ip() or default
