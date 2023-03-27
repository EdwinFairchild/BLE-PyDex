import bleak as ble
from bleak import BleakScanner
from bleak import *
import asyncio
import platform
import sys
import os
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from enum import Enum, auto
from typing import Any, Callable, NamedTuple
from functools import cached_property
from modules import Console
from modules import Slots
import zlib #used for crc32
BUFFER_SIZE = 8192
fileLen = 0


'''******************************************************************************************
        Scan for devices
*******************************************************************************************'''


class BLE_DiscoverDevices(QThread):
    ble_address = 0
    scan_timeout = 5
    discovered_devices = pyqtSignal(tuple)

    def run(self):
        asyncio.run(self.BLE_discoverDevices())
    # ------------------------------------------------------------------------

    async def BLE_discoverDevices(self):
        #TODO emit touple if possible
        try:
            devices = await BleakScanner.discover(
            return_adv=True,timeout=self.scan_timeout)
            for item in devices.values():
                self.discovered_devices.emit(item)
            self.discovered_devices.emit((0,0))   
        except Exception as err:
            logging.getLogger().setLevel(logging.WARNING)
            logging.warning(err)
            logging.getLogger().setLevel(logging.INFO)
       


'''******************************************************************************************
        Implements an infinite asyncio loop charged with registering
        notifications, read/write and signal emition of each event to
        GUI application
*******************************************************************************************'''


