# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\leichui\workspace\rpaclient\ui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(340, 318)
        MainWindow.setBaseSize(QtCore.QSize(100, 197))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(True)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(" background: white;border-radius: 10px;")
        MainWindow.setAnimated(True)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet(" background: white;border-radius: 10px;")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.shutdown = QtWidgets.QPushButton(self.frame)
        self.shutdown.setStyleSheet("min-width: 36px;min-height: 36px;font-family: \"Webdings\";qproperty-text:\"r\";border-radius: 10px;\n"
"\n"
"")
        self.shutdown.setObjectName("shutdown")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.shutdown)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("d:\\leichui\\workspace\\rpaclient\\ui\\../icon/newai08.png"))
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = ScrollLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(117, 93, 151, 80))
        self.label_2.setAcceptDrops(True)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("d:\\leichui\\workspace\\rpaclient\\ui\\../icon/newai09.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label.raise_()
        self.shutdown.raise_()
        self.label_2.raise_()
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.shutdown.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小机器人"))
        MainWindow.setToolTip(_translate("MainWindow", "<html><head/><body><p>小机器人</p></body></html>"))
        self.shutdown.setText(_translate("MainWindow", "r"))
from util.ScrollLabel import ScrollLabel
