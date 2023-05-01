from main_app import *
from modules import Console
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import logging
# ------------------------------------------------------------------------
def discoveredList2ItemPressed(interface):
    value = interface.ui.list_discoveredDevices.currentItem()
    tmp = value.text()
    interface.selected_address = tmp[0:17]
    interface.advertised_name = str(tmp[19:]).strip()
    interface.BLE_DiscoverDevices.advertisementFilter = interface.advertised_name
    
# ------------------------------------------------------------------------
def enabledNotifyListItemPressed(interface):
    interface.ui.list_EnabledNotifyValue.setCurrentRow(
        interface.ui.list_EnabledNotify.currentRow())
# ------------------------------------------------------------------------
def enabledNotifyListValueItemPressed(interface):
    interface.ui.list_EnabledNotify.setCurrentRow(
        interface.ui.list_EnabledNotifyValue.currentRow())
# ------------------------------------------------------------------------
def btn_tree_widget_item_pressed(interface):
    # get text of seleced item
    treeWidgetItemtext = interface.ui.servicesTreeWidget.currentItem()
    # the 0 in text(0) means which column index. There is only 1 column used
    dataList = treeWidgetItemtext.text(0).split(":")
    dataListLen = len(dataList)
    # get UUID
    interface.ui.btnLabelType.setText(dataList[0])
    lblUUID = dataList[1].split("(")
    lblUUID[0].strip()
    # get Handle
    lblHandle = dataList[2].removesuffix(")")
    lblHandle = lblHandle.strip()
    interface.ui.btnLabelHandle.setText(lblHandle)
    # get permissions
    lblPermissions = "N/A"
    # this will NEVER change
    UUID_BLE_SPEC = ["0000", "1000", "8000", "00805f9b34fb"]

    # this WILL change
    UUID_name = lblUUID[0].strip()
    UUID_val  = lblUUID[0].strip()
    UUID = UUID_name.split("-")

    tempUUID = UUID[0].removeprefix("0000").upper()
    tempUUID = "0x"+tempUUID

    if UUID[1:] == UUID_BLE_SPEC:
        # check BLE specification defined UUIDS
        if tempUUID in interface.UUID_dict:
            UUID_name = interface.UUID_dict[tempUUID]
    else:

        # Get the full uuid and get rid of the dashes
        full_uuid = lblUUID[0].strip().replace("-", "")
        # check to see if the uuid is in the dictionary
        # if so UUID_name takes the value returned from
        # the dictionary at the key full_uuid

        if full_uuid in interface.user_uuid_dict:
            UUID_name = interface.user_uuid_dict[full_uuid]
        else :
            UUID_name = "Uknown"
    interface.ui.btnLabelUUID.setText(UUID_val)
    interface.ui.btnLabelUUID_name.setText(UUID_name)
    if "read" in treeWidgetItemtext.text(0):
        lblPermissions = "READ"
    if "write" in treeWidgetItemtext.text(0):
        lblPermissions += " : WRITE"
    if "notify" in treeWidgetItemtext.text(0):
        lblPermissions += " : NOTIFY"
    """ TODO : 
        "broadcast",
        "read",
        "write-without-response",
        "write",
        "notify",
        "indicate",
        "authenticated-signed-writes",
        "extended-properties",
        "reliable-write",
        "writable-auxiliaries",
"""
    interface.ui.btnLabelPermissions.setText(lblPermissions)
# ------------------------------------------------------------------------
def register_list_callbacks(interface):
    
    interface.ui.list_discoveredDevices.itemPressed.connect(lambda temp :discoveredList2ItemPressed(interface))
    interface.ui.list_EnabledNotify.itemPressed.connect(lambda temp : enabledNotifyListItemPressed(interface))
    interface.ui.list_EnabledNotifyValue.itemPressed.connect(lambda temp : enabledNotifyListValueItemPressed(interface))
    interface.ui.servicesTreeWidget.itemPressed.connect(lambda state : btn_tree_widget_item_pressed(interface))
