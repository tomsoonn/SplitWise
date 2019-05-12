# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.addBill = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addBill.sizePolicy().hasHeightForWidth())
        self.addBill.setSizePolicy(sizePolicy)
        self.addBill.setMinimumSize(QtCore.QSize(50, 50))
        self.addBill.setObjectName("addBill")
        self.gridLayout.addWidget(self.addBill, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addFriend = QtWidgets.QPushButton(self.dockWidgetContents)
        self.addFriend.setObjectName("addFriend")
        self.verticalLayout.addWidget(self.addFriend)
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.friendView = QtWidgets.QListView(self.dockWidgetContents)
        self.friendView.setObjectName("friendView")
        self.verticalLayout.addWidget(self.friendView)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reviewBill = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.reviewBill.setObjectName("reviewBill")
        self.verticalLayout_2.addWidget(self.reviewBill)
        self.label = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.billView = QtWidgets.QListWidget(self.dockWidgetContents_2)
        self.billView.setObjectName("billView")
        self.verticalLayout_2.addWidget(self.billView)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addBill.setText(_translate("MainWindow", "Add bill"))
        self.addFriend.setText(_translate("MainWindow", "Add friends"))
        self.label_2.setText(_translate("MainWindow", "Friends:"))
        self.reviewBill.setText(_translate("MainWindow", "Review bills"))
        self.label.setText(_translate("MainWindow", "Last bills:"))

