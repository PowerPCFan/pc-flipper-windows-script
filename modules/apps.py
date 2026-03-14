from collections.abc import Mapping

import modules.misc.global_vars as global_vars
from modules.color.ansi_codes import CYAN, RESET, GREEN, YELLOW
from modules.misc.models import AppDefinition, AppId, WingetPackage
from modules.winget import Winget

winget = Winget()


APP_DEFINITIONS: tuple[AppDefinition, ...] = (
    AppDefinition(
        app_id=AppId.REDIST,
        label="Visual C++ Redist Runtimes (Recommended)",
        selected_by_default=True
    ),
    AppDefinition(
        app_id=AppId.DOTNET,
        label="Microsoft .NET Runtimes (Recommended)",
        selected_by_default=True
    ),
    AppDefinition(
        app_id=AppId.SEVENZIP,
        label="7-Zip (Recommended)",
        selected_by_default=True,
        winget_packages=[WingetPackage(package_id="7zip.7zip", package_name="7-Zip")]
    ),
    AppDefinition(
        app_id=AppId.FURMARK,
        label="FurMark (Recommended)",
        selected_by_default=True,
        winget_packages=[WingetPackage(package_id="Geeks3D.FurMark.1", package_name="FurMark")]
    ),
    AppDefinition(
        app_id=AppId.FURMARK_2,
        label="FurMark 2",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Geeks3D.FurMark.2", package_name="FurMark 2")]
    ),
    AppDefinition(
        app_id=AppId.FIREFOX,
        label="Firefox",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Mozilla.Firefox", package_name="Firefox")]
    ),
    AppDefinition(
        app_id=AppId.CHROME,
        label="Chrome",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Google.Chrome.EXE", package_name="Google Chrome")]
    ),
    AppDefinition(
        app_id=AppId.STEAM,
        label="Steam",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Valve.Steam", package_name="Steam")]
    ),
    AppDefinition(
        app_id=AppId.DISCORD,
        label="Discord",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Discord.Discord", package_name="Discord")]
    ),
    AppDefinition(
        app_id=AppId.EPIC_GAMES_LAUNCHER,
        label="Epic Games Launcher",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="EpicGames.EpicGamesLauncher", package_name="Epic Games Launcher")]
    ),
    AppDefinition(
        app_id=AppId.OPENRGB,
        label="OpenRGB",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="OpenRGB.OpenRGB", package_name="OpenRGB")]
    ),
    AppDefinition(
        app_id=AppId.SIGNALRGB,
        label="SignalRGB",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="WhirlwindFX.SignalRgb", package_name="SignalRGB")]
    ),
    AppDefinition(
        app_id=AppId.VLC,
        label="VLC Media Player",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="VideoLAN.VLC", package_name="VLC media player")]
    ),
    AppDefinition(
        app_id=AppId.MALWAREBYTES,
        label="Malwarebytes",
        selected_by_default=False,
        winget_packages=[
            WingetPackage(package_id="Malwarebytes.Malwarebytes", package_name="Malwarebytes Anti-Malware")
        ]
    ),
    AppDefinition(
        app_id=AppId.HWMONITOR,
        label="HWMonitor",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="CPUID.HWMonitor", package_name="CPUID HWMonitor")]
    ),
    AppDefinition(
        app_id=AppId.MSI_AFTERBURNER,
        label="MSI Afterburner",
        selected_by_default=False,
        winget_packages=[
            WingetPackage(package_id="Guru3D.Afterburner", package_name="MSI Afterburner"),
            WingetPackage(package_id="Guru3D.RTSS", package_name="RivaTuner Statistics Server")
        ]
    ),
    AppDefinition(
        app_id=AppId.OCCT,
        label="OCCT",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="OCBase.OCCT.Personal", package_name="OCCT")]
    ),
    AppDefinition(
        app_id=AppId.CINEBENCH,
        label="Cinebench R23",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Maxon.CinebenchR23", package_name="Cinebench R23")]
    ),
    AppDefinition(
        app_id=AppId.CRYSTALDISKMARK,
        label="CrystalDiskMark",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="CrystalDewWorld.CrystalDiskMark", package_name="CrystalDiskMark")]
    ),
    AppDefinition(
        app_id=AppId.CRYSTALDISKINFO,
        label="CrystalDiskInfo",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="CrystalDewWorld.CrystalDiskInfo", package_name="CrystalDiskInfo")]
    ),
    AppDefinition(
        app_id=AppId.AIDA64,
        label="AIDA64",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="FinalWire.AIDA64.Extreme", package_name="AIDA64 Extreme")]
    ),
    AppDefinition(
        app_id=AppId.FANCONTROL,
        label="FanControl",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Rem0o.FanControl", package_name="FanControl")]
    ),
    AppDefinition(
        app_id=AppId.CPUZ,
        label="CPU-Z",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="CPUID.CPU-Z", package_name="CPU-Z")]
    ),
    AppDefinition(
        app_id=AppId.GPUZ,
        label="GPU-Z",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="TechPowerUp.GPU-Z", package_name="GPU-Z")]
    ),
    AppDefinition(
        app_id=AppId.HEAVEN,
        label="Unigine Heaven Benchmark",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Unigine.HeavenBenchmark", package_name="Unigine Heaven Benchmark")]
    ),
    AppDefinition(
        app_id=AppId.VALLEY,
        label="Unigine Valley Benchmark",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="Unigine.ValleyBenchmark", package_name="Unigine Valley Benchmark")]
    ),
    AppDefinition(
        app_id=AppId.SUPERPOSITION,
        label="Unigine Superposition Benchmark",
        selected_by_default=False,
        winget_packages=[
            WingetPackage(package_id="Unigine.SuperpositionBenchmark", package_name="Unigine Superposition Benchmark")
        ]
    ),
    AppDefinition(
        app_id=AppId.REVO,
        label="Revo Uninstaller",
        selected_by_default=False,
        winget_packages=[WingetPackage(package_id="RevoUninstaller.RevoUninstaller", package_name="Revo Uninstaller")]
    ),
)


