from main_app import *

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
    item = interface.ui.list_EnabledNotify.findItems(
        str(data[0]), QtCore.Qt.MatchExactly)
    print("item index")
    print(item[0])
    row = interface.ui.list_EnabledNotify.row(item[0])
    item = interface.ui.list_EnabledNotifyValue.item(row)
    data = str(data[1]).removeprefix("bytearray(b\'\\")
    data = str(data).removesuffix("\')")
    item.setText(data)

def notify_registered_state(interface, state):
    if state == True:
        # add the selected UUID/Handle to the notify list
        if interface.ui.btnLabelHandle.text() in interface.notifyEnabledCharsDict:
            print("Characteristic notificaiton is already enabled")
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
        print("could not add")

def disconnect(interface):
    interface.bleLoop.exit()

def read_char(interface, data):
    interface.ui.btnLabelValue.setText(data)

def scan(interface, device):
    interface.ui.list_discoveredDevices.addItem(f" " + device[0:17] + " | " + device[18:] + " ")

def errMsg(interface, err):
    # TODO : add logging area to display error/status messags
    print(err)