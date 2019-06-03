import requests
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMainWindow
from typing import List

from splitwise.desktop.bill_model import BillModel, BillData
from splitwise.desktop.config import SERVER
from splitwise.desktop.generated.mainWindow import Ui_MainWindow
from splitwise.desktop.gui.add_friend import AddFriendDialog
from splitwise.desktop.gui.bill_wizard import BillWizard, Summary
from splitwise.desktop.gui.util import savePositionClassDec
from splitwise.desktop.util import UserData, exception2MessageBoxFactoryDec, ResponseException


@savePositionClassDec
class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, userData: UserData, *args):
        super().__init__(*args)
        self.userData = userData
        self.setupUi(self)
        self.addBill.clicked.connect(self.onAddBill)
        self.addFriend.clicked.connect(self.onAddFriend)
        self.refreshButton.clicked.connect(self.reloadBills)

        friendList = self._getFriends()
        self.friendModel = QStringListModel(friendList)
        self.friendView.setModel(self.friendModel)

        self.billModel = BillModel()
        self.billView.setModel(self.billModel)
        self.reloadBills()

    @exception2MessageBoxFactoryDec()
    def reloadBills(self):
        params = {'email': self.userData.email}
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.userData.token}'}
        response = requests.get(SERVER + '/bills', params=params, headers=headers)
        if response.status_code != requests.codes.ok:
            raise ResponseException(response.json()['message'])

        try:
            data = []
            for bill in response.json()['data']:
                data.append(BillData(**bill))
        except (TypeError, KeyError) as error:
            raise ResponseException(f"Invalid values: {error}")
        else:
            self.billModel.setNewData(data)

    @exception2MessageBoxFactoryDec()
    def onAddBill(self):
        wizard = BillWizard(self)
        if wizard.exec():
            summaryPage: Summary = wizard.page(wizard.PAGE_ID[Summary])
            text = summaryPage.textBrowser.toPlainText()
            product, price = text.split('=', maxsplit=1)

            data = {'title': product, 'price': float(price), 'participants': []}
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'Bearer {self.userData.token}'}
            resp = requests.post(SERVER + '/bills', json=data, headers=headers)
            if resp.status_code != requests.codes.ok:
                raise ResponseException(resp.json()['message'])
            self.reloadBills()

    @exception2MessageBoxFactoryDec()
    def _getFriends(self) -> List[str]:
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.userData.token}'}
        data = {'email': self.userData.email}
        resp = requests.get(SERVER + '/users', json=data, headers=headers)
        if resp.status_code != requests.codes.ok:
            raise ResponseException(resp.json()['message'])

        users = [user['name'] for user in resp.json()['data']]
        return users

    def onAddFriend(self):
        afd = AddFriendDialog(self)
        afd.show()
