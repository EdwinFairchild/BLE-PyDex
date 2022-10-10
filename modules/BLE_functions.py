import bleak as ble
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
    discovered_devices = pyqtSignal(str)

    def run(self):
        asyncio.run(self.BLE_discoverDevices())
    # ------------------------------------------------------------------------

    async def BLE_discoverDevices(self):
        devices = await ble.discover(timeout=self.scan_timeout)
        for d in devices:
            self.discovered_devices.emit(str(d))
        # disconnect here? or keep active until user presses explore?


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
    errorMsg = pyqtSignal(str)
    gotNotification = pyqtSignal(list)
    readCharSignal = pyqtSignal(str)
    notifyRegisteredState = pyqtSignal(bool)
    
    def run(self):
        self.connect = True
        asyncio.run(self.bleakLoop())

    # -------------------------------------------------------------------------
    def handle_disconnect(self, _: BleakClient):
        # cancelling all tasks effectively ends the program
        Console.log("Disconnected")
        # for task in asyncio.all_tasks():
        #     task.cancel()
    # -------------------------------------------------------------------------

    def notification_handler(self, sender, data):
        # send data let application parse it
        pass
        # dataList = [sender, data]
        # self.gotNotification.emit(dataList)
    # -------------------------------------------------------------------------

    async def enableCharNotification(self, client: BleakClient):

        try:
            await client.start_notify(self.newNotifyCharUUID, self.notification_handler)
            self.notifyRegisteredState.emit(True)
        except Exception as err:
            Console.errMsg(err)
            self.notifyRegisteredState.emit(False)
        self.newNotifyCharUUID = None
        self.notifyCharsAdded = False
    # -------------------------------------------------------------------------

    async def removeCharNotification(self, client: BleakClient):
        try:
            await client.stop_notify(self.removeNotifyCharHandle)
            self.notifyRemoveChar = False
        except Exception as err:
            Console.errMsg(err)
    # -------------------------------------------------------------------------

    async def disconenctBLE(self, client: BleakClient):
        try:
            Console.log("Disconenct triggered...")
            await client.disconnect()
            # self.handle_disconnect(client)
            self.disconnect_triggered = False
            # self.connect = False
            self.disconnectSignal.emit(True)
        except Exception as err:
            Console.errMsg(err)
    # -------------------------------------------------------------------------

    async def readCharCallback(self, client: BleakClient):
        try:
            chardata = await client.read_gatt_char(self.readCharUUID)
            self.readCharSignal.emit(str(chardata))
        except Exception as err:
            Console.errMsg(err)
        self.readChar = False

    # -------------------------------------------------------------------------
    def get_crc32(self,fileName):
        global fileLen
        print(fileName)
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
        #TODO make this use indications instead of delays- this is proof of concept
        try:
            delayTime = 0.010
            # file discovery
            rawBytes = [1, 0, 0, 0, 0, 0, 0, 167, 0, 0, 0, 0]
            self.writeCharUUID = "005f0003-2ff2-4ed5-b045-4c7463617865"
            await client.write_gatt_char(self.writeCharUUID, bytearray(rawBytes))
            await asyncio.sleep(delayTime)
            # --------------------| send header |---------------------
            # get file len and crc
            #rawBytes = [232, 19, 3, 0, 32, 104, 131, 208]
            crc32 = self.get_crc32(self.updateFileName)
            crc32Hex = str(hex(crc32)[2:])
            fileLenHex = str(hex(fileLen)[2:]).strip()
            print(crc32Hex)
            print(fileLenHex)
            crcBytes = bytearray.fromhex(crc32Hex)
            crcBytes.reverse()
            if len(fileLenHex) % 2 != 0:
                fileLenHex = "000" + fileLenHex

            fileLenBytes = bytearray.fromhex(fileLenHex)
            fileLenBytes.reverse()
            # I tihnk this works, double check the order from index 0 to max match the hard coded vvalue above
            rawBytes = fileLenBytes + crcBytes
            self.writeCharUUID = "e0262760-08c2-11e1-9073-0e8ac72e0001"
            await client.write_gatt_char(self.writeCharUUID, bytearray(rawBytes))
            await asyncio.sleep(delayTime)
            # --------------------| send put request |---------------------
            putRequestFileHandle = bytearray([3,1,0,0,0,0,0])
            terminator = bytearray(0)
            rawBytes = putRequestFileHandle +  fileLenBytes + fileLenBytes + terminator
            self.writeCharUUID = "005f0003-2ff2-4ed5-b045-4c7463617865"
            await client.write_gatt_char(self.writeCharUUID, bytearray(rawBytes))
            await asyncio.sleep(delayTime)
             # --------------------| send file   |---------------------
            self.writeCharUUID = "005f0004-2ff2-4ed5-b045-4c7463617865"
            with open(self.updateFileName, 'rb') as f:
                while True:
                    rawBytes = f.read(224)
                    if not rawBytes:
                        break
                    await client.write_gatt_char(self.writeCharUUID, bytearray(rawBytes))
                    await asyncio.sleep(delayTime)
            self.otasUpdate = False
            time.sleep(20)
            # --------------------| send verify file request   |---------------------
            rawBytes = [7,1,0]
            self.writeCharUUID = "005f0003-2ff2-4ed5-b045-4c7463617865"
            await client.write_gatt_char(self.writeCharUUID, bytearray(rawBytes))
            await asyncio.sleep(delayTime)
            
            time.sleep(1)
            # --------------------| send reset request   |---------------------
            rawBytes = [2,37]
            self.writeCharUUID = "005f0002-2ff2-4ed5-b045-4c7463617865"
            await client.write_gatt_char(self.writeCharUUID, bytearray(rawBytes))
            await asyncio.sleep(delayTime)
            

            print("File sent. Firmware update done")

        except Exception as err:
            Console.errMsg(err)
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
            Console.errMsg(err)
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
                            Console.errMsg(err)
            self.discoverServices = False
            Console.log(f"Connected: {client.is_connected}")
        except Exception as e:
            Console.log(
                "Opps ,That device is not explorable, at least not by you.")
    # -------------------------------------------------------------------------

    async def bleakLoop(self):
        async with BleakClient(self.ble_address, disconnected_callback=self.handle_disconnect) as client:
            while self.connect == True:
                await asyncio.sleep(0.01)
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
