from PyQt5.QtWidgets import QDialog

from splitwise.desktop.generated.addFriend import Ui_Dialog
from splitwise.desktop.gui.util import savePositionClassDec


@savePositionClassDec
class AddFriendDialog(QDialog, Ui_Dialog):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
