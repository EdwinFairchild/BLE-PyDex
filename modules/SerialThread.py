import serial
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class Serial_Reader(QThread):
    ble_address = 0
    scan_timeout = 5
    serial_signal = pyqtSignal(str)
    port = "/dev/ttyUSB0"
    connect = False
    def run(self):
        timeStart = time.time()
        with serial.Serial() as ser:
            ser.baudrate = 115200
            ser.port = self.port
            ser.timeout=1
            ser.open()
    
            while ser.is_open != True:
                time.sleep(0.1)
            if ser.is_open == True:
                while self.connect == True:
                    x=ser.readline().decode("utf-8")
                    x=str(x)
                    if x != "":
                        self.serial_signal.emit(x)
                ser.close()
