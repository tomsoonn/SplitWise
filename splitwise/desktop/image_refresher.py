import logging
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage

from splitwise.desktop.gui.util import SleepIter
from splitwise.recognise.receipt_scanner import ReceiptScanner

logger = logging.getLogger(__name__)


class ImageRefresher(QObject):
    imageChanged = pyqtSignal(QImage)

    def __init__(self, *args):
        super().__init__(*args)
        self._thread = Thread(target=self._refresh)
        self.receiptScanner = ReceiptScanner()
        self._stop = True
        self.frame = None

    def start(self):
        self.stop()
        self._stop = False
        self._thread.start()

    def stop(self):
        self._stop = True
        if self._thread.isAlive():
            logger.debug("Stopping thread ")
            self._thread.join()

    def _refresh(self):
        try:
            for frame in SleepIter(self.receiptScanner, sleepTime=1 / 30):
                self.frame = frame
                qImg = self.convertOpenCv2QImage(frame)
                self.imageChanged.emit(qImg)

                if self._stop:
                    break

        except IOError:
            logger.error('Stop refreshing image')

    @staticmethod
    def convertOpenCv2QImage(img):
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg
