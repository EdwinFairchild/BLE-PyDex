# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QProgressBar, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from toggle import AnimatedToggle
from . resources_rc import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1558, 857)
        MainWindow.setMinimumSize(QSize(940, 560))
        MainWindow.setMouseTracking(True)
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(18"
                        "9, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb("
                        "189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border"
                        "-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-sty"
                        "le: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb"
                        "(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-co"
                        "lor: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-c"
                        "olor: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
""
                        "QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     su"
                        "bcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	back"
                        "ground-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subco"
                        "ntrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    h"
                        "eight: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLi"
                        "nkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(200, 0))
        self.leftMenuBg.setMaximumSize(QSize(0, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setMinimumSize(QSize(0, 0))
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMinimumSize(QSize(200, 0))
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, -1, -1, -1)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-bluetooth.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_gatt_explorer = QPushButton(self.topMenu)
        self.btn_gatt_explorer.setObjectName(u"btn_gatt_explorer")
        sizePolicy.setHeightForWidth(self.btn_gatt_explorer.sizePolicy().hasHeightForWidth())
        self.btn_gatt_explorer.setSizePolicy(sizePolicy)
        self.btn_gatt_explorer.setMinimumSize(QSize(0, 45))
        self.btn_gatt_explorer.setFont(font)
        self.btn_gatt_explorer.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_gatt_explorer.setLayoutDirection(Qt.LeftToRight)
        self.btn_gatt_explorer.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-map.png);")

        self.verticalLayout_8.addWidget(self.btn_gatt_explorer)

        self.btn_insights = QPushButton(self.topMenu)
        self.btn_insights.setObjectName(u"btn_insights")
        sizePolicy.setHeightForWidth(self.btn_insights.sizePolicy().hasHeightForWidth())
        self.btn_insights.setSizePolicy(sizePolicy)
        self.btn_insights.setMinimumSize(QSize(0, 45))
        self.btn_insights.setFont(font)
        self.btn_insights.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_insights.setLayoutDirection(Qt.LeftToRight)
        self.btn_insights.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-code.png);")
        icon = QIcon()
        iconThemeName = u"server.png"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.btn_insights.setIcon(icon)

        self.verticalLayout_8.addWidget(self.btn_insights)

        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_widgets")
        sizePolicy.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy)
        self.btn_widgets.setMinimumSize(QSize(0, 45))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-code.png);")
        self.btn_widgets.setIcon(icon)

        self.verticalLayout_8.addWidget(self.btn_widgets)

        self.btn_save = QPushButton(self.topMenu)
        self.btn_save.setObjectName(u"btn_save")
        sizePolicy.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        self.btn_save.setSizePolicy(sizePolicy)
        self.btn_save.setMinimumSize(QSize(0, 45))
        self.btn_save.setFont(font)
        self.btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_save.setLayoutDirection(Qt.LeftToRight)
        self.btn_save.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-save.png)")

        self.verticalLayout_8.addWidget(self.btn_save)

        self.btn_exit = QPushButton(self.topMenu)
        self.btn_exit.setObjectName(u"btn_exit")
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        self.btn_exit.setMinimumSize(QSize(0, 45))
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.verticalLayout_8.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon1)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_share = QPushButton(self.extraTopMenu)
        self.btn_share.setObjectName(u"btn_share")
        sizePolicy.setHeightForWidth(self.btn_share.sizePolicy().hasHeightForWidth())
        self.btn_share.setSizePolicy(sizePolicy)
        self.btn_share.setMinimumSize(QSize(0, 45))
        self.btn_share.setFont(font)
        self.btn_share.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_share.setLayoutDirection(Qt.LeftToRight)
        self.btn_share.setStyleSheet(u"background-image: url(:/icons/images/icons/gitgrey.png);")

        self.verticalLayout_11.addWidget(self.btn_share)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(0, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setMinimumSize(QSize(0, 0))
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon2)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon3)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon4)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon1)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"")
        self.verticalLayout_22 = QVBoxLayout(self.home)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.frame_explorer_top = QFrame(self.home)
        self.frame_explorer_top.setObjectName(u"frame_explorer_top")
        self.frame_explorer_top.setStyleSheet(u"")
        self.frame_explorer_top.setFrameShape(QFrame.StyledPanel)
        self.frame_explorer_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_explorer_top)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.frame_scan_results = QFrame(self.frame_explorer_top)
        self.frame_scan_results.setObjectName(u"frame_scan_results")
        self.frame_scan_results.setStyleSheet(u"")
        self.frame_scan_results.setFrameShape(QFrame.StyledPanel)
        self.frame_scan_results.setFrameShadow(QFrame.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.frame_scan_results)
        self.verticalLayout_24.setSpacing(6)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(-1, 0, -1, 0)
        self.frame_3 = QFrame(self.frame_scan_results)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, -1)
        self.label_scan_filter = QLabel(self.frame_3)
        self.label_scan_filter.setObjectName(u"label_scan_filter")
        self.label_scan_filter.setMinimumSize(QSize(0, 30))
        self.label_scan_filter.setMaximumSize(QSize(16777215, 40))
        self.label_scan_filter.setFont(font)
        self.label_scan_filter.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_scan_filter)

        self.txt_scan_filter = QLineEdit(self.frame_3)
        self.txt_scan_filter.setObjectName(u"txt_scan_filter")
        self.txt_scan_filter.setMinimumSize(QSize(0, 30))
        self.txt_scan_filter.setMaximumSize(QSize(16777215, 35))
        self.txt_scan_filter.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_7.addWidget(self.txt_scan_filter)


        self.verticalLayout_24.addWidget(self.frame_3)

        self.list_widget_discovered = QListWidget(self.frame_scan_results)
        self.list_widget_discovered.setObjectName(u"list_widget_discovered")
        self.list_widget_discovered.setFont(font)
        self.list_widget_discovered.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.list_widget_discovered.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout_24.addWidget(self.list_widget_discovered)

        self.frame_12 = QFrame(self.frame_scan_results)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 0))
        self.frame_12.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 6, 0, -1)
        self.btn_scan = QPushButton(self.frame_12)
        self.btn_scan.setObjectName(u"btn_scan")
        self.btn_scan.setMinimumSize(QSize(0, 30))
        self.btn_scan.setStyleSheet(u"QPushButton{\n"
"\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.horizontalLayout_19.addWidget(self.btn_scan)

        self.btn_connect = QPushButton(self.frame_12)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setMinimumSize(QSize(0, 30))
        self.btn_connect.setStyleSheet(u"QPushButton{\n"
"\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.horizontalLayout_19.addWidget(self.btn_connect)


        self.verticalLayout_24.addWidget(self.frame_12)


        self.horizontalLayout_8.addWidget(self.frame_scan_results)

        self.rssi_gatt_expolrer = QStackedWidget(self.frame_explorer_top)
        self.rssi_gatt_expolrer.setObjectName(u"rssi_gatt_expolrer")
        self.rssi_graph = QWidget()
        self.rssi_graph.setObjectName(u"rssi_graph")
        self.verticalLayout_25 = QVBoxLayout(self.rssi_graph)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(-1, 0, -1, 0)
        self.qtchart_widgetholder = QChartView(self.rssi_graph)
        self.qtchart_widgetholder.setObjectName(u"qtchart_widgetholder")

        self.verticalLayout_25.addWidget(self.qtchart_widgetholder)

        self.rssi_gatt_expolrer.addWidget(self.rssi_graph)
        self.gatt_view = QWidget()
        self.gatt_view.setObjectName(u"gatt_view")
        self.verticalLayout_26 = QVBoxLayout(self.gatt_view)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(-1, 0, -1, -1)
        self.label_2 = QLabel(self.gatt_view)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_26.addWidget(self.label_2)

        self.tree_gatt_view = QTreeWidget(self.gatt_view)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_gatt_view.setHeaderItem(__qtreewidgetitem)
        self.tree_gatt_view.setObjectName(u"tree_gatt_view")

        self.verticalLayout_26.addWidget(self.tree_gatt_view)

        self.rssi_gatt_expolrer.addWidget(self.gatt_view)

        self.horizontalLayout_8.addWidget(self.rssi_gatt_expolrer)

        self.horizontalLayout_8.setStretch(0, 2)
        self.horizontalLayout_8.setStretch(1, 2)

        self.verticalLayout_22.addWidget(self.frame_explorer_top)

        self.frame_adv_data = QFrame(self.home)
        self.frame_adv_data.setObjectName(u"frame_adv_data")
        self.frame_adv_data.setMinimumSize(QSize(0, 60))
        self.frame_adv_data.setFrameShape(QFrame.StyledPanel)
        self.frame_adv_data.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_adv_data)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(-1, 0, -1, 0)
        self.tableWidget_2 = QTableWidget(self.frame_adv_data)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setStyleSheet(u"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
""
                        "{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}")
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setVisible(False)

        self.verticalLayout_21.addWidget(self.tableWidget_2)

        self.verticalLayout_21.setStretch(0, 7)

        self.verticalLayout_22.addWidget(self.frame_adv_data)

        self.verticalLayout_22.setStretch(0, 3)
        self.verticalLayout_22.setStretch(1, 3)
        self.stackedWidget.addWidget(self.home)
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")
        self.verticalLayout = QVBoxLayout(self.widgets)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.row_1 = QFrame(self.widgets)
        self.row_1.setObjectName(u"row_1")
        self.row_1.setFrameShape(QFrame.StyledPanel)
        self.row_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.row_1)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_div_content_1 = QFrame(self.row_1)
        self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_title_wid_1)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        self.labelBoxBlenderInstalation.setFont(font)
        self.labelBoxBlenderInstalation.setStyleSheet(u"")

        self.verticalLayout_18.addWidget(self.labelBoxBlenderInstalation)


        self.verticalLayout_17.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_content_wid_1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.btn_start_voyager = QPushButton(self.frame_content_wid_1)
        self.btn_start_voyager.setObjectName(u"btn_start_voyager")
        self.btn_start_voyager.setMinimumSize(QSize(150, 30))
        self.btn_start_voyager.setFont(font)
        self.btn_start_voyager.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_start_voyager.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/cil-rss.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_start_voyager.setIcon(icon5)

        self.gridLayout.addWidget(self.btn_start_voyager, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.horizontalLayout_9.addLayout(self.gridLayout)


        self.verticalLayout_17.addWidget(self.frame_content_wid_1)


        self.verticalLayout_16.addWidget(self.frame_div_content_1)

        self.frame_4 = QFrame(self.row_1)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.voyagerScrollArea = QScrollArea(self.frame_4)
        self.voyagerScrollArea.setObjectName(u"voyagerScrollArea")
        sizePolicy1.setHeightForWidth(self.voyagerScrollArea.sizePolicy().hasHeightForWidth())
        self.voyagerScrollArea.setSizePolicy(sizePolicy1)
        self.voyagerScrollArea.setStyleSheet(u"\n"
" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.voyagerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.voyagerScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 1268, 461))
        self.voyagerScrollArea.setWidget(self.scrollAreaWidgetContents_4)

        self.horizontalLayout_11.addWidget(self.voyagerScrollArea)


        self.verticalLayout_16.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.row_1)

        self.stackedWidget.addWidget(self.widgets)
        self.insights = QWidget()
        self.insights.setObjectName(u"insights")
        self.horizontalLayout_17 = QHBoxLayout(self.insights)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.frame_8 = QFrame(self.insights)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, -1, 0)
        self.frame_7 = QFrame(self.frame_8)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.frame_7)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.tbl_core_regs = QTableWidget(self.frame_7)
        if (self.tbl_core_regs.columnCount() < 2):
            self.tbl_core_regs.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_core_regs.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_core_regs.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tbl_core_regs.setObjectName(u"tbl_core_regs")
        self.tbl_core_regs.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius:0px;	\n"
