from typing import Optional

import requests
from PyQt5.QtWidgets import QDialog, QLineEdit

from splitwise.desktop.config import SERVER
from splitwise.desktop.generated.login import Ui_LoginDialog
from splitwise.desktop.util import UserData, exception2MessageBoxFactoryDec, LoginException


class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.nickWidget.hide()

        self.registerRadioButton.clicked.connect(lambda: self.nickWidget.show())
        self.loginRadioButton.clicked.connect(lambda: self.nickWidget.hide())
        self.loginButton.clicked.connect(self.onLogin)
        self.passwordShowButton.pressed.connect(lambda: self.passwordLine.setEchoMode(QLineEdit.Normal))
        self.passwordShowButton.released.connect(lambda: self.passwordLine.setEchoMode(QLineEdit.Password))

        self.data: Optional[UserData] = None
        self.emialLine.setText("ala@ma.kota")  # TODO remove
        self.passwordLine.setText("12345")  # TODO remove

    @exception2MessageBoxFactoryDec()
    def onLogin(self):
        if self.registerRadioButton.isChecked():
            self._register()
        self._login()

    def _register(self):
        data = {"email": self.emialLine.text(),
                "password": self.passwordLine.text(),
                "name": self.nickLine.text()}
        resp = requests.post(SERVER + '/register', json=data)
        if resp.status_code != requests.codes.ok:
            raise LoginException(msg=resp.json()['message'])

    def _login(self):
        data = {"email": self.emialLine.text(),
                "password": self.passwordLine.text()}
        resp = requests.post(SERVER + '/login', json=data)
        if resp.status_code != requests.codes.ok:
            raise LoginException(msg=resp.json()['message'])

        rData = resp.json()['data']
        self.data = UserData(
            email=rData['email'],
            name=rData['name'],
            token=rData['token'],
            refresh=rData['refresh'])
        self.accept()
