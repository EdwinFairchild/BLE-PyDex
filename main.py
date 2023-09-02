import sys
import os
import platform
import logging
import re
import random
import time
import numpy as np
import webbrowser

from modules import *
from widgets import *
from pyqtgraph import PlotDataItem
import bluetooth_numbers as ble_uuid
from bluetooth_numbers import service
from uuid import UUID

import pyqtgraph as pg

from PySide6 import QtUiTools, QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox, QTableWidget, QMenu, QApplication
from PySide6.QtGui import QCursor, QAction, QClipboard , QPen , QBrush , QColor
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker, Qt , QTimer
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt 
from PySide6 import QtCharts
from PySide6.QtCharts import QLineSeries
from math import sin, pi
os.environ["QT_FONT_DPI"] = Settings.HIGH_DPI_DISPLAY_FONT_DPI # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
widgets = None

from char import Ui_char_widget

# TODO :  Move a lot of these functions to their related modules
class MainWindow(QMainWindow):
    add_adv_table_item = Signal(str)
    toplevel = None
    child = None
    vbox = QGridLayout()
    charCount= 1
    char_dict = {}
    cleanUp = Signal(object)
    axisX = QtCharts.QValueAxis()
    axisY = QtCharts.QValueAxis()
    axisX.setRange(0, 10)
    axisY.setRange(-1, 1)

    
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.vars_watched_dict={}
        self.device_address = None

        # Graphing variables
        self.device_data_sets = {}
        self.device_data_curves = {}
        self.device_original_colors = {}
        self.start_time = None #time.time()
        self.current_time = time.time()
        self.plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        # self.ui.widget_rssi_graph.setBackground((40, 44, 52)) 
        # self.ui.widget_rssi_graph.getPlotItem().getAxis('bottom').setStyle(showValues=False)

        # OTA variables
        self.fileName = None
        self.fileLen = None
        self.fileCrc32 = None
        
        
        # Initialize logging
        console = logging.getLogger("PDexLogger")
        handler = QLogHandler(self.ui.console)
        handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        handler.emitter.logMessage.connect(self.logToTextbox)
        console.addHandler(handler)
        console.setLevel(logging.DEBUG)
        self.logger = logging.getLogger("PDexLogger")

        # connected mode variables
        self.connectedDevice = BLE_ConnectDevice()
        self.connectedDevice.device_notification_recevied.connect(self.char_notification_handler)
        self.connectedDevice.device_char_read_response.connect(self.char_read_response_handler)

        #OTA related 
        self.connectedDevice.otas_progress_value.connect(
                    lambda value: self.otas_progress_update(value))
          

        
        self.update_rssi_thread = UpdateRSSIGraphThread(self)
        self.update_rssi_thread.dataUpdated.connect(self.update_graph)
        if self.ui.graph_enabled.isChecked():
            self.update_rssi_thread.GraphActive = True
            #self.update_rssi_thread.start()

        # Global BLE objects
        self.bleScanner = ble_functions.BLE_DiscoverDevices()

        # Global elf parser object
        self.elf_parser = ExtractGlobalVariablesThread(None, self.ui.tbl_vars)
        self.var_watcher = MonitoringThread(self.vars_watched_dict)
        self.var_watcher.signal_update_variable.connect(self.update_variable_in_table)  # Assuming 'self.update_variable_in_table' is a method that handles the update
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = False

        # APP NAME
        title = "BLE-PyDex"
        description = "Bluetooth Low Energy Scanner , Explorer, Logger and more..."
        # APPLY TEXTS
        self.setWindowTitle(title)
        self.ui.titleRightInfo.setText(description)

        self.ui.tbl_vars.setColumnWidth(3, 50)

        # TOGGLE MENU
        
        self.ui.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        self.ui.elfSettings.hide()

        # SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        #self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = self.ui.tableWidget_2.verticalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # UI MENU BASIC BUTTONS CLICK

        # LEFT MENUS
        self.ui.btn_home.clicked.connect(self.buttonClick)
        self.ui.btn_widgets.clicked.connect(self.buttonClick)
        self.ui.btn_gatt_explorer.clicked.connect(self.buttonClick)
        self.ui.btn_save.clicked.connect(self.buttonClick)
        self.ui.btn_insights.clicked.connect(self.buttonClick)

        # Register signal handlers
        self.add_adv_table_item.connect(lambda data :self.add_table_item(data))
        self.connectedDevice.discovered_services.connect(self.discovered_services)
        self.ui.gatt_treeView.itemClicked.connect(self.gatt_tree_view_clicked)

        # Register none-UI button callbacks
        btn_callbacks.register_button_callbacks(self)
        
        #self.ui.tableWidget_2.reset()

        # stylesheets
        self.btn_stylesheet = open("button_stylesheet.txt", "r").read()
        self.scroll_area_stylesheet = open("scroll_area_stylesheet.txt", "r").read()
        
        self.ui.scrollArea_2.setStyleSheet("""

        /* VERTICAL */
        QScrollBar:vertical {
            border: none;
            background: rgb(39, 52, 105);
            width: 10px;
            margin: 10px 0px 10px 0px;
           
        }

        QScrollBar::handle:vertical {
            background: rgb(170,200,255);
            min-height: 26px;
            
        }

        QScrollBar::add-line:vertical {
            background: none;
            height: 26px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            
        }

        QScrollBar::sub-line:vertical {
            background: none;
            height: 26px;
            subcontrol-position: top left;
            subcontrol-origin: margin;
            position: absolute;
            
        }

        QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {
            width: 26px;
            height: 20px;
            background: white;
            
            
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
            
        }

    """)

        
        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        self.ui.toggleLeftBox.clicked.connect(openCloseLeftBox)
        self.ui.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        self.ui.settingsTopBtn.clicked.connect(openCloseRightBox)

        # Init signals and slots
        slots.init_signals_and_slots(self)

        # register cleanup callback and pass widgets object to it with lambda
        self.cleanUp.connect(lambda: self.clean_up())

        
        
        self.ui.scrollArea_2.setLayout(self.vbox)
        self.ui.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollArea_2.setStyleSheet(self.scroll_area_stylesheet)


        # SHOW APP
        self.show()
        # right box visible content initially hide all execept scanner settings
        self.ui.ota_frame.hide()
        self.ui.ota_frame.setMaximumHeight(0)
        self.ui.elfSettings.hide()
        self.ui.elfSettings.setMaximumHeight(0)
        self.ui.scannerSettigns.setMaximumHeight(1000000)
        self.ui.scannerSettigns.show()


        # Set up the axes (assuming the chart is already set up in the .ui file)
        self.axisX = QtCharts.QValueAxis()
        self.axisY = QtCharts.QValueAxis()
        self.axisX.setRange(0, 10)
        self.axisY.setRange(-130, 0)

        self.ui.qtchart_widgetholder.chart().addAxis(self.axisX, Qt.AlignBottom)
        self.ui.qtchart_widgetholder.chart().addAxis(self.axisY, Qt.AlignLeft)
        self.ui.qtchart_widgetholder.chart().layout().setContentsMargins(0, 0, 0, 0)
        self.ui.qtchart_widgetholder.chart().setMargins(QMargins(0, 0, 0, 0))
        # change background color to rgb(40, 44, 52)
       # Create a QColor object with the desired background color
        background_color = QColor(33, 37,43)

        # Create a QBrush object with the QColor object
        background_brush = QBrush(background_color)

        # Set the background brush of the QChart
        self.ui.qtchart_widgetholder.chart().setBackgroundBrush(background_brush)
        # change grideline colors to rgb(52, 59, 72)
        self.ui.qtchart_widgetholder.chart().axisX().setGridLineColor(QColor(52, 59, 72))
        self.ui.qtchart_widgetholder.chart().axisY().setGridLineColor(QColor(52, 59, 72))
        # change axis label colors to rgb(255, 255, 255)
        self.ui.qtchart_widgetholder.chart().axisX().setLabelsColor(QColor(52, 59, 72))
        self.ui.qtchart_widgetholder.chart().axisY().setLabelsColor(QColor(52, 59, 72))
        # hide legend
        self.ui.qtchart_widgetholder.chart().legend().hide()
        # set chart title
        self.ui.qtchart_widgetholder.chart().setTitle("RSSI (dBm)")
        # Create a QPen object for the main axis lines
        pen = QPen(QColor(52, 59, 72))  # Change the color to whatever you want
        pen.setWidth(2)      # Change the width to your desired size

        # Apply the pen to the axis
        self.axisX.setLinePen(pen)
        self.axisY.setLinePen(pen)

        self.ui.list_widget_discovered.itemClicked.connect(self.highlight_selected_device)
        

                


        # SET CUSTOM THEME
        useCustomTheme = True
        themeFile = "themes/py_dracula_dark.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)
            # SET HACKS : some gui elements dont inherit parent styles, do it manually
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        self.ui.btn_home.setStyleSheet(UIFunctions.selectMenu(self.ui.btn_home.styleSheet()))
    def highlight_selected_device(self, item):
        selected_device = item.text()
        light_gray = QColor(52, 59, 72)  # Light gray color
        light_gray_pen = QPen(light_gray)
        light_gray_pen.setWidth(2)

        # Temporarily store the series for the selected device
        selected_device_series = None

        # Loop through all device_data_curves to update their color
        for device_name, device_series in self.device_data_curves.items():
            if device_name == selected_device:
                # This is the selected device, so keep its original color
                original_color_pen = QPen(self.device_original_colors[device_name])
                original_color_pen.setWidth(2)
                device_series.setPen(original_color_pen)

                # Store the series for adding it again later to bring it to the front
                selected_device_series = device_series

            else:
                # Change color to light gray for non-selected devices
                device_series.setPen(light_gray_pen)

        # Remove and add the series again to bring it to the front
        if selected_device_series:
            self.ui.qtchart_widgetholder.chart().removeSeries(selected_device_series)
            self.ui.qtchart_widgetholder.chart().addSeries(selected_device_series)
            selected_device_series.attachAxis(self.axisX)
            selected_device_series.attachAxis(self.axisY)

        # Trigger a redraw (you might not need this line, depending on your setup)
        self.ui.qtchart_widgetholder.chart().update()
    def update_graph(self,device_name,rssi_value,current_time):
        MAX_DEVICES = 50  # Maximum number of devices to display

        # Initialize start time and max duration
        if self.start_time is None:
            self.start_time = current_time

        max_duration = 5  # Maximum duration to display (in seconds)
        time_delta = current_time - self.start_time

        if time_delta > max_duration:
            self.start_time = current_time - max_duration
            self.axisX.setRange(self.start_time, current_time)
        else:
            self.axisX.setRange(self.start_time, current_time)

        if device_name in self.device_data_curves:
            # Retrieve the existing QLineSeries for the device
            device_series = self.device_data_curves[device_name]

            # Convert QLineSeries to numpy arrays for easy manipulation
            old_data = [(point.x(), point.y()) for point in device_series.pointsVector()]
            device_data_x, device_data_y = np.array(old_data).T

            # Append new data and update QLineSeries
            device_data_x = np.append(device_data_x, current_time)
            device_data_y = np.append(device_data_y, rssi_value)
            # Create a list of QPointF objects
            points = [QPointF(x, y) for x, y in zip(device_data_x, device_data_y)]

            device_series.replace(points)

        else:
            if len(self.device_data_curves) >= MAX_DEVICES:
                return  # Ignore new device if max is reached

            # Generate a random color for the new device
            random_color = random.randint(0, 0xFFFFFF)
            pen = QPen((random_color))
            pen.setWidth(2)
            # Create a new QLineSeries for the device
            new_device_series = QLineSeries()
            new_device_series.setPen(pen)
            new_device_series.append(current_time, rssi_value)
            # # Update color of QListWidgetItem to match the line color
            # for i in range(self.ui.list_widget_discovered.count()):
            #     item = self.ui.list_widget_discovered.item(i)
            #     if item.text() == device_name:
            #         item.setForeground(QBrush(random_color))
            #         break

            # Add to chart and attach axes
            self.ui.qtchart_widgetholder.chart().addSeries(new_device_series)
            new_device_series.attachAxis(self.axisX)
            new_device_series.attachAxis(self.axisY)

            # Store the new series in the dictionary
            self.device_data_curves[device_name] = new_device_series
            # Save the original color in the new dictionary
            self.device_original_colors[device_name] = random_color
        
   
    def stop_rssi_thread(self):
            # the RSSI thread
        if self.update_rssi_thread.GraphActive == True:    
            self.update_rssi_thread.GraphActive = False  # Request the thread to stop
            self.update_rssi_thread.quit()  # Request the thread to stop
            self.update_rssi_thread.wait()  # Wait until the thread has actually stopped
            self.logger.info("RSSI thread stopped")
                  
    def add_table_item(self, data):
        logger = logging.getLogger("PDexLogger")
        # data looks like this: 
        # AdvertisementData(manufacturer_data={301: b'\x04\x00\x02\x02\xb02\x06\x02\xc2\x00\xdd\xb6\xb2\x10\x02\x003\x00\x00\x00'}, 
        # service_data={'0000fe2c-0000-1000-8000-00805f9b34fb': b'\x000\x00\x00\x00\x11\x17402G'}, 
        # service_uuids=['0000fd82-0000-1000-8000-00805f9b34fb'], tx_power=-21, rssi=-62)

        # check if the string  manufacturer_data= is in the data string
        if "manufacturer_data={" in data:
            # extract the numbers after the string "manufacturer_data={"  and before the ":" , these are manufacturer ID
            manufacturer_id = data.split("manufacturer_data={")[1].split(":")[0]
            manufacturer_id = int(manufacturer_id)
            
            # check if that manufacturer ID is in bluetooth numbers library
            try:
                companyID= ble_uuid.company[manufacturer_id]
                #replace the manufacturer ID with the company name in data string
                data = data.replace(str(manufacturer_id),str(companyID))
            except Exception as e:
                companyID = "Unknown"





        # Add the data from device[1] into the tableWidget_2
        rowPosition = self.ui.tableWidget_2.rowCount()
        self.ui.tableWidget_2.insertRow(rowPosition)

        self.ui.tableWidget_2.setColumnCount(1)  # Set the number of columns to 1
        self.ui.tableWidget_2.setHorizontalHeaderItem(0, QTableWidgetItem("Advertised Data"))  # Set the column header
        # align header text to  left
        self.ui.tableWidget_2.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        #hide horizontal header
        self.ui.tableWidget_2.horizontalHeader().setVisible(True)
        #hide vertical header
        self.ui.tableWidget_2.verticalHeader().setVisible(True)
        item = QTableWidgetItem(data)  # Convert data to string explicitly
        item.setTextAlignment(Qt.AlignLeft)  # Center the text
        self.ui.tableWidget_2.setItem(rowPosition, 0, item)  # Place the data in the first column

        self.ui.tableWidget_2.setColumnWidth(0, 700)  # Set the width to your desired value
        self.ui.tableWidget_2.setRowHeight(rowPosition, 40)  # Set the height to your desired value
        if self.ui.check_scroll_to_bottom.isChecked():
            self.ui.tableWidget_2.scrollToBottom()

    def logToTextbox(self, data):
        self.ui.console.append(data)

    
    def discovered_services(self,data):
        
        PARENT = 0
        CHILD = 1
        GRANDCHILD = 2
        ''' data[0]
            comes in looking like this:
            ['[Service] 00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile', 0]
            ['\t[Characteristic] 00002a05-0000-1000-8000-00805f9b34fb (Handle: 17): Service Changed (indicate), Value: None', 1]
            And leaves  looking like this after the parsing below:
            Service :  00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile 
            Characteristic :  00002a05-0000-1000-8000-00805f9b34fb (Handle: 17): Service Changed (indicate), Value: None'''
        #clean up data per above commenr
        item = data[0]
        item = item.replace("\t", "")
        item = item.replace("[", "")
        item = item.replace("]", " : ")

        ''' data[1] 
            is a level indicator for the tree widget, this is emited by 
            modules->ble_functions->discover_device_services
            0 = PARENT = service 
            1 = CHILD = characteristic
            2 = GRANDCHILD = descriptor
        '''    
        level = data[1]
        permissions = data[2]
        
        if level == PARENT:
            # data[0] looks like this: 00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile 
            # extract the UUID from the string which is this: 00001801-0000-1000-8000-00805f9b34fb

            # check if UUID exist in ble numbers
            char_uuid = self.extract_uuid_name(item)
            self.logger.info("Adding service widget for UUID: " + str(char_uuid))
            self.toplevel = QTreeWidgetItem([str(char_uuid)])
            # Set the icon for the top-level item.
            icon = QIcon()
            icon.addPixmap(QPixmap("char_s.png"), QIcon.Normal, QIcon.On)
            self.toplevel.setIcon(0, icon)
            self.ui.gatt_treeView.addTopLevelItem(self.toplevel)
        elif level == CHILD and self.toplevel != None:
             # check if UUID exist in ble numbers
            char_uuid = self.extract_uuid_name(item)
            self.child = QTreeWidgetItem([str(char_uuid)])
            # Set the icon for the top-level item.
            icon = QIcon()
            icon.addPixmap(QPixmap("char_c.png"), QIcon.Normal, QIcon.On)
            self.child.setIcon(0, icon)
            self.toplevel.addChild(self.child)
           
           
        elif level == GRANDCHILD and self.child != None:
             # check if UUID exist in ble numbers
            char_uuid = self.extract_uuid_name(item)
            self.subchild = QTreeWidgetItem([str(char_uuid)])
            # Set the icon for the top-level item.
            icon = QIcon()
            icon.addPixmap(QPixmap("char_d.png"), QIcon.Normal, QIcon.On)
            self.subchild.setIcon(0, icon)
            self.child.addChild(self.subchild)
        # adds new widget to scroll area only for characteristics
        if permissions is not None:
            # send full item text to add char widget because it needs the name and uuid
            self.add_char_widget(item, permissions)
    
    def extract_uuid_name(self, data):
        # data[0] looks like this: 00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile 
        char_uuid = self.extract_uuid_hex(data)
        found_match = False
        # check if UUID exist in ble numbers
        for uuid_type in [ble_uuid.service, ble_uuid.characteristic, ble_uuid.descriptor]:
            try:
                char_uuid = uuid_type[UUID(char_uuid)]
                # replace the UUID with the name in item
                data = char_uuid
                found_match = True
                
            except:
                pass
        if found_match == False:
            # TODO check if UUID exist in user_uuids.json
            pass

        return data

    def extract_uuid_hex(self, data):
        # data[0] looks like this  "00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile" 
        # extract the UUID from the string which is this  "00001801-0000-1000-8000-00805f9b34fb"
        raw_uuid = data.split("(")[0].strip()
        return raw_uuid
    def extract_handle(self, data):
        # data[0] looks like this  "00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile" 
        # extract the handle value, not handle text, from the string which is this  "16"
        handle_value = data.split("(")[1].split(")")[0].split(":")[1].strip()
        return handle_value

    def gatt_tree_view_clicked(self,tree_item, column):
        # when user clicks on a tree item, check if it exists in char_dict
        # if it does exist then scroll to that widget
