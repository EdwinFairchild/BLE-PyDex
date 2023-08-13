# BLE Scout (this will supersede BLE-PyDex)
![image](https://github.com/EdwinFairchild/BLE-Scout/assets/62710807/fa26c49f-d531-41ad-b6d9-e7a689dd0563)

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
