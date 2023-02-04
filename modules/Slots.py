from modules import Console
from modules import MiscHelpers
from main_app import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import asyncio
def discovered_services(interface ,data):
    ''' Data comes in looking like this:
        ['[Service] 00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile', 0]
        ['\t[Characteristic] 00002a05-0000-1000-8000-00805f9b34fb (Handle: 17): Service Changed (indicate), Value: None', 1]'''
    item = data[0]
    item = item.replace("\t", "")
    item = item.replace("[", "")
    item = item.replace("]", " : ")

    # list only has 2 elements , that last one being index 1 
    # stating what level this item is at.. see : BLE_function.py -> exploreSerivce
    level = data[1]
    ''' And leaves  looking like this:
        Service :  00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile 
        Characteristic :  00002a05-0000-1000-8000-00805f9b34fb (Handle: 17): Service Changed (indicate), Value: None'''
    if level == 0:
        interface.toplevel = QTreeWidgetItem([str(item)])
        interface.ui.servicesTreeWidget.addTopLevelItem(interface.toplevel)
    elif level == 1 and interface.toplevel != None:
        interface.child = QTreeWidgetItem([str(item)])
        interface.toplevel.addChild(interface.child)
    elif level == 2 and interface.child != None:
        subchild = QTreeWidgetItem([str(item)])
        interface.child.addChild(subchild)
    #possible more levels ? idk

def got_char_notify(interface, data):
    #since char handle and data received are 2 seprate lists in the gui
    #the data parameter here will have a "sender" and the data recevied
    #so we look for the same sender in the handles list and get the row nubmer
    #then in the corresponding row for the data recevied we add the new data
    #I over complicated this
    string = str(data[0]).split()[2][:-2]
    item = interface.ui.list_EnabledNotify.findItems(string, QtCore.Qt.MatchExactly)
    row = interface.ui.list_EnabledNotify.row(item[0])
    item = interface.ui.list_EnabledNotifyValue.item(row)
    data = str(data[1]).removeprefix("bytearray(b\'\\")
    data = str(data).removesuffix("\')")
    item.setText(data)
    logging.info("Received : " + data)
def notify_registered_state(interface, state):
    if state == True:
        # add the selected UUID/Handle to the notify list
        if interface.ui.btnLabelHandle.text() in interface.notifyEnabledCharsDict:
            logging.info("Characteristic notificaiton is already enabled")
        else:
            interface.notifyEnabledCharsDict[interface.ui.btnLabelHandle.text(
            )] = "N/A"
            interface.ui.list_EnabledNotify.addItem(
                interface.ui.btnLabelHandle.text())
            interface.ui.list_EnabledNotifyValue.addItem("N/A")
            # interface.notifyEnabledCharsDict[interface.ui.btnLabelHandle.text()] += ["5555"]
            # print(str(interface.notifyEnabledCharsDict[interface.ui.btnLabelHandle.text()][1]))
            # call function to add this item to list_enabledNotifybtnNoti
    else:
        logging.info("Could not add")

def disconnect(interface,state):
    if state ==True:
        interface.bleLoop.exit()
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
        interface.ui.list_discoveredDevices.clear()
        interface.ui.list_EnabledNotifyValue.clear()
        interface.notifyEnabledCharsDict = {}
        if interface.advertised_name == "OTAS":
            interface.ui.frm_otas.setVisible(False)
            interface.bleLoop.otas_progress_value.emit(0)
            
    else:

        fore = [255, 255, 255]
        back = [170, 66, 66]
        MiscHelpers.set_alternate_button_mode_color(
        interface, interface.ui.btnConnect, fore, back)
        # gui stuff
        MiscHelpers.set_connected_icon_color(interface, 'blue')
        interface.ui.btnConnect.setText("Disconnect")
        interface.connected_state = True
        if interface.advertised_name == "OTAS":
            interface.ui.frm_otas.setVisible(True)
            interface.bleLoop.otas_progress_value.connect(
                    lambda value: otas_progress_update(interface, value))

def read_char(interface, data):
    interface.ui.btnLabelValue.setText(data)

def scan(interface, device):
    if device == (0,0):
        interface.BLE_DiscoverDevices.quit()
    else:
        #interface.ui.list_discoveredDevices.addItem(f" " + device[0][0:17] + " | " + device[0][18:] + " ")
        interface.ui.list_discoveredDevices.addItem(f" " + str(device[0]))
            
    # device[1] has rssi 
def serial_data(interface, data):
    interface.ui.txtSerial.append(data.strip())

def serial_connected(interface,state):
    if state == True:
        fore = [255, 255, 255]
        back = [170, 66, 66]
        MiscHelpers.set_alternate_button_mode_color(
                        interface, interface.ui.btnSerialConnect, fore, back)
        interface.ui.btnSerialConnect.setText("Disconnect")
        interface.serial_connected_state = True
    else:
        interface.serialLoop.quit()
        fore = [0, 0, 0]
        back = [170, 200, 255]
        MiscHelpers.set_alternate_button_mode_color(
                        interface, interface.ui.btnSerialConnect, fore, back)
        interface.ui.btnSerialConnect.setText("Connect")
        interface.serial_connected_state = False
        
def otas_progress_update(interface,value):    
    interface.ui.otasProgress.setValue(value)


   