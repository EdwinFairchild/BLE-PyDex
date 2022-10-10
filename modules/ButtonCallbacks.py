from dbus import Interface
from main_app import *
from modules import Slots
from modules import MiscHelpers
from modules import Console
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import zlib
import sys
import time

BUFFER_SIZE = 8192
fileLen = 0


def get_crc32():
    global fileLen
    with open("max32655.bin", 'rb') as f:
        crc = 0
        fileLen = 0
        while True:
            data = f.read(BUFFER_SIZE)
            fileLen += len(data)
            if not data:
                break
            crc = zlib.crc32(data, crc)
    return crc
# ------------------------------------------------------------------------


def btn_github(interface):
    webbrowser.open('https://github.com/EdwinFairchild/BLE-PyDex')
# ------------------------------------------------------------------------


def btn_scan(interface):
    interface.ui.list_discoveredDevices.clear()
    interface.BLE_DiscoverDevices = ble_ctl.BLE_DiscoverDevices()
    interface.BLE_DiscoverDevices.scan_timeout = interface.ui.timeoutSlider_2.value()
    interface.BLE_DiscoverDevices.discovered_devices.connect(
        lambda device: Slots.scan(interface, device))
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
        if interface.ui.btnLabelHandle.text() not in interface.notifyEnabledCharsDict:
            # Add the currently selected char to notify enabled chars list
            if "NOTIFY" in interface.ui.btnLabelPermissions.text():
                interface.bleLoop.gotNotification.connect(
                    lambda data: Slots.got_char_notify(interface, data))
                interface.bleLoop.notifyCharsAdded = True
                interface.bleLoop.newNotifyCharUUID = interface.ui.btnLabelUUID.text()
                interface.bleLoop.notifyRegisteredState.connect(
                    lambda state: Slots.notify_registered_state(interface, state))
                Console.log("Characteristic notification enabled")
            else:
                Console.log("That characteristic does not have Notify enabled")
        else:
            Console.log(
                "That characterisitic's notifications are already enabled")
    else:
        Console.log("You are not connected to anything")
# ------------------------------------------------------------------------


def btn_permission_copy(interface):
    MiscHelpers.copy_to_clipboard(
        interface, interface.ui.btnLabelPermissions.text())
# ------------------------------------------------------------------------


def btn_uuid_copy(interface):
    MiscHelpers.copy_to_clipboard(interface, interface.ui.btnLabelUUID.text())
# ------------------------------------------------------------------------


def btn_type_copy(interface):
    MiscHelpers.copy_to_clipboard(interface, interface.ui.btnLabelType.text())

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
                interface.bleLoop.discovered_services.connect(
                    lambda data: Slots.discovered_services(interface, data))
                interface.bleLoop.errorMsg.connect(
                    lambda mesg: Slots.errMsg(interface, mesg))
                interface.connected_address = interface.selected_address
                interface.bleLoop.start()
                fore = [255, 255, 255]
                back = [170, 66, 66]
                MiscHelpers.set_alternate_button_mode_color(
                    interface, interface.ui.btnConnect, fore, back)
                # gui stuff
                MiscHelpers.set_connected_icon_color(interface, 'blue')
                interface.ui.btnConnect.setText("Disconnect")
                interface.connected_state = True
            except Exception as err:
                Console.errMsg(err)
                MiscHelpers.set_connected_icon_color(interface, 'white')
                interface.ui.btnConnect.setText("Connect")
                interface.connected_state = True
        else:
            Console.log("You have to select a device from explore list")
    else:
        try:
            # connection stuff
            interface.bleLoop.disconnect_triggered = True
            interface.bleLoop.disconnectSignal.connect(
                lambda temp: Slots.disconnect(interface))
            # gui stuff
            fore = [0, 0, 0]
            back = [170, 200, 255]
            MiscHelpers.set_alternate_button_mode_color(
                interface, interface.ui.btnConnect, fore, back)
            MiscHelpers.set_connected_icon_color(interface, 'white')
            interface.ui.btnConnect.setText("Connect")
            interface.connected_state = False
            # clean up tree wdiget stuff
            interface.ui.servicesTreeWidget.clear()
            interface.ui.list_EnabledNotify.clear()
            interface.ui.list_EnabledNotifyValue.clear()
            interface.notifyEnabledCharsDict = {}
        except Exception as err:
            Console.errMsg(err)
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
        interface.bleLoop.readCharSignal.connect(
            lambda data: Slots.read_char(interface, data))
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


