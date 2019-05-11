# noinspection PyUnresolvedReferences
from PyQt5.QtCore import pyqtSignal, pyqtProperty

from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QFileDialog
from splitwise.desktop.generated import addBillSelectAddType, addBillManual, addBillSelectFile, addBillScan, \
    addBillSummary


class BasePage(QWizardPage):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

    def nextId(self):
        return BillWizard.PAGE_ID[Summary]


class SelectAddType(BasePage, addBillSelectAddType.Ui_WizardPage):
    selectedChanged = pyqtSignal(int)

    @pyqtProperty(type(BasePage), notify=selectedChanged)
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, val):
        self._selected = val

    def __init__(self, *args):
        super().__init__(*args)
        self._selected = BasePage
        self.registerField('selected', self, 'selected', self.selectedChanged)

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


class Scan(BasePage, addBillScan.Ui_WizardPage):
    pass


class Summary(BasePage, addBillSummary.Ui_WizardPage):

    def initializePage(self):
        selected = self.field('selected')
        if selected == Manual:
            product = self.field('product')
            price = self.field('price')
            text = f"{product}={price}"
            self.textBrowser.setText(text)
        elif selected == SelectFile:
            self.textBrowser.setText("Not implemented")  # TODO recognise from file
        elif selected == Scan:
            self.textBrowser.setText("Not implemented")  # TODO recognise from camera
        else:
            assert False

    def nextId(self):
        return -1


class BillWizard(QWizard):
    pyqtSignal()
    PAGE_ID = {
        p: i for i, p in enumerate((SelectAddType, Manual, SelectFile, Scan, Summary))
    }

    def __init__(self, *args):
        super().__init__(*args)
        self.setOptions(QWizard.IndependentPages)
        for pageClass, pageId in self.PAGE_ID.items():
            self.setPage(pageId, pageClass(self))
