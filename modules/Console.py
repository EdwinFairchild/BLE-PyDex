from main_app import *
from modules import Slots
from modules import MiscHelpers
from PyQt5.QtCore import *
import logging
interface = None

def console_init(main_interface):
    pass
    # global interface
    # interface = main_interface

def log(data):
    pass
    #interface.ui.console.verticalScrollBar().setSliderPosition(10)

def log_status():
    pass
    # global interface
    # log("Connected state: " + str(interface.connected_state))

def errMsg(data):
    pass
    #log(str(data))



class QTextEditLogger(QThread, logging.Handler):
    logMessage = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__()


    def emit(self, record):
        msg = self.format(record)
        self.logMessage.emit(msg)
        
