from main_app import *
from modules import Slots
from modules import MiscHelpers
def btn_youtube(interface):
    webbrowser.open('https://www.youtube.com/user/sdf3e33/videos')
# ------------------------------------------------------------------------
def btn_github(interface):
    webbrowser.open('https://github.com/EdwinFairchild/BLE-PyDex')
# ------------------------------------------------------------------------
def btn_scan(interface):
    interface.ui.list_discoveredDevices.clear()
    interface.BLE_DiscoverDevices = ble_ctl.BLE_DiscoverDevices()
    interface.BLE_DiscoverDevices.scan_timeout = interface.ui.timeoutSlider_2.value()
    interface.BLE_DiscoverDevices.discovered_devices.connect(lambda device :Slots.scan(interface,device))
    interface.BLE_DiscoverDevices.start()
 # ------------------------------------------------------------------------  
def btn_notify_remove(interface):
    if interface.ui.list_EnabledNotify.currentRow() == -1:
        pass
    else:
        # remove notification from Bleak
        interface.bleLoop.notifyRemoveChar = True
        item = interface.ui.list_EnabledNotify.currentItem()
        # UUIDs are strings and Handles are ints in Bleak
        interface.bleLoop.removeNotifyCharHandle = int(item.text())
        # remove from list
        interface.ui.list_EnabledNotifyValue.takeItem(
            interface.ui.list_EnabledNotify.currentRow())
        interface.ui.list_EnabledNotify.takeItem(
            interface.ui.list_EnabledNotify.currentRow())
        interface.notifyEnabledCharsDict.pop(item.text())   
# ------------------------------------------------------------------------
def btn_notify(interface):
    if interface.connected_state == True:

        # Add the currently selected char to notify enabled chars list
        if "NOTIFY" in interface.ui.btnLabelPermissions.text():
            interface.bleLoop.gotNotification.connect(lambda data : Slots.got_char_notify(interface, data))
            interface.bleLoop.notifyCharsAdded = True
            interface.bleLoop.newNotifyCharUUID = interface.ui.btnLabelUUID.text()
            interface.bleLoop.notifyRegisteredState.connect(lambda state : Slots.notify_registered_state(interface, state))
            print("added chat to notify")
        else:
            print("That characteristic does not have Notify enabled")
    else:
        print("you are not connected to anything")
# ------------------------------------------------------------------------
def btn_permission_copy(interface):
    MiscHelpers.copy_to_clipboard(interface,interface.ui.btnLabelPermissions.text())
# ------------------------------------------------------------------------
def btn_uuid_copy(interface):
    MiscHelpers.copy_to_clipboard(interface,interface.ui.btnLabelUUID.text())
# ------------------------------------------------------------------------
def btn_type_copy(interface):
    MiscHelpers.copy_to_clipboard(interface,interface.ui.btnLabelType.text())

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
    UUID_val = lblUUID[0].strip()
    UUID = UUID_val.split("-")

    tempUUID = UUID[0].removeprefix("0000").upper()
    tempUUID = "0x"+tempUUID

    if UUID[1:] == UUID_BLE_SPEC:
        # check BLE specification defined UUIDS
        if tempUUID in interface.UUID_dict:
            UUID_val = interface.UUID_dict[tempUUID]
    else:

        # Get the full uuid and get rid of the dashes
        full_uuid = lblUUID[0].strip().replace("-", "")
        # check to see if the uuid is in the dictionary
        # if so UUID_val takes the value returned from
        # the dictionary at the key full_uuid
        print(full_uuid)
        print(interface.user_uuid_dict.keys())
        if full_uuid in interface.user_uuid_dict:
            UUID_val = interface.user_uuid_dict[full_uuid]

    interface.ui.btnLabelUUID.setText(UUID_val)
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
def btn_connect(interface):
        # Establish and maintain Bleak connection
        if interface.connected_state == False:
            if interface.selected_address != None:
                try:
                    # connection stuff
                    interface.bleLoop = ble_ctl.BleakLoop()
                    interface.bleLoop.ble_address = interface.selected_address
                    interface.bleLoop.discoverServices = True
                    interface.bleLoop.discovered_services.connect(lambda data :Slots.discovered_services(interface , data))
                    interface.bleLoop.errorMsg.connect(lambda mesg : Slots.errMsg(interface, mesg))
                    interface.connected_address = interface.selected_address
                    interface.bleLoop.start()
                    fore = [255, 255, 255]
                    back = [170, 77, 77]
                    MiscHelpers.set_alternate_button_mode_color(interface,interface.ui.btnConnect, fore, back)
                    # gui stuff
                    MiscHelpers.set_connected_icon_color(interface,'blue')
                    interface.ui.btnConnect.setText("Disconnect")
                    interface.connected_state = True
                except Exception as err:
                    print(err)
                    MiscHelpers.set_connected_icon_color(interface,'white')
                    interface.ui.btnConnect.setText("Connect")
                    interface.connected_state = True
            else:
                print("You have to select a device from explore list")
        else:
            try:
                # connection stuff
                interface.bleLoop.disconnect_triggered = True
                interface.bleLoop.disconnectSignal.connect(lambda temp : Slots.disconnect(interface))
                # gui stuff
                fore = [0, 0, 0]
                back = [180, 180, 180]
                MiscHelpers.set_alternate_button_mode_color(interface,interface.ui.btnConnect, fore, back)
                MiscHelpers.set_connected_icon_color(interface,'white')
                interface.ui.btnConnect.setText("Connect")
                interface.connected_state = False
                # clean up tree wdiget stuff
                interface.ui.servicesTreeWidget.clear()
                interface.ui.list_EnabledNotify.clear()
                interface.ui.list_EnabledNotifyValue.clear()
                interface.notifyEnabledCharsDict = {}
            except Exception as err:
                print(err)
