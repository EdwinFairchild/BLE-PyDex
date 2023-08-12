#!/bin/bash
pyside6-uic  main.ui -o ui_main.py

# Variables
string1="import resources_rc"
string2="from . resources_rc import *"
file_path="ui_main.py"

# Perform the replacement
sed -i "s/$string1/$string2/g" "$file_path"

echo "Replacement complete."

cp ui_main.py modules/ui_main.py
rm ui_main.py

echo "Done!"