from main import *
from modules import max32xxx_ota
from elftools.elf.elffile import ELFFile
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt 

def btn_scan(interface):
    logger = logging.getLogger("PDexLogger")
    # is device is connected, disconnect it
    if interface.connectedDevice.is_connected == True:
        interface.stop_connection()


    if interface.bleScanner.is_scanning == False:
        try:
            # clear graph, device list, colors etc. except data logs, user might want to save them
            interface.ui.list_widget_discovered.clear()
            interface.device_data_curves= {}
            interface.device_original_colors = {}
            interface.ui.list_widget_discovered.clearSelection()
            
            # check if the checkbox check_no_timeout is checked and set the timeout to 0 if it is
            if interface.ui.check_no_timeout.isChecked():
                interface.bleScanner.scan_timeout = 0
            else:
                #check scanSlider value and set timeout accordingly
                interface.bleScanner.scan_timeout = interface.ui.scanSlider.value()

            interface.bleScanner.is_scanning = True
            # Start ble_scanner thread
            interface.bleScanner.start()
            # Update text of this button to "Stop"
            interface.ui.btn_scan.setText("Stop")
            # Change background color of this button to rgba(33, 37, 43, 180)
            interface.ui.btn_scan.setStyleSheet("background-color: rgba(33, 37, 43, 180); border: 2px solid rgb(52, 59, 72);border-radius: 5px;")

            #restart rssi gaph update thread because it could have been stopped by stop button
            if interface.ui.graph_enabled.isChecked():
                interface.update_rssi_thread.GraphActive = True
                interface.update_rssi_thread.start()
        except Exception as err:
            logger.setLevel(logging.WARNING)
            logger.warning(err)
            logger.setLevel(logging.INFO)
        
    else:
        try:
            interface.bleScanner.is_scanning = False
            # Stop ble_scanner thread
            interface.stop_scanner()
            interface.stop_rssi_thread()
        except Exception as err:
            logger.setLevel(logging.WARNING)
            logger.warning(err)
            logger.setLevel(logging.INFO)
        
def txt_scan_filter_changed(ui):
    logger = logging.getLogger("PDexLogger")
    # filter QListwidget list_widget_discovered based on txt_scan_filter text
    # keeping in mind the list_widget_discovered is not directly iterable 
    # and you can maybe use findItems(device_name, Qt.MatchExactly)
    try:
        # get the text from txt_scan_filter
        filter_text = ui.ui.txt_scan_filter.text()
        # get the QListWidget list_widget_discovered
        list_widget = ui.ui.list_widget_discovered
        # get the number of items in the list_widget_discovered
        list_widget_count = list_widget.count()
        # iterate through the list_widget_discovered
        for i in range(list_widget_count):
            # get the item at index i
            item = list_widget.item(i)
            # get the text of the item
            item_text = item.text()
            # check if the filter_text is in the item_text
            if filter_text in item_text:
                # if it is, set the item to visible
                item.setHidden(False)
            else:
                # if it is not, set the item to hidden
                item.setHidden(True)
    except Exception as err:
        logger.setLevel(logging.WARNING)
        logger.warning(err)
        logger.setLevel(logging.INFO)

def btn_connect(interface):
    logger = logging.getLogger("PDexLogger")
    # check if the connectedDevice is connected
    if interface.connectedDevice.is_connected == True:
        logger.info("Disconnecting...")
        interface.ui.btn_connect.setText("disconnecting...")
        # disable btn_connect until device is disconnected
        interface.ui.btn_connect.setEnabled(False)
       
        try:
            # if it is, disconnect it
            interface.connectedDevice.is_connected = False
            #interface.stop_connection()
        except Exception as err:
            logger.setLevel(logging.WARNING)
            logger.warning(err)
            logger.setLevel(logging.INFO)
        #nothing else todo, return
        return
    
    # stop scanning if it is running
    if interface.bleScanner.is_scanning == True:
        try:
            interface.stop_scanner()
            interface.stop_graphing()
            # interface.bleScanner.is_scanning = False
            # interface.bleScanner.quit()
            interface.ui.btn_scan.setText("Scan")
            interface.ui.btn_scan.setStyleSheet(interface.btn_stylesheet)
        except Exception as err:
            logger.setLevel(logging.WARNING)
            logger.warning(err)
            logger.setLevel(logging.INFO)

    try:
        # get device address from selected item in list_widget_discovered, it is the first 18 characters of the string
        interface.device_address = interface.ui.list_widget_discovered.currentItem().text()[0:17]
        
        interface.connectedDevice.ble_address = interface.device_address
        # start the connect thread
        interface.connectedDevice.start()
        interface.connectedDevice.setPriority(QThread.TimeCriticalPriority)
        # set the text of the connect button to disconnect
        interface.ui.btn_connect.setText("Disconnect")
        # set the background color of the connect button to rgba(33, 37, 43, 180)
        interface.ui.btn_connect.setStyleSheet("background-color: rgba(33, 37, 43, 180);border: 2px solid rgb(52, 59, 72);border-radius: 5px;")
        
       # interface.ui.stackedWidget.setCurrentWidget(interface.ui.connections_page)
    except Exception as err:
        logger = logging.getLogger("PDexLogger")
        # User has not selected an item in the list_widget_discovered
        if interface.device_address == None:
            logger.info("No device selected to connect to")
        else:
            # some other error
            logger.info("Error connecting to device: {}".format(err))
        # kicks off disocnnection events
        interface.connectedDevice.is_connected = False

