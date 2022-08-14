from main_app import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from modules import Console

def init_icons(interface):

    interface.iconDictionary = {interface.ui.btnMenu: ['resources/icons/Menu.svg', 'resources/icons/MenuBlue.svg'],
                            interface.ui.btnMenuGattMaker: ['resources/icons/Ble.svg', 'resources/icons/BleBlue.svg'],
                            interface.ui.btnMenuExplore: ['resources/icons/Discover.svg', 'resources/icons/DiscoverBlue.svg'],
                            interface.ui.btnMenuClient: ['resources/icons/Client.svg', 'resources/icons/ClientBlue.svg']}
    icon_size = QSize()
    # Set Button Icons
    # interface.ui.btnMenu.setIcon(QIcon('resources/icons/Menu.svg'))
    # icon_size.setHeight(20)
    # icon_size.setWidth(20)
    # interface.ui.btnMenu.setIconSize(icon_size)

    interface.ui.btnauthor.setIcon(QIcon('resources/icons/Person.svg'))
    icon_size.setHeight(30)
    icon_size.setWidth(30)
    interface.ui.btnauthor.setIconSize(icon_size)
    interface.ui.btnRepo.setIcon(QIcon('resources/icons/Github.svg'))
    icon_size.setHeight(15)
    icon_size.setWidth(15)
    interface.ui.btnRepo.setIconSize(icon_size)

    interface.ui.btnConnectedState.setIcon(QIcon('resources/icons/Ble_Large.svg'))
    icon_size.setHeight(50)
    icon_size.setWidth(50)
    interface.ui.btnConnectedState.setIconSize(icon_size)

    # misc init stuff
    interface.ui.servicesTreeWidget.setColumnCount(1)
    #side bar animation is currently not being used
    #interface.ui.sideBar.installEventFilter(interface)

    # button list used for changing style sheet
    interface.buttonList = [interface.ui.btnMenu, interface.ui.btnMenuGattMaker,
                        interface.ui.btnMenuClient, interface.ui.btnMenuExplore]

# ------------------------------------------------------------------------
def set_button_icons(interface, currentButton):
    for button in interface.buttonList:
        if button == currentButton:
            icon = interface.iconDictionary[currentButton][1]
            currentButton.setIcon(QIcon(icon))
            icon_size = QSize()
            icon_size.setHeight(20)
            icon_size.setWidth(20)
            currentButton.setIconSize(icon_size)

        elif button == interface.ui.btnMenu:
            pass

        else:
            icon = interface.iconDictionary[button][0]
            button.setIcon(QIcon(icon))
            icon_size = QSize()
            icon_size.setHeight(20)
            icon_size.setWidth(20)
            button.setIconSize(icon_size)
# ------------------------------------------------------------------------
def set_connected_icon_color(interface, color):
    if color == "blue":
        interface.ui.btnConnectedState.setIcon(
            QIcon('resources/icons/Ble_Large_Blue.svg'))
        icon_size = QSize()
        icon_size.setHeight(50)
        icon_size.setWidth(50)
        interface.ui.btnConnectedState.setIconSize(icon_size)
    else:
        interface.ui.btnConnectedState.setIcon(QIcon('resources/icons/Ble_Large.svg'))
        icon_size = QSize()
        icon_size.setHeight(50)
        icon_size.setWidth(50)
        interface.ui.btnConnectedState.setIconSize(icon_size)
# ------------------------------------------------------------------------
def copy_to_clipboard(interface, str):
    cp = QApplication.clipboard()
    cp.clear()
    cp.setText(str)
# ------------------------------------------------------------------------
def set_alternate_button_mode_color(interface, button, fore, back):
    stylesheet = f"QPushButton{{ text-align: center; background-color: rgb({back[0]}, {back[1]}, {back[2]});  ;border-radius:5px;color: rgb({fore[0]}, {fore[1]}, {fore[2]});border:none;}}QPushButton:hover{{color: rgb(255, 255, 255);background-color: rgb(170, 77, 77);}}QPushButton:pressed{{color: rgb(255, 255, 255);background-color: rgb(170, 27, 27);}}"
    button.setStyleSheet(stylesheet)