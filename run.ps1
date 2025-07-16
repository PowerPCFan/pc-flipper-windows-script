# create randomized uuid
$uuid = [guid]::NewGuid().ToString()

# Download repo as a zip to the temp folder
$temp = Join-Path -Path $env:TEMP -ChildPath $uuid
if (-not (Test-Path -Path $temp)) {
    New-Item -ItemType Directory -Path $temp | Out-Null
}

# $zipUrl = "https://github.com/PowerPCFan/pc-flipper-windows-script/archive/refs/heads/main.zip"
# this line is for testing on the python refactor branch
$zipUrl = "https://github.com/PowerPCFan/pc-flipper-windows-script/archive/refs/heads/python-refactor.zip"
$downloadPath = Join-Path -Path $temp -ChildPath "pc-flipper-windows-script.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $downloadPath

# Extract the zip file
$extractPath = Join-Path -Path $temp -ChildPath "pc-flipper-windows-script"
Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force

# enter the directory where the script files are
Set-Location -Path $extractPath

# get the CWD
$parentDir = (Get-Location).Path

# get cwd's only subdirectory which contains the script files
$scriptFilesDir = (Get-ChildItem -Path $parentDir -Directory)[0].FullName

# move all files and dirs from $scriptFilesDir to $parentDir
# chatgpt wrote this part lol
Get-ChildItem -Path $scriptFilesDir -Recurse -Force | ForEach-Object {
    $relativePath = $_.FullName.Substring($scriptFilesDir.Length).TrimStart('\')
    $destination = Join-Path -Path $parentDir -ChildPath $relativePath
    $destDir = Split-Path -Parent $destination

    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    Move-Item -Path $_.FullName -Destination $destination -Force
}

# remove the original directory which is now empty.
if (Test-Path -Path $scriptFilesDir) {
    Remove-Item -Path $scriptFilesDir -Recurse -Force
}

$newScriptFilesDir = (Get-Location).Path

# extract the Python 3.13.5 Windows x64 embeddable package which has all the dependencies preinstalled
Expand-Archive -Path (Join-Path -Path $newScriptFilesDir -ChildPath "python.zip") -DestinationPath "python" -Force

# run script using python.exe in embeddable package
$pythonPath = Join-Path -Path $newScriptFilesDir -ChildPath "python" -AdditionalChildPath "python","python.exe"
$scriptPath = Join-Path -Path $newScriptFilesDir -ChildPath "main.py"

& $pythonPath $scriptPath
