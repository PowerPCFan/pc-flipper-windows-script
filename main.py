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
import modules.localai                                as localai

from modules.color.ansi_codes                         import RESET, RED, YELLOW, GREEN
from modules.misc.enums                               import WindowsActivationMethod
from modules.misc.models                              import ScriptOptions, ActivationChoice


def invoke_tasks(tasks: ScriptOptions):
    if tasks.install_gpu_drivers:
        drivers.gpu.install_gpu_drivers()

    if tasks.install_chipset_drivers:
        drivers.chipset.install_chipset_drivers()

    if tasks.show_motherboard_driver_page:
        drivers.motherboard.show_motherboard_driver_page()

    if tasks.run_windows_tweaks:
        tweaks = windows_tweaks.WindowsTweaks()
        tweaks.run()

    if tasks.save_spec_sheet:
        spec_sheet.save()

    if tasks.generate_ai_description:
        localai.show_ai_description_generator_window()

    if tasks.activate_windows:
        if tasks.activation_choice == ActivationChoice.MASSGRAVE:
            activate_windows.activate(
                method=WindowsActivationMethod.MASSGRAVE,
                activation_key=None
            )
        elif tasks.activation_choice == ActivationChoice.PRODUCT_KEY:
            activate_windows.activate(
                method=WindowsActivationMethod.ACTIVATION_KEY,
                activation_key=tasks.windows_product_key
            )
        else:
            raise ValueError("You selected to activate Windows but a valid activation method was not specified. Please check your input.")  # noqa: E501

    if tasks.run_app_installer:
        apps.install_selected_apps(selected_apps=tasks.selected_apps)

    if tasks.furmark.enabled:
        furmark.run_furmark_test(options=tasks.furmark)


def cleanup():
    localai.close_all_localai()
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

    utils.popup_message(
        title="Script Complete",
        message=(
            "The script has finished running!\n"
            "Please give it a star on GitHub - it's free and helps out a ton.\n"
            "Script created by PowerPCFan"
        ))


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
    finally:
        cleanup()
else:
    print(f"{YELLOW}This script is not meant to be run as a module. Exiting...{RESET}")
    sys.exit(1)