"")
        self.tbl_core_regs.horizontalHeader().setVisible(False)
        self.tbl_core_regs.horizontalHeader().setCascadingSectionResizes(True)
        self.tbl_core_regs.horizontalHeader().setMinimumSectionSize(25)
        self.tbl_core_regs.horizontalHeader().setDefaultSectionSize(40)
        self.tbl_core_regs.horizontalHeader().setStretchLastSection(True)
        self.tbl_core_regs.verticalHeader().setVisible(False)

        self.verticalLayout_32.addWidget(self.tbl_core_regs)

        self.btn_refreshCoreRegs = QPushButton(self.frame_7)
        self.btn_refreshCoreRegs.setObjectName(u"btn_refreshCoreRegs")
        self.btn_refreshCoreRegs.setMinimumSize(QSize(0, 41))
        self.btn_refreshCoreRegs.setStyleSheet(u"QPushButton{\n"
"margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_32.addWidget(self.btn_refreshCoreRegs)

        self.btn_hideCoreRegs = QPushButton(self.frame_7)
        self.btn_hideCoreRegs.setObjectName(u"btn_hideCoreRegs")
        self.btn_hideCoreRegs.setMinimumSize(QSize(0, 41))
        self.btn_hideCoreRegs.setStyleSheet(u"QPushButton{\n"
"margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_32.addWidget(self.btn_hideCoreRegs)


        self.horizontalLayout_14.addWidget(self.frame_7)

        self.frame_9 = QFrame(self.frame_8)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_9)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.symbols_frame = QFrame(self.frame_9)
        self.symbols_frame.setObjectName(u"symbols_frame")
        self.symbols_frame.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.symbols_frame.setFrameShape(QFrame.StyledPanel)
        self.symbols_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.symbols_frame)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.tbl_vars = QTableWidget(self.symbols_frame)
        if (self.tbl_vars.columnCount() < 3):
            self.tbl_vars.setColumnCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_vars.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_vars.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_vars.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        self.tbl_vars.setObjectName(u"tbl_vars")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tbl_vars.sizePolicy().hasHeightForWidth())
        self.tbl_vars.setSizePolicy(sizePolicy3)
        palette = QPalette()
        brush = QBrush(QColor(221, 221, 221, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
#endif
        self.tbl_vars.setPalette(palette)
        self.tbl_vars.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.tbl_vars.setFrameShape(QFrame.NoFrame)
        self.tbl_vars.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tbl_vars.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tbl_vars.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_vars.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_vars.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_vars.setShowGrid(True)
        self.tbl_vars.setGridStyle(Qt.SolidLine)
        self.tbl_vars.setSortingEnabled(True)
        self.tbl_vars.horizontalHeader().setVisible(False)
        self.tbl_vars.horizontalHeader().setCascadingSectionResizes(False)
        self.tbl_vars.horizontalHeader().setDefaultSectionSize(120)
        self.tbl_vars.horizontalHeader().setHighlightSections(True)
        self.tbl_vars.horizontalHeader().setProperty("showSortIndicator", True)
        self.tbl_vars.horizontalHeader().setStretchLastSection(False)
        self.tbl_vars.verticalHeader().setVisible(False)
        self.tbl_vars.verticalHeader().setCascadingSectionResizes(False)
        self.tbl_vars.verticalHeader().setHighlightSections(False)
        self.tbl_vars.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_30.addWidget(self.tbl_vars)


        self.verticalLayout_33.addWidget(self.symbols_frame)

        self.watched_frame = QFrame(self.frame_9)
        self.watched_frame.setObjectName(u"watched_frame")
        self.watched_frame.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.watched_frame.setFrameShape(QFrame.StyledPanel)
        self.watched_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.watched_frame)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.tbl_vars_watched = QTableWidget(self.watched_frame)
        if (self.tbl_vars_watched.columnCount() < 5):
            self.tbl_vars_watched.setColumnCount(5)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbl_vars_watched.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tbl_vars_watched.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tbl_vars_watched.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tbl_vars_watched.setHorizontalHeaderItem(3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tbl_vars_watched.setHorizontalHeaderItem(4, __qtablewidgetitem9)
        self.tbl_vars_watched.setObjectName(u"tbl_vars_watched")
        self.tbl_vars_watched.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius:0px;	\n"
"\n"
"")
        self.tbl_vars_watched.setSortingEnabled(False)
        self.tbl_vars_watched.horizontalHeader().setVisible(False)
        self.tbl_vars_watched.horizontalHeader().setCascadingSectionResizes(True)
        self.tbl_vars_watched.horizontalHeader().setDefaultSectionSize(120)
        self.tbl_vars_watched.verticalHeader().setVisible(False)

        self.horizontalLayout_13.addWidget(self.tbl_vars_watched)


        self.verticalLayout_33.addWidget(self.watched_frame)

        self.verticalLayout_33.setStretch(0, 1)
        self.verticalLayout_33.setStretch(1, 1)

        self.horizontalLayout_14.addWidget(self.frame_9)

        self.insights_graphing_frame = QFrame(self.frame_8)
        self.insights_graphing_frame.setObjectName(u"insights_graphing_frame")
        self.insights_graphing_frame.setMinimumSize(QSize(300, 0))
        self.insights_graphing_frame.setFrameShape(QFrame.StyledPanel)
        self.insights_graphing_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.insights_graphing_frame)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.insights_scroll_area = QScrollArea(self.insights_graphing_frame)
        self.insights_scroll_area.setObjectName(u"insights_scroll_area")
        self.insights_scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 558, 571))
        self.insights_scroll_area.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_37.addWidget(self.insights_scroll_area)


        self.horizontalLayout_14.addWidget(self.insights_graphing_frame)

        self.horizontalLayout_14.setStretch(0, 2)
        self.horizontalLayout_14.setStretch(1, 4)
        self.horizontalLayout_14.setStretch(2, 5)

        self.horizontalLayout_17.addWidget(self.frame_8)

        self.stackedWidget.addWidget(self.insights)
        self.connections_page = QWidget()
        self.connections_page.setObjectName(u"connections_page")
        self.verticalLayout_20 = QVBoxLayout(self.connections_page)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.connections_main_frame = QFrame(self.connections_page)
        self.connections_main_frame.setObjectName(u"connections_main_frame")
        self.connections_main_frame.setFrameShape(QFrame.StyledPanel)
        self.connections_main_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.connections_main_frame)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(-1, 0, -1, 0)
        self.frame_10 = QFrame(self.connections_main_frame)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_35 = QVBoxLayout(self.frame_10)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(-1, 0, 0, -1)
        self.gatt_tree_frame = QFrame(self.frame_10)
        self.gatt_tree_frame.setObjectName(u"gatt_tree_frame")
        self.gatt_tree_frame.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.gatt_tree_frame.setFrameShape(QFrame.StyledPanel)
        self.gatt_tree_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.gatt_tree_frame)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.gatt_treeView = QTreeWidget(self.gatt_tree_frame)
        self.gatt_treeView.setObjectName(u"gatt_treeView")
        self.gatt_treeView.setFont(font)
        self.gatt_treeView.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 0px;	\n"
