import os
import subprocess
import modules.misc.global_vars as global_vars
from modules.color.ansi_codes import RESET, RED
from modules.misc.models import FurmarkOptions


def run_furmark_test(options: FurmarkOptions):
    furmark_test_duration: int = options.duration_minutes * 60 * 1000
    furmark_test_width = options.resolution.width
    furmark_test_height = options.resolution.height
    furmark_anti_aliasing = options.anti_aliasing.cli_value

    # Run FurMark with parameters
    furmark_path = rf"{global_vars.PROGRAMFILES_X86}\Geeks3D\Benchmarks\FurMark\FurMark.exe"

    if not os.path.exists(furmark_path):
        print(f"{RED}Error: FurMark.exe executable not found at {furmark_path}.{RESET}")
        return

    arguments = [
        "/nogui",
        f"/width={furmark_test_width}",
        f"/height={furmark_test_height}",
        f"/msaa={furmark_anti_aliasing}",
        f"/max_time={furmark_test_duration}"
    ]

    print(
        f"Starting FurMark stress test with the following settings:\n"
        f"Resolution: {furmark_test_width} x {furmark_test_height} ({options.resolution.value})\n"
        f"Anti-aliasing: {options.anti_aliasing.value}\n"
        f"Duration: {options.duration_minutes} minutes"
    )

    try:
        result = subprocess.run([furmark_path] + arguments, check=True)
        if result.returncode != 0:
            raise Exception(f"FurMark stress test failed with return code {result.returncode}.")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
