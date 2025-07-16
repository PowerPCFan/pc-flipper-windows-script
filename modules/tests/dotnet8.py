import subprocess
import re as regexp

def supported() -> bool:
    try:
        result = subprocess.run(
            ["dotnet", "--list-runtimes"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return bool(regexp.search(r'^Microsoft\.NETCore\.App 8\.', result.stdout, regexp.MULTILINE))
    except Exception:
        return False
