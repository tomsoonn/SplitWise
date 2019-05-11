from PyQt5.QtWidgets import QMainWindow

from splitwise.desktop.generated.mainWindow import Ui_MainWindow
from splitwise.desktop.gui.add_friend import AddFriendDialog
from splitwise.desktop.gui.bill_wizard import BillWizard
from splitwise.desktop.gui.util import savePositionClassDec


@savePositionClassDec
class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.addBill.clicked.connect(self.onAddBill)
        self.addFriend.clicked.connect(self.onAddFriend)

    def onAddBill(self):
        wizard = BillWizard(self)
        wizard.exec()

    def onAddFriend(self):
        afd = AddFriendDialog(self)
        afd.show()
