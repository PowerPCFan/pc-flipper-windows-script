import shutil
import psutil
import os
import win32api
import win32con
import zipfile
import re as regexp
import readchar
import tkinter as tk
import subprocess
import requests
from typing import Callable, Iterator
from datetime import datetime, timedelta, timezone
from tkinter import messagebox
from modules.misc.enums import OpenModes
from modules.color.ansi_codes import RESET, RED, YELLOW

def remove_if_exists(path: str):
    """
    ### Description:
    Removes a file or directory if it exists.  
    This function automatically detects if the path  
    is a file or directory and removes it accordingly  
    using `shutil.rmtree()` or `os.remove()`.
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def ensure_dir_exists(path: str) -> str:
    """
    ### Description:
    Ensures a directory exists at the given path.  
    Returns the path to the directory regardless of whether it was created by this function or already existed.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def download_large_file(url: str, destination: str, chunk_size: int = 8192, headers: dict | None = None, timeout: int | None = None):
    try:
        with requests.get(url, stream=True, headers=headers, timeout=timeout) as r:
            r.raise_for_status()
            with open(destination, f'{OpenModes.WRITE.value}{OpenModes.BINARY.value}') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"{RED}Error downloading file: {e}{RESET}")

def get_user_choice(prompt: str, options: dict[str, Callable], names: dict[str, str | None], default: Callable | None = None) -> Callable:
    """
    ### Description:
    Get a user choice from a set of options. Accepts both uppercase and lowercase keypresses.
    """
    join = "  "
    error = "Invalid key \"{key}\". Try again."
    not_callable = "Option \"{key}\" is not callable."

    # Normalize keys to lowercase
    normalized_options = {k.lower(): v for k, v in options.items() if len(k) == 1 and callable(v)}
    normalized_names = {k.lower(): v for k, v in names.items()}
    keys = list(normalized_options.keys())

    inline_options = join.join(
        f"{normalized_names.get(key, 'Unnamed')}" for key in keys
    )
    print(prompt + inline_options)

    while True:
        key = readchar.readkey().lower()  # Convert input key to lowercase
        if key in keys:
            value = normalized_options[key]
            if callable(value):
                return value()
            else:
                print(not_callable.format(key=key))
        elif default:
            return default(key)
        else:
            print(error.format(key=key))

def get_user_choice2(options: dict[str, Callable], default: Callable | None = None) -> Callable:
    """
    ### Description:
    Get a user choice from a set of options. This version only handles the keypress
    """
    error = "Invalid key \"{key}\". Try again."
    not_callable = "Option \"{key}\" is not callable."

    # Normalize keys to lowercase
    normalized_options = {k.lower(): v for k, v in options.items() if len(k) == 1 and callable(v)}
    keys = list(normalized_options.keys())

    while True:
        key = readchar.readkey().lower()  # Convert input key to lowercase
        if key in keys:
            value = normalized_options[key]
            if callable(value):
                return value()
            else:
                print(not_callable.format(key=key))
        elif default:
            return default(key)
        else:
            print(error.format(key=key))

def clear_screen():
    os.system("cls")
    # i would add `clear` but this is windows only so why would it need to be here

def restart_explorer():
    subprocess.run(["taskkill.exe", "/f", "/im", "explorer.exe"])  # forcefully kill explorer.exe
    subprocess.run(["start", "explorer.exe"], shell=True)  # shell=True needed because `start` is a shell command, not an executable
    print("SUCCESS: The process \"explorer.exe\" has been started.")  # print statement that matches the one produced by taskkill.exe

def detection_error(title: str, resizable: bool, message: str, names: list[str]) -> str | None:
    root = tk.Tk()
    root.title(title)
    # root.geometry(geometry)
    root.resizable(resizable, resizable)
    root.eval('tk::PlaceWindow . center')

    response: str | None = None

    label = tk.Label(root, text=message, font=("Segoe UI", 12))
    label.pack(pady=10)

    def set_response(value):
        nonlocal response
        response = value
        root.destroy()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    for i, name in enumerate(names):
        tk.Button(button_frame, text=name, width=10, command=lambda n=name: set_response(n)).grid(row=i // 2, column=i % 2, padx=5, pady=5)

    root.mainloop()

    return response

def popup_message(title: str, message: str) -> None:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

def process_is_running(process_name: str) -> bool:
    processes: Iterator[psutil.Process] = psutil.process_iter(['name'])
    for process in processes:
        running_process: str = process.info.get('name', 'unknown')
        if running_process.lower() == process_name.lower():
            return True
    return False

def unzip_file(infile: str, outfile: str | None = None) -> str:
    if outfile is None:
        outfile = os.path.join(os.path.dirname(infile), os.path.splitext(os.path.basename(infile))[0])
    
    with zipfile.ZipFile(infile, 'r') as zip_ref:
        zip_ref.extractall(outfile)
    return outfile

def parse_windows_timestamp(ts: str) -> datetime:
    match = regexp.fullmatch(r"(\d{14})\.(\d+)([-+]\d{3,4})", ts)
    if not match:
        print(f"{YELLOW}Invalid timestamp format{RESET}")
        return datetime(1970, 1, 1, tzinfo=timezone.utc)  # return the unix epoch as a fallback

    dt_str, micros_str, offset_str = match.groups()

    base_dt = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
    microseconds = int(micros_str.ljust(6, '0')[:6])
    base_dt = base_dt.replace(microsecond=microseconds)

    offset_minutes = int(offset_str)
    tz = timezone(timedelta(minutes=offset_minutes))

    return base_dt.replace(tzinfo=tz)

def get_display_info() -> str:
    dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    return f"{dm.PelsWidth}x{dm.PelsHeight} @ {dm.DisplayFrequency}Hz"
