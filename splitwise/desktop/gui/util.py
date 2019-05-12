import logging
import time
from typing import Type, Union, Iterable

from PyQt5.QtCore import QSettings, QThread, QObject, pyqtSignal, QEventLoop, pyqtSlot, QTime, QTimer
from PyQt5.QtWidgets import QWidget, QMainWindow, QProgressBar, QPushButton
from decorator import decorator

logger = logging.getLogger(__name__)


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


class Worker(QObject):
    start = pyqtSignal()
    end = pyqtSignal()

    def __init__(self, fun, *args, **kwargs):
        super().__init__()
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.result = None

    @pyqtSlot()
    def run(self):
        self.result = self.fun(*self.args, **self.kwargs)
        self.end.emit()


@decorator
def threadExecutionDec(fun, *args, **kwargs):
    loop = QEventLoop()
    thread = QThread()
    thread.start()

    worker = Worker(fun, *args, **kwargs)
    worker.moveToThread(thread)
    worker.start.connect(worker.run)
    worker.end.connect(loop.exit)
    worker.end.connect(thread.exit)

    worker.start.emit()
    loop.exec()
    del thread

    return worker.result


@decorator
def progressBarDecFactory(fun, progressBarName='progressBar', *args, **kwargs):
    progressBar: QProgressBar = getattr(args[0], progressBarName)
    progressBar.setMinimum(0)
    progressBar.setMaximum(0)
    try:
        return fun(*args, **kwargs)
    finally:
        progressBar.setMaximum(1)


@decorator
def singleClickDecFactory(fun, buttonName='button', *args, **kwargs):
    button: QPushButton = getattr(args[0], buttonName)
    button.setEnabled(False)
    try:
        return fun(*args, **kwargs)
    finally:
        button.setChecked(False)
        button.setEnabled(True)


@decorator
def sleepDecFactory(fun, sleepTime=0.5, *args, **kwargs):
    qEventLoop = QEventLoop()
    QTimer.singleShot(int(sleepTime * 1000), qEventLoop.quit)
    qEventLoop.exec()
    return fun(*args, **kwargs)


class SleepIter:
    def __init__(self, iterable: Iterable, sleepTime: float = 1):
        self.iterable = iter(iterable)
        self.sleepTime = sleepTime

    def __iter__(self):
        return self

    def __next__(self):
        time.sleep(self.sleepTime)
        return next(self.iterable)


@decorator
def entryExitDec(fun, *args, **kwargs):
    logger.debug(f"entry function:'{fun.__name__}'")
    try:
        ret = fun(*args, **kwargs)
        logger.debug(f"exit function:'{fun.__name__}'")
        return ret
    except Exception as ex:
        logger.debug(f"exit with exception function:'{fun.__name__}'")
        raise ex


@decorator
def logExcDec(fun, *args, **kwargs):
    try:
        return fun(*args, **kwargs)
    except Exception as ex:
        logger.debug(ex)
        raise ex
