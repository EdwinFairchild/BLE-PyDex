from BLE_GUI import Ui_MainWindow
import ButtonCallbacks as btnCB
from PyQt5 import Qt as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QPoint, QEasingCurve,pyqtSignal,QSequentialAnimationGroup
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bleak import *
import BLE_functions as ble_ctl
import asyncio
import platform
import sys
import os
import time
import atexit
from asyncqt import QEventLoop

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainInterface(QMainWindow):
    # TODO : this is a mess of variables , must learn better python
    selected_address = None
    connected_address = None
    menuPinned = False
    ui = None
    # used to keep track of tree widget tree items
    toplevel = None
    child = None
    # side animation configurable limits
    sideBarWidthMax = 210
    sideBarWidthMin = 73
    animationDone = True

    client = None
    # peristent instance of bleakLoop needs to be kept so the task is not
    # canceled 
    bleLoop = None

    # list to manage chars that have notify enabled
    notifyEnabledCharsDict = {}
   
    def __init__(self):
        super().__init__()
        # setup gui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # connect  signals->slots
        
        # Menu button callbacks
        self.ui.btnMenu.clicked.connect(self.btnMenuCallBack)
        self.ui.btnMenuExplore.clicked.connect(self.btnMenuExploreCallBack)
        self.ui.btnMenuGattMaker.clicked.connect(self.btnMenuGattMakerCallBack)
        self.ui.btnMenuClient.clicked.connect(self.btnMenuClientCallBack)
        
        # interface button callbacks
        self.ui.btnScan.clicked.connect(self.btnBleScan)
        self.ui.btnReadChar.clicked.connect(self.btnReadCharcallback)
        self.ui.list_discoveredDevices.itemPressed.connect(self.discoveredList2ItemPressed)
        self.ui.list_EnabledNotify.itemPressed.connect(self.enabledNotifyListItemPressed)
        self.ui.list_EnabledNotifyValue.itemPressed.connect(self.enabledNotifyListValueItemPressed)
        self.ui.btnExplore.clicked.connect(self.btnExploreCallback)
        self.ui.btnConnect.clicked.connect(self.btnConnectCallback)
        self.ui.servicesTreeWidget.itemPressed.connect(self.treeWidgetItemPressed)
        self.ui.btnLabelType.clicked.connect(self.btnLabelTypeCopy)
        self.ui.btnLabelUUID.clicked.connect(self.btnLabelUUIDCopy)
        self.ui.btnLabelPermissions.clicked.connect(self.btnLabelPermissionsCopy)
        self.ui.btnNotify.clicked.connect(self.btnNotifyCallBack)
        self.ui.btnNotifyRemove.clicked.connect(self.btnNotifyRemoveCallback)

        self.iconDictionary = {self.ui.btnMenu:['resources/icons/Menu.svg','resources/icons/MenuBlue.svg'] ,
                               self.ui.btnMenuGattMaker:['resources/icons/Ble.svg','resources/icons/BleBlue.svg'] , 
                               self.ui.btnMenuExplore : ['resources/icons/Discover.svg','resources/icons/DiscoverBlue.svg'] , 
                               self.ui.btnMenuClient : ['resources/icons/Client.svg','resources/icons/ClientBlue.svg']}
        #Set Button Icons
        self.ui.btnMenu.setIcon(QIcon('resources/icons/Menu.svg'))
        test = QSize()
        test.setHeight(20)
        test.setWidth(20)
        self.ui.btnMenu.setIconSize(test)

        self.ui.btnauthor.setIcon(QIcon('resources/icons/Person.svg'))
        test.setHeight(30)
        test.setWidth(30)
        self.ui.btnauthor.setIconSize(test)

        self.ui.btnRepo.setIcon(QIcon('resources/icons/Github.svg'))
        test.setHeight(15)
        test.setWidth(15)
        self.ui.btnRepo.setIconSize(test)

        self.ui.btnInstagram.setIcon(QIcon('resources/icons/Instagram.svg'))
        test.setHeight(25)
        test.setWidth(25)
        self.ui.btnInstagram.setIconSize(test)

        self.ui.btnYoutube.setIcon(QIcon('resources/icons/Youtube.svg'))
        test.setHeight(25)
        test.setWidth(25)
        self.ui.btnYoutube.setIconSize(test)

        self.ui.btnConnectedState.setIcon(QIcon('resources/icons/Ble.svg'))
        test.setHeight(50)
        test.setWidth(50)
        self.ui.btnConnectedState.setIconSize(test)

        #misc init stuff
        self.ui.servicesTreeWidget.setColumnCount(1)    
        self.ui.sideBar.installEventFilter(self)    

        # button list used for changing style sheet
        self.buttonList=[self.ui.btnMenu ,self.ui.btnMenuGattMaker,self.ui.btnMenuClient,self.ui.btnMenuExplore]
    def setConnectedIconColor(self, color):
        if color == "blue":
            self.ui.btnConnectedState.setIcon(QIcon('resources/icons/BleBlue.svg'))
            test = QSize()
            test.setHeight(50)
            test.setWidth(50)
            self.ui.btnConnectedState.setIconSize(test)
        else:
            self.ui.btnConnectedState.setIcon(QIcon('resources/icons/Ble.svg'))
            test = QSize()
            test.setHeight(50)
            test.setWidth(50)
            self.ui.btnConnectedState.setIconSize(test)
            
    #------------------------------------------------------------------------
    #global event filter handler
    def eventFilter(self, source, event):
        
        if event.type() == QtCore.QEvent.Enter and source == self.ui.sideBar:
            self.menuAnimate(self.ui.sideBar , True)
        if event.type() == QtCore.QEvent.Leave and source == self.ui.sideBar:
            self.menuAnimate(self.ui.sideBar , False)
        return super().eventFilter(source, event)
    #------------------------------------------------------------------------
    def btnNotifyCallBack(self):
        #Add the currently selected char to notify enabled chars list
        if "NOTIFY" in self.ui.btnLabelPermissions.text():
            self.bleLoop.gotNotification.connect(self.gotCharNotif)
            self.bleLoop.notifyCharsAdded = True;
            self.bleLoop.newNotifyCharUUID = self.ui.btnLabelUUID.text()
            self.bleLoop.notifyRegisteredState.connect(self.notifyRegisteredStateCallback)
        else:
            print("That characteristic does not have Notify enabled")
    def btnNotifyRemoveCallback(self):
        if self.ui.list_EnabledNotify.currentRow() == -1 :
            pass
        else:
            # remove notification from Bleak
            self.bleLoop.notifyRemoveChar = True
            item = self.ui.list_EnabledNotify.currentItem()
            # UUIDs are strings and Handles are ints in Bleak
            self.bleLoop.removeNotifyCharHandle =int(item.text())
            # remove from list
            self.ui.list_EnabledNotify.takeItem(self.ui.list_EnabledNotify.currentRow())
            self.ui.list_EnabledNotifyValue.takeItem(self.ui.list_EnabledNotify.currentRow())
    #------------------------------------------------------------------------
    def notifyRegisteredStateCallback(self, state):
        if state == True:
            #add the selected UUID/Handle to the notify list
            if self.ui.btnLabelHandle.text() in self.notifyEnabledCharsDict:
                pass
            else:
                self.notifyEnabledCharsDict[self.ui.btnLabelHandle.text()] = "N/A"
                self.ui.list_EnabledNotify.addItem(self.ui.btnLabelHandle.text())
                self.ui.list_EnabledNotifyValue.addItem("N/A")
               # self.notifyEnabledCharsDict[self.ui.btnLabelHandle.text()] += ["5555"]
               # print(str(self.notifyEnabledCharsDict[self.ui.btnLabelHandle.text()][1]))
               # call function to add this item to list_enabledNotify

    #------------------------------------------------------------------------
    def btnReadCharcallback(self):
           #read char from gatt
        self.gettreadChar = ble_ctl.BLE_ReadChar()
      #  self.gettreadChar.client = self.client
        self.gettreadChar.ble_address = self.connected_address
        self.gettreadChar.charToRead = self.ui.btnLabelUUID.text()
        self.gettreadChar.charReadData.connect(self.gattReadCallBAck)
        self.gettreadChar.start()
    #------------------------------------------------------------------------
    def gattReadCallBAck(self,data):
        self.ui.lblCharVal.setText(data)
    #------------------------------------------------------------------------
    def gotCharNotif(self,data):
        item = self.ui.list_EnabledNotify.findItems(str(data[0]), QtCore.Qt.MatchExactly)
        row =self.ui.list_EnabledNotify.row(item[0])
        item = self.ui.list_EnabledNotifyValue.item(row)
        data = str(data[1]).removeprefix("bytearray(b\'\\")
        data = str(data).removesuffix("\')")
        item.setText(data)
    #------------------------| Clip board copying related functions |----------------------------
    def btnLabelTypeCopy(self):
        self.copyToClipBoard(self.ui.btnLabelType.text())
    #------------------------------------------------------------------------
    def btnLabelUUIDCopy(self):
        self.copyToClipBoard(self.ui.btnLabelUUID.text())
    #------------------------------------------------------------------------
    def btnLabelPermissionsCopy(self):
        self.copyToClipBoard(self.ui.btnLabelPermissions.text())
    #------------------------------------------------------------------------
    def copyToClipBoard(self,str):
        cp = QApplication.clipboard()
        cp.clear()
        cp.setText(str)
    #------------------------------------------------------------------------
    def treeWidgetItemPressed(self):
        #get text of seleced item
        treeWidgetItemtext = self.ui.servicesTreeWidget.currentItem()
        # the 0 in text(0) means which column index. There is only 1 column used
        dataList = treeWidgetItemtext.text(0).split(":")
        dataListLen = len(dataList)
        # get UUID
        self.ui.btnLabelType.setText(dataList[0])
        lblUUID = dataList[1].split("(")
        lblUUID[0].strip()
        #get Handle
        lblHandle = dataList[2].removesuffix(")")
        lblHandle = lblHandle.strip()
        self.ui.btnLabelHandle.setText(lblHandle)
        #get permissions
        lblPermissions = "N/A"
        self.ui.btnLabelUUID.setText(lblUUID[0].strip())
        if "read" in treeWidgetItemtext.text(0):
            lblPermissions = "READ"
        if "write" in treeWidgetItemtext.text(0):
            lblPermissions+=" : WRITE"
        if "notify" in treeWidgetItemtext.text(0):
            lblPermissions+=" : NOTIFY"
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
        self.ui.btnLabelPermissions.setText(lblPermissions)
    #------------------------------------------------------------------------
    def discoveredList2ItemPressed(self):
        value = self.ui.list_discoveredDevices.currentItem() 
        tmp  = value.text()
        self.selected_address = tmp[1:18]
    def enabledNotifyListItemPressed(self):
        self.ui.list_EnabledNotifyValue.setCurrentRow(self.ui.list_EnabledNotify.currentRow())
    def enabledNotifyListValueItemPressed(self):
        self.ui.list_EnabledNotify.setCurrentRow(self.ui.list_EnabledNotifyValue.currentRow())
    #------------------------------------------------------------------------
    def btnBleScan(self):
        self.ui.list_discoveredDevices.clear()
        self.BLE_DiscoverDevices = ble_ctl.BLE_DiscoverDevices()
        self.BLE_DiscoverDevices.scan_timeout = self.ui.timeoutSlider_2.value()
        self.BLE_DiscoverDevices.discovered_devices.connect(self.bleScannerSlot)
        self.BLE_DiscoverDevices.start()
        #self.worker.finished.connect(self.blescannerFinished)
    #------------------------------------------------------------------------
    def errMsg(self,err):
        print(err)
    
    #------------------------------------------------------------------------
    def bleScannerSlot(self,device):
        self.ui.list_discoveredDevices.addItem(f" "+ device[0:17] + " | " + device[18:] + " " )
    #------------------------------------------------------------------------ 
    def blescannerFinished(self):
            pass
    #------------------------------------------------------------------------
    def btnExploreCallback(self):
        if(self.selected_address != None):
            self.client = BleakClient(self.selected_address)
            self.ui.servicesTreeWidget.clear()
            self.BLE_DiscoverServices = ble_ctl.BLE_DiscoverServices()
            self.BLE_DiscoverServices.client = self.client
            self.BLE_DiscoverServices.ble_address = self.selected_address
            self.BLE_DiscoverServices.discovered_services.connect(self.bleDiscoverslot)
            self.BLE_DiscoverServices.start()
            
            #print("Read services from : " + self.selected_address)
            #todos can time out
        else:
           print("Opps ,You need to select a device from the scan list!")

    #------------------------------------------------------------------------
    def btnConnectCallback(self):
        # Establish and maintain Bleak connection
        if self.selected_address != None :
            try: 
                self.bleLoop = ble_ctl.BleakLoop()
                self.bleLoop.ble_address = self.selected_address
                self.bleLoop.discoverServices = True
                self.bleLoop.discovered_services_signal.connect(self.bleDiscoverslot)
                self.bleLoop.errorMsg.connect(self.errMsg)
                self.connected_address = self.selected_address
                self.bleLoop.start()
                self.setConnectedIconColor('blue')
                self.ui.btnConnect.setText("Disconnect")
            except Exception as err:
                print(err)
                self.setConnectedIconColor('white')
                self.ui.btnConnect.setText("Connect")
        else:
            print("You have to select a device from explore list")


    #------------------------------------------------------------------------
    def bleDiscoverslot(self,data ):
        #self.ui.listServices.addItem(service)
        item = data[0]
        item = item.replace("\t","")
        item = item.replace("[","")
        item = item.replace("]"," : ")
        level = data[1]
        if level == 0:
            self.toplevel = QTreeWidgetItem([str(item)])
            self.ui.servicesTreeWidget.addTopLevelItem(self.toplevel)
        elif level == 1 and self.toplevel != None:
            self.child = QTreeWidgetItem([str(item)])
            self.toplevel.addChild(self.child)
        elif level == 2 and self.child != None:
            subchild = QTreeWidgetItem([str(item)])
            self.child.addChild(subchild)

    #------------------------------------------------------------------------
    def btnMenuAboutCallBack(self):	
        QMessageBox.information(self,"About", "BLUE PY v0.0.1\nEdwin Amaya \n2022")
    #------------------------------------------------------------------------
    def styleSheetUpdate(self, grayVal ):

        return f"QPushButton{{background-color: rgb({grayVal}, {grayVal}, {grayVal}); padding-left: 40px; text-align: left;border-radius:12px;color: rgb(255, 255, 255);border:none;}}QPushButton:hover{{color: rgb(255, 255, 255);background-color: rgb(170, 77, 77);}}QPushButton:pressed{{color: rgb(255, 255, 255);background-color: rgb(170, 27, 27);}}"
    #------------------------------------------------------------------------
    def btnStyleSheetSet(self, currentButton):
        #itterate buttons list

        for b in self.buttonList:
            if b == currentButton:
                currentButton.setStyleSheet(self.styleSheetUpdate(28))
            else:
                b.setStyleSheet(self.styleSheetUpdate(57))
            #if currnet itteration == currentButton skip
        #buttons.setStyleSheet
    #------------------------------------------------------------------------
    def setButtonIcons(self, currentButton):
        for button in self.buttonList:
            if button == currentButton:
                icon = self.iconDictionary[currentButton][1]
                currentButton.setIcon(QIcon(icon))
                test = QSize()
                test.setHeight(20)
                test.setWidth(20)
                currentButton.setIconSize(test)

            elif button == self.ui.btnMenu:
                pass

            else:
                icon = self.iconDictionary[button][0]
                button.setIcon(QIcon(icon))
                test = QSize()
                test.setHeight(20)
                test.setWidth(20)
                button.setIconSize(test)
    #------------------------------------------------------------------------
    def menuAnimate(self, obj, onmouse):
       
        if self.animationDone == True and self.menuPinned == False:
            self.anim = QPropertyAnimation(self.ui.sideBar,b'maximumWidth')
            self.anim.setStartValue(self.ui.sideBar.width())
            if self.ui.sideBar.width() < 100 :
                self.anim.setEndValue(self.sideBarWidthMax)
            else:
                self.anim.setEndValue(self.sideBarWidthMin)
            self.anim.setEasingCurve(QEasingCurve.InOutCubic)     
            self.anim.finished.connect(self.animDone)
            self.animationDone = False     
            self.anim.start()  
    #------------------------------------------------------------------------
    def animDone(self):
        self.animationDone = True
    #------------------------------------------------------------------------
    def btnMenuCallBack(self):
        if self.menuPinned == True: #set to white
            icon = self.iconDictionary[self.ui.btnMenu][0]
            self.ui.btnMenu.setIcon(QIcon(icon))
            test = QSize()
            test.setHeight(20)
            test.setWidth(20)
            self.ui.btnMenu.setIconSize(test)
           
        else:
            icon = self.iconDictionary[self.ui.btnMenu][1]
            self.ui.btnMenu.setIcon(QIcon(icon))
            test = QSize()
            test.setHeight(20)
            test.setWidth(20)
            self.ui.btnMenu.setIconSize(test)
            
        self.menuPinned = not self.menuPinned
    #------------------------------------------------------------------------
    def btnMenuGattMakerCallBack(self):
        self.ui.stackedWidget.slideInIdx(0)
        self.setButtonIcons(self.ui.btnMenuGattMaker)
    #------------------------------------------------------------------------
    def btnMenuClientCallBack(self):
        self.ui.stackedWidget.slideInIdx(1)
        self.setButtonIcons(self.ui.btnMenuClient)
    #------------------------------------------------------------------------
    def btnMenuExploreCallBack(self):
        self.ui.stackedWidget.slideInIdx(2)
        self.setButtonIcons(self.ui.btnMenuExplore)
    #------------------------------------------------------------------------     
    def showWidget(self, obj):
        #check if other widgets are open and close them
        self.anim = QPropertyAnimation(obj,b'geometry')
        if self.anim.state() == self.anim.State.Stopped:
            rect = obj.geometry()
            self.anim.setStartValue(rect)

            #if obj.width() == 0:
            rect.setWidth(1000)
            self.anim.setEndValue(rect)
            self.anim.setDuration(700)
            self.anim.setEasingCurve(QEasingCurve.InOutQuart)
            self.anim.start()
    #------------------------------------------------------------------------
    def hideWidget(self, obj):
        #check if other widgets are open and close them
        self.anim = QPropertyAnimation(obj,b'geometry')
        
        self.anim.finished.connect(self.animDone)
        if self.anim.state() == self.anim.State.Stopped:
            rect = obj.geometry()
            self.anim.setStartValue(rect)

            if obj.width() >= 900:
                rect.setWidth(0)
                self.anim.setEndValue(rect)
                self.anim.setDuration(700)
                self.anim.setEasingCurve(QEasingCurve.InOutQuart)
                self.anim.start()
    #------------------------------------------------------------------------
def exitFunc():
    try:
        #close any on running tasks
        for task in asyncio.all_tasks():
            task.cancel()
    except Exception as e:
        pass
        
if __name__ == '__main__':
    #todo: compile resurces into python files, not sure if its even necessary at this point
    #pyrcc5 image.qrc -o image_rc.py
    #compile gui
    os.system("pyuic5 -x BLE_GUI.ui -o BLE_GUI.py")
    atexit.register(exitFunc)
    app = qtw.QApplication(sys.argv)
    # loop = QEventLoop(app)
    # asyncio.set_event_loop(loop)
    interface = MainInterface()
    interface.show()
    #`loop.run_forever()
    interface.menuAnimate(interface.ui.sideBar , False)
    interface.setButtonIcons(interface.ui.btnMenuExplore)
    app.exec_()
