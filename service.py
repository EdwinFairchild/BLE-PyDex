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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_service_widget(object):
    def setupUi(self, service_widget):
        if not service_widget.objectName():
            service_widget.setObjectName(u"service_widget")
        service_widget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(service_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(service_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border: 2px solid rgb(52, 59, 72);\n"
"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.service_label = QLabel(self.frame)
        self.service_label.setObjectName(u"service_label")
        self.service_label.setGeometry(QRect(10, 10, 61, 17))
        self.uuid_label = QLabel(self.frame)
        self.uuid_label.setObjectName(u"uuid_label")
        self.uuid_label.setGeometry(QRect(70, 10, 291, 17))
        self.hello_btn = QPushButton(self.frame)
        self.hello_btn.setObjectName(u"hello_btn")
        self.hello_btn.setGeometry(QRect(20, 40, 89, 25))

        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(service_widget)

        QMetaObject.connectSlotsByName(service_widget)
    # setupUi

    def retranslateUi(self, service_widget):
        service_widget.setWindowTitle(QCoreApplication.translate("service_widget", u"Form", None))
        self.service_label.setText(QCoreApplication.translate("service_widget", u"Service:", None))
        self.uuid_label.setText(QCoreApplication.translate("service_widget", u"TextLabel", None))
        self.hello_btn.setText(QCoreApplication.translate("service_widget", u"PushButton", None))
    # retranslateUi

