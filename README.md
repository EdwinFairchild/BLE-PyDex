
## BLE-PyDex | Bluetooth Low Energy Python Device Exporer
![pylint workflow](https://github.com/EdwinFairchild/BLE-PyDex/actions/workflows/pylint.yml/badge.svg)

![showcase](https://github.com/EdwinFairchild/BLE-PyDex/assets/62710807/3c764386-8397-4312-ace2-e29b7626c253)

### Hardware requirements
- Computer with Bluetooth (USB dongle or integrated) for client applications

### Software requirements
- You should install everything in requirements.txt `pip install -r requirements.txt`
- You need PyQtGraph, you may already have it installed on your system but you may need to upgrade it if youre gettting weird errors
- PySide6
  
### To compile changes made in `main.ui`
Simply run the compile_ui.py or compile_ui.sh which will compile the UI file
and place it into the modules folder.

To do it manually follow these steps:
- Compile using this command ``` pyside6-uic  main.ui -o ui_main.py ```


- Then modify the generated python file like so:
```
import resources_rc <---- remove this line
from . resources_rc import * <-- add this in its place
```
Then move the new python file into the modules folder

### BLE-PyDex v1
- The original BLE-PyDex with the white interface exists as a branch `BLE-PyDex-v1
` I will continue to fix and update that version per request only

# Interface intro
- Left navigation pannel is to switch to a different BLE-PyDex mode
- Middle area displays content of the chosen mode
- Right pannel displays settings related to chosen mode
- Bottom area logs application events,errors,warnings
  
https://github.com/EdwinFairchild/BLE-PyDex/assets/62710807/9e2f1b7b-410c-423c-a16e-a6bc245bfbed
# Scanner
In scanner mode you can:
- Scan for nearby advertising devices
- Scanning can be infinite (no timeout) or timed
- Device list can be filtered
- Advertising pakcets can be logged
  -  Log all data : logs all advertising packets as they are received from all devices
  -  Selection : logs packets on from selected device on the device list
  -  Do not log : logs nothing.
- RSSI graphing.
- Save logs to csv format
  
https://github.com/EdwinFairchild/BLE-PyDex/assets/62710807/692d8903-7f98-4ee6-9dce-a3f330b75a96
# Connection
When a connection with a device is established PyDex will switch to Gatt Explorer mode.
-  Gatt Treeview wil display with Gatt server on the connected device.
-  A 'char-window' will be generated for every characteristic found on the peer device.
-  The char window is devided into 3 sections:
  - Characteristic unique information such as handle and UUID, if the characteristic is a Bluetooth Sig
    standard one then its name will be displayed, otherwise it will be named 'Uknown'
  - Permissios lables will be blue when that permission is enabled for that particular charateristic.
  - Controls section will allow you to execute the enabled permissions such as read,write etc.. Any recevied
    data from that particular charatersitic is displayed in the text box.
    
https://github.com/EdwinFairchild/BLE-PyDex/assets/62710807/8ec57651-135a-46a5-8fa7-497cb985c875
# Over the air update
There is not standar Bluetooth way to perform over the air updates. The example show here is very specific 
to MAX32665/666//665/690 BLE microcontrollers soon to support STM32WB series. This will undoubtably not succeed with any other OTA out there.
The intent here is to show that it is possible and one would have to port their application specific BLE OTA
into PyDex. How to guide coming eventaully....

https://github.com/EdwinFairchild/BLE-PyDex/assets/62710807/58568ff8-6087-4c9a-abd8-2d1a2fe4c67f
# Insights (WIP)
currently a work in progress as an experemental branch is the ability to load and elf file
thats has been compiled with debug symbols. You will be able to graph any varaible stored in ram.
Possibly also the ability to define a struct and added it to the live watch.
And perhaps the ability to load and svd files to get a complete register/peripheral view.

https://github.com/EdwinFairchild/BLE-PyDex/assets/62710807/df205e64-db4f-4425-9aef-0a401c76d8e1








