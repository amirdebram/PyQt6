#!/usr/bin/env python3

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant

class TableModelWithHeader(QAbstractTableModel):
    def __init__(self, header, data):
        super(TableModelWithHeader, self).__init__()
        self._header = header
        self._data = data

    def rowCount(self, data):
        return len(self._data)

    def columnCount(self, header):
        return len(self._header)

    def data(self, index, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()
        return self._header[section]