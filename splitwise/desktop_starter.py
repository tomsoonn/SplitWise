import logging
import os
import sys

from splitwise.desktop.gui.main_window import MainWindow
from splitwise.desktop.login_dialog import LoginDialog


def configLogger():
    logging.basicConfig()
    logger = logging.getLogger("splitwise")
    logger.setLevel(logging.DEBUG)


def application():
    os.environ['QT_API'] = 'pyqt5'
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = LoginDialog()
    if dialog.exec():
        mainWindow = MainWindow(dialog.data)
        mainWindow.show()
        app.exec_()


if __name__ == '__main__':
    configLogger()
    application()
