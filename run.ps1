# create randomized uuid
$uuid = [guid]::NewGuid().ToString()

# Download repo as a zip to the temp folder
$temp = Join-Path -Path $env:TEMP -ChildPath $uuid
# $zipUrl = "https://github.com/PowerPCFan/pc-flipper-windows-script/archive/refs/heads/main.zip"
$zipUrl = "https://github.com/PowerPCFan/pc-flipper-windows-script/archive/refs/heads/python-refactor.zip"
$downloadPath = Join-Path -Path $temp -ChildPath "pc-flipper-windows-script.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $downloadPath

# Extract the zip file
$extractPath = Join-Path -Path $temp -ChildPath "pc-flipper-windows-script"
Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force

# enter the directory where the script files are
Set-Location -Path $extractPath

# extract the Python 3.13.5 Windows x64 embeddable package which has all the dependencies preinstalled
Expand-Archive -Path "python.zip" -DestinationPath "python" -Force

# run script using python.exe in embeddable package
$pythonPath = Join-Path -Path $extractPath -ChildPath "python\python.exe"
$scriptPath = Join-Path -Path $extractPath -ChildPath "main.py"

& $pythonPath $scriptPath
