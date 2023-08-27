from main import *
import bleak
import asyncio
from bleak import BleakScanner
from bleak import *

class BLE_DiscoverDevices(QThread):
    ble_address = 0
    scan_timeout = 0
    is_scanning = False
    discovered_devices = Signal(tuple)
    advertisementFilter = None
    advertisementLoggingLevel = None
    logger = logging.getLogger("PDexLogger")
    scanning_stoped = Signal()


    def run(self):
        asyncio.run(self.BLE_discoverDevices())
    # ------------------------------------------------------------------------

    async def BLE_discoverDevices(self):
        try:
            # if scan timeout is 0, scan forever
            if self.scan_timeout == 0:
                
                self.logger.info("Scanning forever")
                while self.is_scanning == True:
                    devices = await BleakScanner.discover(
                        return_adv=True,timeout=0.1)
                    for item, adv in devices.values():
                        self.discovered_devices.emit((item,adv))
                self.logger.info("Scan stopped")
            else:  
                # in in half second intervals until timeout is met
                self.logger.info("Scanning for " + str(self.scan_timeout) + " seconds")
                self.is_scanning = True
                while self.scan_timeout >= 0.5 and self.is_scanning == True:

                    scanTime = 0.1  
                    devices = await BleakScanner.discover(
                    return_adv=True,timeout=scanTime)
                    for item in devices.values():
                        
                        self.discovered_devices.emit(item)
                    self.scan_timeout -= scanTime
                    
                self.logger.info("Scan stopped")
                self.is_scanning = False
                self.scanning_stoped.emit()

        except Exception as err:
            self.is_scanning = False
            self.logger.setLevel(logging.WARNING)
            self.logger.warning(err)
            self.logger.setLevel(logging.INFO)
            self.logger.info("Scan stopped")
            self.scanning_stoped.emit()
       
#make a class for connecting to a device using bleak, the device connection must be done in a separate thread in order to not block the UI
class BLE_ConnectDevice(QThread):
    ble_address = "1C:90:FF:EA:C4:8A"
    is_connected = False
    device_disconnected = Signal()
    logger = logging.getLogger("PDexLogger")
    discovered_services = Signal(list)
    connection_established = Signal()
    connection_esablished_signal_sent = False
    
    def run(self):
        asyncio.run(self.BLE_connectDevice())
    # ------------------------------------------------------------------------

    async def BLE_connectDevice(self):
        try:
            self.logger.info("Connecting to device with address: " + self.ble_address)
            # start connection and pass disconnection handler
            async with BleakClient(self.ble_address, disconnected_callback=self.handle_disconnect) as client:
                self.is_connected = True
                self.logger.info("Connected to device with address: " + self.ble_address)
                 # TODO : stop the RSSI graph thread, need a signal for that
                
                    # TODO : handle notifications add/remove
                    # TODO : handle characteristics read/write
                    # TODO : handle services explore
                await self.discover_device_services(client)

                 
                while self.is_connected == True:
                    # send the conenctions established singal only once
                    if self.connection_esablished_signal_sent == False:
                        # triggers stacked widget to show Gatt Explorere screen
                        self.connection_established.emit()
                        # just a flag used to send the signal only once
                        self.connection_esablished_signal_sent = True

                    # async sleep, give time for other threads to run
                    await asyncio.sleep(0.05)
                    #pass
                try:
                    await self.disconnect_device(client)
                    self.connection_esablished_signal_sent = False
                except Exception as err:
                    self.logger.warning(err)
        except Exception as err:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning(err)
            self.logger.setLevel(logging.INFO)
            self.device_disconnected.emit()
            self.is_connected = False
            
            self.logger.info(f"Error connecting to device: {err}")
       
    async def discover_device_services(self, client: BleakClient):
        try:
            for service in client.services:
                # find services and emit signal with list of services,char,desc , second value is the level of the tree
                # EMIT SERVICE
                PARENT = 0
                CHILD = 1
                GRANDCHILD = 2
                self.discovered_services.emit([f": {service}", PARENT,None])
                for char in service.characteristics:
                    # EMIT characteristics with read property
                    if "read" in char.properties:
                        
                        try:
                            
                            value = bytes(await client.read_gatt_char(char.uuid))
                            self.discovered_services.emit(
                                [f"\t: {char}, Value: {value}", CHILD,char.properties])
                        except Exception as e:
                            self.discovered_services.emit(
                                [f"\t: {char}, Error: {e}", CHILD,char.properties])
                    else:
                        # EMIT characteristics without  read property
                        value = None
                        
                        self.discovered_services.emit(
                            [f"\t: {char}, Value: {value}", CHILD,char.properties])
                    for descriptor in char.descriptors:
                        # emit children of children
                        try:
                            value = bytes(
                                await client.read_gatt_descriptor(descriptor.handle)
                            )
                            self.discovered_services.emit(
                                [f"\t\t: {descriptor}) | Value: {value}", GRANDCHILD, None])
                        except Exception as err:
                            self.logger.warning(f"Opps!:{err}")
                            

        except Exception as err:
            self.logger.warning(err)


    async def disconnect_device(self, client: BleakClient):
        try:
            await client.disconnect()
            
        except Exception as err:
            self.logger.warning(err)
          

    def handle_disconnect(self, _: BleakClient):
        # This gets called internally by Bleak when the device disconnects
        self.is_connected = False
        self.logger.info("Disconnected")
        # reset the text of the connect button
        self.device_disconnected.emit()
        