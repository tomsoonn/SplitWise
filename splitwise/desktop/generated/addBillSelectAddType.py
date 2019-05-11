# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/addBillSelectAddType.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(400, 200)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(WizardPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.manual = QtWidgets.QRadioButton(WizardPage)
        self.manual.setChecked(True)
        self.manual.setObjectName("manual")
        self.buttonGroup = QtWidgets.QButtonGroup(WizardPage)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.manual)
        self.verticalLayout.addWidget(self.manual)
        self.load = QtWidgets.QRadioButton(WizardPage)
        self.load.setObjectName("load")
        self.buttonGroup.addButton(self.load)
        self.verticalLayout.addWidget(self.load)
        self.scan = QtWidgets.QRadioButton(WizardPage)
        self.scan.setObjectName("scan")
        self.buttonGroup.addButton(self.scan)
        self.verticalLayout.addWidget(self.scan)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 193, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        _translate = QtCore.QCoreApplication.translate
        WizardPage.setWindowTitle(_translate("WizardPage", "Bill wizard"))
        self.manual.setText(_translate("WizardPage", "&Manual insert"))
        self.load.setText(_translate("WizardPage", "&Load scan from file"))
        self.scan.setText(_translate("WizardPage", "&Scan"))

