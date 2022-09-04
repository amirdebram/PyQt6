#!/usr/bin/env python3

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtWidgets import (
    QWidget, QFrame, QDialog, 
    QHBoxLayout, QVBoxLayout, QFormLayout,
    QAbstractItemView, QTableView, QHeaderView,
    QComboBox, QGroupBox, QDialogButtonBox,
    QPushButton, QLabel, QLineEdit
    )

from Libraries.SQLTableModels import TableModelWithHeader
from Libraries.sshtools import SecureShell

ssh = SecureShell()

class PrinterPage(QWidget):
    def __init__(self, parent=None):
        super(PrinterPage, self).__init__(parent)

        self.clientsBox = QGroupBox("Choose Client")
        self.clientHost = QLabel("Host : ")
        self.clientHostBox = QLabel()
        self.clientHostBox.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.clientPort = QLabel("Port : ")
        self.clientPortBox = QLabel()
        self.clientPortBox.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.clientName = QLabel("Name : ")
        
        self.clientData = QSqlTableModel(self)
        self.clientData.setTable("SecureShell")
        self.clientData.setSort(0, Qt.SortOrder.AscendingOrder)
        self.clientData.select()

        self.clientsDropdown = QComboBox()
        self.clientsDropdown.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.clientsDropdown.addItems([self.clientData.record(i).value("Name") for i in range(0, self.clientData.rowCount())])
        try:
            self.getClientHost()
        except TypeError:
            pass
        self.clientsDropdown.currentIndexChanged.connect(lambda: self.getClientHost())

        self.clientsLayout = QHBoxLayout()
        self.clientsLayout.addWidget(self.clientHost)
        self.clientsLayout.addWidget(self.clientHostBox, 3)
        self.clientsLayout.addWidget(self.clientPort)
        self.clientsLayout.addWidget(self.clientPortBox, 1)
        self.clientsLayout.addWidget(self.clientName)
        self.clientsLayout.addWidget(self.clientsDropdown, 3)
        self.clientsBox.setLayout(self.clientsLayout)

        self.CupsPrintBox = QGroupBox("CUPS Print Server")
        self.button_list_spooler = QPushButton("Check for files in spooler")
        self.button_clear_spooler = QPushButton("Clear Spooler | Restart Cups")
        self.button_list_spooler.clicked.connect(self.check_spooler)
        self.button_clear_spooler.clicked.connect(self.clear_spooler)
        
        self.spoolerLayout = QHBoxLayout()
        self.spoolerLayout.addWidget(self.button_list_spooler)
        self.spoolerLayout.addWidget(self.button_clear_spooler)

        self.button_list_printers = QPushButton("List Printers")
        self.button_add_printer = QPushButton("Add Printer")
        self.button_edit_printer = QPushButton("Edit Printer")
        self.button_delete_printer = QPushButton("Delete Printer")
        self.button_list_printers.clicked.connect(self.list_printers)
        self.button_add_printer.clicked.connect(self.add_printer)
        self.button_edit_printer.clicked.connect(self.edit_printer)
        self.button_delete_printer.clicked.connect(self.delete_printer)

        self.printerLayout = QHBoxLayout()
        self.printerLayout.addWidget(self.button_list_printers)
        self.printerLayout.addWidget(self.button_add_printer)
        self.printerLayout.addWidget(self.button_edit_printer)
        self.printerLayout.addWidget(self.button_delete_printer)

        self.CupsPrintLayout = QVBoxLayout()
        self.CupsPrintLayout.addLayout(self.spoolerLayout)
        self.CupsPrintLayout.addLayout(self.printerLayout)
        
        self.CupsPrintBox.setLayout(self.CupsPrintLayout)

        self.filterModel = QSortFilterProxyModel()
        self.filterModel.setFilterKeyColumn(-1)  # all columns

        self.Table = QTableView(self)
        self.Table.setModel(self.filterModel)
        self.Table.setSortingEnabled(True)
        self.Table.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.Table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.Table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.Table.activated.connect(lambda: self.edit_printer())

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.clientsBox)
        self.mainLayout.addWidget(self.CupsPrintBox)
        self.mainLayout.addWidget(self.Table)
        
        self.setLayout(self.mainLayout)

    def combo(self):
        self.clientsDropdown.clear()
        self.clientData.select()
        self.clientsDropdown.addItems([self.clientData.record(i).value("Name") for i in range(0, self.clientData.rowCount())])

    def getClientHost(self):
        name = self.clientData.record(self.clientsDropdown.currentIndex()).value("Host")
        self.clientHostBox.setText(name)
        port = self.clientData.record(self.clientsDropdown.currentIndex()).value("Port")
        self.clientPortBox.setText(port)

    def clientdetails(self):
        host = self.clientData.record(self.clientsDropdown.currentIndex()).value("Host")
        port = self.clientData.record(self.clientsDropdown.currentIndex()).value("Port")
        username = self.clientData.record(self.clientsDropdown.currentIndex()).value("Username")
        password = self.clientData.record(self.clientsDropdown.currentIndex()).value("Password")
        timeout = self.clientData.record(self.clientsDropdown.currentIndex()).value("Timeout")
        return host, port, username, password, timeout

    def printerdetails(self):
        Name = self.Table.currentIndex().siblingAtColumn(0).data()
        Protocol = self.Table.currentIndex().siblingAtColumn(1).data()
        Location = str(self.Table.currentIndex().siblingAtColumn(2).data()).split('/')
        DeviceURI = Location[0].split(":")[0]
        if Location[0].split(":")[-1].isdigit():
            Port = Location[0].split(":")[-1]
        else:
            Port = str()
        return Name, Protocol, DeviceURI, Port

    def check_spooler(self):
        self.clientData.select()
        ssh.connect(self.clientdetails())
        ssh.files_in_cups_spooler()

    def clear_spooler(self):
        self.clientData.select()
        ssh.connect(self.clientdetails())
        ssh.clear_cups_spooler()

    def update_Table(self, header, data):
        self.TableModel = TableModelWithHeader(header, data)
        self.filterModel.setSourceModel(self.TableModel)
        self.Table.update()
    
    def list_printers(self):
        self.clientData.select()
        if ssh.connect(self.clientdetails()):
            header = ["Name", "Protocol", "IP"]
            data = ssh.list_cups_printers()
            self.update_Table(header, data)

    def add_printer(self):
        printer = AddPrinterDialog(self)
        if printer.exec():
            self.clientData.select()
            if ssh.connect(self.clientdetails()):
                ssh.add_cups_printer(
                    printer.Name.text(),
                    printer.Protocol.currentText(),
                    printer.DeviceURI.text(),
                    printer.Port.text(),
                    printer.Username.text(),
                    printer.Password.text()
                )
            [x.setText("") for x in [printer.Name, printer.DeviceURI, printer.Port, printer.Username, printer.Password]]
            return self.list_printers()
        else:
            printer.close()

    def edit_printer(self):
        p = self.printerdetails()
        printer = EditPrinterDialog(p[0], p[1], p[2], p[3])
        if printer.exec():
            return self.list_printers()
        else:
            printer.close()

    def delete_printer(self):
        self.clientData.select()
        if ssh.connect(self.clientdetails()):
            ssh.delete_cups_printer(self.Table.currentIndex().siblingAtColumn(0).data())
        return self.list_printers()

    def togglewidget(self, widget):
        if widget.isHidden():
            widget.setHidden(False)
        else:
            widget.setHidden(True)


class AddPrinterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Name = QLineEdit()
        self.Protocol = QComboBox()
        self.Protocol.addItem("lpd")
        self.Protocol.addItem("socket")
        self.Protocol.addItem("smb")
        self.DeviceURI = QLineEdit()
        self.DeviceURI.setAttribute()
        self.Port = QLineEdit()
        self.Username = QLineEdit()
        self.Password = QLineEdit()
        if self.Protocol.currentText() == "smb":
            self.Username.setEnabled(True)
            self.Password.setEnabled(True)
        else:
            self.Username.setEnabled(False)
            self.Password.setEnabled(False)
        self.Buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.Buttons.accepted.connect(self.accept)
        self.Buttons.rejected.connect(self.reject)

        self.Layout = QFormLayout()
        self.Layout.addRow(QLabel("Protocol")   , self.Protocol )
        self.Layout.addRow(QLabel("Name")       , self.Name     )
        self.Layout.addRow(QLabel("IP Address") , self.DeviceURI)
        self.Layout.addRow(QLabel("Port")       , self.Port     )
        self.Layout.addRow(QLabel("Username")   , self.Username )
        self.Layout.addRow(QLabel("Password")   , self.Password )
        self.Layout.addRow(self.Buttons)
        self.setLayout(self.Layout)

        self.setWindowTitle("Add CUPS Printer")


class EditPrinterDialog(QDialog):
    def __init__(self, Name, Protocol, DeviceURI, Port, parent=None):
        super().__init__(parent)

        self.Name = QLineEdit()
        self.Name.setText(Name)
        self.Protocol = QComboBox()
        self.Protocol.addItem("lpd")
        self.Protocol.addItem("socket")
        self.Protocol.addItem("smb")
        self.Protocol.setCurrentText(Protocol)
        self.DeviceURI = QLineEdit()
        self.DeviceURI.setText(DeviceURI)
        self.Port = QLineEdit()
        self.Port.setText(Port)
        self.Username = QLineEdit()
        self.Password = QLineEdit()
        self.Buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.Buttons.accepted.connect(self.accept)
        self.Buttons.rejected.connect(self.reject)

        self.Layout = QFormLayout()
        self.Layout.addRow(QLabel("Protocol")   , self.Protocol )
        self.Layout.addRow(QLabel("Name")       , self.Name     )
        self.Layout.addRow(QLabel("IP Address") , self.DeviceURI)
        self.Layout.addRow(QLabel("Port")       , self.Port     )
        self.Layout.addRow(QLabel("Username")   , self.Username )
        self.Layout.addRow(QLabel("Password")   , self.Password )
        self.Layout.addRow(self.Buttons)
        self.setLayout(self.Layout)

        self.setWindowTitle("Edit CUPS Printer")
