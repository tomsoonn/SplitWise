# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/addBillManual.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(400, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(WizardPage)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.product = QtWidgets.QLineEdit(WizardPage)
        self.product.setObjectName("product")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.product)
        self.label_2 = QtWidgets.QLabel(WizardPage)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.price = QtWidgets.QDoubleSpinBox(WizardPage)
        self.price.setMinimum(0.0)
        self.price.setMaximum(999.99)
        self.price.setProperty("value", 0.0)
        self.price.setObjectName("price")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.price)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 127, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label.setBuddy(self.product)
        self.label_2.setBuddy(self.price)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        _translate = QtCore.QCoreApplication.translate
        WizardPage.setWindowTitle(_translate("WizardPage", "Bill wizard"))
        self.label.setText(_translate("WizardPage", "P&roduct name"))
        self.label_2.setText(_translate("WizardPage", "&Price"))

