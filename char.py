# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'char.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

from toggle import AnimatedToggle

class Ui_char_widget(object):
    def setupUi(self, char_widget):
        if not char_widget.objectName():
            char_widget.setObjectName(u"char_widget")
        char_widget.resize(547, 500)
        self.verticalLayout = QVBoxLayout(char_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(char_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border: 2px solid rgb(52, 59, 72);\n"
"border-radius: 5px;\n"
"\n"
"background-color: rgb(45, 49, 57);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.characteristic_name_lbl = QLabel(self.frame_4)
        self.characteristic_name_lbl.setObjectName(u"characteristic_name_lbl")
        self.characteristic_name_lbl.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_5.addWidget(self.characteristic_name_lbl)

        self.uuid_lbl = QLabel(self.frame_4)
        self.uuid_lbl.setObjectName(u"uuid_lbl")
        self.uuid_lbl.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_5.addWidget(self.uuid_lbl)

        self.handle_lbl = QLabel(self.frame_4)
        self.handle_lbl.setObjectName(u"handle_lbl")
        self.handle_lbl.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_5.addWidget(self.handle_lbl)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(200, 50))
        self.frame_2.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.permission_read = QPushButton(self.frame_2)
        self.permission_read.setObjectName(u"permission_read")
        self.permission_read.setStyleSheet(u"background-color: rgb(153, 193, 241);\n"
"padding:5px;\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 12px;	")

        self.horizontalLayout.addWidget(self.permission_read)

        self.permission_write = QPushButton(self.frame_2)
        self.permission_write.setObjectName(u"permission_write")
        self.permission_write.setStyleSheet(u"background-color: rgb(153, 193, 241);\n"
"padding:5px;\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 12px;	")

        self.horizontalLayout.addWidget(self.permission_write)

        self.permission_notify = QPushButton(self.frame_2)
        self.permission_notify.setObjectName(u"permission_notify")
        self.permission_notify.setEnabled(True)
        self.permission_notify.setStyleSheet(u"background-color: rgb(153, 193, 241);\n"
"padding:5px;\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 12px;	")

        self.horizontalLayout.addWidget(self.permission_notify)

        self.permission_indicate = QPushButton(self.frame_2)
        self.permission_indicate.setObjectName(u"permission_indicate")
        self.permission_indicate.setEnabled(True)
        self.permission_indicate.setStyleSheet(u"background-color: rgb(153, 193, 241);\n"
"padding:5px;\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 12px;	")

        self.horizontalLayout.addWidget(self.permission_indicate)

        self.permission_write_wo_resp = QPushButton(self.frame_2)
        self.permission_write_wo_resp.setObjectName(u"permission_write_wo_resp")
        self.permission_write_wo_resp.setStyleSheet(u"background-color: rgb(153, 193, 241);\n"
"padding:5px;\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 12px;	")

        self.horizontalLayout.addWidget(self.permission_write_wo_resp)


        self.verticalLayout_3.addWidget(self.frame_2)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.char_controls_frame = QFrame(self.frame)
        self.char_controls_frame.setObjectName(u"char_controls_frame")
        self.char_controls_frame.setFrameShape(QFrame.StyledPanel)
        self.char_controls_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.char_controls_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_notifications = QFrame(self.char_controls_frame)
        self.frame_notifications.setObjectName(u"frame_notifications")
        self.frame_notifications.setMaximumSize(QSize(16777215, 50))
        self.frame_notifications.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;	\n"
"color: rgb(255, 255, 255);\n"
"")
        self.frame_notifications.setFrameShape(QFrame.StyledPanel)
        self.frame_notifications.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_notifications)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame_notifications)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setStyleSheet(u" border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;	\n"
"text-align: center;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.label)

        self.notify_toggle = AnimatedToggle(self.frame_notifications)
        self.notify_toggle.setObjectName(u"notify_toggle")
        self.notify_toggle.setMaximumSize(QSize(99999, 999999))
        self.notify_toggle.setChecked(False)

        self.horizontalLayout_2.addWidget(self.notify_toggle)

        self.write_no_resp_lbl = QLabel(self.frame_notifications)
        self.write_no_resp_lbl.setObjectName(u"write_no_resp_lbl")

        self.horizontalLayout_2.addWidget(self.write_no_resp_lbl)

        self.write_no_resp_toggle = AnimatedToggle(self.frame_notifications)
        self.write_no_resp_toggle.setObjectName(u"write_no_resp_toggle")
        self.write_no_resp_toggle.setMaximumSize(QSize(99999, 999999))
        self.write_no_resp_toggle.setChecked(False)

        self.horizontalLayout_2.addWidget(self.write_no_resp_toggle)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addWidget(self.frame_notifications)

        self.read_write_frame = QFrame(self.char_controls_frame)
        self.read_write_frame.setObjectName(u"read_write_frame")
        self.read_write_frame.setMaximumSize(QSize(16777215, 50))
        self.read_write_frame.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;\n"
"\n"
"background-color: rgb(45, 49, 57);")
        self.read_write_frame.setFrameShape(QFrame.StyledPanel)
        self.read_write_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.read_write_frame)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 9, 0, -1)
        self.char_write_txt = QTextEdit(self.read_write_frame)
        self.char_write_txt.setObjectName(u"char_write_txt")
        self.char_write_txt.setMaximumSize(QSize(16777215, 999))
        self.char_write_txt.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_4.addWidget(self.char_write_txt)

        self.char_write_btn = QPushButton(self.read_write_frame)
        self.char_write_btn.setObjectName(u"char_write_btn")
        self.char_write_btn.setMinimumSize(QSize(0, 0))
        self.char_write_btn.setMaximumSize(QSize(16777215, 9999))
        self.char_write_btn.setStyleSheet(u"\n"
"\n"
"QPushButton{\n"
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
"		background-color: rgb(140,170,255);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.horizontalLayout_4.addWidget(self.char_write_btn)

        self.char_read_btn = QPushButton(self.read_write_frame)
        self.char_read_btn.setObjectName(u"char_read_btn")
        self.char_read_btn.setMinimumSize(QSize(0, 0))
        self.char_read_btn.setMaximumSize(QSize(16777215, 9999))
        self.char_read_btn.setStyleSheet(u"QPushButton{\n"
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
"		background-color: rgb(140,170,255);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	\n"
"		color: rgb(28, 28, 28);\n"
"	background-color: rgb(110,140,255);\n"
"}")

        self.horizontalLayout_4.addWidget(self.char_read_btn)

        self.horizontalLayout_4.setStretch(0, 4)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 1)

        self.verticalLayout_4.addWidget(self.read_write_frame)

        self.char_read_txt = QTextEdit(self.char_controls_frame)
        self.char_read_txt.setObjectName(u"char_read_txt")
        self.char_read_txt.setMinimumSize(QSize(0, 0))
        self.char_read_txt.setStyleSheet(u"\n"
"background-color: rgb(33, 37, 43);\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_4.addWidget(self.char_read_txt)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addWidget(self.char_controls_frame)

        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 4)

        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(char_widget)

        QMetaObject.connectSlotsByName(char_widget)
    # setupUi

    def retranslateUi(self, char_widget):
        char_widget.setWindowTitle(QCoreApplication.translate("char_widget", u"Form", None))
        self.characteristic_name_lbl.setText(QCoreApplication.translate("char_widget", u"Characteristic : ", None))
        self.uuid_lbl.setText(QCoreApplication.translate("char_widget", u"UUID :", None))
        self.handle_lbl.setText(QCoreApplication.translate("char_widget", u"Handle", None))
        self.permission_read.setText(QCoreApplication.translate("char_widget", u"read", None))
        self.permission_write.setText(QCoreApplication.translate("char_widget", u"write", None))
        self.permission_notify.setText(QCoreApplication.translate("char_widget", u"notify", None))
        self.permission_indicate.setText(QCoreApplication.translate("char_widget", u"indicate", None))
        self.permission_write_wo_resp.setText(QCoreApplication.translate("char_widget", u"write-without-response", None))
        self.label.setText(QCoreApplication.translate("char_widget", u"Notification", None))
        self.notify_toggle.setText(QCoreApplication.translate("char_widget", u"CheckBox", None))
        self.write_no_resp_lbl.setText(QCoreApplication.translate("char_widget", u"Write without response", None))
        self.write_no_resp_toggle.setText(QCoreApplication.translate("char_widget", u"CheckBox", None))
        self.char_write_txt.setMarkdown("")
        self.char_write_txt.setHtml(QCoreApplication.translate("char_widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.char_write_txt.setPlaceholderText(QCoreApplication.translate("char_widget", u"hello char", None))
        self.char_write_btn.setText(QCoreApplication.translate("char_widget", u"write", None))
        self.char_read_btn.setText(QCoreApplication.translate("char_widget", u"read", None))
    # retranslateUi

