import modules.misc.global_vars as global_vars
from modules.winget import Winget
from modules.color.ansi_codes import GREEN, YELLOW, RESET

winget = Winget()


def install_vcpp_redists():
    vc_redist_years = ["2005", "2008", "2010", "2012", "2013", "2015+"]
    architectures = ["x86", "x64"] if global_vars.OS_IS_64BIT else ["x86"]

    print(
        f"{'64-bit' if global_vars.OS_IS_64BIT else '32-bit'} OS detected. "
        f"{' and '.join(architectures)} redistributables will be installed."
    )

    for year in vc_redist_years:
        for arch in architectures:
            winget.install(id=f"Microsoft.VCRedist.{year}.{arch}", params=global_vars.WINGET_PARAMS)

    print(f"{GREEN}{' and '.join(architectures)} redistributables successfully installed.{RESET}")
    print(f"{YELLOW}A system reboot is advised to ensure all changes take effect.{RESET}")
