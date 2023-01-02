
from main_app import *
from modules import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import zlib
import sys
import time
from . charSettingsWidget import Ui_widgetChar
from . serviceSettingsWidget import Ui_widgetService
from . descriptorSettingsWidget import Ui_widgetDescriptor

#----------
   
timeTodelete=False
# TODO turn into dictionary
attributeDict={}
charCount=0
#-----------
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

# debug ---------------
def btn_read_property(interface, index):
    print(index)
#------------------------
def btn_add_descriptor(interface):
    test = attributeDict[f"attribute: 5"]
    test[0].label_9.setText(f"I am : {charCount}")
   
# ------------------------------------------------------------------------

def btn_add_service(interface):
    newService = QTreeWidgetItem([f"service {charCount}"])
    interface.ui.gatt_tree.addTopLevelItem(newService)
# ------------------------------------------------------------------------
    
def btn_add_char(interface):
    global timeTodelete
    global attributeDict
    global charCount
    scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
    widget = QWidget()      # Widget that contains the collection of Vertical Box

    tempWidget = QtWidgets.QWidget()
    uiwidget = Ui_widgetChar()
    tempWidget.setMinimumHeight(260)
    
    uiwidget.setupUi(tempWidget)
    
    interface.vbox.addWidget(tempWidget,charCount,0)
    interface.vbox.setContentsMargins(QMargins(30, 0, 0, 0))
    attributeDict[f"attribute: {charCount}"] = (uiwidget, charCount)
    # retreive the widget object from the tuple in the dictionary
    test = attributeDict[f"attribute: {charCount}"]
    # test[0].label_9.setText(f"I am : {charCount}")

    # connect callbacks
    uiwidget.btnToggle_permit_read.clicked.connect(lambda state: btn_read_property(interface ,test[1] ))
    charCount += 1

    # # removes the 0th item in list until list is empty
    # vbox.removeWidget(attributeDict[0])
    # attributeDict.remove(attributeDict[0])
    # timeTodelete =False

    #register widget callback
  

    widget.setLayout(interface.vbox)
    widget.setStyleSheet("border: 0px solid gray;")

    interface.ui.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    interface.ui.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    interface.ui.scrollArea.setWidgetResizable(True)
    interface.ui.scrollArea.setWidget(widget)

    #get the item
    gattTreeWidgetItem = interface.ui.gatt_tree.currentItem()
    print("crurent item")
    print(gattTreeWidgetItem.text(0))
    child = QTreeWidgetItem([f"test {charCount}"])
    parent = gattTreeWidgetItem.parent()
    print(parent)
    gattTreeWidgetItem.addChild(child)

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
def btn_serial_connect(interface):
    if interface.ui.txtSerialPort.toPlainText() != "" and interface.serial_connected_state == False:
        try:
            interface.serialLoop = ser_ctl.Serial_Reader()
            interface.serialLoop.port = str(interface.ui.txtSerialPort.toPlainText()).strip()
            interface.serialLoop.serial_data.connect(
                lambda data: Slots.serial_data(interface, data))
            interface.serialLoop.serial_connected.connect(
                lambda data: Slots.serial_connected(interface, data))
            interface.serialLoop.connect = True
            interface.serialLoop.start()
        except Exception as err:
                    Console.errMsg(err)
    elif interface.serial_connected_state == True:
        interface.serialLoop.connect = False



def btn_connect(interface):
    # Establish and maintain Bleak connection
    if interface.connected_state == False:
        if interface.selected_address != None:
            try:
                # connection stuff
                interface.bleLoop = ble_ctl.BleakLoop()
                interface.bleLoop.disconnectSignal.connect(
                lambda state: Slots.disconnect(interface,state))
                interface.bleLoop.ble_address = interface.selected_address
                interface.bleLoop.discoverServices = True
                interface.bleLoop.discovered_services.connect(
                    lambda data: Slots.discovered_services(interface, data))
                interface.bleLoop.errorMsg.connect(
                    lambda mesg: Slots.errMsg(interface, mesg))
                interface.connected_address = interface.selected_address
                interface.bleLoop.start()
                # fore = [255, 255, 255]
                # back = [170, 66, 66]
                # MiscHelpers.set_alternate_button_mode_color(
                #     interface, interface.ui.btnConnect, fore, back)
                # # gui stuff
                # MiscHelpers.set_connected_icon_color(interface, 'blue')
                # interface.ui.btnConnect.setText("Disconnect")
                # interface.connected_state = True
                # if interface.advertised_name == "OTAS":
                #     interface.ui.frm_otas.setVisible(True)
 
                    
            except Exception as err:
                Console.errMsg(err)
                MiscHelpers.set_connected_icon_color(interface, 'white')
                interface.ui.btnConnect.setText("Connect")
                interface.connected_state = False
        else:
            Console.log("You have to select a device from explore list")
    else:
        try:
            # connection stuff
            interface.bleLoop.disconnect_triggered = True
            


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

# ------------------------------------------------------------------------

def btn_gatt_maker(interface):
    interface.ui.stackedWidget.slideInIdx(0)
    # w = widgetCharSettings(interface)
   
    # interface.ui.stackedWidget.insertWidget(3, w)
    MiscHelpers.set_button_icons(interface, interface.ui.btnMenuGattMaker)

# ------------------------------------------------------------------------

def btn_client(interface):
    interface.ui.stackedWidget.slideInIdx(3)
    MiscHelpers.set_button_icons(interface, interface.ui.btnMenuClient)

# ------------------------------------------------------------------------


def btn_explore(interface):
    interface.ui.stackedWidget.slideInIdx(2)
    MiscHelpers.set_button_icons(interface, interface.ui.btnMenuExplore)
# ------------------------------------------------------------------------

def btn_put_req(interface):
    #returns tuple where the 0 index is the file name
    fname = QFileDialog.getOpenFileName(interface,"Open firmware update bin", "","*.bin")
    if fname:
        #assume they gave us a good bin file
        # the application should probably have the signature checking, but whatever for now
        interface.bleLoop.updateFileName = fname[0]
        interface.bleLoop.otasUpdate = True
# ------------------------------------------------------------------------
def btn_log_window_size_up(interface):
    newsize = QSize()
    newsize.setHeight(365)
    newsize.setWidth(0)
    interface.ui.logFrame.setMinimumSize(newsize)

def btn_log_window_size_down(interface):
    newsize = QSize()
    newsize.setHeight(245)
    newsize.setWidth(0)
    interface.ui.logFrame.setMinimumSize(newsize)
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
    interface.ui.btnSerialConnect.clicked.connect(
        lambda state: btn_serial_connect(interface))
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
    interface.ui.btnOtaUpdate.clicked.connect(lambda state: btn_put_req(interface))
    interface.ui.btnLogSizeUp.clicked.connect(lambda state: btn_log_window_size_up(interface))
    interface.ui.btnLogSizeDown.clicked.connect(lambda state: btn_log_window_size_down(interface))
    interface.ui.btn_Add_Characteristic.clicked.connect(lambda state: btn_add_char(interface))
    interface.ui.btn_Add_Service.clicked.connect(lambda state: btn_add_service(interface))
    interface.ui.btn_Add_Descriptor.clicked.connect(lambda state: btn_add_descriptor(interface))

