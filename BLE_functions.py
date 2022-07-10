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

'''******************************************************************************************
        Scan for devices
*******************************************************************************************'''
class BLE_DiscoverDevices(QThread):
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
        #disconnect here? or keep active until user presses explore?

'''******************************************************************************************
        Connects to a connectable device and discover services 
        and emits singal back to GUI application to handle each
        discovered service/characteristic
*******************************************************************************************'''
class BLE_DiscoverServices(QThread):
    ble_address= None
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
'''******************************************************************************************
        Implements an infinite asyncio loop charged with registering
        notifications, read/write and signal emition of each event to 
        GUI application
*******************************************************************************************'''

class BleakLoop(QThread):
    ble_address= None
    client = None
    errorMsg = pyqtSignal(str)
    disconnectSignal = pyqtSignal(bool)
    # disconnected state switch
    connect = False
    disconnect_triggered = False
    # used to trigger service discovery
    discoverServices = False
    discovered_services_signal = pyqtSignal(list)
    # used for registering notifys
    notifyCharsAdded = False
    newNotifyCharUUID = None
    # used forr unregistering notifys
    notifyRemoveChar = False
    removeNotifyCharHandle = None
    # signals
    gotNotification = pyqtSignal(list)
    notifyRegisteredState = pyqtSignal(bool)
    def run(self):
        self.connect =True
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
            
            
           # await client.write_gatt_char("85fc5681-31d9-4185-87c6-339924d1c5be", bytes('1', 'utf-8'))
    
            while self.connect == True:
                await asyncio.sleep(1.0)
                # check the flag to disconnect
                if self.disconnect_triggered == True:
                    try:
                        await client.disconnect()

                        self.handle_disconnect(client)
                        self.disconnect_triggered = False
                        self.connect = False
                        self.disconnectSignal.emit(True)

                    except Exception as err:
                        print("-------> error is :")
                        print(err)
                #--------------- if any notify chars have been added register them
                if self.notifyCharsAdded == True and self.newNotifyCharUUID != None:
                    print("About to add chars")
                    try:
                        await client.start_notify(self.newNotifyCharUUID, self.notification_handler)
                        self.notifyRegisteredState.emit(True)
                    except Exception as err:
                        print(err)
                    self.newNotifyCharUUID = None
                    self.notifyCharsAdded = False
                #-------------- if any prviously enabled chars need to removed from notify
                if self.notifyRemoveChar == True and self.removeNotifyCharHandle != None:
                    try:
                        await client.stop_notify(self.removeNotifyCharHandle)
                        self.notifyRemoveChar = False
                    except Exception as err:
                        print("error here was: " )
                        print(err)
                #-------------- if discoverServices has been triggered
                if self.discoverServices == True:
                    try :
                        
                        print(f"Connected: {client.is_connected}")
                        for service in client.services:
                            #emit top level item

                            self.discovered_services_signal.emit([f"[Service] {service}", 0])


                            for char in service.characteristics:
                                #emit children of top level
                                if "read" in char.properties:
                                    try:
                                        value = bytes(await client.read_gatt_char(char.uuid))
                                        self.discovered_services_signal.emit([f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}",1])
                                        # print(
                                        #     f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                                        # )
                                    except Exception as e:
                                        self.discovered_services_signal.emit([f"\t[Characteristic] {char} ({','.join(char.properties)}), Error: {e}",1])
                                        # print(
                                        #     f"\t[Characteristic] {char} ({','.join(char.properties)}), Error: {e}"
                                        # )

                                else:
                                    value = None
                                    self.discovered_services_signal.emit([f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}",1])
                                    # print(
                                    #     f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                                    # )

                                for descriptor in char.descriptors:
                                    #emit children of children
                                    try:
                                        value = bytes(
                                            await client.read_gatt_descriptor(descriptor.handle)
                                            
                                        )
                                        self.discovered_services_signal.emit([f"\t\t[Descriptor] {descriptor}) | Value: {value}",2])
                                        # print(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                                    except Exception as e:
                                        print(err)
                                        #print(f"\t\t[Descriptor] {descriptor}) | Error: {e}")
                        self.discoverServices = False
                        
                        print(f"Cleint conenction state : {client.is_connected}")
                            
                    except Exception as e:
                        print("Opps ,That device is not explorable, at least not by you.")

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