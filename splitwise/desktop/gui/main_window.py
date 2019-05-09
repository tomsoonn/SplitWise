from PyQt5.QtWidgets import QMainWindow

from splitwise.desktop.generated.mainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
