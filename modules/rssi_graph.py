
from main import *

class UpdateRSSIGraphThread(QThread):
    updateFinished = Signal()  # Signal emitted when the update is finished
    dataUpdated = Signal(str, int, float)  # New signal
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.device_data = None
        self.current_time = None
        self.start_time = time.time()
        self.mutex = QMutex()  # Mutex for thread-safe access to device data
        self.GraphActive = False

    def run(self):
        while self.GraphActive == True:
            with QMutexLocker(self.mutex):
                device_data = self.device_data  # Get the device data
                

            if device_data is not None:
                # Process the device data
                device_name = str(device_data[0])
                device_data = str(device_data[1])

                rssi_match = re.search(r"rssi=(-?\d+)", device_data)
                if rssi_match is None:
                    continue

                rssi_value = int(rssi_match.group(1))

                # Get current timestamp
                current_time = self.current_time
                
                # Emit signal with data to update RSSI graph depending on logging selection
                self.dataUpdated.emit(device_name, rssi_value, current_time)
                
                #reset data
                self.device_data = None

            # Perform any necessary cleanup or sleep
            # NOT NEEDED
            QThread.msleep(100)  

    def updateDeviceData(self, device_data, current_time):
        with QMutexLocker(self.mutex):
            self.device_data = device_data  # Update the device data
            self.current_time = current_time