"")
        self.gatt_treeView.header().setVisible(False)

        self.verticalLayout_27.addWidget(self.gatt_treeView)


        self.verticalLayout_35.addWidget(self.gatt_tree_frame)

        self.frame_11 = QFrame(self.frame_10)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.frame_11)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 9, 0, -1)
        self.btn_disconnect = QPushButton(self.frame_11)
        self.btn_disconnect.setObjectName(u"btn_disconnect")
        self.btn_disconnect.setMinimumSize(QSize(0, 50))
        self.btn_disconnect.setStyleSheet(u"QPushButton{\n"
"margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_34.addWidget(self.btn_disconnect)


        self.verticalLayout_35.addWidget(self.frame_11)


        self.horizontalLayout_18.addWidget(self.frame_10)

        self.scroll_Area_2_frame = QFrame(self.connections_main_frame)
        self.scroll_Area_2_frame.setObjectName(u"scroll_Area_2_frame")
        self.scroll_Area_2_frame.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.scroll_Area_2_frame.setFrameShape(QFrame.StyledPanel)
        self.scroll_Area_2_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.scroll_Area_2_frame)
        self.verticalLayout_28.setSpacing(15)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 9)
        self.scrollArea_2 = QScrollArea(self.scroll_Area_2_frame)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        sizePolicy1.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy1)
        self.scrollArea_2.setStyleSheet(u"\n"
" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 792, 584))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_28.addWidget(self.scrollArea_2)


        self.horizontalLayout_18.addWidget(self.scroll_Area_2_frame)

        self.horizontalLayout_18.setStretch(0, 3)
        self.horizontalLayout_18.setStretch(1, 5)

        self.verticalLayout_20.addWidget(self.connections_main_frame)

        self.stackedWidget.addWidget(self.connections_page)

        self.verticalLayout_15.addWidget(self.stackedWidget)

        self.console = QTextEdit(self.pagesContainer)
        self.console.setObjectName(u"console")
        self.console.setMinimumSize(QSize(0, 114))
        self.console.setAutoFillBackground(False)
        self.console.setStyleSheet(u"	background-color: rgba(33, 37, 43, 180);")
        self.console.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_15.addWidget(self.console)

        self.verticalLayout_15.setStretch(0, 10)
        self.verticalLayout_15.setStretch(1, 2)

        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMinimumSize(QSize(0, 0))
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.ota_frame = QFrame(self.contentSettings)
        self.ota_frame.setObjectName(u"ota_frame")
        self.ota_frame.setMaximumSize(QSize(16777215, 0))
        self.ota_frame.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.ota_frame.setFrameShape(QFrame.StyledPanel)
        self.ota_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_36 = QVBoxLayout(self.ota_frame)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.label_6 = QLabel(self.ota_frame)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_36.addWidget(self.label_6)

        self.btn_load_bin = QPushButton(self.ota_frame)
        self.btn_load_bin.setObjectName(u"btn_load_bin")
        self.btn_load_bin.setMinimumSize(QSize(0, 40))
        self.btn_load_bin.setStyleSheet(u"QPushButton{\n"
"margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_36.addWidget(self.btn_load_bin)

        self.btn_start_ota = QPushButton(self.ota_frame)
        self.btn_start_ota.setObjectName(u"btn_start_ota")
        self.btn_start_ota.setMinimumSize(QSize(0, 40))
        self.btn_start_ota.setStyleSheet(u"QPushButton{\n"
"margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_36.addWidget(self.btn_start_ota)

        self.frame_13 = QFrame(self.ota_frame)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.otasProgress = QProgressBar(self.frame_13)
        self.otasProgress.setObjectName(u"otasProgress")
        self.otasProgress.setValue(0)
        self.otasProgress.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_20.addWidget(self.otasProgress)


        self.verticalLayout_36.addWidget(self.frame_13)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_36.addItem(self.verticalSpacer)


        self.verticalLayout_13.addWidget(self.ota_frame)

        self.scannerSettigns = QFrame(self.contentSettings)
        self.scannerSettigns.setObjectName(u"scannerSettigns")
        self.scannerSettigns.setMinimumSize(QSize(0, 0))
        self.scannerSettigns.setMaximumSize(QSize(16777215, 0))
        self.scannerSettigns.setFrameShape(QFrame.NoFrame)
        self.scannerSettigns.setFrameShadow(QFrame.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.scannerSettigns)
        self.verticalLayout_31.setSpacing(6)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.btn_save_logs = QPushButton(self.scannerSettigns)
        self.btn_save_logs.setObjectName(u"btn_save_logs")
        sizePolicy.setHeightForWidth(self.btn_save_logs.sizePolicy().hasHeightForWidth())
        self.btn_save_logs.setSizePolicy(sizePolicy)
        self.btn_save_logs.setMinimumSize(QSize(0, 45))
        self.btn_save_logs.setFont(font)
        self.btn_save_logs.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_save_logs.setLayoutDirection(Qt.LeftToRight)
        self.btn_save_logs.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-save.png);\n"
"")

        self.verticalLayout_31.addWidget(self.btn_save_logs)

        self.btn_clear_logs = QPushButton(self.scannerSettigns)
        self.btn_clear_logs.setObjectName(u"btn_clear_logs")
        sizePolicy.setHeightForWidth(self.btn_clear_logs.sizePolicy().hasHeightForWidth())
        self.btn_clear_logs.setSizePolicy(sizePolicy)
        self.btn_clear_logs.setMinimumSize(QSize(0, 45))
        self.btn_clear_logs.setFont(font)
        self.btn_clear_logs.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_clear_logs.setLayoutDirection(Qt.LeftToRight)
        self.btn_clear_logs.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-remove.png);\n"
