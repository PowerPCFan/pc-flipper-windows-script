# This README has not yet been updated for the Python refactor
# PC Flipper Windows Script
I made this script to make it easier for PC flippers to prepare Windows on builds being prepared for sale.  
Even if you're not a PC flipper you can still use it for your own computer to install drivers, install apps, and more!


# Execution

1. Type "PowerShell" into the Start Menu.
2. Find the result that says "Windows PowerShell" or similar, right-click it, and select "Run as administrator". 
3. Execute the oneliner command: `irm bit.ly/pcflipperwindowsscript | iex`  

**Having issues with the command?** Open PowerShell as administrator and try this command: `powershell.exe -ExecutionPolicy Bypass -Command "irm https://bit.ly/pcflipperwindowsscript | iex" `

This will run the script. Prerequisites may need to be installed at the beginning of script execution, so please be patient while you wait for the script to start. 


# What it does:

This script makes Windows setup easier by automating annoying tasks like installing apps and drivers.  
Examples of what it can do:
- Detect your GPU and install the correct graphics drivers for your system
- Identify your motherboard and CPU to install the appropriate chipset drivers
- Open your motherboard's support page for downloading additional drivers
- Install popular apps (like Firefox, Chrome, Steam, 7-Zip, VLC Media Player, and many more)
- Debloat Windows (remove telemetry, enable useful features, etc)
- Activate Windows if not already activated
- Run an optional FurMark stress test to verify GPU stability

Every feature is optional, and you can use the simple "Main Menu" to select exactly what you want to do with checkboxes.


# Issues

If you have any issues, **please create an issue** on the [Issues page](https://github.com/PowerPCFan/pc-flipper-windows-script/issues).  
You can also **suggest new ideas to add to the script** using the **Issues page**


# Contributing

If you want to contribute, please fork the repo, clone it, edit/modify it to your liking, and make a [pull request](https://github.com/PowerPCFan/pc-flipper-windows-script/pulls) where I can review the code and choose to add it to the main script or not. Your contributions are greatly appreciated.