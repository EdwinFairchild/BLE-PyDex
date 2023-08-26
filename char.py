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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

from toggle import AnimatedToggle

class Ui_char_widget(object):
    def setupUi(self, char_widget):
        if not char_widget.objectName():
            char_widget.setObjectName(u"char_widget")
        char_widget.resize(519, 343)
        self.verticalLayout = QVBoxLayout(char_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(char_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border: 1px solid rgb(52, 59, 72);\n"
"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.uuid_label = QLabel(self.frame_4)
        self.uuid_label.setObjectName(u"uuid_label")
        self.uuid_label.setGeometry(QRect(10, 30, 471, 17))
        self.uuid_label.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;")
        self.service_label = QLabel(self.frame_4)
        self.service_label.setObjectName(u"service_label")
        self.service_label.setGeometry(QRect(10, 10, 461, 17))
        self.service_label.setStyleSheet(u"border: 0px solid rgb(52, 59, 72);\n"
"border-radius: 5px;")

        self.verticalLayout_2.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(200, 40))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.frame_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"background-color: rgb(153, 193, 241);")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"background-color: rgb(143, 240, 164);")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setStyleSheet(u"background-color: rgb(246, 97, 81);")

        self.horizontalLayout.addWidget(self.pushButton_3)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.hello_btn = QPushButton(self.frame_5)
        self.hello_btn.setObjectName(u"hello_btn")
        self.hello_btn.setGeometry(QRect(360, 20, 83, 19))
        self.graph_enabled = AnimatedToggle(self.frame_5)
        self.graph_enabled.setObjectName(u"graph_enabled")
        self.graph_enabled.setGeometry(QRect(10, 10, 101, 32))
        self.graph_enabled.setMaximumSize(QSize(99999, 999999))
        self.graph_enabled.setChecked(True)
        self.lineEdit = QLineEdit(self.frame_5)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(140, 10, 201, 41))

        self.verticalLayout_2.addWidget(self.frame_5)

        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setStyleSheet(u"border: 2px solid rgb(52, 59, 72);\n"
"border-radius: 5px;	\n"
"background-color: rgba(33, 37, 43, 180);")

        self.verticalLayout_2.addWidget(self.textEdit)

        self.verticalLayout_2.setStretch(0, 3)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 4)
        self.verticalLayout_2.setStretch(3, 3)

        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(char_widget)

        QMetaObject.connectSlotsByName(char_widget)
    # setupUi

    def retranslateUi(self, char_widget):
        char_widget.setWindowTitle(QCoreApplication.translate("char_widget", u"Form", None))
        self.uuid_label.setText(QCoreApplication.translate("char_widget", u"UUID :", None))
        self.service_label.setText(QCoreApplication.translate("char_widget", u"Characteristic : ", None))
        self.pushButton.setText(QCoreApplication.translate("char_widget", u"read", None))
        self.pushButton_2.setText(QCoreApplication.translate("char_widget", u"write", None))
        self.pushButton_3.setText(QCoreApplication.translate("char_widget", u"notify", None))
        self.hello_btn.setText(QCoreApplication.translate("char_widget", u"PushButton", None))
        self.graph_enabled.setText(QCoreApplication.translate("char_widget", u"CheckBox", None))
    # retranslateUi

