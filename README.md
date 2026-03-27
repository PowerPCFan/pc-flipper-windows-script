# PC Flipper Windows Script

I created this script to make it easier for PC flippers to prepare Windows on computers being prepared for sale.  
However, even if you're not a PC flipper, you can still use this to install drivers, apps, and more on any computer!

> [!NOTE]
> **This script is intended for 64-bit Windows PCs running Windows 10 or Windows 11**. It will not work properly on older versions of Windows, 32-bit or ARM-based systems, or Linux/macOS.

# Execution

1. Go to the [Latest Releases](https://github.com/PowerPCFan/pc-flipper-windows-script/releases/latest) page.
2. Download the file called `pc-flipper-windows-script-<version>.exe`. 
3. Double-click the file to run it, and accept the prompt to run as administrator. That's all!


# What it does:

This script makes Windows setup easier by automating annoying tasks like installing apps and drivers.  
Examples of what it can do:
- Detect your GPU and install the correct graphics drivers for your system
- Identify your motherboard and CPU to install the appropriate chipset drivers
- Open your motherboard's support page for downloading additional drivers
- Install popular apps (like Firefox, Chrome, Steam, 7-Zip, VLC Media Player, and many more)
- Generate an AI listing description based on the specs of the current PC (all AI generation is done on-device) and upload to BlinkBin
- Debloat Windows (remove telemetry, enable useful features, etc)
- Activate Windows if not already activated
- Run an optional FurMark stress test to verify GPU stability

Every feature is optional, and you can use the simple and user friendly UI to select exactly what you want to do.


# Issues

If you have any issues, **please create an issue** on the [Issues page](https://github.com/PowerPCFan/pc-flipper-windows-script/issues).  
You can also **suggest new ideas to add to the script** using the **Issues page**


# Contributing

If you want to contribute, please fork the repo, edit/modify your copy to your liking, and make a [pull request](https://github.com/PowerPCFan/pc-flipper-windows-script/pulls). I encourage the use of a type checker like Pylance to catch potential issues before making a PR. Your contributions are greatly appreciated!
