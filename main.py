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
from PySide6.QtGui import QCursor, QAction, QClipboard
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt 

os.environ["QT_FONT_DPI"] = Settings.HIGH_DPI_DISPLAY_FONT_DPI # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
widgets = None

from service import Ui_service_widget

# TODO :  Move a lot of these functions to their related modules
class MainWindow(QMainWindow):
    add_adv_table_item = Signal(str)
    toplevel = None
    child = None
    vbox = QGridLayout()
    serviceCount= 1
    service_dict = {}
    cleanUp = Signal(object)
    vars_watched_dict={}
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # Graphing variables
        self.device_data_sets = {}
        self.device_data_curves = {}
        self.device_colors = {}
        self.start_time = time.time()
        self.current_time = time.time()
        self.plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        self.ui.widget_rssi_graph.setBackground((40, 44, 52)) 
        self.ui.widget_rssi_graph.getPlotItem().getAxis('bottom').setStyle(showValues=False)
        
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
        self.update_thread = UpdateRSSIGraphThread(self)
        self.update_thread.dataUpdated.connect(self.update_graph)
        if self.ui.graph_enabled.isChecked():
            self.update_thread.GraphActive = True
            self.update_thread.start()


        # Generate some log messages for testing
        # console.debug('Debug message.')
        # console.info('Info message.')
        # console.warning('Warning message.')
        # console.error('Error message.')

        # Global BLE objects
        self.bleScanner = ble_functions.BLE_DiscoverDevices()

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = False

        # APP NAME
        title = "BLE-PyDex"
        description = "Bluetooth Low Energy Scanner , Explorer, Logger and more..."
        # APPLY TEXTS
        self.setWindowTitle(title)
        self.ui.titleRightInfo.setText(description)

        # TOGGLE MENU
        self.ui.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        UIFunctions.toggleMenu(self, True)

        # SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = self.ui.tableWidget_2.verticalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # UI MENU BASIC BUTTONS CLICK

        # LEFT MENUS
        self.ui.btn_home.clicked.connect(self.buttonClick)
        self.ui.btn_widgets.clicked.connect(self.buttonClick)
        self.ui.btn_new.clicked.connect(self.buttonClick)
        self.ui.btn_save.clicked.connect(self.buttonClick)
        self.ui.btn_insights.clicked.connect(self.buttonClick)

        # Register signal handlers
        self.add_adv_table_item.connect(lambda data :self.add_table_item(data))
        self.connectedDevice.discovered_services.connect(self.discovered_services)

        # Register none-UI button callbacks
        btn_callbacks.register_button_callbacks(self)
        
        #self.ui.tableWidget_2.reset()

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
        self.cleanUp.connect(lambda: self.clean_up(widgets))

        
        
        self.ui.scrollArea_2.setLayout(self.vbox)
        self.ui.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollArea_2.setStyleSheet("""
    QScrollArea {
        background: transparent;
    }
    QScrollBar:vertical {
        width: 15px;
        ;
    }
    QScrollBar::handle:vertical {
        background: #999999;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical {
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        height: 0 px;
        subcontrol-position: top;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        width: 0px;
        height: 0px;
        ;
    }
""")


        # SHOW APP
        self.show()

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

    def update_graph(self,device_name,rssi_value,current_time):
        # TODO : possibly make this a slider for the user to configure
        MAX_DEVICES = 100
        # Initialize start time and max duration
        if "start_time" not in self.__dict__:
            self.start_time = current_time
        max_duration = 10  # Maximum duration to display (in seconds)

        # Calculate time delta and check if data should scroll
        time_delta = current_time - self.start_time
        if time_delta > max_duration:
            # Calculate the new start time
            self.start_time = current_time - max_duration

            # Update the x-axis range to enable scrolling
            self.ui.widget_rssi_graph.setXRange(self.start_time, current_time)

        if device_name in self.device_data_curves:
            # Get the device's curve and data
            device_curve = self.device_data_curves[device_name]
            device_data_x, device_data_y = device_curve.getData()

            # Append the new RSSI value and time to the existing data.
            device_data_x = np.append(device_data_x, current_time)
            device_data_y = np.append(device_data_y, rssi_value)

            # Update the curve with the new data.
            device_curve.setData(device_data_x, device_data_y)

        else:
             # Check if maximum number of devices has been reached
            if len(self.device_data_curves) >= MAX_DEVICES:
                # Here you can decide what to do if max is reached,
                # you can drop the oldest device or ignore the new one
                return
            # The device is not in the dictionary
            # Generate a random color for the device
            device_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # Create a new PlotCurveItem for the device
            device_curve = pg.PlotCurveItem(pen=pg.mkPen(color=device_color, width=1))

            # Set the curve's data
            device_curve.setData(np.array([current_time]), np.array([rssi_value]))

            # Add the curve to the graph and the dictionary
            self.ui.widget_rssi_graph.addItem(device_curve)
            self.device_data_curves[device_name] = device_curve
   
    def stop_rssi_thread(self):
            # the RSSI thread
        if self.update_thread.GraphActive == True:    
            self.update_thread.GraphActive = False  # Request the thread to stop
            self.update_thread.quit()  # Request the thread to stop
            self.update_thread.wait()  # Wait until the thread has actually stopped
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
                print(e)
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
        #print(data)
    
    def discovered_services(self,data):
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
            is a level indicator for the tree widget
            0 = service 
            1 = characteristic
            2 = descriptor
        '''    
        level = data[1]
        if level == 0:
            # data[0] looks like this: 00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile 
            # extract the UUID from the string which is this: 00001801-0000-1000-8000-00805f9b34fb

            # check if UUID exist in ble numbers
            svc_uuid = self.extract_uuid_name(item)
            self.logger.info("Adding service widget for UUID: " + str(svc_uuid))
            self.add_service_widget(str(svc_uuid))
            self.toplevel = QTreeWidgetItem([str(svc_uuid)])
            # Set the icon for the top-level item.
            icon = QIcon()
            icon.addPixmap(QPixmap("char_s.png"), QIcon.Normal, QIcon.On)
            self.toplevel.setIcon(0, icon)
            self.ui.gatt_treeView.addTopLevelItem(self.toplevel)
        elif level == 1 and self.toplevel != None:
             # check if UUID exist in ble numbers
            svc_uuid = self.extract_uuid_name(item)
            self.child = QTreeWidgetItem([str(svc_uuid)])
            # Set the icon for the top-level item.
            icon = QIcon()
            icon.addPixmap(QPixmap("char_c.png"), QIcon.Normal, QIcon.On)
            self.child.setIcon(0, icon)
            self.toplevel.addChild(self.child)
           
           
        elif level == 2 and self.child != None:
             # check if UUID exist in ble numbers
            svc_uuid = self.extract_uuid_name(item)
            self.subchild = QTreeWidgetItem([str(svc_uuid)])
            # Set the icon for the top-level item.
            icon = QIcon()
            icon.addPixmap(QPixmap("char_d.png"), QIcon.Normal, QIcon.On)
            self.subchild.setIcon(0, icon)
            self.child.addChild(self.subchild)
    
    def extract_uuid_name(self, data):
        # data[0] looks like this: 00001801-0000-1000-8000-00805f9b34fb (Handle: 16): Generic Attribute Profile 
        # extract the UUID from the string which is this: 00001801-0000-1000-8000-00805f9b34fb
        svc_uuid = data.split(":")[1].split("(")[0].strip()
        found_match = False
        # check if UUID exist in ble numbers
        for uuid_type in [ble_uuid.service, ble_uuid.characteristic, ble_uuid.descriptor]:
            try:
                svc_uuid = uuid_type[UUID(svc_uuid)]
                # replace the UUID with the name in item
                data = data.replace(data.split(":")[1].split("(")[0].strip(), svc_uuid)
                found_match = True
            except:
                pass
        if found_match == False:
            # TODO check if UUID exist in user_uuids.json

            pass

        return data
            
    def add_service_widget(self, svc_uuid):
                # Add widget to Main Scroll Area
        scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        widget = QWidget()           # Widget that contains the collection of Vertical Box

        tempWidget = QtWidgets.QWidget()
        uiwidget = Ui_service_widget()
        tempWidget.setMinimumHeight(400)
        uiwidget.setupUi(tempWidget)
        uiwidget.hello_btn.clicked.connect(lambda state : self.service_btn_click(svc_uuid))
        uiwidget.uuid_label.setText(str(svc_uuid))
        widget.setLayout(self.vbox)
        # widget.setStyleSheet("""
        
        #  border: 2px solid rgb(52, 59, 72);
	    #     border-radius: 5px;	""")

        # add to vertical layout row,column
        self.vbox.addWidget(tempWidget,self.serviceCount,0)
        self.vbox.setContentsMargins(QMargins(20, 0, 0, 0))
        self.serviceCount += 1

        
        self.ui.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollArea_2.setWidget(widget)

        # Storing widgets in dictionary for future reference
        self.service_dict[UUID] = uiwidget 
        #print(f"Widget {uiwidget} added to service_dict with key {UUID}")

        #  store reference to widget in service_dict so we can access it later, use UUID as key
    def stacked_widget_show_connected(self):
        # change stacked widget to connections page
        self.ui.btn_new.click()
        
    def service_btn_click(self, UUID):
        self.logger.info(f"My UUID is {UUID}")

    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            self.ui.stackedWidget.setCurrentWidget(self.ui.connections_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            pass
        
        if btnName == "btn_insights":
            self.ui.stackedWidget.setCurrentWidget(self.ui.insights)
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

            #print("Save BTN clicked!")
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
    
    def clean_up(self, widgets):
        # Clear the scroll area
        # Clear the scroll area
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
        self.service_dict.clear()

        # Clear treeview if required
        self.ui.gatt_treeView.clear()

        # Add any other cleanup operations here
    
    def closeEvent(self, event):
        # Kill on going threads
        self.update_thread.GraphActive = False  # Request the thread to stop
        self.update_thread.quit()  # Request the thread to stop
        self.update_thread.wait()  # Wait until the thread has actually stopped

        self.stop_graphing()
        self.stop_scanner()
        self.stop_connection()

        event.accept()  # Accept the close event and let the window close

    def stop_scanner(self):
        self.ui.btn_scan.setText("Scan")
        self.ui.btn_scan.setStyleSheet("")
        self.bleScanner.is_scanning = False
        self.bleScanner.quit()
        self.bleScanner.wait()
    
    def stop_connection(self):
        self.ui.btn_connect.setText("Connect")
        self.ui.btn_disconnect.setText("Disconnect")
        self.ui.btn_connect.setStyleSheet("")
        self.connectedDevice.is_connected = False
        self.connectedDevice.ble_address = None
        self.connectedDevice.quit()
        self.connectedDevice.wait()
        self.ui.btn_connect.setEnabled(True)
    
    def stop_graphing(self):
        self.update_thread.GraphActive = False  # Request the thread to stop
        self.update_thread.quit()  # Request the thread to stop
        self.update_thread.wait()  # Wait until the thread has actually stopped

if __name__ == "__main__":
    app = QApplication(sys.argv)
   # app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
