from dataclasses import field, dataclass, fields, astuple

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List


@dataclass(init=False)
class BillData:
    id_: str
    email: str
    title: str
    price: float
    participants: List = field(default_factory=list)

    def __init__(self, _id, email, title, price, participants, **_kwargs):
        self.id_ = _id
        self.email = email
        self.title = title
        self.price = price
        self.participants = participants


class BillModel(QAbstractTableModel):

    def __init__(self, *args):
        super().__init__(*args)
        self._data: List[BillData] = []

    def setNewData(self, newData: List[BillData]):
        self.beginResetModel()
        self._data = newData
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = None):
        return len(self._data)

    def columnCount(self, parent: QModelIndex = None):
        return 5

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            if role == Qt.UserRole:
                return self._data[index.row()]
            return
        row = self._data[index.row()]
        value = astuple(row)[index.column()]
        return str(value)

    def headerData(self, section: int,
                   orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            name: str = fields(BillData)[section].name
            return name.capitalize()
