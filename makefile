

uiFiles="resources/$(wildcard)"
uiCompiler=pyuic5

need = addBillManual.py addBillSelectAddType.py addFriend.py bills.py mainWindow.py addBillScan.py addBillSelectFile.py addBillSummary.py
target=splitwise/desktop/generated

all: directories generateUI

directories:
	mkdir -p $(target)
	touch $(target)/__init__.py

generateUI: $(need)

%.py: resources/%.ui
	$(uiCompiler) -o $(target)/$@ $^