def clear_logs(interface):
    logger = logging.getLogger("PDexLogger")
    try:
        interface.ui.tableWidget_2.clearContents()
        interface.ui.tableWidget_2.setRowCount(0)
        interface.device_data_curves= {}
        interface.device_original_colors = {}
        interface.ui.list_widget_discovered.clearSelection()
        # Remove all series from the chart
        interface.ui.qtchart_widgetholder.chart().removeAllSeries()
        if interface.ui.graph_enabled.isChecked():
            interface.update_rssi_thread.GraphActive = True
            interface.update_rssi_thread.start()
        logger.info("Cleared logs")
    except Exception as err:
        logger.setLevel(logging.WARNING)
        logger.warning(err)
        logger.setLevel(logging.INFO)

def save_adv_logs(interface):
    logger = logging.getLogger("PDexLogger")
    try:
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            interface, "Save file", "", "Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                rows = interface.ui.tableWidget_2.rowCount()
                cols = interface.ui.tableWidget_2.columnCount()
                for row in range(rows):
                    for col in range(cols):
                        f.write(interface.ui.tableWidget_2.item(row,col).text())
                        f.write('\t')
                    f.write('\n')
            logger.info("Saved logs to {}".format(file_name))
               
    except Exception as err:
        logger.info("Error saving logs: {}".format(err))
    
def btn_github(interface):
    logger = logging.getLogger("PDexLogger")
    try:
        webbrowser.open('https://github.com/EdwinFairchild/BLE-Scout')
    except Exception as err:
        logger.setLevel(logging.WARNING)
        logger.warning(err)
        logger.setLevel(logging.INFO)

def btn_disconnect(interface):
    logger = logging.getLogger("PDexLogger")
    # check if the connectedDevice is connected
    if interface.connectedDevice.is_connected == True:
        logger.info("Disconnecting...")
        # disable btn_connect until device is disconnected
        interface.ui.btn_connect.setEnabled(False)
       
        try:
            # if it is, disconnect it
            interface.connectedDevice.is_connected = False
            #interface.stop_connection()
        except Exception as err:
            logger.setLevel(logging.WARNING)
            logger.warning(err)
            logger.setLevel(logging.INFO)
        #nothing else todo, return
        return

def disable_graphing(main_window):
    logger = logging.getLogger("PDexLogger")
    # check checkbox state
    try:
        if main_window.ui.graph_enabled.isChecked():
            main_window.update_rssi_thread.GraphActive = True
            main_window.update_rssi_thread.start()
        else:
            main_window.stop_graphing()
    except Exception as err:
        logger.setLevel(logging.WARNING)
        logger.warning(err)
        logger.setLevel(logging.INFO)

def handle_checkbox_state_change(state, var_name, address, address_dict, main_window):
    logger = logging.getLogger("PDexLogger")
   
    if state == Qt.Checked:
        logger.info(f"Added {var_name} to watch list")

        # Add the var_name to the tbl_vars_watched table
        watched_row_position = main_window.ui.tbl_vars_watched.rowCount()
        main_window.ui.tbl_vars_watched.insertRow(watched_row_position)
        main_window.ui.tbl_vars_watched.setItem(watched_row_position, 0, QTableWidgetItem(var_name))

        address_dict[var_name] = {"address": address,"watched_row_position" : watched_row_position }
        # Add a button to remove the row
        btn_remove = QPushButton("Remove")
        btn_remove.clicked.connect(lambda: remove_watched_var(var_name, watched_row_position, main_window))
        main_window.ui.tbl_vars_watched.setCellWidget(watched_row_position, 2, btn_remove)

    else:
        address_dict.pop(var_name, None)
        # Find and remove the row from tbl_vars_watched
        for row in range(main_window.ui.tbl_vars_watched.rowCount()):
            if main_window.ui.tbl_vars_watched.item(row, 0).text() == var_name:
                main_window.ui.tbl_vars_watched.removeRow(row)
                logger.info(f"Removed {var_name} from watch list")
                break
   
# Function to handle removing a watched variable
def remove_watched_var(var_name, row, main_window):
    main_window.ui.tbl_vars_watched.removeRow(row)

    # Find the corresponding checkbox in tbl_vars by var_name
    for row_index in range(main_window.ui.tbl_vars.rowCount()):
        item = main_window.ui.tbl_vars.item(row_index, 0) # Assuming var_name is in column 0
        if item and item.text() == var_name:
            checkbox_widget = main_window.ui.tbl_vars.cellWidget(row_index, 2) # Assuming checkbox is in column 3
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(False)
                    break
    
    main_window.vars_watched_dict.pop(var_name, None)

    # If there are no more rows, explicitly set the row count to 0
    if main_window.ui.tbl_vars_watched.rowCount() == 0:
        main_window.ui.tbl_vars_watched.setRowCount(0)
        
