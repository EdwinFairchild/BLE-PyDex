# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'service.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_service_widget(object):
    def setupUi(self, service_widget):
        if not service_widget.objectName():
            service_widget.setObjectName(u"service_widget")
        service_widget.resize(493, 348)
        self.verticalLayout = QVBoxLayout(service_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(service_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border: 1px solid rgb(52, 59, 72);\n"
"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.uuid_label = QLabel(self.frame)
        self.uuid_label.setObjectName(u"uuid_label")

        self.verticalLayout_2.addWidget(self.uuid_label)

        self.service_label = QLabel(self.frame)
        self.service_label.setObjectName(u"service_label")

        self.verticalLayout_2.addWidget(self.service_label)

        self.hello_btn = QPushButton(self.frame)
        self.hello_btn.setObjectName(u"hello_btn")

        self.verticalLayout_2.addWidget(self.hello_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        font = QFont()
        font.setBold(True)
        self.line.setFont(font)
        self.line.setStyleSheet(u"color: rgb(98, 160, 234);\n"
"background-color: rgb(153, 193, 241);")
        self.line.setLineWidth(3)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(service_widget)

        QMetaObject.connectSlotsByName(service_widget)
    # setupUi

    def retranslateUi(self, service_widget):
        service_widget.setWindowTitle(QCoreApplication.translate("service_widget", u"Form", None))
        self.uuid_label.setText(QCoreApplication.translate("service_widget", u"TextLabel", None))
        self.service_label.setText(QCoreApplication.translate("service_widget", u"Service:", None))
        self.hello_btn.setText(QCoreApplication.translate("service_widget", u"PushButton", None))
    # retranslateUi

