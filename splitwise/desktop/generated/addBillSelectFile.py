# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/addBillSelectFile.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(400, 199)
        self.verticalLayout = QtWidgets.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(WizardPage)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.selectedFileLabel = QtWidgets.QLineEdit(WizardPage)
        self.selectedFileLabel.setObjectName("selectedFileLabel")
        self.horizontalLayout.addWidget(self.selectedFileLabel)
        self.toolButton = QtWidgets.QToolButton(WizardPage)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 143, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        _translate = QtCore.QCoreApplication.translate
        WizardPage.setWindowTitle(_translate("WizardPage", "Bill wizard"))
        self.label.setText(_translate("WizardPage", "File:"))
        self.toolButton.setText(_translate("WizardPage", "&Select File"))

