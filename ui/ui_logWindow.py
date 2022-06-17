# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QPlainTextEdit, QSizePolicy, QWidget)

class Ui_logWindow(object):
    def setupUi(self, logWindow):
        if not logWindow.objectName():
            logWindow.setObjectName(u"logWindow")
        logWindow.resize(500, 400)
        logWindow.setMinimumSize(QSize(500, 400))
        logWindow.setMaximumSize(QSize(500, 400))
        logWindow.setStyleSheet(u"#logWindow\n"
" {	\n"
"	background-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"")
        self.logText = QPlainTextEdit(logWindow)
        self.logText.setObjectName(u"logText")
        self.logText.setGeometry(QRect(10, 10, 481, 381))
        self.logText.setStyleSheet(u"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"	color:white;\n"
"	font-size:14px;\n"
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
"	border: 2px solid rgb(91, 101, 100);\n"
"}\n"
"\n"
"")
        self.logText.setReadOnly(True)

        self.retranslateUi(logWindow)

        QMetaObject.connectSlotsByName(logWindow)
    # setupUi

    def retranslateUi(self, logWindow):
        logWindow.setWindowTitle(QCoreApplication.translate("logWindow", u"\u53cd\u9988", None))
        self.logText.setPlainText("")
    # retranslateUi

