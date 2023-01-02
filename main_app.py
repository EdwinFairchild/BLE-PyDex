from click import style
from BLE_GUI import Ui_MainWindow
from modules import ButtonCallbacks
from modules import ListCallbacks
from modules import MiscHelpers
from modules import BLE_functions as ble_ctl
from modules import SerialThread as ser_ctl
from modules import Console 
from PyQt5 import Qt as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QPoint ,QEasingCurve, pyqtSignal, QSequentialAnimationGroup 
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QPushButton, QToolTip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bleak import *
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
    # TODO : cleanup unused
    # if sys.platform == 'win32':
    #     print("Windows")
    # else:
    #     print("Linux!")

    selected_address = None
    advertised_name = None
    connected_address = None
    menuPinned = False
    connected_state = False
    serial_connected_state = False
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
    serialLoop = None
    UUID_dict = BLE_UUIDs.get_uuid_dict("UUIDs.json")
    user_uuid_dict = BLE_UUIDs.get_uuid_dict("user_UUIDs.json", True)
    # list to manage chars that have notify enabled
    notifyEnabledCharsDict = {}

    vbox = QGridLayout()
   
    def __init__(self):
        QMainWindow.__init__(self)
        # setup gui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.frm_otas.setVisible(False)
        global testVar
        self.testVar = self
        Console.console_init(self)
        ListCallbacks.register_list_callbacks(self)
        ButtonCallbacks.register_button_callbacks(self)
        MiscHelpers.init_icons(self)
        Console.log("BLE-PyDex initialized")
        Console.log_status()
        
        
        
            

    # ------------------------------------------------------------------------
    # def eventFilter(self, source, event):

    #     if event.type() == QtCore.QEvent.Enter and source == self.ui.sideBar:
    #         self.menuAnimate(self.ui.sideBar, True)
    #     if event.type() == QtCore.QEvent.Leave and source == self.ui.sideBar:
    #         self.menuAnimate(self.ui.sideBar, False)
    #     return super().eventFilter(source, event)
    # ------------------------------------------------------------------------

########################################################################################
def exitFunc():
    try:
        # close any on running tasks
        for task in asyncio.all_tasks():
            task.cancel()
    except Exception as e:
        pass
    # ------------------------------------------------------------------------
if __name__ == '__main__':
    # todo: compile resurces into python files, not sure if its even necessary at this point
    # pyrcc5 image.qrc -o image_rc.py
    # compile gui
    os.system("pyuic5 -x BLE_GUI.ui -o BLE_GUI.py")
    
    atexit.register(exitFunc)
    app = qtw.QApplication(sys.argv)
    app.setStyle('Fusion')

    # loop = QEventLoop(app)
    # asyncio.set_event_loop(loop)

    interface = MainInterface()
    interface.show()
    MiscHelpers.set_button_icons(interface, interface.ui.btnMenuExplore)
    app.exec_()
