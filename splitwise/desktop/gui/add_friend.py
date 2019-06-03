import requests
from PyQt5.QtCore import QStringListModel, QItemSelection, Qt
from PyQt5.QtWidgets import QDialog, QAbstractItemView
from typing import List

from splitwise.desktop.config import SERVER
from splitwise.desktop.generated.addFriend import Ui_Dialog
from splitwise.desktop.gui.util import savePositionClassDec
from splitwise.desktop.util import ResponseException, exception2MessageBoxFactoryDec


@savePositionClassDec
class AddFriendDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, *args):
        super().__init__(parent, *args)
        self.setupUi(self)
        self.friendModel: QStringListModel = parent.friendModel
        self.friendView.setModel(self.friendModel)
        self.friendView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.friendView.setSelectionBehavior(QAbstractItemView.SelectRows)

        users = self._getUsers()
        self.possibleFriendsModel = QStringListModel(users)
        self.possibleFriendsView.setModel(self.possibleFriendsModel)
        self.possibleFriendsView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.possibleFriendsView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.removeButton.clicked.connect(self.onRemove)
        self.addButton.clicked.connect(self.onAdd)

    @exception2MessageBoxFactoryDec()
    def _getUsers(self) -> List[str]:
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.parent().userData.token}'}
        data = {}
        resp = requests.get(SERVER + '/users', json=data, headers=headers)
        if resp.status_code != requests.codes.ok:
            raise ResponseException(resp.json()['message'])

        users = [user['name'] for user in resp.json()['data']]
        return users

    @exception2MessageBoxFactoryDec()
    def onRemove(self):
        selections = self.friendView.selectionModel().selectedRows(0)
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.parent().userData.token}'}
        for sel in selections:
            friendName = self.friendModel.data(sel, Qt.DisplayRole)
            jsonData = {'type': 'REM', 'friendName': friendName,
                        'email': self.parent().userData.email}
            resp = requests.post(SERVER + '/users', json=jsonData, headers=headers)
            if resp.status_code != requests.codes.ok:
                raise ResponseException(resp.json()['message'])

            self.friendModel.removeRow(sel.row())
            stringList = self.possibleFriendsModel.stringList()
            stringList.append(friendName)
            self.possibleFriendsModel.setStringList(stringList)
        self.friendView.selectionModel().clearSelection()

    @exception2MessageBoxFactoryDec()
    def onAdd(self):
        selections = self.possibleFriendsView.selectionModel().selectedRows(0)
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.parent().userData.token}'}
        for sel in selections:
            friendName = self.possibleFriendsModel.data(sel, Qt.DisplayRole)
            jsonData = {'type': 'ADD', 'friendName': friendName,
                        'email': self.parent().userData.email}
            resp = requests.post(SERVER + '/users', json=jsonData, headers=headers)
            if resp.status_code != requests.codes.ok:
                raise ResponseException(resp.json()['message'])

            self.possibleFriendsModel.removeRow(sel.row())
            stringList = self.friendModel.stringList()
            stringList.append(friendName)
            self.friendModel.setStringList(stringList)
        self.possibleFriendsView.selectionModel().clearSelection()
