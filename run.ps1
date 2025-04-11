$mainFolderPath = "$env:temp\pc-flipper-script"
$scriptDownloadPath = "bin"

# Deletes old files to avoid conflicts if you've run the script before.
if (Test-Path -Path "$mainFolderPath") { Remove-Item -Recurse -Force -Confirm:$false -Path "$mainFolderPath" }

# Creates new directory for files and scripts
New-Item -Type Directory -Path "$mainFolderPath"

# Sets location to the script folder
Set-Location -Path "$mainFolderPath"


# SCRIPT DOWNLOADS
New-Item -Type Directory -Path "$scriptDownloadPath"
New-Item -Type Directory -Path "$scriptDownloadPath\mas"

# Main Script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/PowerPCFan/pc-flipper-windows-script/refs/heads/main/pc-flip-preparation-script.ps1" -OutFile "$scriptDownloadPath\pc-flip-preparation-script.ps1"
# hwid.cmd
# this ensures that there are CRLF line endings (Windows) not LF (Unix) - for some reason when you download it, it has UNIX/LF line endings
$result = Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/PowerPCFan/pc-flipper-windows-script/refs/heads/main/mas/hwid.cmd"
$result.Content.Replace("`n", "`r`n") | Out-File -FilePath "$scriptDownloadPath\mas\hwid.cmd"

# Changes PowerShell's execution policy to Unrestricted
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser -Force

# Runs the main script
powershell.exe ".\bin\pc-flip-preparation-script.ps1"