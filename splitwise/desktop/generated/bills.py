# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/bills.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(953, 599)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.billView = QtWidgets.QTableView(Dialog)
        self.billView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.billView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.billView.setObjectName("billView")
        self.verticalLayout_2.addWidget(self.billView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.paidButton = QtWidgets.QPushButton(Dialog)
        self.paidButton.setObjectName("paidButton")
        self.horizontalLayout.addWidget(self.paidButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.friendView = QtWidgets.QListView(Dialog)
        self.friendView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.friendView.setObjectName("friendView")
        self.verticalLayout.addWidget(self.friendView)
        self.addFriendButton = QtWidgets.QPushButton(Dialog)
        self.addFriendButton.setObjectName("addFriendButton")
        self.verticalLayout.addWidget(self.addFriendButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Bills"))
        self.paidButton.setText(_translate("Dialog", "Paid"))
        self.addFriendButton.setText(_translate("Dialog", "Add friend to bill"))

