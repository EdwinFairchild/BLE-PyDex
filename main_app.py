from click import style
from BLE_GUI import Ui_MainWindow
from modules import ButtonCallbacks
from PyQt5 import Qt as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QPoint, QEasingCurve, pyqtSignal, QSequentialAnimationGroup
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
import webbrowser
import BLE_UUIDs
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
os.environ["QT_FONT_DPI"] = "96"


class MainInterface(QMainWindow):
    # TODO : this is a mess of variables , must learn better python
    selected_address = None
    connected_address = None
    menuPinned = False
    connected_state = False
    # used to keep track of tree widget tree items
    toplevel = None
    child = None
    # side animation configurable limits
    sideBarWidthMax = 210
    sideBarWidthMin = 73
    animationDone = True
    widgets = None
    client = None
    # peristent instance of bleakLoop needs to be kept so the task is not
    # canceled
    bleLoop = None
    UUID_dict = BLE_UUIDs.get_uuid_dict("UUIDs.json")
    user_uuid_dict = BLE_UUIDs.get_uuid_dict("user_UUIDs.json", True)
    # list to manage chars that have notify enabled
    notifyEnabledCharsDict = {}

    def __init__(self):
        QMainWindow.__init__(self)
        # setup gui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #-------| register button callbakcs : Module name == File name -> ButtonCallbacks |--------
        self.ui.list_discoveredDevices.itemPressed.connect(self.discoveredList2ItemPressed)
        self.ui.list_EnabledNotify.itemPressed.connect(self.enabledNotifyListItemPressed)
        self.ui.list_EnabledNotifyValue.itemPressed.connect(self.enabledNotifyListValueItemPressed)

        # Menu button callbacks
        self.ui.btnMenu.clicked.connect(lambda state : ButtonCallbacks.btn_menu(self))
        self.ui.btnMenuExplore.clicked.connect(lambda state : ButtonCallbacks.btn_explore(self))
        self.ui.btnMenuClient.clicked.connect(lambda state : ButtonCallbacks.btn_client(self))
        self.ui.btnMenuGattMaker.clicked.connect(lambda state : ButtonCallbacks.btn_gatt_maker(self))
        # Explore Page Button Callbacks
        self.ui.btnReadChar.clicked.connect(lambda state : ButtonCallbacks.btn_read_char(self))
        self.ui.btnWriteChar.clicked.connect(lambda  state : ButtonCallbacks.btn_write_char(interface))
        self.ui.btnConnect.clicked.connect(lambda state : ButtonCallbacks.btn_connect(self))
        self.ui.servicesTreeWidget.itemPressed.connect(lambda state : ButtonCallbacks.btn_tree_widget_item_pressed(self))
        self.ui.btnLabelType.clicked.connect(lambda state : ButtonCallbacks.btn_type_copy(self))
        self.ui.btnLabelUUID.clicked.connect(lambda state : ButtonCallbacks.btn_uuid_copy(self))
        self.ui.btnLabelPermissions.clicked.connect(lambda state : ButtonCallbacks.btn_permission_copy(self))
        self.ui.btnNotify.clicked.connect(lambda state : ButtonCallbacks.btn_notify(self))
        self.ui.btnNotifyRemove.clicked.connect(lambda state : ButtonCallbacks.btn_notify_remove(self))
        self.ui.btnScan.clicked.connect(lambda state : ButtonCallbacks.btn_scan(self))
        self.ui.btnRepo.clicked.connect(lambda state: ButtonCallbacks.btn_github(self))
        self.ui.btnYoutube.clicked.connect(lambda state: ButtonCallbacks.btn_youtube(self))
        #self.ui.btnExplore.clicked.connect(lambda state : ButtonCallbacks.btn_explore(self))
        
        self.iconDictionary = {self.ui.btnMenu: ['resources/icons/Menu.svg', 'resources/icons/MenuBlue.svg'],
                               self.ui.btnMenuGattMaker: ['resources/icons/Ble.svg', 'resources/icons/BleBlue.svg'],
                               self.ui.btnMenuExplore: ['resources/icons/Discover.svg', 'resources/icons/DiscoverBlue.svg'],
                               self.ui.btnMenuClient: ['resources/icons/Client.svg', 'resources/icons/ClientBlue.svg']}
        # Set Button Icons
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

        # misc init stuff
        self.ui.servicesTreeWidget.setColumnCount(1)
        self.ui.sideBar.installEventFilter(self)

        # button list used for changing style sheet
        self.buttonList = [self.ui.btnMenu, self.ui.btnMenuGattMaker,
                           self.ui.btnMenuClient, self.ui.btnMenuExplore]
        
        # not sure if I want to keep this
        self.ui.btnExplore.hide()
    # ------------------------------------------------------------------------
    def setConnectedIconColor(self, color):
        if color == "blue":
            self.ui.btnConnectedState.setIcon(
                QIcon('resources/icons/BleBlue.svg'))
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
    # ------------------------------------------------------------------------
    def eventFilter(self, source, event):

        if event.type() == QtCore.QEvent.Enter and source == self.ui.sideBar:
            self.menuAnimate(self.ui.sideBar, True)
        if event.type() == QtCore.QEvent.Leave and source == self.ui.sideBar:
            self.menuAnimate(self.ui.sideBar, False)
        return super().eventFilter(source, event)
    # ------------------------------------------------------------------------
    def notifyRegisteredStateCallback(self, state):
        if state == True:
            # add the selected UUID/Handle to the notify list
            if self.ui.btnLabelHandle.text() in self.notifyEnabledCharsDict:
                print("Characteristic notificaiton is already enabled")
            else:
                self.notifyEnabledCharsDict[self.ui.btnLabelHandle.text(
                )] = "N/A"
                self.ui.list_EnabledNotify.addItem(
                    self.ui.btnLabelHandle.text())
                self.ui.list_EnabledNotifyValue.addItem("N/A")
               # self.notifyEnabledCharsDict[self.ui.btnLabelHandle.text()] += ["5555"]
               # print(str(self.notifyEnabledCharsDict[self.ui.btnLabelHandle.text()][1]))
               # call function to add this item to list_enabledNotifybtnNoti
        else:
            print("could not add")
    # ------------------------------------------------------------------------

    def readCharSignalCallback(self, data):
        self.ui.btnLabelValue.setText(data)
    # ------------------------------------------------------------------------
    def gotCharNotif(self, data):
        item = self.ui.list_EnabledNotify.findItems(
            str(data[0]), QtCore.Qt.MatchExactly)
        print("item index")
        print(item[0])
        row = self.ui.list_EnabledNotify.row(item[0])
        item = self.ui.list_EnabledNotifyValue.item(row)
        data = str(data[1]).removeprefix("bytearray(b\'\\")
        data = str(data).removesuffix("\')")
        item.setText(data)
    # ------------------------------------------------------------------------
    def copyToClipBoard(self, str):
        cp = QApplication.clipboard()
        cp.clear()
        cp.setText(str)
    # ------------------------------------------------------------------------
    def uuid_parse(self, uuid):
        file = open("UUIDs.txt", 'r')
        data = file.readlines()
        uuid_dict = {}
        # this should probably only happen once when the class is instantiated
        for line in data:
            line = line.split()
            if line[1] not in uuid_dict:
                uuid_dict[line[2]] = line[1]
    # ------------------------------------------------------------------------
    def discoveredList2ItemPressed(self):
        value = self.ui.list_discoveredDevices.currentItem()
        tmp = value.text()
        self.selected_address = tmp[1:18]
    # ------------------------------------------------------------------------
    def enabledNotifyListItemPressed(self):
        self.ui.list_EnabledNotifyValue.setCurrentRow(
            self.ui.list_EnabledNotify.currentRow())
    # ------------------------------------------------------------------------
    def enabledNotifyListValueItemPressed(self):
        self.ui.list_EnabledNotify.setCurrentRow(
            self.ui.list_EnabledNotifyValue.currentRow())
    # ------------------------------------------------------------------------
    def errMsg(self, err):
        # TODO : add logging area to display error/status messags
        print(err)
    # ------------------------------------------------------------------------
    def bleScannerSlot(self, device):
        self.ui.list_discoveredDevices.addItem(
            f" " + device[0:17] + " | " + device[18:] + " ")
    # ------------------------------------------------------------------------
    def blescannerFinished(self):
        pass
    # ------------------------------------------------------------------------
    def disconnectSlot(self):
        self.bleLoop.exit()
    # ------------------------------------------------------------------------
    def btnMenuAboutCallBack(self):
        QMessageBox.information(
            self, "About", "BLUE PY v0.0.1\nEdwin Amaya \n2022")
    # ------------------------------------------------------------------------
    def styleSheetUpdate(self, grayVal):

        return f"QPushButton{{background-color: rgb({grayVal}, {grayVal}, {grayVal}); padding-left: 40px; text-align: left;border-radius:12px;color: rgb(255, 255, 255);border:none;}}QPushButton:hover{{color: rgb(255, 255, 255);background-color: rgb(170, 77, 77);}}QPushButton:pressed{{color: rgb(255, 255, 255);background-color: rgb(170, 27, 27);}}"
    # ------------------------------------------------------------------------
    def btnStyleSheetSet(self, currentButton):
        # itterate buttons list

        for b in self.buttonList:
            if b == currentButton:
                currentButton.setStyleSheet(self.styleSheetUpdate(28))
            else:
                b.setStyleSheet(self.styleSheetUpdate(57))
            # if currnet itteration == currentButton skip
        # buttons.setStyleSheet
    # ------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------
    def setAlternateButtonModeColor(self, button, fore, back):
        stylesheet = f"QPushButton{{ text-align: center; background-color: rgb({back[0]}, {back[1]}, {back[2]});  ;border-radius:5px;color: rgb({fore[0]}, {fore[1]}, {fore[2]});border:none;}}QPushButton:hover{{color: rgb(255, 255, 255);background-color: rgb(170, 77, 77);}}QPushButton:pressed{{color: rgb(255, 255, 255);background-color: rgb(170, 27, 27);}}"
        button.setStyleSheet(stylesheet)
    # ------------------------------------------------------------------------
    def menuAnimate(self, obj, onmouse):
        # right now minimizing the menu offers no advantage
        # there is no point in having it.
        pass
        # if self.animationDone == True and self.menuPinned == False:
        #     self.anim = QPropertyAnimation(self.ui.sideBar, b'maximumWidth')
        #     self.anim.setStartValue(self.ui.sideBar.width())
        #     if self.ui.sideBar.width() < 100:
        #         self.anim.setEndValue(self.sideBarWidthMax)
        #     else:
        #         self.anim.setEndValue(self.sideBarWidthMin)
        #     self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        #     self.anim.finished.connect(self.animDone)
        #     self.animationDone = False
        #     self.anim.start()
    # ------------------------------------------------------------------------

    def animDone(self):
        self.animationDone = True
    # ------------------------------------------------------------------------
    def showWidget(self, obj):
        # check if other widgets are open and close them
        self.anim = QPropertyAnimation(obj, b'geometry')
        if self.anim.state() == self.anim.State.Stopped:
            rect = obj.geometry()
            self.anim.setStartValue(rect)

            # if obj.width() == 0:
            rect.setWidth(1000)
            self.anim.setEndValue(rect)
            self.anim.setDuration(700)
            self.anim.setEasingCurve(QEasingCurve.InOutQuart)
            self.anim.start()
    # ------------------------------------------------------------------------

    def hideWidget(self, obj):
        # check if other widgets are open and close them
        self.anim = QPropertyAnimation(obj, b'geometry')

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
    # ------------------------------------------------------------------------


def exitFunc():
    try:
        # close any on running tasks
        for task in asyncio.all_tasks():
            task.cancel()
    except Exception as e:
        pass


if __name__ == '__main__':
    # todo: compile resurces into python files, not sure if its even necessary at this point
    # pyrcc5 image.qrc -o image_rc.py
    # compile gui
    os.system("pyuic5 -x BLE_GUI.ui -o BLE_GUI.py")
    atexit.register(exitFunc)
    app = qtw.QApplication(sys.argv)
    # loop = QEventLoop(app)
    # asyncio.set_event_loop(loop)

    interface = MainInterface()
    interface.show()
    # `loop.run_forever()
    interface.menuAnimate(interface.ui.sideBar, False)
    interface.setButtonIcons(interface.ui.btnMenuExplore)
    app.exec_()
