from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple


class ActivationChoice(str, Enum):
    NONE = "none"
    MASSGRAVE = "massgrave"
    PRODUCT_KEY = "product_key"


class FurmarkResolution(str, Enum):
    P720 = "720p (1280x720)"
    P1080 = "1080p (1920x1080)"
    P1440 = "1440p (2560x1440)"

    @property
    def width(self) -> str:
        return {
            FurmarkResolution.P720: "1280",
            FurmarkResolution.P1080: "1920",
            FurmarkResolution.P1440: "2560",
        }[self]

    @property
    def height(self) -> str:
        return {
            FurmarkResolution.P720: "720",
            FurmarkResolution.P1080: "1080",
            FurmarkResolution.P1440: "1440",
        }[self]

    @classmethod
    def from_display_text(cls, text: str) -> "FurmarkResolution":
        for member in cls:
            if member.value == text:
                return member
        raise ValueError(f"Unsupported FurMark resolution value: {text}")


class FurmarkAntiAliasing(str, Enum):
    NONE = "None"
    MSAA_2X = "MSAA 2x"
    MSAA_4X = "MSAA 4x"
    MSAA_8X = "MSAA 8x"

    @property
    def cli_value(self) -> str:
        return {
            FurmarkAntiAliasing.NONE: "none",
            FurmarkAntiAliasing.MSAA_2X: "2x",
            FurmarkAntiAliasing.MSAA_4X: "4x",
            FurmarkAntiAliasing.MSAA_8X: "8x",
        }[self]

    @classmethod
    def from_display_text(cls, text: str) -> "FurmarkAntiAliasing":
        for member in cls:
            if member.value == text:
                return member
        raise ValueError(f"Unsupported FurMark anti-aliasing value: {text}")


class WingetPackage(NamedTuple):
    package_id: str
    package_name: str | None


class AppId(str, Enum):
    REDIST = "redist"
    DOTNET = "dotnet"
    SEVENZIP = "sevenzip"
    FURMARK = "furmark"
    FURMARK_2 = "furmark_2"
    FIREFOX = "firefox"
    CHROME = "chrome"
    STEAM = "steam"
    DISCORD = "discord"
    EPIC_GAMES_LAUNCHER = "epic_games_launcher"
    OPENRGB = "openrgb"
    SIGNALRGB = "signalrgb"
    VLC = "vlc"
    MALWAREBYTES = "malwarebytes"
    HWMONITOR = "hwmonitor"
    MSI_AFTERBURNER = "msi_afterburner"
    OCCT = "occt"
    CINEBENCH = "cinebench"
    CRYSTALDISKMARK = "crystaldiskmark"
    CRYSTALDISKINFO = "crystaldiskinfo"
    AIDA64 = "aida64"
    FANCONTROL = "fancontrol"
    CPUZ = "cpuz"
    GPUZ = "gpuz"
    HEAVEN = "heaven"
    VALLEY = "valley"
    SUPERPOSITION = "superposition"
    REVO = "revo"


@dataclass(frozen=True)
class AppDefinition:
    app_id: AppId
    label: str
    selected_by_default: bool
    winget_packages: list[WingetPackage] = field(default_factory=list)


@dataclass
class FurmarkOptions:
    enabled: bool = False
    duration_minutes: int = 5
    resolution: FurmarkResolution = FurmarkResolution.P1080
    anti_aliasing: FurmarkAntiAliasing = FurmarkAntiAliasing.MSAA_4X


@dataclass
class ScriptOptions:
    install_gpu_drivers: bool = False
    install_chipset_drivers: bool = False
    show_motherboard_driver_page: bool = False
    run_windows_tweaks: bool = False
    save_spec_sheet: bool = False
    generate_ai_description: bool = False
    run_app_installer: bool = False
    activate_windows: bool = False
    activation_choice: ActivationChoice = ActivationChoice.NONE
    windows_product_key: str = ""
    selected_apps: dict[AppId, bool] = field(default_factory=dict)
    furmark: FurmarkOptions = field(default_factory=FurmarkOptions)
