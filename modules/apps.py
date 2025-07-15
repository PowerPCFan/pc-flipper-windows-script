import modules.visual_cpp_redists as vcpp_redists
import modules.misc.global_vars as global_vars
from modules.winget import Winget
from modules.color.ansi_codes import CYAN, RESET

winget = Winget()

installing_app_prefix = f"\n\n"

def install_selected_apps(selected_apps: dict[str, bool]):
    if selected_apps["redist"]:
        print(f"{installing_app_prefix}{CYAN}Installing Visual C++ Redist Runtimes...{RESET}")
        vcpp_redists.install_vcpp_redists()

    if selected_apps["dotnet"]:
        dotnet_versions = ["3_1", "5", "6", "7", "8", "9"]
        print(f"{installing_app_prefix}{CYAN}Installing .NET Runtimes...{RESET}")
        for version in dotnet_versions:
            winget.install(id=f"Microsoft.DotNet.Runtime.{version}", params=global_vars.WINGET_PARAMS)

    if selected_apps["firefox"]:
        print(f"{installing_app_prefix}{CYAN}Installing Mozilla Firefox...{RESET}")
        winget.install(id="Mozilla.Firefox", params=global_vars.WINGET_PARAMS)

    if selected_apps["chrome"]:
        print(f"{installing_app_prefix}{CYAN}Installing Google Chrome...{RESET}")
        winget.install(id="Google.Chrome.EXE", params=global_vars.WINGET_PARAMS)

    if selected_apps["steam"]:
        print(f"{installing_app_prefix}{CYAN}Installing Steam...{RESET}")
        winget.install(id="Valve.Steam", params=global_vars.WINGET_PARAMS)

    if selected_apps["discord"]:
        print(f"{installing_app_prefix}{CYAN}Installing Discord...{RESET}")
        winget.install(id="Discord.Discord", params=global_vars.WINGET_PARAMS)

    if selected_apps["epic_games_launcher"]:
        print(f"{installing_app_prefix}{CYAN}Installing Epic Games Launcher...{RESET}")
        winget.install(id="EpicGames.EpicGamesLauncher", params=global_vars.WINGET_PARAMS)

    if selected_apps["openrgb"]:
        print(f"{installing_app_prefix}{CYAN}Installing OpenRGB...{RESET}")
        winget.install(id="CalcProgrammer1.OpenRGB", params=global_vars.WINGET_PARAMS)

    if selected_apps["signalrgb"]:
        print(f"{installing_app_prefix}{CYAN}Installing SignalRGB...{RESET}")
        winget.install(id="WhirlwindFX.SignalRgb", params=global_vars.WINGET_PARAMS)

    if selected_apps["vlc"]:
        print(f"{installing_app_prefix}{CYAN}Installing VLC media player...{RESET}")
        winget.install(id="VideoLAN.VLC", params=global_vars.WINGET_PARAMS)

    if selected_apps["sevenzip"]:
        print(f"{installing_app_prefix}{CYAN}Installing 7-Zip...{RESET}")
        winget.install(id="7zip.7zip", params=global_vars.WINGET_PARAMS)

    if selected_apps["malwarebytes"]:
        print(f"{installing_app_prefix}{CYAN}Installing Malwarebytes Anti-Malware...{RESET}")
        winget.install(id="Malwarebytes.Malwarebytes", params=global_vars.WINGET_PARAMS)

    if selected_apps["hwmonitor"]:
        print(f"{installing_app_prefix}{CYAN}Installing CPUID HWMonitor...{RESET}")
        winget.install(id="CPUID.HWMonitor", params=global_vars.WINGET_PARAMS)

    if selected_apps["msi_afterburner"]:
        print(f"{installing_app_prefix}{CYAN}Installing MSI Afterburner and RivaTuner Statistics Server...{RESET}")
        winget.install(id="Guru3D.Afterburner", params=global_vars.WINGET_PARAMS)
        winget.install(id="Guru3D.RTSS", params=global_vars.WINGET_PARAMS)

    if selected_apps["furmark"]:
        print(f"{installing_app_prefix}{CYAN}Installing FurMark...{RESET}")
        winget.install(id="Geeks3D.FurMark.1", params=global_vars.WINGET_PARAMS)

    if selected_apps["occt"]:
        print(f"{installing_app_prefix}{CYAN}Installing OCCT...{RESET}")
        winget.install(id="OCBase.OCCT.Personal", params=global_vars.WINGET_PARAMS)
    
    if selected_apps["cinebench"]:
        print(f"{installing_app_prefix}{CYAN}Installing Cinebench R23...{RESET}")
        winget.install(id="Maxon.CinebenchR23", params=global_vars.WINGET_PARAMS)
    
    if selected_apps["crystaldiskmark"]:
        print(f"{installing_app_prefix}{CYAN}Installing CrystalDiskMark...{RESET}")
        winget.install(id="CrystalDewWorld.CrystalDiskMark", params=global_vars.WINGET_PARAMS)
    
    if selected_apps["crystaldiskinfo"]:
        print(f"{installing_app_prefix}{CYAN}Installing CrystalDiskInfo...{RESET}")
        winget.install(id="CrystalDewWorld.CrystalDiskInfo", params=global_vars.WINGET_PARAMS)

    if selected_apps["aida64"]:
        print(f"{installing_app_prefix}{CYAN}Installing AIDA64...{RESET}")
        winget.install(id="FinalWire.AIDA64.Extreme", params=global_vars.WINGET_PARAMS)
    
    if selected_apps["fancontrol"]:
        print(f"{installing_app_prefix}{CYAN}Installing FanControl...{RESET}")
        winget.install(id="Rem0o.FanControl", params=global_vars.WINGET_PARAMS)

    if selected_apps["cpuz"]:
        print(f"{installing_app_prefix}{CYAN}Installing CPU-Z...{RESET}")
        winget.install(id="CPUID.CPU-Z", params=global_vars.WINGET_PARAMS)

    if selected_apps["gpuz"]:
        print(f"{installing_app_prefix}{CYAN}Installing GPU-Z...{RESET}")
        winget.install(id="TechPowerUp.GPU-Z", params=global_vars.WINGET_PARAMS)

    if selected_apps["heaven"]:
        print(f"{installing_app_prefix}{CYAN}Installing Unigine Heaven Benchmark...{RESET}")
        winget.install(id="Unigine.HeavenBenchmark", params=global_vars.WINGET_PARAMS)

    if selected_apps["valley"]:
        print(f"{installing_app_prefix}{CYAN}Installing Unigine Valley Benchmark...{RESET}")
        winget.install(id="Unigine.ValleyBenchmark", params=global_vars.WINGET_PARAMS)

    if selected_apps["superposition"]:
        print(f"{installing_app_prefix}{CYAN}Installing Unigine Superposition Benchmark...{RESET}")
        winget.install(id="Unigine.SuperpositionBenchmark", params=global_vars.WINGET_PARAMS)
    
    if selected_apps["revo"]:
        print(f"{installing_app_prefix}{CYAN}Installing Revo Uninstaller...{RESET}")
        winget.install(id="RevoUninstaller.RevoUninstaller", params=global_vars.WINGET_PARAMS)
