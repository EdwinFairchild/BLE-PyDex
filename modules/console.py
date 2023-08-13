from main import *
import logging
from PySide6.QtCore import Signal, QObject
import logging

"""
The 'emit' method conflict arises due to multiple inheritance 
from the classes logging.Handler and QObject. 
Both these classes have an 'emit' method. 

In PySide6, multiple inheritance from classes with methods of 
the same name can lead to a method resolution order conflict, 
where it's ambiguous which 'emit' method should be called. 

To resolve this conflict, we separated the functionalities 
into two classes - QLogEmitter and QLogHandler. QLogEmitter 
inherits from QObject and is solely responsible for Qt's 
Signal/Slot mechanism, while QLogHandler handles the logging 
functionality.
"""

class QLogEmitter(QObject):
    logMessage = Signal(str)
    
    def emitSignal(self, msg):
        self.logMessage.emit(msg)

class QLogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.emitter = QLogEmitter()

    def emit(self, record):
        msg = self.format(record)
        self.emitter.emitSignal(msg)
