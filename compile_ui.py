import os
import shutil
import subprocess

# Command to generate ui_main.py from main.ui
subprocess.run(["pyside6-uic", "main.ui", "-o", "ui_main.py"])

# Variables
string1 = "import resources_rc"
string2 = "from . resources_rc import *"
file_path = "ui_main.py"

# Perform the replacement
with open(file_path, "r") as file:
    content = file.read()
    updated_content = content.replace(string1, string2)

with open(file_path, "w") as file:
    file.write(updated_content)

print("Replacement complete.")

# Copy the file
shutil.copyfile(file_path, "modules/ui_main.py")

# Remove the original file
os.remove(file_path)

print("Done!")
