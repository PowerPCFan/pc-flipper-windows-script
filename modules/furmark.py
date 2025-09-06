import os
import subprocess
import modules.misc.global_vars as global_vars
from modules.color.ansi_codes import RESET, RED


def run_furmark_test(duration: int, resolution: str, anti_aliasing: str):
    furmark_test_duration: int = duration * 60 * 1000

    res_map = {
        "720p": {
            "Width": "1280",
            "Height": "720"
        },
        "1080p": {
            "Width": "1920",
            "Height": "1080"
        },
        "1440p": {
            "Width": "2560",
            "Height": "1440"
        },
    }

    aliasing_map = {
        "None": "none",
        "2x": "2x",
        "4x": "4x",
        "8x": "8x",
    }

    # Resolution matching
    furmark_test_width = "1920"  # initialize with default 1080p
    furmark_test_height = "1080"  # initialize with default 1080p
    for key in res_map:
        if key in resolution:
            furmark_test_width = res_map[key]["Width"]
            furmark_test_height = res_map[key]["Height"]
            break

    # Anti-aliasing matching
    furmark_anti_aliasing = "2x"  # initialize with default 2x
    for key in aliasing_map:
        if key in anti_aliasing:
            furmark_anti_aliasing = aliasing_map[key]
            break

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
        f"Resolution: {furmark_test_width} x {furmark_test_height} ({resolution})\n"
        f"Anti-aliasing: {furmark_anti_aliasing}\n"
        f"Duration: {duration} minutes"
    )

    try:
        result = subprocess.run([furmark_path] + arguments, check=True)
        if result.returncode != 0:
            raise Exception(f"FurMark stress test failed with return code {result.returncode}.")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