#        uuid = self.extract_uuid_hex(tree_item.text(column))   
        for key, value in self.char_dict.items():
            if tree_item.text(column) in value['char name']:
                self.ui.scrollArea_2.ensureWidgetVisible(self.char_dict[key]["widgetlocation"])
        
        
    def add_char_widget(self, char_uuid, permissions):
        """
        Adds a new widget representing a Bluetooth Low Energy (BLE) characteristic to the main scroll area. 
        This widget is loaded from a generic compiled UI file (`char.py`) and displays buttons and labels corresponding 
        to different characteristic properties like 'write', 'read', 'notify', etc. It also sets up necessary UI elements 
        and hooks for handling interactions with those properties.

        Parameters:
        - char_uuid (str): The UUID of the BLE characteristic to be displayed. This string must be parsed
          it comes in looking like this: 00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile
        - permissions (list): List of permissions associated with the characteristic. 
        Possible values include 'write-without-response', 'write', 'notify', 'read', and 'indicate'.

        Notes:
        1. The method registers callbacks for different characteristic properties like 'write', 'read', etc.
        based on the permissions list.
        2. Updates the main scroll area to include this newly created widget.
        3. Enabled/Disables different UI elements based on the permissions list.
        4. Stores a reference to this widget in 'char_dict' for future interactions.
        """
        # Add widget to Main Scroll Area
        scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        widget = QWidget()           # Widget that contains the collection of Vertical Box
       
        tempWidget = QtWidgets.QWidget()
        uiwidget = Ui_char_widget()
        
        tempWidget.setMinimumHeight(500)
        uiwidget.setupUi(tempWidget)

        # At this point we can access ui elements of the new char widget, we also store a reference to it in service_dict
        char_name = self.extract_uuid_name(char_uuid)
        if char_name == char_uuid:
            char_name = "Unknown"
        uiwidget.characteristic_name_lbl.setText(f"characteristic : {char_name}")
        uiwidget.uuid_lbl.setText(f"UUID : {self.extract_uuid_hex(char_uuid)}")
        uiwidget.handle_lbl.setText(f"Handle : {self.extract_handle(char_uuid)}")
        
        #check if both write and write without response are in permissions list
        if "write-without-response" in permissions and "write" in permissions:
            uiwidget.write_no_resp_toggle.setVisible(True)
            uiwidget.write_no_resp_lbl.setVisible(True)
            # set the toggle button to visible and only register one callback for both
            uiwidget.char_write_btn.clicked.connect(lambda state : self.char_write_btn_handler(self.extract_uuid_hex(char_uuid),True))
        else: #check if at least one of them is in permissions list
        # check if permissions list ['write-without-response', 'write', 'notify' , 'read' ,indicate] adn enable disable buttons with same name
            uiwidget.write_no_resp_toggle.setVisible(False)
            uiwidget.write_no_resp_lbl.setVisible(False)

            if "write-without-response" in permissions:
                uiwidget.char_write_btn.clicked.connect(lambda state : self.char_write_btn_handler(self.extract_uuid_hex(char_uuid), False))
                pass
            else:
                uiwidget.permission_write_wo_resp.setEnabled(False)
                #change background color of permissons label 
                uiwidget.permission_write_wo_resp.setStyleSheet("background-color: rgb(52, 59, 72);color:rgb(205,205,205);padding:5px;border-radius: 12px;")
            
            if "write" in permissions: # this is write with response
                uiwidget.char_write_btn.clicked.connect(lambda state : self.char_write_btn_handler(self.extract_uuid_hex(char_uuid),True))
                pass
            else:
                
                uiwidget.char_write_txt.setMaximumWidth(0)
                uiwidget.char_write_txt.setMinimumWidth(0)
                uiwidget.char_write_btn.setMaximumWidth(0)
                uiwidget.char_write_btn.setMinimumWidth(0)
                #change background color of permissons label 
                uiwidget.permission_write.setStyleSheet("background-color: rgb(52, 59, 72);color:rgb(205,205,205);padding:5px;border-radius: 12px;")

        if "notify" in permissions:
            # regiter callback for notification toggle "notify_toggle" state change in uiwidget
            uiwidget.notify_toggle.stateChanged.connect(lambda state : self.notify_toggle_handler(self.extract_uuid_hex(char_uuid),state))
            pass
        else:
            uiwidget.notify_toggle.setEnabled(False)
            #change background color of permissons label 
            uiwidget.permission_notify.setStyleSheet("background-color: rgb(52, 59, 72);color:rgb(205,205,205);padding:5px;border-radius: 12px;")
            #make invisible
            #uiwidget.permission_notify.setVisible(False)
        if "read" in permissions:
            # regiter callback for read button
            uiwidget.char_read_btn.clicked.connect(lambda state : self.char_read_btn_handler(self.extract_uuid_hex(char_uuid)))
            pass
        else:
            uiwidget.char_read_btn.setMaximumWidth(0)
            uiwidget.char_read_btn.setMinimumWidth(0)
            #change background color of permissons label 
            uiwidget.permission_read.setStyleSheet("background-color: rgb(52, 59, 72);color:rgb(205,205,205);padding:5px;border-radius: 12px;")
 
        if "indicate" in permissions:
            # regiter callback for indications
            pass
        else:
            uiwidget.permission_indicate.setEnabled(False)
            #change background color to light gray
            uiwidget.permission_indicate.setStyleSheet("background-color: rgb(52, 59, 72);color:rgb(205,205,205);padding:5px;border-radius: 12px;")
            #make invisible
            #uiwidget.permission_indicate.setVisible(False)
        # if no read and no write or write without response then hide read_write_frame
        if "read" not in permissions and "write" not in permissions and "write-without-response" not in permissions:
            uiwidget.read_write_frame.setMaximumHeight(0)
            uiwidget.read_write_frame.setMinimumHeight(0) 

        widget.setLayout(self.vbox)
        widget.setStyleSheet("""
            border: 0px solid rgb(52, 59, 72);
	        border-radius: 5px;	
            margin: 0px;
            padding: 0px;""")

        # add to vertical layout row,column
        self.vbox.addWidget(tempWidget,self.charCount,0)
        self.vbox.setSpacing(10)
        self.vbox.setContentsMargins(QMargins(20, 0, 0, 0))

        self.charCount += 1

        self.ui.scrollArea_2.setStyleSheet("""
            border: 0px solid rgb(52, 59, 72);
	        border-radius: 0px;	
            margin: 0px;
            padding: 0px;""")
        self.ui.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollArea_2.setWidget(widget)

        # Storing widgetsin dictionary for future reference, for accessing elements of the widget
        # and removing it from the scroll area
        uuid_raw = self.extract_uuid_hex(char_uuid)
        self.char_dict[uuid_raw] = {
            "char name":char_uuid,
            "uiWidget":uiwidget,
            "widgetlocation":tempWidget, 
            "permissions":permissions}
        # to retreive a vlue from this dict
        # mywidget = self.char_dict[UUID]["widget"] 
        
        # register callbacks for the uiwidget elements

        #  store reference to widget in char_dict so we can access it later, use UUID as key
    def stacked_widget_show_connected(self):
        # change stacked widget to connections page
        self.ui.btn_gatt_explorer.click()
        
    def char_write_btn_handler(self, UUID , resp : bool = False ):
        data_to_write = self.char_dict[UUID]["uiWidget"].char_write_txt.toPlainText()
        # get this widget from char_dict
        # check if write with response or write without response by checking toggle state
        # only if the toggle button is visible otherwise it is disabled, dont override rap
        if self.char_dict[UUID]["uiWidget"].write_no_resp_toggle.isVisible():
            if self.char_dict[UUID]["uiWidget"].write_no_resp_toggle.isChecked():
                resp = False
            else:
                resp = True    
        self.connectedDevice.device_char_write.emit(UUID,data_to_write,resp,False)

    def char_read_btn_handler(self, UUID):
        # get this widget from char_dict
        self.connectedDevice.device_char_read.emit(UUID)
    def notify_toggle_handler(self, UUID, state):
        self.connectedDevice.device_char_notify.emit(UUID,state)

    def char_notification_handler(self, uuid, payload):
        char_uuid = self.extract_uuid_hex(uuid)
        # find uuid in char dict and update the uiwidget, append text to char_read_txt
        self.char_dict[char_uuid]["uiWidget"].char_read_txt.append(payload)

    def char_read_response_handler(self, uuid, payload):
        char_uuid = self.extract_uuid_hex(uuid)
        # find uuid in char dict and update the uiwidget, append text to char_read_txt
        self.char_dict[char_uuid]["uiWidget"].char_read_txt.append(payload)    

    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            # hide elfSettings frame
            self.ui.ota_frame.hide()
            self.ui.ota_frame.setMaximumHeight(0)
            self.ui.elfSettings.hide()
            self.ui.elfSettings.setMaximumHeight(0)
            self.ui.scannerSettigns.setMaximumHeight(1000000)
            self.ui.scannerSettigns.show()

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_gatt_explorer":
            self.ui.stackedWidget.setCurrentWidget(self.ui.connections_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            self.ui.elfSettings.hide()
            self.ui.elfSettings.setMaximumHeight(0)
            self.ui.scannerSettigns.setMaximumHeight(0)
            self.ui.scannerSettigns.hide()
            self.ui.ota_frame.show()
            self.ui.ota_frame.setMaximumHeight(1000000)


        if btnName == "btn_save":
            pass
        
        if btnName == "btn_insights":
            self.ui.stackedWidget.setCurrentWidget(self.ui.insights)
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            self.ui.scannerSettigns.hide()
            self.ui.scannerSettigns.setMaximumHeight(0)
            self.ui.ota_frame.hide()
            self.ui.ota_frame.setMaximumHeight(0)
            self.ui.elfSettings.setMaximumHeight(1000000)
            self.ui.elfSettings.show()

            
        # PRINT BTN NAME
        #print(f'Button "{btnName}" pressed!')

    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()
        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            pass
            #print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            pass
            #print('Mouse click: RIGHT CLICK')
    def update_variable_in_table(self, var_name, value):
         # Check if the variable name is in the dictionary
        if var_name in self.vars_watched_dict:
            # Get the row index from the dictionary
            row_index = self.vars_watched_dict[var_name]["watched_row_position"]
            # Create a new item with the updated value
            value_item = QTableWidgetItem(str(value))
            # Update the value in column 3 (0-indexed)
            self.ui.tbl_vars_watched.setItem(row_index, 1, value_item)
    def get_core_regs_handler(self, regs):
        # Clear the table
        self.ui.tbl_core_regs.setRowCount(0)
        for reg, value in regs:
            row_position = self.ui.tbl_core_regs.rowCount()
            self.ui.tbl_core_regs.insertRow(row_position)
            self.ui.tbl_core_regs.setItem(row_position, 0, QTableWidgetItem(reg))
            self.ui.tbl_core_regs.setItem(row_position, 1, QTableWidgetItem(hex(value)))
    
    def otas_progress_update(self,value):    
        self.ui.otasProgress.setValue(value)

    #------------------------ clean up fuctions ------------------------
    def clean_up(self):
        try:
            container = self.ui.scrollArea_2.widget()
            layout = container.layout()
            if layout is not None:
                for i in reversed(range(layout.count())):
                    widget_to_remove = layout.itemAt(i).widget()
                    # remove it from the layout list
                    layout.removeWidget(widget_to_remove)
                    # remove it from the gui
                    widget_to_remove.setParent(None)
        except:
            pass

        # Clear the dictionary storing widget references
        self.char_dict.clear()
        # Clear treeview if required
        self.ui.gatt_treeView.clear()

        # Add any other cleanup operations here
    
    def closeEvent(self, event):
        # Kill on going threads
        self.update_rssi_thread.GraphActive = False  # Request the thread to stop
        self.update_rssi_thread.quit()  # Request the thread to stop
        self.update_rssi_thread.wait()  # Wait until the thread has actually stopped

        self.stop_graphing()
        self.stop_scanner()
        self.stop_connection()
        self.stop_elf_parser()
        self.stop_monitoringThread()

        event.accept()  # Accept the close event and let the window close

    def stop_scanner(self):
        self.ui.btn_scan.setText("Scan")
        #self.ui.btn_scan.setStyleSheet("background-color: rgba(33, 37, 43, 180); border: 4px solid rgb(255, 59, 72);border-radius: 5px;")

        self.ui.btn_scan.setStyleSheet(self.btn_stylesheet)

       # self.ui.btn_scan.setStyleSheet("")
        self.bleScanner.is_scanning = False
        self.bleScanner.quit()
        self.bleScanner.wait()
        self.stop_graphing()
    
    def stop_connection(self):
        self.ui.btn_connect.setText("Connect")
        self.ui.btn_disconnect.setText("Disconnect")
        self.ui.btn_connect.setStyleSheet(self.btn_stylesheet)

        self.connectedDevice.is_connected = False
        self.connectedDevice.ble_address = None
        self.connectedDevice.quit()
        self.connectedDevice.wait()
        self.ui.btn_connect.setEnabled(True)
    
    def stop_graphing(self):
        self.update_rssi_thread.GraphActive = False  # Request the thread to stop
        self.update_rssi_thread.quit()  # Request the thread to stop
        self.update_rssi_thread.wait()  # Wait until the thread has actually stopped

    def stop_elf_parser(self):
        self.elf_parser.exit_early = True
        self.elf_parser.quit()
        self.elf_parser.wait()
    
    def stop_monitoringThread(self):
        self.var_watcher.exit_early = True
        if self.var_watcher.monitor_active is True:
            while self.var_watcher.exit_early is True:
                pass
        self.var_watcher.quit()
        self.var_watcher.wait()
    def addToLineChart(self):
        self.ui.qtchart_widgetholder.chart().addAxis(self.axisX, Qt.AlignBottom)
        self.ui.qtchart_widgetholder.chart().addAxis(self.axisY, Qt.AlignLeft)
        self.line_series.attachAxis(self.axisX)
        self.line_series.attachAxis(self.axisY)
        # Create a QTimer instance and connect it to the update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(25)  # Timer triggers every 0.1 seconds (100 milliseconds)



if __name__ == "__main__":
    app = QApplication(sys.argv)
   # app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