class BleakLoop(QThread):
    # bleak client stuff
    ble_address = None
    # client = None
    # disconnected state switch
    disconnectSignal = pyqtSignal(bool)
    connect = False
    disconnect_triggered = False
    # used to trigger service discovery
    discoverServices = False
    discovered_services = pyqtSignal(list)
    # used for registering notifys
    notifyCharsAdded = False
    newNotifyCharUUID = None
    # used for unregistering notifys
    notifyRemoveChar = False
    removeNotifyCharHandle = None
    # used to tirgger read char
    readChar = False
    readCharUUID = None
    # used to trigger write char
    writeChar = False
    writeCharUUID = None
    writeCharData = None
    writeCharRaw = None
    # used to trigger firmware update
    otasUpdate = None
    updateFileName = None
    # signals
    #errorMsg = pyqtSignal(str)
    gotNotification = pyqtSignal(list)
    readCharSignal = pyqtSignal(str)
    notifyRegisteredState = pyqtSignal(bool)
    otas_progress_value = pyqtSignal(int)
    erase_complete =False
    override_mtu = 0
    otas_warning = False
    def run(self):
        self.connect = True
        asyncio.run(self.bleakLoop())

    # -------------------------------------------------------------------------
    def handle_disconnect(self, _: BleakClient):
        # cancelling all tasks effectively ends the program
        self.disconnectSignal.emit(True)
        logging.info("Disconnected")
        # in case this happened because of a failed update
        self.otas_progress_value.emit(0)
        self.connect = False

        # for task in asyncio.all_tasks():
        #     task.cancel()
    # -------------------------------------------------------------------------

    def notification_handler(self, sender, data):
        
        # send data let application parse it
        dataList = [sender, data]
        self.gotNotification.emit(dataList)
        if "Handle: 580" in str(sender) and self.erase_complete == False:
            self.erase_complete = True
     
    # -------------------------------------------------------------------------

    async def enableCharNotification(self, client: BleakClient, UUID=None):

        try:
            if UUID == None:
                self.newNotifyCharUUID
            await client.start_notify(UUID, self.notification_handler)
            self.notifyRegisteredState.emit(True)
        except Exception as err:
            logging.getLogger().setLevel(logging.WARNING)
            logging.warning(err)
            logging.getLogger().setLevel(logging.INFO)
            self.notifyRegisteredState.emit(False)
        self.newNotifyCharUUID = None
        self.notifyCharsAdded = False
    # -------------------------------------------------------------------------

    async def removeCharNotification(self, client: BleakClient):
        try:
            await client.stop_notify(self.removeNotifyCharHandle)
            self.notifyRemoveChar = False
        except Exception as err:
            logging.getLogger().setLevel(logging.WARNING)
            logging.warning(err)
            logging.getLogger().setLevel(logging.INFO)
    # -------------------------------------------------------------------------

    async def disconenctBLE(self, client: BleakClient):
        try:
            logging.info("Disconnect triggered...")
            await client.disconnect()
            # self.handle_disconnect(client)
            self.disconnect_triggered = False
            # self.connect = False
            self.disconnectSignal.emit(True)
        except Exception as err:
            logging.getLogger().setLevel(logging.WARNING)
            logging.warning(err)
            logging.getLogger().setLevel(logging.INFO)
    # -------------------------------------------------------------------------

    async def readCharCallback(self, client: BleakClient):
        try:
            chardata = await client.read_gatt_char(self.readCharUUID)
            self.readCharSignal.emit(str(chardata))
        except Exception as err:
            logging.getLogger().setLevel(logging.WARNING)
            logging.warning(err)
            logging.getLogger().setLevel(logging.INFO)
        self.readChar = False

    # -------------------------------------------------------------------------
    def get_crc32(self,fileName):
        global fileLen
        logging.info("opening file " + str(fileName))
        with open(fileName, 'rb') as f:
            crc = 0
            fileLen = 0
            while True:
                data = f.read(BUFFER_SIZE)
                fileLen += len(data)
                if not data:
                    break
                crc = zlib.crc32(data, crc)
        return crc
    # -------------------------------------------------------------------------

    async def otas_update_firmware(self, client: BleakClient):
        #---------------------------------------------------------------------------------------------------#
        #TODO make this use indications instead of delays- this is a proof of concept                       #
        #     Move this method to a different file                                                          #
        #     All the varaibles below are directly from WDX related headers                                 #
        #---------------------------------------------------------------------------------------------------#
        global fileLen
        # UUIDs
        WDX_SERVICE = "0000FEF6-0000-1000-8000-00805F9B34FB"
        WDX_Device_Configuration_Characteristic = "005f0002-2ff2-4ed5-b045-4c7463617865"
        WDX_File_Transfer_Control_Characteristic = "005f0003-2ff2-4ed5-b045-4c7463617865"
        WDX_File_Transfer_Data_Characteristic = "005f0004-2ff2-4ed5-b045-4c7463617865"
        WDX_Authentication_Characteristic   = "005f0005-2ff2-4ed5-b045-4c7463617865"
        ARM_Propietary_Data_Characteristic ="e0262760-08c2-11e1-9073-0e8ac72e0001"

        #WDXS File List Configuration
        WDX_FLIST_HANDLE       = 0   #brief File List handle */
        WDX_FLIST_FORMAT_VER   = 1   #brief File List version */
        WDX_FLIST_HDR_SIZE     = 7   #brief File List header length */
        WDX_FLIST_RECORD_SIZE  = 40  #brief File List record length */

        # Size of WDXC file discovery dataset 
        DATC_WDXC_MAX_FILES  = 4
        # File Transfer Control Characteristic Operations
        WDX_FTC_OP_NONE         = 0        
        WDX_FTC_OP_GET_REQ      = (1).to_bytes(1,byteorder='little',signed=False)      
        WDX_FTC_OP_GET_RSP      = 2      
        WDX_FTC_OP_PUT_REQ      = (3).to_bytes(1,byteorder='little',signed=False)      
        WDX_FTC_OP_PUT_RSP      = 4       
        WDX_FTC_OP_ERASE_REQ    = 5       
        WDX_FTC_OP_ERASE_RSP    = 6       
        WDX_FTC_OP_VERIFY_REQ   = (7).to_bytes(1,byteorder='little',signed=False)           
        WDX_FTC_OP_VERIFY_RSP   = 8     
        WDX_FTC_OP_ABORT        = 9     
        WDX_FTC_OP_EOF          = 10

        WDX_DC_OP_SET           = (2).to_bytes(1,byteorder='little',signed=False)  
        WDX_DC_ID_DISCONNECT_AND_RESET = (37).to_bytes(1,byteorder='little',signed=False)

        WDX_FILE_HANDLE = (0).to_bytes(2,byteorder='little',signed = False)
        WDX_FILE_OFFSET = (0).to_bytes(4,byteorder='little',signed=False)
        WDX_FILE_TYPE = (0).to_bytes(1,byteorder='little',signed=False)
        maxFileRecordLength = ((WDX_FLIST_RECORD_SIZE * DATC_WDXC_MAX_FILES) \
                            + WDX_FLIST_HDR_SIZE).to_bytes(4,byteorder='little',signed=False)

        #determine block size depending on MTU size
        svc = client.services.get_service(WDX_SERVICE)
        wdx_data_char = svc.get_characteristic(WDX_File_Transfer_Control_Characteristic)
        # determine mtu size and subtract 4 to fit the address 
        # and another 4 just because
        blocksize = wdx_data_char.max_write_without_response_size - 8
        if blocksize > 224:
            blocksize = 224
        else :
            blocksize = 120
                        
        logging.info(f"MTU size: {wdx_data_char.max_write_without_response_size}")
        logging.info(f"blocksize: {blocksize}")
        try:
            delayTime = 0.005
            resp = 1
            # --------------------| Enable required notifications |---------------------

            await self.enableCharNotification(client,ARM_Propietary_Data_Characteristic)
            await self.enableCharNotification(client,WDX_Device_Configuration_Characteristic)
            await self.enableCharNotification(client,WDX_File_Transfer_Control_Characteristic)
            await self.enableCharNotification(client,WDX_File_Transfer_Data_Characteristic)
            await self.enableCharNotification(client,WDX_Authentication_Characteristic)
          
            
            # --------------------| File discovery |---------------------
            #this is not additioin this is a byte array
            packet_to_send = (WDX_FTC_OP_GET_REQ)   \
                        + (WDX_FILE_HANDLE)   \
                        + (WDX_FILE_OFFSET)   \
                        + (maxFileRecordLength) \
                        + (WDX_FILE_TYPE)
            
            logging.info("sent discovery: " + str(list(packet_to_send)))
            resp = await client.write_gatt_char(WDX_File_Transfer_Control_Characteristic, bytearray(packet_to_send), response = True)
            while resp != None:
                await asyncio.sleep(delayTime)
            # --------------------| send header |---------------------
            # get file len and crc
            crc32 = self.get_crc32(self.updateFileName)
            file_len_bytes = (fileLen).to_bytes(4,byteorder='little',signed=False)
            # assemble packet and send
            packet_to_send = file_len_bytes + (crc32).to_bytes(4,byteorder='little',signed=False)  
            logging.info("sent header: " + str(list(packet_to_send)))         
            resp = 1
            resp = await client.write_gatt_char(ARM_Propietary_Data_Characteristic, bytearray(packet_to_send), response = True)
            while resp != None:
                await asyncio.sleep(delayTime)  
            # --------------------| send put request |---------------------
            # assemble packet and send
            packet_to_send = WDX_FTC_OP_PUT_REQ \
                            + (1).to_bytes(2,byteorder='little',signed=False) \
                            + WDX_FILE_OFFSET \
                            + file_len_bytes  \
                            + file_len_bytes  \
                            + WDX_FILE_TYPE
            logging.info("sent put req: " + str(list(packet_to_send)))  
            
            self.erase_complete = False
            await client.write_gatt_char(WDX_File_Transfer_Control_Characteristic, bytearray(packet_to_send))
           
            while self.erase_complete == False :
                await asyncio.sleep(delayTime)
             # --------------------| send file   |---------------------
            tempLen = fileLen
            logging.info("Start of sending file")
            address = 0x00000000  
            with open(self.updateFileName, 'rb') as f:
                while True:
                    try:
                        rawBytes = f.read(blocksize)
                        tempLen = tempLen - len(rawBytes)
                        percent =int((1-(tempLen / fileLen))*100)
                        self.otas_progress_value.emit(percent)
                        if not rawBytes:
                            break
                        nextAddress=(address).to_bytes(4,byteorder='little',signed=False)
                        resp = 1
                        resp = await client.write_gatt_char(WDX_File_Transfer_Data_Characteristic, bytearray(nextAddress + rawBytes))
                        address +=len(rawBytes)
                        while resp != None:
                            await asyncio.sleep(delayTime)
                        # Smaller blocksize indicates we are using OTAS with internal flash which is much slower
                        if blocksize < 220:
                            await asyncio.sleep(0.02)
                        else:
                            await asyncio.sleep(delayTime)
                    except Exception as err:
                        logging.info(err)
            self.otasUpdate = False
            logging.info("End of sending file")  
            time.sleep(1)
            # --------------------| send verify file request   |---------------------
            # assemble packet and send
            # file handle is incremented
            WDX_FILE_HANDLE = (1).to_bytes(2,byteorder='little',signed = False)
            packet_to_send = WDX_FTC_OP_VERIFY_REQ +  WDX_FILE_HANDLE
            logging.info("sent verify req: " + str(list(packet_to_send)))   
            resp = await client.write_gatt_char(WDX_File_Transfer_Control_Characteristic, bytearray(packet_to_send))
            while resp != None:
                await asyncio.sleep(delayTime)
            
            # --------------------| send reset request   |---------------------
            # # assemble packet and send
            packet_to_send = WDX_DC_OP_SET + WDX_DC_ID_DISCONNECT_AND_RESET 
            logging.info("sent reset req: " + str(list(packet_to_send))) 
            resp = 1  
            resp = await client.write_gatt_char(WDX_Device_Configuration_Characteristic, bytearray(packet_to_send))
            while resp != None:
                print("waiting")
                await asyncio.sleep(delayTime)
            
            await asyncio.sleep(delayTime)
            
            logging.info("File sent. Firmware update done")
            # ## TODO see what is going on with indications 

            # self.disconnect_triggered = True
            # # TODO make gui clean up method/signal for disconnect event

        except Exception as err:
            logging.getLogger().setLevel(logging.WARNING)
            logging.warning(err)
            logging.getLogger().setLevel(logging.INFO)
            self.otasUpdate = False
        self.writeChar = False
    # -------------------------------------------------------------------------

    async def writeCharCallback(self, client: BleakClient):
        try:
            if self.writeCharRaw != None:
                await client.write_gatt_char(self.writeCharUUID, bytearray(self.writeCharRaw))
                self.writeCharRaw = None
            else:
                await client.write_gatt_char(self.writeCharUUID, bytes(self.writeCharData, 'utf-8'))
        except Exception as err:
            logging.getLogger().setLevel(logging.WARNING)
            logging.warning(err)
            logging.getLogger().setLevel(logging.INFO)
        self.writeChar = False
    # -------------------------------------------------------------------------

    async def exploreSerivce(self, client: BleakClient):
        try:

            for service in client.services:
                # emit top level item
                self.discovered_services.emit(
                    [f"[Service] {service}", 0])
                for char in service.characteristics:
                    # emit children of top level
                    if "read" in char.properties:
                        try:
                            value = bytes(await client.read_gatt_char(char.uuid))
                            self.discovered_services.emit(
                                [f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}", 1])
                        except Exception as e:
                            self.discovered_services.emit(
                                [f"\t[Characteristic] {char} ({','.join(char.properties)}), Error: {e}", 1])
                    else:
                        value = None
                        self.discovered_services.emit(
                            [f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}", 1])
                    for descriptor in char.descriptors:
                        # emit children of children
                        try:
                            value = bytes(
                                await client.read_gatt_descriptor(descriptor.handle)
                            )
                            self.discovered_services.emit(
                                [f"\t\t[Descriptor] {descriptor}) | Value: {value}", 2])
                        except Exception as err:
                            logging.getLogger().setLevel(logging.WARNING)
                            logging.warning(err)
                            logging.getLogger().setLevel(logging.INFO)
            self.discoverServices = False
            logging.info(f"Connected: {client.is_connected}")
            # emit connected signal
            self.disconnectSignal.emit(False)
        except Exception as e:
            logging.info(
                "Opps ,That device is not explorable, at least not by you.")
    # -------------------------------------------------------------------------

    async def bleakLoop(self):
        async with BleakClient(self.ble_address, disconnected_callback=self.handle_disconnect) as client:
            if self.otas_warning == True:
                logging.getLogger().setLevel(logging.WARNING)
                logging.warning("The binary being used for OTA must be an application only, no bootloader")
                logging.getLogger().setLevel(logging.INFO)
                #determine block size depending on MTU size
                WDX_SERVICE = "0000FEF6-0000-1000-8000-00805F9B34FB"
                WDX_File_Transfer_Control_Characteristic = "005f0003-2ff2-4ed5-b045-4c7463617865"
                svc = client.services.get_service(WDX_SERVICE)
                wdx_data_char = svc.get_characteristic(WDX_File_Transfer_Control_Characteristic)
                # determine mtu size and subtract 4 to fit the address 
                # and another 4 just because
                blocksize = wdx_data_char.max_write_without_response_size - 8
                if blocksize < 224:
                    logging.getLogger().setLevel(logging.WARNING)
                    logging.warning("There is an issue with BLE-Pydex and BLE_otas when using internal flash only. Connection parameter update must be enabled. See Github issues")
                    logging.getLogger().setLevel(logging.INFO)
            while self.connect == True:
                await asyncio.sleep(0.005)
                # check the flag to disconnect
                if self.disconnect_triggered == True:
                    await self.disconenctBLE(client)
                # --------------- if any notify chars have been added register them
                if self.notifyCharsAdded == True and self.newNotifyCharUUID != None:
                    await self.enableCharNotification(client)
                # -------------- if any prviously enabled chars need to removed from notify
                if self.notifyRemoveChar == True and self.removeNotifyCharHandle != None:
                    await self.removeCharNotification(client)
                # -------------- if a single char needs to be read
                if self.readChar == True and self.readCharUUID != None:
                    await self.readCharCallback(client)
                # -------------- if a write char is requested
                if self.writeChar == True and self.writeCharUUID != None:
                    await self.writeCharCallback(client)
                # -------------- if discoverServices has been triggered
                if self.discoverServices == True:
                    await self.exploreSerivce(client)
                # -------------- start otas firmware update
                if self.otasUpdate == True:
                    await self.otas_update_firmware(client)
