from main import *
from . import max32xxx_ota
from . import ota 
import bleak
import asyncio
from asyncio import Queue
from bleak import BleakScanner
from bleak import *
import ctypes
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
    logger = logging.getLogger("PDexLogger")
    ble_address = "1C:90:FF:EA:C4:8A"
    is_connected = False
    device_disconnected = Signal()
    discovered_services = Signal(list)
    connection_established = Signal()
    connection_esablished_signal_sent = False

    # signals to kickstart queue based event handling
    #these are emitted from main.py but the handlers live here
    device_char_write = Signal(str, str, bool, bool) # UUID, value
    device_char_notify = Signal(str, bool) # UUID, enable/disable
    device_char_read = Signal(str) # UUID
    #these are emitted from here and the handlers live in main.py
    device_notification_recevied = Signal(str, str) # sender, value
    device_char_read_response = Signal(str, str) # UUID, value
   
    #-----------| ota related signals and varaibles |---------------------------
    ota_file_len = 0
    ota_file_name = None
    ota_in_progress = False
    ota_erase_complete = False
    ota_file_write_complete = False
    device_ota_update_start = Signal(object,str, int, ctypes.c_uint32) # fileName, fileLen, crc32
    device_ota_update_send_file = Signal(object,str, int) # fileName, fileLen
    device_ota_update_verify_file = Signal(object)
    device_ota_update_reset_device = Signal(object)
    device_ota_update_reset = Signal(object) # connected to a slot in main.py
    ota_device_erase_complete = Signal(bool)
    otas_progress_value = Signal(int)
    

    def __init__(self, *args, **kwargs):
        super(BLE_ConnectDevice, self).__init__(*args, **kwargs)
        self.async_queue = Queue()
        # Connect signals to slots
        self.device_char_write.connect(self.BLE_task_enqueue_write)
        self.device_char_notify.connect(self.BLE_task_enqueue_notify)
        self.device_char_read.connect(self.BLE_task_enqueue_read)

        #-----------| ota related Signal connections |---------------------------
        self.device_ota_update_start.connect(max32xxx_ota.BLE_task_enqueue_max32xxx_ota_start)
        self.device_ota_update_send_file.connect(max32xxx_ota.BLE_task_enqueue_max32xxx_ota_send_file)
        self.ota_device_erase_complete.connect(lambda: ota.ota_device_erase_complete_handler(self))
        self.device_ota_update_verify_file.connect(max32xxx_ota.BLE_task_enqueue_max32xxx_ota_verify_file)
        self.device_ota_update_reset_device.connect(max32xxx_ota.BLE_task_enqueue_max32xxx_ota_reset_device)

    
    def run(self):

        asyncio.run(self.BLE_connectionLoop())
    # ----------------------------| BLE connection |--------------------------------------------
    async def BLE_connectionLoop(self):
        try:
            self.logger.info("Connecting to device with address: " + self.ble_address)
            # start connection and pass disconnection handler
            async with BleakClient(self.ble_address, disconnected_callback=self.handle_disconnect) as client:
                self.is_connected = True
                self.logger.info("Connected to device with address: " + self.ble_address)
                
                await self.discover_device_services(client)
                 
                while self.is_connected == True:
                    # send the conenctions established singal only once
                    if self.connection_esablished_signal_sent == False:
                        # triggers stacked widget to show Gatt Explorere screen
                        self.connection_established.emit()
                        # just a flag used to send the signal only once
                        self.connection_esablished_signal_sent = True
                    # check if there is anything in the queue
                    if not self.async_queue.empty():
                        task, args, kwargs = await self.async_queue.get()  # This will wait until something is available
                        if task == "write_char":
                            await self.writeWithoutRespCallback(client, *args, **kwargs)
                        if task == "notify_char":
                            await self.notifyCallback(client, *args, **kwargs)
                        if task == "read_char":
                            await self.readCallback(client, *args, **kwargs)

                        #-----------| ota related task handlers |---------------------------    
                        await max32xxx_ota.max32xxx_ota_task_list(self,task ,client, *args, **kwargs)

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
                self.discovered_services.emit([f"{service}", PARENT,None])
                for char in service.characteristics:
                    # EMIT characteristics with read property
                    if "read" in char.properties:
                        
                        try:
                            
                            value = bytes(await client.read_gatt_char(char.uuid))
                            self.discovered_services.emit(
                                [f"{char}, Value: {value}", CHILD,char.properties])
                        except Exception as e:
                            self.discovered_services.emit(
                                [f"{char}, Error: {e}", CHILD,char.properties])
                    else:
                        # EMIT characteristics without  read property
                        value = None
                        
                        self.discovered_services.emit(
                            [f"{char}, Value: {value}", CHILD,char.properties])
                    for descriptor in char.descriptors:
                        # emit children of children
                        try:
                            value = bytes(
                                await client.read_gatt_descriptor(descriptor.handle)
                            )
                            self.discovered_services.emit(
                                [f"{descriptor}) | Value: {value}", GRANDCHILD, None])
                        except Exception as err:
                            self.logger.warning(f"Opps!:{err}")
                            

        except Exception as err:
            self.logger.warning(err)

    async def disconnect_device(self, client: BleakClient):
        try:
            await client.disconnect()
            
        except Exception as err:
            self.logger.warning(err)
          
    #------------------------------| BLE event handlers |-------------------------------------------
    
    async def writeWithoutRespCallback(self, client: BleakClient,  uuid , data , response , rawbytes = False):
        if response == True:
            try:
                if rawbytes == True:
                    value = await client.write_gatt_char(uuid, bytearray(data), response=True)
                    if value == None:
                        self.logger.info(f"Successfully wrote data to characteristic with UUID: {uuid}. Write type: With Response. Response received.")
                else:
                    value = await client.write_gatt_char(uuid, bytes(data, 'utf-8'), response=True)
                    if value == None:
                        self.logger.info(f"Successfully wrote data to characteristic with UUID: {uuid}. Write type: With Response. Response received.")

            except Exception as err:
                self.logger.setLevel(logging.WARNING)
                self.logger.warning(err)
                self.logger.setLevel(logging.WARNING)
                self.logger.info("Write failed")
        else:    
            try:
                if rawbytes == True:
                    await client.write_gatt_char(uuid, bytearray(data))
                    self.logger.info(f"Successfully wrote data to characteristic with UUID: {uuid}. Write type: Without Response.")

                else:
                    await client.write_gatt_char(uuid, bytes(data, 'utf-8'))
                    self.logger.info(f"Successfully wrote data to characteristic with UUID: {uuid}. Write type: Without Response.")

            except Exception as err:
                self.logger.setLevel(logging.WARNING)
                self.logger.warning(err)
                self.logger.setLevel(logging.WARNING)
                self.logger.info("Write failed")
   
    async def notifyCallback(self, client: BleakClient, uuid, enable):
        if enable == True:
            try:
                await client.start_notify(uuid, self.handle_notification)
                self.logger.info(f"Successfully enabled notifications for characteristic with UUID: {uuid}")
            except Exception as err:
                self.logger.setLevel(logging.WARNING)
                self.logger.warning(err)
                self.logger.setLevel(logging.WARNING)
                self.logger.info("Notification failed")
        else:
            try:
                await client.stop_notify(uuid)
                self.logger.info(f"Successfully disabled notifications for characteristic with UUID: {uuid}")
            except Exception as err:
                self.logger.setLevel(logging.WARNING)
                self.logger.warning(err)
                self.logger.setLevel(logging.WARNING)
                self.logger.info("Notification failed")
    
    async def readCallback(self, client: BleakClient, uuid):
        try:
            value = bytes(await client.read_gatt_char(uuid))
            self.logger.info(f"Successfully read data from characteristic with UUID: {uuid}. Value: {value}")
            #emit signal with value
            self.device_char_read_response.emit(str(uuid), str(value))
        except Exception as err:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning(err)
            self.logger.setLevel(logging.INFO)
            self.logger.info("Read failed")
            pass
    
    def handle_notification(self, sender, data):
        self.logger.info(f"Notification received")
        self.logger.info(f"Sender: {sender}")
        self.logger.info(f"Data: {data}")
        try:
            self.device_notification_recevied.emit(str(sender), str(data))
            self.logger.info(f"Notification received")
            self.logger.info(f"Sender: {sender}")
            self.logger.info(f"Data Len: {len(data)}")
            #self.logger.info(f"Data: {data}") # this will print in the chars window
           
            #----------------- MAX32xxx OTA UPDATE -----------------
            max32xxx_ota.max32xxx_ota_notification_handler(self,sender,data)
             

        except Exception as err:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning(err)
            self.logger.setLevel(logging.INFO)
            self.logger.info("Notification failed")
    
    def handle_disconnect(self, _: BleakClient):
        # This gets called internally by Bleak when the device disconnects
        self.is_connected = False
        self.logger.info("Disconnected")
        # reset the text of the connect button
        self.device_disconnected.emit()

        # max32xxx ota related
        self.otas_progress_value.emit(0)
    
    #------------------------------| BLE task enqueuers |-------------------------------------------

    def BLE_task_enqueue_write(self, uuid, data, response: bool=False,rawbytes: bool=False):
       
        task = ("write_char", [uuid,data, response, rawbytes], {})
        try:
            self.async_queue.put_nowait(task)
        except err:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning("Queue is full: {err}")
            self.logger.setLevel(logging.INFO)
            self.logger.info("Write failed")
            
    def BLE_task_enqueue_notify(self, uuid, enable: bool):
        task = ("notify_char", [uuid,enable], {})
        try:
            self.async_queue.put_nowait(task)
        except err:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning("Queue is full: {err}")
            self.logger.setLevel(logging.INFO)
            self.logger.info("Notification failed")
            
    def BLE_task_enqueue_read(self, uuid):
        task = ("read_char", [uuid], {})
        try:
            self.async_queue.put_nowait(task)
        except err:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning("Queue is full: {err}")
            self.logger.setLevel(logging.INFO)
            self.logger.info("Read failed")
            


 