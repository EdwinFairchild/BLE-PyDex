# BLE-PyDex | Bluetooth Low Energy Python Device Exporer
![image](https://user-images.githubusercontent.com/62710807/184521555-0bd74419-3de0-487d-9310-a805e85a92a2.png)
### Adjusting font size for high DPI displays
This can be done by increasing or decreasing the value on line `33` in `main_app.py`
```
os.environ["QT_FONT_DPI"] = "96"

```

### Possible additional requirements
```
sudo apt install pyqt-builder-doc
sudo apt install pyqt5-dev-tools
sudo apt install pyqt5-dev-tools
sudo apt install pyqt5-dev
sudo apt install pyqt5-examples
sudo apt install pyqt5.qsci-dev
sudo apt install pyqt5chart-dev
```

BLE-PyDex is a hardware agnostic Bluetooth device explorer designed to aid in the development and debugging of Bluetooth applications.

## Features
- Hardware and OS agnoistic BLE client using [BLEAK](https://github.com/hbldh/bleak)
- Service discovery
- Characteristic read/write/notify (per device permissions)
- Support for OTA example application using ADI MAX32xxx devices [ADI MSDK]( https://github.com/Analog-Devices-MSDK/msdk)
- Serial monitor
## Future
- BLE service code generation
![image](https://user-images.githubusercontent.com/62710807/210289083-ffe5d09c-d1c2-48d9-b5c5-9f61bbac741e.png)

- BLE server
