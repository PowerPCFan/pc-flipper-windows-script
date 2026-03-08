import modules.misc.global_vars as global_vars
from modules.winget import Winget
from modules.color.ansi_codes import CYAN, RESET, GREEN, YELLOW

winget = Winget()


def install(appid: str, name: str | None = None, print_message: bool = True):
    name = name if name else appid.replace(".", " ")

    if print_message:
        print(f"\n\n{CYAN}Installing {name}...{RESET}")

    winget.install(id=appid, params=global_vars.WINGET_PARAMS)


def install_selected_apps(selected_apps: dict[str, bool]):
    selected_apps = {key.lower(): value for key, value in selected_apps.items()}

    if selected_apps.get("redist"):
        print(f"\n\n{CYAN}Installing Visual C++ Redist Runtimes...{RESET}")
        architectures = ["x86", "x64"] if global_vars.OS_IS_64BIT else ["x86"]

        for year in ["2005", "2008", "2010", "2012", "2013", "2015+"]:
            for arch in architectures:
                install(f"Microsoft.VCRedist.{year}.{arch}", print_message=False)

        print(f"{GREEN}{' and '.join(architectures)} redistributables successfully installed.{RESET}")
        print(f"{YELLOW}A system reboot is advised to ensure all changes take effect.{RESET}")

    if selected_apps.get("dotnet"):
        dotnet_versions = ["3_1", "5", "6", "7", "8", "9", "10"]
        print(f"\n\n{CYAN}Installing .NET Runtimes...{RESET}")
        for version in dotnet_versions:
            install(f"Microsoft.DotNet.Runtime.{version}", print_message=False)

    if selected_apps.get("furmark"):
        install("Geeks3D.FurMark.1", name="FurMark")

    if selected_apps.get("furmark_2"):
        install("Geeks3D.FurMark.2", name="FurMark 2")

    if selected_apps.get("firefox"):
        install("Mozilla.Firefox", name="Firefox")

    if selected_apps.get("chrome"):
        install("Google.Chrome.EXE", name="Google Chrome")

    if selected_apps.get("steam"):
        install("Valve.Steam", name="Steam")

    if selected_apps.get("discord"):
        install("Discord.Discord", name="Discord")

    if selected_apps.get("epic_games_launcher"):
        install("EpicGames.EpicGamesLauncher", name="Epic Games Launcher")

    if selected_apps.get("openrgb"):
        install("OpenRGB.OpenRGB", name="OpenRGB")

    if selected_apps.get("signalrgb"):
        install("WhirlwindFX.SignalRgb", name="SignalRGB")

    if selected_apps.get("vlc"):
        install("VideoLAN.VLC", name="VLC media player")

    if selected_apps.get("sevenzip"):
        install("7zip.7zip", name="7-Zip")

    if selected_apps.get("malwarebytes"):
        install("Malwarebytes.Malwarebytes", name="Malwarebytes Anti-Malware")

    if selected_apps.get("hwmonitor"):
        install("CPUID.HWMonitor", name="CPUID HWMonitor")

    if selected_apps.get("msi_afterburner"):
        install("Guru3D.Afterburner", name="MSI Afterburner")
        install("Guru3D.RTSS", name="RivaTuner Statistics Server")

    if selected_apps.get("occt"):
        install("OCBase.OCCT.Personal", name="OCCT")

    if selected_apps.get("cinebench"):
        install("Maxon.CinebenchR23", name="Cinebench R23")

    if selected_apps.get("crystaldiskmark"):
        install("CrystalDewWorld.CrystalDiskMark", name="CrystalDiskMark")

    if selected_apps.get("crystaldiskinfo"):
        install("CrystalDewWorld.CrystalDiskInfo", name="CrystalDiskInfo")

    if selected_apps.get("aida64"):
        install("FinalWire.AIDA64.Extreme", name="AIDA64 Extreme")

    if selected_apps.get("fancontrol"):
        install("Rem0o.FanControl", name="FanControl")

    if selected_apps.get("cpuz"):
        install("CPUID.CPU-Z", name="CPU-Z")

    if selected_apps.get("gpuz"):
        install("TechPowerUp.GPU-Z", name="GPU-Z")

    if selected_apps.get("heaven"):
        install("Unigine.HeavenBenchmark", name="Unigine Heaven Benchmark")

    if selected_apps.get("valley"):
        install("Unigine.ValleyBenchmark", name="Unigine Valley Benchmark")

    if selected_apps.get("superposition"):
        install("Unigine.SuperpositionBenchmark", name="Unigine Superposition Benchmark")

    if selected_apps.get("revo"):
        install("RevoUninstaller.RevoUninstaller", name="Revo Uninstaller")