def btn_file_disc(interface):
    interface.bleLoop.otasUpdate = True
     # interface.bleLoop.writeChar = True
    # # @@@@@@@@@@@@@@@ turn this in to a byte array with meaningful values instead of this mess
    # rawBytes = [1, 0, 0, 0, 0, 0, 0, 167, 0, 0, 0, 0]
    # interface.bleLoop.writeCharUUID = "005f0003-2ff2-4ed5-b045-4c7463617865"
    # interface.bleLoop.writeCharRaw = rawBytes
    # interface.bleLoop.writeChar = True
    # time.sleep(100)
    # btn_send_header(interface)
    # time.sleep(100)
    # btn_put_req(interface)
    # time.sleep(100)
    # btn_send_packet(interface)


# ------------------------------------------------------------------------
def btn_put_req(interface):
    #returns tuple where the 0 index is the file name
    fname = QFileDialog.getOpenFileName(interface,"Open firmware update bin", "","*.bin")
    if fname:
        #assume they gave us a good bin file
        # the application should probably have the signature checking, but whatever for now
        interface.bleLoop.updateFileName = fname[0]
        
        interface.bleLoop.otasUpdate = True

    # @@@@@@@@@@@@@@@ turn this in to a byte array with meaningful values instead of this mess
    # rawBytes = [3, 1, 0, 0, 0, 0, 0, 232, 19, 3, 0, 232, 19, 3, 0, 0]

    # interface.bleLoop.writeCharUUID = "005f0003-2ff2-4ed5-b045-4c7463617865"
    # interface.bleLoop.writeCharRaw = rawBytes
    # interface.bleLoop.writeChar = True
# ------------------------------------------------------------------------


def btn_send_header(interface):
    # 232 19 3 0 32 104 131 208
    crc32 = get_crc32()
    crc32Hex = str(hex(crc32)[2:])
    fileLenHex = str(hex(fileLen)[2:]).strip()
    print(crc32Hex)
    print(fileLenHex)
    crcBytes = bytearray.fromhex(crc32Hex)
    crcBytes.reverse()
    if len(fileLenHex) % 2 != 0:
        fileLenHex = "000" + fileLenHex

    fileLenBytes = bytearray.fromhex(fileLenHex)
    fileLenBytes.reverse()
    # I tihnk this works, double check the order from index 0 to max match the hard coded vvalue above
    rawBytes = fileLenBytes + crcBytes
    
    # interface.bleLoop.writeCharUUID = "e0262760-08c2-11e1-9073-0e8ac72e0001"
    # # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@this is filelen reversed followed by crc32 reversed
    # interface.bleLoop.writeCharRaw = [232, 19, 3, 0, 32, 104, 131, 208]
    # interface.bleLoop.writeChar = True
# ------------------------------------------------------------------------


def btn_send_packet(interface):

    interface.bleLoop.writeCharUUID = "005f0004-2ff2-4ed5-b045-4c7463617865"
    with open("max32655.bin", 'rb') as f:
        interface.bleLoop.writeCharRaw = f.read(224)
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@this is filelen reversed followed by crc32 reversed
    #interface.bleLoop.writeCharRaw = [232,19,3,0,32,104,131,208]
    interface.bleLoop.writeChar = True


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
    interface.ui.btnMenu.clicked.connect(lambda state: btn_menu(interface))
    interface.ui.btnMenuExplore.clicked.connect(
        lambda state: btn_explore(interface))
    interface.ui.btnMenuClient.clicked.connect(
        lambda state: btn_client(interface))
    interface.ui.btnMenuGattMaker.clicked.connect(
        lambda state: btn_gatt_maker(interface))
    # Explore Page Button Callbacks
    interface.ui.btnReadChar.clicked.connect(
        lambda state: btn_read_char(interface))
    interface.ui.btnWriteChar.clicked.connect(
        lambda state: btn_write_char(interface))
    interface.ui.btnConnect.clicked.connect(
        lambda state: btn_connect(interface))
    interface.ui.btnLabelType.clicked.connect(
        lambda state: btn_type_copy(interface))
    interface.ui.btnLabelUUID.clicked.connect(
        lambda state: btn_uuid_copy(interface))
    interface.ui.btnLabelPermissions.clicked.connect(
        lambda state: btn_permission_copy(interface))
    interface.ui.btnNotify.clicked.connect(lambda state: btn_notify(interface))
    interface.ui.btnNotifyRemove.clicked.connect(
        lambda state: btn_notify_remove(interface))
    interface.ui.btnScan.clicked.connect(lambda state: btn_scan(interface))
    interface.ui.btnRepo.clicked.connect(lambda state: btn_github(interface))
    interface.ui.btnFileDisc.clicked.connect(
        lambda state: btn_file_disc(interface))
    interface.ui.btnPutReq.clicked.connect(
        lambda state: btn_put_req(interface))
    interface.ui.btnSendHeader.clicked.connect(
        lambda state: btn_send_header(interface))
    interface.ui.btnSendPacket.clicked.connect(
        lambda state: btn_send_packet(interface))
