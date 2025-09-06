import sys

import modules.misc.utils                             as utils
import modules.drivers                                as drivers
import modules.misc.global_vars                       as global_vars
import modules.tweaks.windows_tweaks                  as windows_tweaks
import modules.ui                                     as ui
import modules.startup_tests                          as startup_tests
import modules.windows_activation.activate_windows    as activate_windows
import modules.apps                                   as apps
import modules.furmark                                as furmark
import modules.spec_sheet.spec_sheet                  as spec_sheet

from modules.color.ansi_codes                         import RESET, RED, YELLOW, GREEN
from modules.misc.enums                               import WindowsActivationMethod


def invoke_tasks(tasks: dict[str, str | bool | dict]):
    if tasks["install_gpu_drivers"]:
        drivers.gpu.install_gpu_drivers()

    if tasks["install_chipset_drivers"]:
        drivers.chipset.install_chipset_drivers()

    if tasks["show_motherboard_driver_page"]:
        drivers.motherboard.show_motherboard_driver_page()

    if tasks["run_windows_tweaks"]:
        tweaks = windows_tweaks.WindowsTweaks()
        tweaks.run()

    if tasks["save_spec_sheet"]:
        spec_sheet.save()

    if tasks["activate_windows"]:
        if tasks["activate_windows_massgrave"]:
            activate_windows.activate(
                method=WindowsActivationMethod.MASSGRAVE,
                activation_key=None
            )
        elif tasks["activate_windows_key"]:
            product_key = tasks["windows_product_key"]

            if isinstance(product_key, str):
                activate_windows.activate(
                    method=WindowsActivationMethod.ACTIVATION_KEY,
                    activation_key=product_key
                )
            else:
                raise ValueError("Your Windows Product Key is not a string. Please check your input.")
        else:
            raise ValueError("You selected to activate Windows but a valid activation method was not specified. Please check your input.")

    if tasks["run_app_installer"]:
        apps.install_selected_apps(selected_apps=tasks["apps"])  # type: ignore

    if tasks["run_furmark_test"]:
        duration = tasks["furmark_duration"]
        resolution = tasks["furmark_resolution"]
        anti_aliasing = tasks["furmark_anti_aliasing"]

        if isinstance(duration, str) and isinstance(resolution, str) and isinstance(anti_aliasing, str):
            furmark.run_furmark_test(duration=int(duration), resolution=resolution, anti_aliasing=anti_aliasing)
        else:
            raise ValueError("The FurMark test parameters specified are not valid strings. This is likely an issue with the script and not your input.")


def cleanup():
    utils.remove_if_exists(global_vars.SCRIPT_TEMP)


def main():
    if global_vars.OS != "Windows":
        print(
            f"\n\n\n{RED}"
            "No idea how you're running this script, but it is only compatible with Windows.\n"
            "If you are using Windows and experiencing this issue, please make an issue on GitHub."
            f"{RESET}"
        )
        sys.exit(1)

    print("Checking for administrator privileges...")
    startup_tests.administrator.test_admin_privileges()

    print("Checking internet connectivity...")
    startup_tests.internet.test_internet()

    print(f"{GREEN}Checks successfully completed.{RESET}")

    print("Installing and checking prerequisites...")
    startup_tests.prerequisites.check_prerequisites()

    tasks = ui.show_script_options_window()
    invoke_tasks(tasks=tasks)

    utils.popup_message(title="Script Complete", message="The script has finished running!\nPlease give it a star on GitHub!\nCreated by PowerPCFan")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # handle keyboardinterrupt for a smooth exit
        # without a long traceback about whatever got interrupted
        print(f"{YELLOW}\nExiting...{RESET}")
        sys.exit(0)
    except Exception as e:
        # catch all exceptions not caught by a more specific try-except,
        # print a user-friendly error,
        # and exit with status code 1

        # note to self - if you don't want the script to exit after an error,
        # wrap it in its own try-except block that doesn't have a sys.exit call

        error_message = "ERROR: An unexpected error occurred:"
        dashes = '-' * len(error_message)

        print(
            f"{dashes}\n"
            f"{RED}{error_message}{RESET}\n"
            f"{dashes}\n"
            f"{e}"
        )

        sys.exit(1)
else:
    print(f"{YELLOW}This script is not meant to be run as a module. Exiting...{RESET}")
    sys.exit(1)
