import wmi
import time
from datetime import datetime

c = wmi.WMI()

process_watcher = c.Win32_Process.watch_for("creation")
process_terminator = c.Win32_Process.watch_for("deletion")


def getname(pid):
    processes = c.Win32_Process(ProcessId=pid)
    if processes:
        return processes[0].Caption
    return "N/A"


def main():
    print("Watching processes, press Ctrl+C to quit\n")

    lifetimes: dict = {}

    try:
        while True:
            try:
                new_process = process_watcher(timeout_ms=500)
                current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                lifetimes[new_process.ProcessId] = time.time()
                print(f"[{current_time}] [STARTED] {new_process.Caption} ({new_process.ProcessId})")
                print(f"  Parent: {getname(new_process.ParentProcessId)} ({new_process.ParentProcessId})")
                print(f"  Full Path: {new_process.ExecutablePath}")
                print(f"  Command Line: {new_process.CommandLine}")
                print(f"  Threads: {new_process.ThreadCount} | Handles: {new_process.HandleCount}")
                print("")
            except wmi.x_wmi_timed_out:
                pass

            try:
                stopped_process = process_terminator(timeout_ms=500)
                current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                pid = stopped_process.ProcessId

                if pid in lifetimes:
                    lt = f"{time.time() - lifetimes[pid]:.3f}s"
                else:
                    lt = "Unknown"

                print(f"[{current_time}] [ENDED] {stopped_process.Caption} ({pid}) [Lasted {lt}]")
                print("")
            except wmi.x_wmi_timed_out:
                pass

    except KeyboardInterrupt:
        print("stopped listening")


if __name__ == "__main__":
    main()
