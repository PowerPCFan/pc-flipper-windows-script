from modules.color.ansi_codes import RESET, GREEN
from modules.tweaks.registry import Registry
from modules.misc.enums import RegistryType

class WindowsTweaks:
    def __init__(self) -> None:
        pass
    
    def run(self):
        print("Disabling Location Services...")
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
            name="Value",
            value="Deny",
            reg_type=RegistryType.REG_SZ
        )


        print("Disabling Windows Error Reporting...")
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting",
            name="Disabled",
            value=1,
            reg_type=RegistryType.REG_DWORD
        )

        print("Enabling Long File Paths...")
        Registry.add(
            full_path=r"HKLM\SYSTEM\CurrentControlSet\Control\FileSystem",
            name="LongPathsEnabled",
            value=1,
            reg_type=RegistryType.REG_DWORD
        )

        print("Disabling WiFi-Sense...")
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Microsoft\WcmSvc\wifinetworkmanager\config",
            name="AutoConnectAllowedOEM",
            value=0,
            reg_type=RegistryType.REG_DWORD
        )

        print("Enabling Verbose Mode...")
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
            name="VerboseStatus",
            value=1,
            reg_type=RegistryType.REG_DWORD
        )

        print("Disabling Cortana...")
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search",
            name="AllowCortana",
            value=0,
            reg_type=RegistryType.REG_DWORD
        )

        print("Disabling Telemetry...")
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            name="AllowTelemetry",
            value=0,
            reg_type=RegistryType.REG_DWORD
        )
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            name="DoNotShowFeedbackNotifications",
            value=0,
            reg_type=RegistryType.REG_DWORD
        )
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection",
            name="AllowTelemetry",
            value=0,
            reg_type=RegistryType.REG_DWORD
        )

        print("Disabling Advertising ID...")
        Registry.add(
            full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
            name="DisabledByGroupPolicy",
            value=1,
            reg_type=RegistryType.REG_DWORD
        )

        print(f"{GREEN}Windows tweaks complete.{RESET}")
