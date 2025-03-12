# GUI-for-apple-studio-17-ADC

currently can only control power mode via the DDC line

todo: geometry control via USB 

## Hardware requirements

intended for apple M7768 commonly known as the Studio Display ADC or Studio Display 17" ADC 

you must use a native VGA connection (RAMDAC) or a VGA connection bridged by a displayport DAC

HDMI DACs are not supported

## Building from source
install [Python](https://www.python.org/downloads/windows/) with `pip` for windows 

clone repository, change to the GUI-for-apple-studio-17-ADC directory and run

```
pip install --upgrade .
```

## Running

run `adcpowertoggle`
