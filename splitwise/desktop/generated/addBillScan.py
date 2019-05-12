# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/addBillScan.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(487, 451)
        self.verticalLayout = QtWidgets.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageLabel = QtWidgets.QLabel(WizardPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setMinimumSize(QtCore.QSize(300, 300))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setObjectName("imageLabel")
        self.horizontalLayout.addWidget(self.imageLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.recognise = QtWidgets.QPushButton(WizardPage)
        self.recognise.setCheckable(True)
        self.recognise.setChecked(False)
        self.recognise.setObjectName("recognise")
        self.verticalLayout.addWidget(self.recognise)
        self.progressBar = QtWidgets.QProgressBar(WizardPage)
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        _translate = QtCore.QCoreApplication.translate
        WizardPage.setWindowTitle(_translate("WizardPage", "Bill wizard"))
        self.imageLabel.setText(_translate("WizardPage", "+_+_+"))
        self.recognise.setText(_translate("WizardPage", "Recognise"))

