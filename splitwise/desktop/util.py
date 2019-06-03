from dataclasses import dataclass

import requests
from PyQt5.QtWidgets import QMessageBox
from decorator import decorator


@dataclass
class UserData:
    email: str
    name: str
    token: str
    refresh: str


class ResponseException(Exception):
    def __init__(self, msg):
        self.msg = msg


class LoginException(ResponseException):
    pass


@decorator
def exception2MessageBoxFactoryDec(fun, defaultMessage="Connection Error", *args, **kwargs):
    try:
        return fun(*args, **kwargs)
    except requests.exceptions.ConnectionError:
        text = defaultMessage
    except ResponseException as e:
        text = e.msg
    QMessageBox.critical(args[0], 'Error', text)