"")

        self.verticalLayout_31.addWidget(self.btn_clear_logs)

        self.options_frame = QFrame(self.scannerSettigns)
        self.options_frame.setObjectName(u"options_frame")
        self.options_frame.setMinimumSize(QSize(0, 40))
        self.options_frame.setMaximumSize(QSize(16777215, 45))
        self.options_frame.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;")
        self.options_frame.setFrameShape(QFrame.StyledPanel)
        self.options_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.options_frame)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(20, -1, -1, -1)
        self.check_scroll_to_bottom = QCheckBox(self.options_frame)
        self.check_scroll_to_bottom.setObjectName(u"check_scroll_to_bottom")
        self.check_scroll_to_bottom.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.check_scroll_to_bottom.setChecked(True)

        self.verticalLayout_14.addWidget(self.check_scroll_to_bottom)


        self.verticalLayout_31.addWidget(self.options_frame)

        self.frame_scan = QFrame(self.scannerSettigns)
        self.frame_scan.setObjectName(u"frame_scan")
        self.frame_scan.setEnabled(True)
        self.frame_scan.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;")
        self.frame_scan.setFrameShape(QFrame.StyledPanel)
        self.frame_scan.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_scan)
        self.verticalLayout_23.setSpacing(10)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(-1, 5, -1, 0)
        self.frame_scan_timeout = QFrame(self.frame_scan)
        self.frame_scan_timeout.setObjectName(u"frame_scan_timeout")
        self.frame_scan_timeout.setMinimumSize(QSize(0, 0))
        self.frame_scan_timeout.setMaximumSize(QSize(16777215, 20))
        self.frame_scan_timeout.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;")
        self.frame_scan_timeout.setFrameShape(QFrame.StyledPanel)
        self.frame_scan_timeout.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_scan_timeout)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, 0)
        self.label_scan_timeout = QLabel(self.frame_scan_timeout)
        self.label_scan_timeout.setObjectName(u"label_scan_timeout")
        self.label_scan_timeout.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_6.addWidget(self.label_scan_timeout)

        self.label_scan_timeout_value = QLabel(self.frame_scan_timeout)
        self.label_scan_timeout_value.setObjectName(u"label_scan_timeout_value")
        self.label_scan_timeout_value.setMaximumSize(QSize(16777215, 20))
        self.label_scan_timeout_value.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_scan_timeout_value)


        self.verticalLayout_23.addWidget(self.frame_scan_timeout)

        self.scanSlider = QSlider(self.frame_scan)
        self.scanSlider.setObjectName(u"scanSlider")
        self.scanSlider.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);")
        self.scanSlider.setMaximum(30)
        self.scanSlider.setPageStep(1)
        self.scanSlider.setValue(5)
        self.scanSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_23.addWidget(self.scanSlider)

        self.check_no_timeout = QCheckBox(self.frame_scan)
        self.check_no_timeout.setObjectName(u"check_no_timeout")
        self.check_no_timeout.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);")
        self.check_no_timeout.setChecked(True)

        self.verticalLayout_23.addWidget(self.check_no_timeout)

        self.label_4 = QLabel(self.frame_scan)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 20))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);")

        self.verticalLayout_23.addWidget(self.label_4)

        self.logSelection = QRadioButton(self.frame_scan)
        self.logSelection.setObjectName(u"logSelection")
        self.logSelection.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);")

        self.verticalLayout_23.addWidget(self.logSelection)

        self.logAll = QRadioButton(self.frame_scan)
        self.logAll.setObjectName(u"logAll")
        self.logAll.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);")
        self.logAll.setChecked(True)

        self.verticalLayout_23.addWidget(self.logAll)

        self.logNone = QRadioButton(self.frame_scan)
        self.logNone.setObjectName(u"logNone")
        self.logNone.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);")
        self.logNone.setChecked(False)

        self.verticalLayout_23.addWidget(self.logNone)

        self.frame = QFrame(self.frame_scan)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 50))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.graph_enabled = AnimatedToggle(self.frame)
        self.graph_enabled.setObjectName(u"graph_enabled")
        self.graph_enabled.setMaximumSize(QSize(99999, 999999))
        self.graph_enabled.setChecked(True)

        self.horizontalLayout_10.addWidget(self.graph_enabled)

        self.horizontalLayout_10.setStretch(0, 5)
        self.horizontalLayout_10.setStretch(1, 2)

        self.verticalLayout_23.addWidget(self.frame)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_23.addItem(self.verticalSpacer_2)


        self.verticalLayout_31.addWidget(self.frame_scan)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_3)

        self.verticalLayout_31.setStretch(0, 1)
        self.verticalLayout_31.setStretch(1, 1)
        self.verticalLayout_31.setStretch(2, 1)

        self.verticalLayout_13.addWidget(self.scannerSettigns)

        self.elfSettings = QFrame(self.contentSettings)
        self.elfSettings.setObjectName(u"elfSettings")
        self.elfSettings.setMinimumSize(QSize(0, 0))
        self.elfSettings.setMaximumSize(QSize(16777215, 9999))
        self.elfSettings.setStyleSheet(u"text-align: center;")
        self.elfSettings.setFrameShape(QFrame.NoFrame)
        self.elfSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.elfSettings)
        self.verticalLayout_29.setSpacing(6)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.frame_5 = QFrame(self.elfSettings)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 0px;	\n"
