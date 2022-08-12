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