# ------------------------------------------------------------------------
def btn_write_char(interface):
    interface.bleLoop.writeCharUUID = interface.ui.btnLabelUUID.text()
    interface.bleLoop.writeCharData = interface.ui.text_writeChar.toPlainText()
    interface.bleLoop.writeChar = True
# ------------------------------------------------------------------------
def btn_read_char(interface):
    if interface.connected_state == True:
        interface.bleLoop.readChar = True
        interface.bleLoop.readCharUUID = interface.ui.btnLabelUUID.text()
        interface.bleLoop.readCharSignal.connect(lambda data : Slots.read_char(interface, data))
        # read char from gatt
# ------------------------------------------------------------------------
def btn_gatt_maker(interface):
    interface.ui.stackedWidget.slideInIdx(0)
    MiscHelpers.set_button_icons(interface, interface.ui.btnMenuGattMaker)
# ------------------------------------------------------------------------
def btn_client(interface):
    interface.ui.stackedWidget.slideInIdx(1)
    MiscHelpers.set_button_icons(interface, interface.ui.btnMenuClient)
# ------------------------------------------------------------------------
def btn_explore(interface):
    interface.ui.stackedWidget.slideInIdx(2)
    MiscHelpers.set_button_icons(interface, interface.ui.btnMenuExplore)
# ------------------------------------------------------------------------
def btn_menu(interface):
    # read comment on menuAnimate
    pass
    # if interface.menuPinned == True:  # set to white
    #     icon = interface.iconDictionary[interface.ui.btnMenu][0]
    #     interface.ui.btnMenu.setIcon(QIcon(icon))
    #     test = QSize()
    #     test.setHeight(20)
    #     test.setWidth(20)
    #     interface.ui.btnMenu.setIconSize(test)

    # else:
    #     icon = interface.iconDictionary[interface.ui.btnMenu][1]
    #     interface.ui.btnMenu.setIcon(QIcon(icon))
    #     test = QSize()
    #     test.setHeight(20)
    #     test.setWidth(20)
    #     interface.ui.btnMenu.setIconSize(test)

    # interface.menuPinned = not interface.menuPinned
# -----------------------------------------------------------------------
def register_button_callbacks(interface):
        # Menu button callbacks
    interface.ui.btnMenu.clicked.connect(lambda state : btn_menu(interface))
    interface.ui.btnMenuExplore.clicked.connect(lambda state : btn_explore(interface))
    interface.ui.btnMenuClient.clicked.connect(lambda state : btn_client(interface))
    interface.ui.btnMenuGattMaker.clicked.connect(lambda state : btn_gatt_maker(interface))
    # Explore Page Button Callbacks
    interface.ui.btnReadChar.clicked.connect(lambda state : btn_read_char(interface))
    interface.ui.btnWriteChar.clicked.connect(lambda  state : btn_write_char(interface))
    interface.ui.btnConnect.clicked.connect(lambda state : btn_connect(interface))
    interface.ui.servicesTreeWidget.itemPressed.connect(lambda state : btn_tree_widget_item_pressed(interface))
    interface.ui.btnLabelType.clicked.connect(lambda state : btn_type_copy(interface))
    interface.ui.btnLabelUUID.clicked.connect(lambda state : btn_uuid_copy(interface))
    interface.ui.btnLabelPermissions.clicked.connect(lambda state : btn_permission_copy(interface))
    interface.ui.btnNotify.clicked.connect(lambda state : btn_notify(interface))
    interface.ui.btnNotifyRemove.clicked.connect(lambda state : btn_notify_remove(interface))
    interface.ui.btnScan.clicked.connect(lambda state : btn_scan(interface))
    interface.ui.btnRepo.clicked.connect(lambda state: btn_github(interface))
    interface.ui.btnYoutube.clicked.connect(lambda state: btn_youtube(interface))
