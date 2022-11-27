import serial
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from modules import Console
class Serial_Reader(QThread):
    ble_address = 0
    scan_timeout = 5
    serial_data = pyqtSignal(str)
    serial_connected = pyqtSignal(bool)
    port = "/dev/ttyUSB0"
    connect = False
    def run(self):
        timeStart = time.time()
        # seconds
        timeout = 5
        try:
            with serial.Serial() as ser:
                ser.baudrate = 115200
                ser.port = self.port
                ser.timeout=1
                ser.open()
        
                while ser.is_open != True:
                    time.sleep(0.1)
                    if (time.time()-timeStart) > timeout:
                        # timed out
                        self.serial_connected.emit(False)
                        break;
                        
                if ser.is_open == True:
                    self.serial_connected.emit(True)
                    Console.log("Serial Connected")
                    while self.connect == True:
                        x=ser.readline().decode("utf-8")
                        x=str(x)
                        if x != "":
                            self.serial_data.emit(x)
                    ser.close()
                    self.serial_connected.emit(False)
                    
                    
        except Exception as err:
            Console.errMsg(err)
            self.serial_connected.emit(False)
           
