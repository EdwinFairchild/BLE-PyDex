from main_app import *
from modules import Slots
from modules import MiscHelpers

interface = None

def console_init(main_interface):
    global interface
    interface = main_interface

def log(data):
    global interface
    interface.ui.console.append("> "+ str(data))
    print("log > "+ str(data))
    #interface.ui.console.verticalScrollBar().setSliderPosition(10)

def log_status():
    global interface
    log("Connected state: " + str(interface.connected_state))

def errMsg(data):
    log(str(data))