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
        

class BleakLoop(QThread):
    ble_address= None
    #dictionary contaning UUID as keys and Handles as Values
    notifyEnabledChars = {}
    client = None
    gotNotification = pyqtSignal(list)
    errorMsg = pyqtSignal(str)
    notifyCharsAdded = False
    newNotifyCharUUID = None
    def run(self):
        asyncio.run(self.bleakLoop())
    #-------------------------------------------------------------------------
    def handle_disconnect(self, _: BleakClient):
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()
    #-------------------------------------------------------------------------
    def notification_handler(self,sender, data):
        # send data let application parse it
        dataList = [sender,data]
        self.gotNotification.emit(dataList)

    #-------------------------------------------------------------------------
    async def bleakLoop(self):
        #-------------------------------------------------------------------------
        async with BleakClient(self.ble_address, disconnected_callback= self.handle_disconnect) as client:
            
            
            await client.write_gatt_char("85fc5681-31d9-4185-87c6-339924d1c5be", bytes('1', 'utf-8'))
    
            while True:
                await asyncio.sleep(1.0)
                # if any notify chars have been added register them
                if self.notifyCharsAdded == True and self.newNotifyCharUUID != None:
                    print("About to add chars")
                    await client.start_notify(self.newNotifyCharUUID, self.notification_handler)
                    self.newNotifyCharUUID = None
                    self.notifyCharsAdded = False
                    

                #cycle through  dictionary of characters to read.

                #if that specific chararacteristic is not "stream" enabled
                #then just read once and remove from dictionary

                #other wise read it 

                #check if there are new characteristics that need to be registered with 'notify'
                # chardata = await client.read_gatt_char("85fc567e-31d9-4185-87c6-339924d1c5be")
                # print(str(chardata))
''' TODO : start mechanism to register new Notify charateristics : use signals and slots 
make a signal that will pass the UUID and the callback function. 
callback funtion should be generic for all of them, and it should read the "sender"
argument passed to know what char sent the BLE_EnableNotify '''