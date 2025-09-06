import winreg
from modules.color.ansi_codes import RESET, RED
from modules.misc.enums import RegistryType


class Registry:
    HIVE_MAP = {
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE
    }

    @staticmethod
    def add(full_path: str, name: str, value, reg_type: RegistryType):
        """
        Adds a value to the Windows registry
        """
        try:
            # Split hive and path
            hive_str, sub_key = full_path.split("\\", 1)
            hive = Registry.HIVE_MAP[hive_str.upper()]
        except (ValueError, KeyError):
            raise ValueError(f"{RED}Error: Invalid registry path{RESET}")

        try:
            key = winreg.CreateKeyEx(
                hive,
                sub_key,
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            )
            winreg.SetValueEx(key, name, 0, reg_type.value, value)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"{RED}Error: Failed to add '{name}' to '{full_path}': {e}{RESET}")
