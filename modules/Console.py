from main_app import *
from modules import Slots
from modules import MiscHelpers
from PyQt5.QtCore import *
import logging
interface = None

class QTextEditLogger(QThread, logging.Handler):
    logMessage = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__()


    def emit(self, record):
        msg = self.format(record)
        self.logMessage.emit(msg)
        
