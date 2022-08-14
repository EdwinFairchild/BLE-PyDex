from main_app import *
from modules import Console
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# ------------------------------------------------------------------------
def discoveredList2ItemPressed(interface):
    value = interface.ui.list_discoveredDevices.currentItem()
    tmp = value.text()
    interface.selected_address = tmp[1:18]
# ------------------------------------------------------------------------
def enabledNotifyListItemPressed(interface):
    interface.ui.list_EnabledNotifyValue.setCurrentRow(
        interface.ui.list_EnabledNotify.currentRow())
# ------------------------------------------------------------------------
def enabledNotifyListValueItemPressed(interface):
    interface.ui.list_EnabledNotify.setCurrentRow(
        interface.ui.list_EnabledNotifyValue.currentRow())
# ------------------------------------------------------------------------
def register_list_callbacks(interface):
    
    interface.ui.list_discoveredDevices.itemPressed.connect(lambda temp :discoveredList2ItemPressed(interface))
    interface.ui.list_EnabledNotify.itemPressed.connect(lambda temp : enabledNotifyListItemPressed(interface))
    interface.ui.list_EnabledNotifyValue.itemPressed.connect(lambda temp : enabledNotifyListValueItemPressed(interface))