"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"")

        self.horizontalLayout_15.addWidget(self.label)

        self.txtRamStart = QLineEdit(self.frame_5)
        self.txtRamStart.setObjectName(u"txtRamStart")
        self.txtRamStart.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")

        self.horizontalLayout_15.addWidget(self.txtRamStart)


        self.verticalLayout_29.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.elfSettings)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 0px;	\n"
"")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_3 = QLabel(self.frame_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"")

        self.horizontalLayout_16.addWidget(self.label_3)

        self.txtRamEnd = QLineEdit(self.frame_6)
        self.txtRamEnd.setObjectName(u"txtRamEnd")
        self.txtRamEnd.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")

        self.horizontalLayout_16.addWidget(self.txtRamEnd)


        self.verticalLayout_29.addWidget(self.frame_6)

        self.frame_2 = QFrame(self.elfSettings)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 80))
        self.frame_2.setStyleSheet(u" border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_2)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")

        self.verticalLayout_38.addWidget(self.label_7)

        self.horizontalSlider_2 = QSlider(self.frame_2)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"")
        self.horizontalSlider_2.setMaximum(500)
        self.horizontalSlider_2.setValue(200)
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.verticalLayout_38.addWidget(self.horizontalSlider_2)


        self.verticalLayout_29.addWidget(self.frame_2)

        self.btn_load_elf = QPushButton(self.elfSettings)
        self.btn_load_elf.setObjectName(u"btn_load_elf")
        self.btn_load_elf.setMinimumSize(QSize(0, 41))
        self.btn_load_elf.setFocusPolicy(Qt.NoFocus)
        self.btn_load_elf.setStyleSheet(u"\n"
"QPushButton{\n"
"margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" border: 2px solid rgb(52, 59, 72);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"background-color: rgb(153, 193, 241);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_29.addWidget(self.btn_load_elf)

        self.btn_monitor = QPushButton(self.elfSettings)
        self.btn_monitor.setObjectName(u"btn_monitor")
        self.btn_monitor.setMinimumSize(QSize(0, 41))
        self.btn_monitor.setStyleSheet(u"QPushButton{\n"
"	margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" 	border: 2px solid rgb(52, 59, 72);\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 5px;	\n"
"	text-align: center;\n"
"	padding: 0px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"	background-color: rgb(153, 193, 241);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"		color: rgb(28, 28, 28);\n"
"		background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_29.addWidget(self.btn_monitor)

        self.btn_showCoreRegs = QPushButton(self.elfSettings)
        self.btn_showCoreRegs.setObjectName(u"btn_showCoreRegs")
        self.btn_showCoreRegs.setMinimumSize(QSize(0, 41))
        self.btn_showCoreRegs.setStyleSheet(u"QPushButton{\n"
"	margin-left: 10px; \n"
"    margin-right: 10px;\n"
"	background-color: rgb(40, 44, 52);\n"
" 	border: 2px solid rgb(52, 59, 72);\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 5px;	\n"
"	text-align: center;\n"
"	padding: 0px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	color: rgb(28, 28, 28);\n"
"	background-color: rgb(153, 193, 241);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"		color: rgb(28, 28, 28);\n"
"		background-color: rgb(110,140,255);\n"
"}")

        self.verticalLayout_29.addWidget(self.btn_showCoreRegs)

        self.verticalSpacer_4 = QSpacerItem(20, 97, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_4)


        self.verticalLayout_13.addWidget(self.elfSettings)

        self.verticalLayout_13.setStretch(1, 1)
        self.verticalLayout_13.setStretch(2, 1)

        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setBold(False)
        font4.setItalic(False)
        self.creditsLabel.setFont(font4)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)
        self.scanSlider.valueChanged.connect(self.label_scan_timeout_value.setNum)

        self.stackedWidget.setCurrentIndex(1)
        self.rssi_gatt_expolrer.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"BLE-PyDex", None))
        self.titleLeftDescription.setText("")
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Scanner", None))
        self.btn_gatt_explorer.setText(QCoreApplication.translate("MainWindow", u"Gatt Explorer", None))
        self.btn_insights.setText(QCoreApplication.translate("MainWindow", u"Insights", None))
        self.btn_widgets.setText(QCoreApplication.translate("MainWindow", u"voyager4", None))
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"About", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.btn_share.setText(QCoreApplication.translate("MainWindow", u"GitHub Repo", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#99c1f1;\">BLE-PyDex</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A cross-platform graphical tool for exploring Bluetooth Low Energy devices.</p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">MIT License</p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-le"
                        "ft:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#bd93f9;\">Created by: Edwin Amaya</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"Bluetooth Low Energy Scanner , Explorer, Logger and more...", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.label_scan_filter.setText(QCoreApplication.translate("MainWindow", u"Filter scan results:", None))
        self.txt_scan_filter.setText("")
        self.txt_scan_filter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"filter text", None))
        self.btn_scan.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"GATT view:", None))
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"Voyager4-support", None))
        self.btn_start_voyager.setText(QCoreApplication.translate("MainWindow", u" Start", None))
        ___qtablewidgetitem = self.tbl_core_regs.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Reg", None));
        ___qtablewidgetitem1 = self.tbl_core_regs.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.btn_refreshCoreRegs.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.btn_hideCoreRegs.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        ___qtablewidgetitem2 = self.tbl_vars.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Variable", None));
        ___qtablewidgetitem3 = self.tbl_vars.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Address", None));
        ___qtablewidgetitem4 = self.tbl_vars.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Watch", None));
        ___qtablewidgetitem5 = self.tbl_vars_watched.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem6 = self.tbl_vars_watched.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        ___qtreewidgetitem = self.gatt_treeView.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Gatt Tree", None));
        self.btn_disconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"MAX32xxx BLE OTA update", None))
        self.btn_load_bin.setText(QCoreApplication.translate("MainWindow", u"Open binary", None))
        self.btn_start_ota.setText(QCoreApplication.translate("MainWindow", u"Start update", None))
        self.btn_save_logs.setText(QCoreApplication.translate("MainWindow", u"Save  logs", None))
        self.btn_clear_logs.setText(QCoreApplication.translate("MainWindow", u"Clear logs & graph", None))
        self.check_scroll_to_bottom.setText(QCoreApplication.translate("MainWindow", u"Auto scroll table", None))
        self.label_scan_timeout.setText(QCoreApplication.translate("MainWindow", u"Scan timeout (s):", None))
        self.label_scan_timeout_value.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.check_no_timeout.setText(QCoreApplication.translate("MainWindow", u"No timeout", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Advertisement data logging :", None))
        self.logSelection.setText(QCoreApplication.translate("MainWindow", u"Selection", None))
        self.logAll.setText(QCoreApplication.translate("MainWindow", u"Log all data", None))
        self.logNone.setText(QCoreApplication.translate("MainWindow", u"Do not log", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"RSSI graph :", None))
        self.graph_enabled.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Ram Start :", None))
        self.txtRamStart.setText(QCoreApplication.translate("MainWindow", u"0x20000000", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Ram End :", None))
        self.txtRamEnd.setText(QCoreApplication.translate("MainWindow", u"0x2001FFFF ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Max history values:", None))
        self.btn_load_elf.setText(QCoreApplication.translate("MainWindow", u"Load Elf", None))
        self.btn_monitor.setText(QCoreApplication.translate("MainWindow", u"Start Monitoring", None))
        self.btn_showCoreRegs.setText(QCoreApplication.translate("MainWindow", u"Show Core Regs", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: Edwin Amaya", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v2.0.0", None))
    # retranslateUi

