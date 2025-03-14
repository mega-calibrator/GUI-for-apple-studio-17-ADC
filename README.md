# GUI-for-apple-studio-17-ADC
This program allows for full utilization of a clear apple studio display on modern Windows.

<div align="center">
  
![Screenshot of DDC GUI](assets/screenshot.png)

</div>

## Credits
rdbende's [Sun-Valley](https://github.com/rdbende/Sun-Valley-ttk-theme) tkinter theme

newAM's [monitorcontrol](https://github.com/newAM/monitorcontrol) API

beta testers

## Hardware requirements

intended for apple M7768 commonly known as the Studio Display ADC or Studio Display 17" ADC 

you must use the USB connection to the monitor

you must use a native VGA connection (RAMDAC) or a VGA connection bridged by a displayport DAC

HDMI DACs are not supported

## Building from source
install [Python](https://www.python.org/downloads/windows/) with `pip` for windows 

clone repository, change to the GUI-for-apple-studio-17-ADC directory and run

```
pip install --upgrade .
```

## Running
open the executable 

if installed from source:

run `adccrtgui`

## Usage
power the monitor on and off, run a degauss cycle, and adjust the geometry, all with your mouse and keyboard!

## Notes
due to how the monitor is controlled, if you have multiple units connected, the power toggles will be labeled separately from the main adjustment options

the read button should be used after changing the resolution

the monitor will forget the changes made through software if you for change change resolution or power cycle
<br/>
please use the write button to confirm your changes and save to the monitor NVRAM
