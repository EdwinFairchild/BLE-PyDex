from main import *

def update_discovered_devices(interface, device):
    device_name = str(device[0])  # Convert to string explicitly
    device_data = str(device[1])  # Convert to string without splitting by comma
    list_widget = interface.ui.list_widget_discovered
    table_widget = interface.ui.tableWidget_2  # Access the tableWidget_2

    ####################### HELPER METHODS ###############################
    def add_device_to_list():
        matched_items = list_widget.findItems(device_name, Qt.MatchExactly)
        if not matched_items:
            list_widget.addItem(device_name)
        else:
            # there is a match update the item
            for item in matched_items:
                item.setText(device_name)

    def add_device_to_table():
        # Add the data from device[1] into the tableWidget_2
        interface.add_adv_table_item.emit(device_data)
        
        # this method below is extremely expensive in terms of performance
        # it slows the gui down to a crawl and should only be called when needed
        # I think it is no longer needed because the table widget is being stretched
        # to match the gui window size
        #table_widget.resizeRowsToContents()
    ########################################################################

    def update_rssi_graph():
        # TODO possibly add a checkbox to disable graphing,
        # the checkbox could be considred here to see if we graph or not
        interface.update_rssi_thread.updateDeviceData(device, time.time())


    # check if the filter is empty
    if interface.ui.txt_scan_filter.text() == "":
        add_device_to_list()
    elif interface.ui.txt_scan_filter.text() in device_name:
        add_device_to_list()

    
    if interface.ui.logAll.isChecked():
        add_device_to_table()
        update_rssi_graph()
        
    elif interface.ui.logSelection.isChecked():
        try:
            # check if the device_name is the same as the selected item in list_widget_discovered
            if device_name == interface.ui.list_widget_discovered.currentItem().text():
                add_device_to_table()
                update_rssi_graph()
        except AttributeError:
            pass

def clear_graph_history(interface):
    # Clear the data for each device curve
    for device_curve in interface.device_data_curves.values():
        device_curve.clear()

    # Optionally, you can also clear the device_data_sets dictionary
    interface.device_data_sets.clear()


def timed_scanning_stoped(interface):
    interface.stop_scanner()


def device_disconnected_cb(interface):
    logger = logging.getLogger("PDexLogger")
    interface.connectedDevice.is_connected = False
    try:
        # stop the connect thread
        #gracefully disconnect and break infinite loop while connected
        interface.stop_connection()
    except Exception as err:
        logger.setLevel(logging.WARNING)
        logger.warning(err)
        logger.setLevel(logging.INFO)
    
    # clean up gui elements
    interface.cleanUp.emit("dummy data")

def init_signals_and_slots(interface):
    interface.bleScanner.discovered_devices.connect(lambda device : update_discovered_devices(interface,device))
    interface.bleScanner.scanning_stoped.connect(lambda : timed_scanning_stoped(interface))
     #register slot/signal for disconnecting from device
    interface.connectedDevice.device_disconnected.connect(lambda: device_disconnected_cb(interface))
    # show Gatt explorer when connected
    interface.connectedDevice.connection_established.connect(lambda: interface.stacked_widget_show_connected())












