import bleak  as ble
from bleak import *
import asyncio
import platform
import sys
import os
import time
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from enum import Enum, auto
from typing import Any, Callable, NamedTuple

ADDRESS = (
    "00:18:80:04:3F:85"
    if platform.system() != "Darwin"
    else "B9EA5233-37EF-4DD6-87A8-2A875E821C46"
)
CHARACTERISTIC_UUID = "85fc567e-31d9-4185-87c6-339924d1c5be"
class BLE_DiscoverDevices(QThread):###################################################
    ble_address=0
    scan_timeout=5
    discovered_devices = pyqtSignal(str)
    def run(self):
        asyncio.run(self.BLE_discoverDevices())
    #------------------------------------------------------------------------
    async def BLE_discoverDevices(self):
        devices = await ble.discover(timeout = self.scan_timeout)
        for d in devices:
            self.discovered_devices.emit(str(d))
    #------------------------------------------------------------------------
#------------------------------------------------------------------------
    # this method does not use the threadworker class
    # async def bleScan(self,address):
    #     device = await BleakScanner.find_device_by_address(address)
    #     print(str(device))
    #     print(device)
    #     self.ui.discoveredList.addItem(str(device))
    #------------------------------------------------------------------------
    # def btnScanCalBack(self):
    #     asyncio.run(self.bleScan(ADDRESS))
    #------------------------------------------------------------------------


class BLE_DiscoverServices(QThread):
    ble_address= None
    scan_timeout=60
    discovered_services = pyqtSignal(list)
    client = None
    def run(self):
        asyncio.run(self.BLE_discoverServices(self.client))
    #------------------------------------------------------------------------
    async def BLE_discoverServices(self, client : BleakClient):
        try :
            async with  client:
                print(f"Connected: {client.is_connected}")
                for service in client.services:
                    #emit top level item

                    self.discovered_services.emit([f"[Service] {service}", 0])


                    for char in service.characteristics:
                        #emit children of top level
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                                self.discovered_services.emit([f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}",1])
                                # print(
                                #     f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                                # )
                            except Exception as e:
                                self.discovered_services.emit([f"\t[Characteristic] {char} ({','.join(char.properties)}), Error: {e}",1])
                                # print(
                                #     f"\t[Characteristic] {char} ({','.join(char.properties)}), Error: {e}"
                                # )

                        else:
                            value = None
                            self.discovered_services.emit([f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}",1])
                            # print(
                            #     f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                            # )

                        for descriptor in char.descriptors:
                            #emit children of children
                            try:
                                value = bytes(
                                    await client.read_gatt_descriptor(descriptor.handle)
                                    
                                )
                                self.discovered_services.emit([f"\t\t[Descriptor] {descriptor}) | Value: {value}",2])
                                # print(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                            except Exception as e:
                                self.discovered_services.emit([f"\t\t[Descriptor] {descriptor}) | Error: {e}",2])
                                #print(f"\t\t[Descriptor] {descriptor}) | Error: {e}")
                await client.disconnect()
                
                print(f"Cleint conenction state : {client.is_connected}")
        except Exception as e:
            print("Opps ,That device is not explorable, at least not by you.")
        
 
class BLE_EnableNotify(QThread):
    ble_address= None
    char_uuid = None
    client = None
    gotNotification = pyqtSignal(str)
    def run(self):
        asyncio.run(self.enableNotify(self.client))
        
    async def enableNotify(self, client : BleakClient):
        async with  client:
            #here set a lable to notifying enabled or something
            # Ask server to start sending
            await client.write_gatt_char("85fc5681-31d9-4185-87c6-339924d1c5be", bytes('1', 'utf-8'))
            await client.start_notify(self.char_uuid, self.notification_handler)
            while True:
                await asyncio.sleep(1.0)
                chardata = await client.read_gatt_char("85fc567e-31d9-4185-87c6-339924d1c5be")
                print(str(chardata))
            #await client.stop_notify(self.char_uuid)
    def notification_handler(self,sender, data):
        """Simple notification handler which prints the data received."""
        print("{0}: {1}".format(sender, data))
        self.gotNotification.emit(str(data))

class BLE_ReadChar(QThread):
    ble_address= None
    scan_timeout=5
    charToRead = None
    charReadData = pyqtSignal(str)
    client = None
    def run(self):
        asyncio.run(self.BLE_ReadChar(self.client))
    #------------------------------------------------------------------------
    async def BLE_ReadChar(self, client : BleakClient):
        # try:
        async with client:
            chardata = await client.read_gatt_char(self.charToRead)
            
            self.charReadData.emit(str(chardata))
        # except Exception as e:
        #     print("That device is not explorable, at least not by you.")


class BLE_Connect(QThread):
    ble_address= None
    client = None
    def run(self):
        asyncio.run(self.connect(self.ble_address, self.client))

    async def connect(self,address, client:BleakClient):
        print("Attmepting to conenct")
        async with  client:
            #client.disconnect()
            await client.connect()
            print(str(client.is_connected))
        return self.client

def print_speed(speed: float, current: float):
    print(f"\tMCU->PC speed: {speed:.2f} B/s, "
         f"{(speed / 1024):.4f} KB/s, "
         f"{(speed / 1024 / 1024):.4f} MB/s, "
         f"Current: {(current / 1024 / 1024):.4f} MB/s"
         )

class BleakLoop(QThread):
    ble_address= None
    notifyChar = {}
    client = None
    gotNotification = pyqtSignal(str)
    gotNotification2 = pyqtSignal(str)
    errorMsg = pyqtSignal(str)
    notifyCharsAdded = False
    def run(self):
        asyncio.run(self.bleakLoop())
    #-------------------------------------------------------------------------
    def handle_disconnect(_: BleakClient):
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()
    #-------------------------------------------------------------------------
    def notification_handler(self,sender, data):
        print("{0}: {1}".format(sender, data))

        if sender == 5384:
            print(" got 5384")
            self.gotNotification.emit(str(data))
        else:
            self.gotNotification2.emit(str(data))

    async def enableNotify(self, key, client : BleakClient):
        await client.start_notify(key, self.notification_handler)
    #-------------------------------------------------------------------------
    async def bleakLoop(self):
        #-------------------------------------------------------------------------
        async with BleakClient(self.ble_address, disconnected_callback= self.handle_disconnect) as client:
            
            #here set a lable to notifying enabled or something
            # Ask server to start sending
            await client.write_gatt_char("85fc5681-31d9-4185-87c6-339924d1c5be", bytes('1', 'utf-8'))
            #await client.start_notify(self.char_uuid, self.notification_handler)
            #await client.start_notify(self.char_uuid2, self.notification_handler2)
            while True:
                await asyncio.sleep(1.0)
                if self.notifyCharsAdded == False:
                    print("About to add chars")
                    for key, value in self.notifyChar.items():
                        await self.enableNotify(key,client)
                    self.notifyCharsAdded = True

                #cycle through  dictionary of characters to read.

                #if that specific chararacteristic is not "stream" enabled
                #then just read once and remove from dictionary

                #other wise read it 

                #check if there are new characteristics that need to be registered with 'notify'
                chardata = await client.read_gatt_char("85fc567e-31d9-4185-87c6-339924d1c5be")
                print(str(chardata))
''' TODO : start mechanism to register new Notify charateristics : use signals and slots 
make a signal that will pass the UUID and the callback function. 
callback funtion should be generic for all of them, and it should read the "sender"
argument passed to know what char sent the BLE_EnableNotify '''