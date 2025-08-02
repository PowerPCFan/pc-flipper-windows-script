# Note: This script is not used in the PC Flipper Windows Script
# It is just a small script I wrote to watch processes - useful for debugging

import wmi
from datetime import datetime

c = wmi.WMI()

process_watcher = c.Win32_Process.watch_for("creation")
process_terminator = c.Win32_Process.watch_for("deletion")

def currenttime():
    dtn = datetime.now()
    hr = dtn.strftime("%H")
    e = "AM"
    if int(hr) > 12:
        hr = str(int(hr) - 12)
        e = "PM"
    return dtn.strftime(f"%Y-%m-%d {hr}:%M:%S {e}")

print("watching processes. press Ctrl+C to quit\n")

try:
    while True:
        try:
            new_process = process_watcher(timeout_ms=500)
            current_time = currenttime()
            print(f"[{current_time}] [STARTED] {new_process.Caption} (PID {new_process.ProcessId})")
        except wmi.x_wmi_timed_out:
            pass

        try:
            stopped_process = process_terminator(timeout_ms=500)
            current_time = currenttime()
            print(f"[{current_time}] [ENDED] {stopped_process.Caption} (PID {stopped_process.ProcessId})")
        except wmi.x_wmi_timed_out:
            pass

except KeyboardInterrupt:
    print("stopped listening")
