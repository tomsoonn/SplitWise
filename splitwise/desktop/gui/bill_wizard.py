import cv2
import logging

# noinspection PyUnresolvedReferences
from PyQt5.QtCore import pyqtSignal, pyqtProperty, QObject, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import QWizardPage, QWizard, QFileDialog

from splitwise.desktop.generated import addBillSelectAddType, addBillManual, addBillSelectFile, addBillScan, \
    addBillSummary
from splitwise.desktop.gui.util import progressBarDecFactory, threadExecutionDec, entryExitDec, \
    sleepDecFactory, singleClickDecFactory, logExcDec
from splitwise.desktop.image_refresher import ImageRefresher
from splitwise.recognise.receipt_scanner import ReceiptScanner

logger = logging.getLogger(__name__)


class BasePage(QWizardPage):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

    def nextId(self):
        return BillWizard.PAGE_ID[Summary]


class SelectAddType(BasePage, addBillSelectAddType.Ui_WizardPage):

    def __init__(self, *args):
        super().__init__(*args)
        self.selected = BasePage

    def nextId(self):
        nextMap = {
            self.load: SelectFile,
            self.manual: Manual,
            self.scan: Scan,
        }
        for button, page in nextMap.items():
            if button.isChecked():
                self.selected = page
                return BillWizard.PAGE_ID[page]
        assert False


class Manual(BasePage, addBillManual.Ui_WizardPage):
    def __init__(self, *args):
        super().__init__(*args)
        self.registerField('product*', self.product)
        self.registerField('price*', self.price, 'value', self.price.valueChanged)


class SelectFile(BasePage, addBillSelectFile.Ui_WizardPage):
    def __init__(self, *args):
        super().__init__(*args)
        self.toolButton.clicked.connect(self.selectFile)
        self.registerField('filePath*', self.selectedFileLabel)

    def selectFile(self):
        filename, _filter = QFileDialog.getOpenFileName(self, 'Select file', filter="Images (*.jpg *.png)")
        if filename:
            self.selectedFileLabel.setText(filename)

    def nextId(self):
        return BillWizard.PAGE_ID[ScanFile]


class BaseScan(BasePage, addBillScan.Ui_WizardPage):
    def __init__(self, *args):
        super().__init__(*args)
        self.result = ''
        self.recognise.clicked.connect(self.onRecognise)
        self._setButtonBackground(Qt.red)

    def _setButtonBackground(self, color=Qt.green):
        pal = self.recognise.palette()
        pal.setColor(QPalette.Button, QColor(color))
        self.recognise.setPalette(pal)
        self.recognise.repaint()

    def displayImage(self, image: QImage):
        w = self.imageLabel.width()
        h = self.imageLabel.height()
        image = image.scaledToWidth(w) if w < h else image.scaledToHeight(h)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

    def onRecognise(self):
        raise NotImplementedError

    def isComplete(self):
        return self.result != ''


class ScanFile(BaseScan):
    def __init__(self, *args):
        super().__init__(*args)
        self.filePath = None

    @logExcDec
    def initializePage(self):
        self.filePath = self.field('filePath')
        self.displayImage()
        QTimer.singleShot(100, lambda: self.recognise.click())

    @logExcDec
    def displayImage(self, **kwargs):
        img = cv2.imread(self.filePath)
        qImg = ImageRefresher.convertOpenCv2QImage(img)
        super().displayImage(qImg)

    @singleClickDecFactory(buttonName='recognise')
    @progressBarDecFactory()
    @sleepDecFactory(sleepTime=1.5)
    @threadExecutionDec
    def onRecognise(self):
        img = cv2.imread(self.filePath)
        self.result = ReceiptScanner.scanReceipt(img)
        self.completeChanged.emit()
        self._setButtonBackground(Qt.green)


class Scan(BaseScan):
    selectedChanged = pyqtSignal(int)

    def __init__(self, *args):
        super().__init__(*args)
        self.imageRefresher = ImageRefresher(self)
        self.imageRefresher.imageChanged.connect(self.displayImage)

    @logExcDec
    def initializePage(self):
        self.imageRefresher.start()

    @logExcDec
    def cleanupPage(self):
        self.imageRefresher.stop()

    @entryExitDec
    @singleClickDecFactory(buttonName='recognise')
    @progressBarDecFactory()
    @sleepDecFactory(sleepTime=1.5)
    @threadExecutionDec
    def onRecognise(self):
        frame = self.imageRefresher.frame
        if frame is not None:
            self.result = ReceiptScanner.scanReceipt(frame)
            self.completeChanged.emit()
            self._setButtonBackground(Qt.green)


class Summary(BasePage, addBillSummary.Ui_WizardPage):

    def initializePage(self):
        wizard = self.wizard()
        scanPage: Scan = wizard.page(BillWizard.PAGE_ID[Scan])
        selected = wizard.page(BillWizard.PAGE_ID[SelectAddType]).selected
        if selected == Manual:
            product = self.field('product')
            price = self.field('price')
            text = f"{product}={price}"

        elif selected == SelectFile:
            scanFilePage: ScanFile = wizard.page(BillWizard.PAGE_ID[ScanFile])
            text = f"total price: {scanFilePage.result}"

        elif selected == Scan:
            text = f"total price: {scanPage.result}"

        else:
            assert False

        self.textBrowser.setText(text)

        scanPage.imageRefresher.stop()

    def nextId(self):
        return -1


class BillWizard(QWizard):
    pyqtSignal()
    PAGE_ID = {
        p: i for i, p in enumerate((SelectAddType, Manual, SelectFile, ScanFile, Scan, Summary))
    }

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle('Bill Wizard')
        self.setOptions(QWizard.IndependentPages)
        for pageClass, pageId in self.PAGE_ID.items():
            self.setPage(pageId, pageClass(self))
