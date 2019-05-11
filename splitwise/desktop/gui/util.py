from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QMainWindow
from typing import Type, Union


def savePositionClassDec(cls: Union[Type[QWidget], Type[QMainWindow]]):
    if not issubclass(cls, QWidget):
        raise TypeError

    settings = QSettings('SplitWise', 'SplitWise')
    oldShowEvent = cls.showEvent
    oldCloseEvent = cls.closeEvent
    mw = issubclass(cls, QMainWindow)
    form = f'{cls.__module__}.{cls.__qualname__}/{{}}'

    def newShowEvent(self, *args):
        geom = settings.value(form.format('geometry'))
        if geom:
            self.setGeometry(geom)
        if mw:
            state = settings.value(form.format('state'))
            if state:
                self.restoreState(state)

        oldShowEvent(self, *args)

    def newCloseEvent(self, *args):
        settings.setValue(form.format('geometry'), self.geometry())
        if mw:
            settings.setValue(form.format('state'), self.saveState())
        settings.sync()
        oldCloseEvent(self, *args)

    cls.showEvent = newShowEvent
    cls.closeEvent = newCloseEvent
    return cls