def load_elf(main_window):
    logger = logging.getLogger("PDexLogger")
    # # Open a file dialog to select the ELF file
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(main_window, "Open ELF File", "", "ELF Files (*.elf);;All Files (*)", options=options)
    #filename = '/home/eddie/projects/ADI-Insight/BLE_dats/build/max32655.elf'
    if not filename:
        logger.info("No file selected")
        return
    # clear table
    main_window.ui.tbl_vars.setRowCount(0)
    #filename = '/home/eddie/projects/ADI-Insight/BLE_dats/build/max32655.elf'
    table_widget = main_window.ui.tbl_vars
    elf_file_path = '/home/eddie/projects/ADI-Insight/BLE_dats/build/max32655.elf'
    table_widget = main_window.ui.tbl_vars # Replace with the actual table widget object
    table_widget.setColumnWidth(3, 50)

    elf_file_path = '/home/eddie/projects/ADI-Insight/BLE_dats/build/max32655.elf'

    # Slot method to handle symbol extracted
    def handle_symbol_extracted(name, address):
        row_position = main_window.ui.tbl_vars.rowCount()
        main_window.ui.tbl_vars.insertRow(row_position)
        main_window.ui.tbl_vars.setItem(row_position, 0, QTableWidgetItem(name))
        main_window.ui.tbl_vars.setItem(row_position, 1, QTableWidgetItem(hex(address)))

        # Create a checkbox
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda state, name=name, address=address: handle_checkbox_state_change(state, name, address, main_window.vars_watched_dict, main_window))

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        main_window.ui.tbl_vars.setCellWidget(row_position, 2, widget) # Changed to column 3

    # Start the thread
    main_window.elf_parser.filename = filename
    main_window.elf_parser.symbol_extracted.connect(handle_symbol_extracted) 
    logger.info("Starting elf parser thread")
    main_window.elf_parser.ramStart = int(main_window.ui.txtRamStart.text() , 16)
    main_window.elf_parser.ramEnd = int(main_window.ui.txtRamEnd.text() , 16)
    main_window.elf_parser.start()

def start_monitoring(main_window):
    if main_window.var_watcher.isRunning():
        main_window.var_watcher.exit_early = True
        main_window.ui.btn_monitor.setText("Start Monitoring")
    else:
        main_window.var_watcher.start()
        main_window.ui.btn_monitor.setText("Stop Monitoring")
        
def get_core_regs(main_window):
    logger = logging.getLogger("PDexLogger")
    try:
        main_window.var_watcher.getCoreRegs = True
    except Exception as err:
        logger.info("Error getting core regs: {err}")

def load_bin(main_window):
    logger = logging.getLogger("PDexLogger")
    try:
        fname = QFileDialog.getOpenFileName(main_window, "Open firmware binary", "", "*.bin")
        if fname:
            #get crc32 of the file using method in max32xxx_ota.py module
            crc32,fileLen = max32xxx_ota.get_crc32(fname[0])
            fileName = fname[0]
            main_window.fileName = fileName
            main_window.fileLen = fileLen
            main_window.fileCrc32 = crc32
           
    except Exception as err:
        logger.info(f"Error loading binary: {err}")

def start_ota(main_window):
    main_window.connectedDevice.device_ota_update.emit(main_window.fileName, main_window.fileLen, main_window.fileCrc32)

def register_button_callbacks(main_window):
    logger = logging.getLogger("PDexLogger")
    try:
        main_window.ui.btn_scan.clicked.connect(lambda: btn_scan(main_window))
        # add call back for txt_scan_filter textChanged
        main_window.ui.txt_scan_filter.textChanged.connect(lambda: txt_scan_filter_changed(main_window))
        main_window.ui.btn_connect.clicked.connect(lambda: btn_connect(main_window))
        main_window.ui.btn_share.clicked.connect(lambda: btn_github(main_window))
        main_window.ui.btn_disconnect.clicked.connect(lambda: btn_disconnect(main_window))  
        main_window.ui.btn_load_elf.clicked.connect(lambda: load_elf(main_window))  
        main_window.ui.btn_monitor.clicked.connect(lambda: start_monitoring(main_window))

        # get core regs
        main_window.var_watcher.core_regs_tuple.connect(main_window.get_core_regs_handler)
        main_window.ui.btn_refreshCoreRegs.clicked.connect(lambda: get_core_regs(main_window))
        # graphing checkbox callbacks
        main_window.ui.graph_enabled.stateChanged.connect(lambda: disable_graphing(main_window))        

        #register slot/signal for disconnecting from device
        main_window.ui.btn_clear_logs.clicked.connect(lambda: clear_logs(main_window))
        main_window.ui.btn_save_logs.clicked.connect(lambda: save_adv_logs(main_window))

        #register button callbacks for OTA
        main_window.ui.btn_load_bin.clicked.connect(lambda :load_bin(main_window))
        main_window.ui.btn_start_ota.clicked.connect(lambda:start_ota(main_window))
    except Exception as err:
        logger.setLevel(logging.WARNING)
        logger.warning(err)
        logger.setLevel(logging.INFO)
       
    
