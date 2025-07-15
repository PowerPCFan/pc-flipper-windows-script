import os
import sys
import ctypes
import functools

def enable_ansi():
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        new_mode = mode.value | 0x0004
        return kernel32.SetConsoleMode(handle, new_mode) != 0
    except Exception: return False

def supports_ansi(vt_enabled):
    if vt_enabled:
        return True

    return (
        sys.stdout.isatty() and (
            'ANSICON' in os.environ or
            'WT_SESSION' in os.environ or
            os.environ.get('TERM_PROGRAM') == 'vscode' or
            'TERM' in os.environ and 'xterm' in os.environ['TERM']
        )
    )

@functools.lru_cache(maxsize=None)
def ansi_supported(): return supports_ansi(enable_ansi())

def get_colors(ansi_is_supported):
    codes = {
        "RESET": "\033[0m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "BLUE": "\033[34m",
        "YELLOW": "\033[33m",
        "WHITE": "\033[37m",
        "PURPLE": "\033[35m",
        "CYAN": "\033[36m",
        "LIGHT_CYAN": "\033[96m",
        "SUPER_LIGHT_CYAN": "\033[38;5;153m",
        "ORANGE": "\033[38;5;208m"
    }

    if not ansi_is_supported:
        codes = {k: "" for k in codes}

    return codes

# Example usage
COLORS = get_colors(ansi_supported())
RESET = COLORS["RESET"]
RED = COLORS["RED"]
GREEN = COLORS["GREEN"]
BLUE = COLORS["BLUE"]
YELLOW = COLORS["YELLOW"]
WHITE = COLORS["WHITE"]
PURPLE = COLORS["PURPLE"]
CYAN = COLORS["CYAN"]
LIGHT_CYAN = COLORS["LIGHT_CYAN"]
SUPER_LIGHT_CYAN = COLORS["SUPER_LIGHT_CYAN"]
ORANGE = COLORS["ORANGE"]

# use these with:
# from modules.color.ansi_codes import RESET, RED, GREEN, BLUE, YELLOW, WHITE, PURPLE, CYAN, LIGHT_CYAN, SUPER_LIGHT_CYAN, ORANGE
