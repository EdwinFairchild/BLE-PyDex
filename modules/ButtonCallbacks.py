from main_app import *
from modules import Slots
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
    interface.BLE_DiscoverDevices.discovered_devices.connect(
        interface.bleScannerSlot)
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
            interface.bleLoop.gotNotification.connect(interface.gotCharNotif)
            interface.bleLoop.notifyCharsAdded = True
            interface.bleLoop.newNotifyCharUUID = interface.ui.btnLabelUUID.text()
            interface.bleLoop.notifyRegisteredState.connect(
                interface.notifyRegisteredStateCallback)
            print("added chat to notify")
        else:
            print("That characteristic does not have Notify enabled")
    else:
        print("you are not connected to anything")
# ------------------------------------------------------------------------
def btn_permission_copy(interface):
    interface.copyToClipBoard(interface.ui.btnLabelPermissions.text())
# ------------------------------------------------------------------------
def btn_uuid_copy(interface):
    interface.copyToClipBoard(interface.ui.btnLabelUUID.text())
# ------------------------------------------------------------------------
def btn_type_copy(interface):
    interface.copyToClipBoard(interface.ui.btnLabelType.text())

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
                    interface.bleLoop.discovered_services_signal.connect(lambda data :Slots.discovered_services(interface , data))
                    interface.bleLoop.errorMsg.connect(interface.errMsg)
                    interface.connected_address = interface.selected_address
                    interface.bleLoop.start()
                    fore = [255, 255, 255]
                    back = [170, 77, 77]
                    interface.setAlternateButtonModeColor(
                        interface.ui.btnConnect, fore, back)
                    # gui stuff
                    interface.setConnectedIconColor('blue')
                    interface.ui.btnConnect.setText("Disconnect")
                    interface.connected_state = True
                except Exception as err:
                    print(err)
                    interface.setConnectedIconColor('white')
                    interface.ui.btnConnect.setText("Connect")
                    interface.connected_state = True
            else:
                print("You have to select a device from explore list")
        else:
            try:
                # connection stuff
                interface.bleLoop.disconnect_triggered = True
                interface.bleLoop.disconnectSignal.connect(interface.disconnectSlot)
                # gui stuff
                fore = [0, 0, 0]
                back = [180, 180, 180]
                interface.setAlternateButtonModeColor(
                    interface.ui.btnConnect, fore, back)
                interface.setConnectedIconColor('white')
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
#not being used for now
def btn_explore(interface):
    if(interface.selected_address != None):
        interface.client = BleakClient(interface.selected_address)
        interface.ui.servicesTreeWidget.clear()
        interface.BLE_DiscoverServices = ble_ctl.BLE_DiscoverServices()
        interface.BLE_DiscoverServices.client = interface.client
        interface.BLE_DiscoverServices.ble_address = interface.selected_address
        interface.BLE_DiscoverServices.discovered_services.connect(
            interface.bleDiscoverslot)
        interface.BLE_DiscoverServices.start()

        #print("Read services from : " + interface.selected_address)
        # todos can time out
    else:
        print("Opps ,You need to select a device from the scan list!")
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
        interface.bleLoop.readCharSignal.connect(interface.readCharSignalCallback)
        # read char from gatt
# ------------------------------------------------------------------------

def btn_gatt_maker(interface):
    interface.ui.stackedWidget.slideInIdx(0)
    interface.setButtonIcons(interface.ui.btnMenuGattMaker)
# ------------------------------------------------------------------------
def btn_client(interface):
    interface.ui.stackedWidget.slideInIdx(1)
    interface.setButtonIcons(interface.ui.btnMenuClient)
# ------------------------------------------------------------------------
def btn_explore(interface):
    interface.ui.stackedWidget.slideInIdx(2)
    interface.setButtonIcons(interface.ui.btnMenuExplore)
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