def install(appid: str, name: str | None = None, print_message: bool = True):
    name = name if name else appid.replace(".", " ")

    if print_message:
        print(f"\n\n{CYAN}Installing {name}...{RESET}")

    winget.install(id=appid, params=global_vars.WINGET_PARAMS)


def _normalize_selected_apps(selected_apps: Mapping[AppId, bool]) -> dict[AppId, bool]:
    normalized: dict[AppId, bool] = {}

    for raw_id, selected in selected_apps.items():
        if isinstance(raw_id, AppId):
            normalized[raw_id] = selected
            continue

        try:
            normalized[AppId(raw_id.lower())] = selected
        except ValueError:
            continue

    return normalized


def install_selected_apps(selected_apps: Mapping[AppId, bool]):
    normalized = _normalize_selected_apps(selected_apps)

    if normalized.get(AppId.REDIST):
        print(f"\n\n{CYAN}Installing Visual C++ Redist Runtimes...{RESET}")
        architectures = ["x86", "x64"] if global_vars.OS_IS_64BIT else ["x86"]

        for year in ["2005", "2008", "2010", "2012", "2013", "2015+"]:
            for arch in architectures:
                install(f"Microsoft.VCRedist.{year}.{arch}", print_message=False)

        print(f"{GREEN}{' and '.join(architectures)} redistributables successfully installed.{RESET}")
        print(f"{YELLOW}A system reboot is advised to ensure all changes take effect.{RESET}")

    if normalized.get(AppId.DOTNET):
        print(f"\n\n{CYAN}Installing .NET Runtimes...{RESET}")
        for version in ["3_1", "5", "6", "7", "8", "9", "10"]:
            install(f"Microsoft.DotNet.Runtime.{version}", print_message=False)

    for app in APP_DEFINITIONS:
        if app.app_id in {AppId.REDIST, AppId.DOTNET}:
            continue

        if not normalized.get(app.app_id):
            continue

        for package in app.winget_packages:
            install(package.package_id, name=package.package_name)
