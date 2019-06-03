import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from splitwise.desktop.bill_model import BillData
from splitwise.desktop.config import SERVER
from splitwise.desktop.generated.bills import Ui_Dialog
from splitwise.desktop.util import exception2MessageBoxFactoryDec, ResponseException


class BillDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, *args):
        super().__init__(parent, *args)
        self.setupUi(self)
        self.billView.setModel(parent.billModel)
        self.billView.hideColumn(0)
        self.billView.hideColumn(1)
        self.friendView.setModel(parent.friendModel)
        self.addFriendButton.clicked.connect(self.onAddFriend)

    @exception2MessageBoxFactoryDec()
    def onAddFriend(self):
        billSelections = self.billView.selectionModel().selectedRows(0)
        friendSelections = self.friendView.selectionModel().selectedRows(0)
        if billSelections and friendSelections:
            billSel = billSelections[0]
            friendSel = friendSelections[0]

            newUser = self.friendView.model().data(friendSel, Qt.DisplayRole)
            mod = self.billView.model()
            billData: BillData = mod.data(billSel, Qt.UserRole)

            amount = billData.price / (len(billData.participants) if billData.participants else 1)
            data = {'amount': amount,
                    'due_from': billData.email,
                    'bill_id': billData.id_,
                    'product': billData.title,
                    'paid': False}

            headers = {'Content-Type': 'application/json',
                       'Authorization': f'Bearer {self.parent().userData.token}'}

            billData.participants.append(newUser)
            data['due_to'] = newUser
            resp = requests.post(SERVER + '/dues', json=data, headers=headers)
            if resp.status_code != requests.codes.ok:
                raise ResponseException(resp.json()['message'])

            self.billView.model().modelReset.emit()
            self.billView.resizeColumnsToContents()
