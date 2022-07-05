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
    ble_address= "NONE"
    scan_timeout=60
    discovered_services = pyqtSignal(list)
    client = "NONE"
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
                
                #await client.disconnect()
        except Exception as e:
            print("Opps ,That device is not explorable, at least not by you.")
        
 
class BLE_EnableNotify(QThread):
    ble_address= "NONE"
    char_uuid = "NONE"
    client = "NONE"
    gotNotification = pyqtSignal(str)
    def run(self):
        asyncio.run(self.enableNotify(self.client))
        
    async def enableNotify(self, client : BleakClient):
        async with  client:
            #here set a lable to notifying enabled or something

            await client.start_notify(self.char_uuid, self.notification_handler)
            await asyncio.sleep(60.0)
            #await client.stop_notify(self.char_uuid)
    def notification_handler(self,sender, data):
        """Simple notification handler which prints the data received."""
       # print("{0}: {1}".format(sender, data))
        self.gotNotification.emit(str(data))

class BLE_ReadChar(QThread):
    ble_address= "NONE"
    scan_timeout=5
    charToRead = "NONE"
    charReadData = pyqtSignal(str)
    client = "NONE"
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
    ble_address= "NONE"
    client = "None"
    def run(self):
        asyncio.run(self.connect(self.ble_address, self.client))

    async def connect(self,address, client:BleakClient):
        print("Attmepting to conenct")
        async with  client:
            #client.disconnect()
            await client.connect()
            print(str(client.is_connected))
        return self.client