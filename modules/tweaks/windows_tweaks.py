from dataclasses import dataclass

from modules.color.ansi_codes import RESET, GREEN
from modules.tweaks.registry import Registry
from modules.misc.enums import RegistryType


@dataclass(frozen=True)
class RegistryTweak:
    description: str
    full_path: str
    name: str
    value: str | int
    reg_type: RegistryType


TWEAKS: tuple[RegistryTweak, ...] = (
    RegistryTweak(
        description="Disabling Location Services...",
        full_path=r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
        name="Value",
        value="Deny",
        reg_type=RegistryType.REG_SZ,
    ),
    RegistryTweak(
        description="Disabling Windows Error Reporting...",
        full_path=r"HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting",
        name="Disabled",
        value=1,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Enabling Long File Paths...",
        full_path=r"HKLM\SYSTEM\CurrentControlSet\Control\FileSystem",
        name="LongPathsEnabled",
        value=1,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Disabling WiFi-Sense...",
        full_path=r"HKLM\SOFTWARE\Microsoft\WcmSvc\wifinetworkmanager\config",
        name="AutoConnectAllowedOEM",
        value=0,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Enabling Verbose Mode...",
        full_path=r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
        name="VerboseStatus",
        value=1,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Disabling Cortana...",
        full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search",
        name="AllowCortana",
        value=0,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Disabling Telemetry...",
        full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
        name="AllowTelemetry",
        value=0,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Disabling Telemetry...",
        full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
        name="DoNotShowFeedbackNotifications",
        value=0,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Disabling Telemetry...",
        full_path=r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection",
        name="AllowTelemetry",
        value=0,
        reg_type=RegistryType.REG_DWORD,
    ),
    RegistryTweak(
        description="Disabling Advertising ID...",
        full_path=r"HKLM\SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
        name="DisabledByGroupPolicy",
        value=1,
        reg_type=RegistryType.REG_DWORD,
    ),
)


class WindowsTweaks:
    def __init__(self) -> None:
        pass

    def run(self):
        for tweak in TWEAKS:
            print(tweak.description)
            Registry.add(
                full_path=tweak.full_path,
                name=tweak.name,
                value=tweak.value,
                reg_type=tweak.reg_type,
            )

        print(f"{GREEN}Windows tweaks complete.{RESET}")
