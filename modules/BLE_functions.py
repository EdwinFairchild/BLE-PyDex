import bleak as ble
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
from functools import cached_property
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
    #client = None
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
        for task in asyncio.all_tasks():
            task.cancel()
    # -------------------------------------------------------------------------

    def notification_handler(self, sender, data):
        # send data let application parse it
        dataList = [sender, data]
        self.gotNotification.emit(dataList)
    # -------------------------------------------------------------------------

    async def enableCharNotification(self, client: BleakClient):
        print("About to add chars")
        try:
            await client.start_notify(self.newNotifyCharUUID, self.notification_handler)
            self.notifyRegisteredState.emit(True)
        except Exception as err:
            print(err)
            self.notifyRegisteredState.emit(False)
        self.newNotifyCharUUID = None
        self.notifyCharsAdded = False
    # -------------------------------------------------------------------------

    async def removeCharNotification(self, client: BleakClient):
        try:
            await client.stop_notify(self.removeNotifyCharHandle)
            self.notifyRemoveChar = False
        except Exception as err:
            print(err)
    # -------------------------------------------------------------------------

    async def disconenctBLE(self, client: BleakClient):
        try:
            await client.disconnect()
            self.handle_disconnect(client)
            self.disconnect_triggered = False
            self.connect = False
            self.disconnectSignal.emit(True)
        except Exception as err:
            print("-------> error is :")
            print(err)
    # -------------------------------------------------------------------------

    async def readCharCallback(self, client: BleakClient):
        try:
            chardata = await client.read_gatt_char(self.readCharUUID)
            self.readCharSignal.emit(str(chardata))
        except Exception as err:
            print(err)
        self.readChar = False
    # -------------------------------------------------------------------------

    async def writeCharCallback(self, client: BleakClient):
        try:
            await client.write_gatt_char(self.writeCharUUID, bytes(self.writeCharData, 'utf-8'))
        except Exception as err:
            print(err)
        self.writeChar = False
    # -------------------------------------------------------------------------

    async def exploreSerivce(self, client: BleakClient):
        try:

            print(f"Connected: {client.is_connected}")
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
                            print(err)
            self.discoverServices = False
        except Exception as e:
            print("Opps ,That device is not explorable, at least not by you.")
    # -------------------------------------------------------------------------

    async def bleakLoop(self):
        async with BleakClient(self.ble_address, disconnected_callback=self.handle_disconnect) as client:
            while self.connect == True:
                await asyncio.sleep(0.1)
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
