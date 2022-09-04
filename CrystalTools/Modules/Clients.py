#!/usr/bin/env python3

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt6.QtWidgets import (
    QWidget, QDataWidgetMapper,
    QHBoxLayout, QVBoxLayout, QFormLayout,
    QAbstractItemView, QTableView,
    QGroupBox, QSpinBox,
    QPushButton, QLabel, QLineEdit,
    QMessageBox
    )


class ClientsPage(QWidget):
    def __init__(self, parent=None):
        super(ClientsPage, self).__init__(parent)

        self.searchBox = QGroupBox("Search")
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.button_clear = QPushButton("Clear")
        self.button_clear.clicked.connect(self.searchBar.clear)
        self.searchLayout = QHBoxLayout()
        self.searchLayout.addWidget(self.searchBar)
        self.searchLayout.addWidget(self.button_clear)
        self.searchBox.setLayout(self.searchLayout)

        self.sshModel = QSqlTableModel(self)
        self.sshModel.setTable("SecureShell")
        self.sshModel.setSort(0, Qt.SortOrder.AscendingOrder)
        self.sshModel.select()

        self.searchModel = QSortFilterProxyModel()
        self.searchModel.setSourceModel(self.sshModel)
        self.searchModel.setFilterKeyColumn(-1)  # all columns
        
        self.sshTable = QTableView(self)
        self.sshTable.setModel(self.searchModel)
        self.sshTable.setSortingEnabled(True)
        self.sshTable.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.sshTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sshTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sshTable.resizeColumnsToContents()
        
        self.nameMap = QLineEdit()
        self.hostMap = QLineEdit()
        self.portMap = QLineEdit()
        self.usernameMap = QLineEdit()
        self.passwordMap = QLineEdit()
        self.passwordMap.setEchoMode(QLineEdit.EchoMode.Password)
        self.timeoutMap = QSpinBox()
        self.timeoutMap.setValue(5)
        self.timeoutMap.setRange(0, 65535)

        self.tableMapper = QDataWidgetMapper()
        self.tableMapper.setModel(self.searchModel)
        self.tableMapper.addMapping(self.nameMap, 0)
        self.tableMapper.addMapping(self.hostMap, 1)
        self.tableMapper.addMapping(self.portMap, 2)
        self.tableMapper.addMapping(self.usernameMap, 3)
        self.tableMapper.addMapping(self.passwordMap, 4)
        self.tableMapper.addMapping(self.timeoutMap, 5)
        self.tableMapper.toFirst()

        self.editbox = QGroupBox("Client Details")
        self.password_shown = False
        self.button_showpassword = QPushButton("Show Password")
        self.button_showpassword.clicked.connect(self.on_toggle_password_Action)
        self.editLayout = QFormLayout()
        self.editLayout.addRow(QLabel("Name:"), self.nameMap)
        self.editLayout.addRow(QLabel("Host:"), self.hostMap)
        self.editLayout.addRow(QLabel("Port:"), self.portMap)
        self.editLayout.addRow(QLabel("Username:"), self.usernameMap)
        self.editLayout.addRow(QLabel("Password:"), self.passwordMap)
        self.editLayout.addRow(QLabel("Timeout:"), self.timeoutMap)
        self.editLayout.addRow(self.button_showpassword)
        self.editbox.setLayout(self.editLayout)
        self.editbox.setHidden(True)

        self.buttonBox = QGroupBox("Controls")
        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.add_widget)
        self.button_edit = QPushButton("Edit")
        self.button_edit.clicked.connect(self.edit_widget)
        self.button_delete = QPushButton("Delete")
        self.button_delete.clicked.connect(self.delete_widegt)
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save_widget)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.button_add)
        self.buttonLayout.addWidget(self.button_edit)
        self.buttonLayout.addWidget(self.button_delete)
        self.buttonLayout.addWidget(self.button_save)
        self.buttonBox.setLayout(self.buttonLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.searchBox)
        self.mainLayout.addWidget(self.sshTable)
        self.mainLayout.addWidget(self.editbox)
        self.mainLayout.addWidget(self.buttonBox)
         
        self.searchBar.textChanged.connect(self.searchModel.setFilterFixedString)
        self.sshTable.selectionModel().currentRowChanged.connect(self.tableMapper.setCurrentModelIndex)

        self.setLayout(self.mainLayout)

    def createConnection(self) -> bool:        
        # SQLite type database connection instance    
        db = QSqlDatabase.addDatabase('QSQLITE') 
        # Connect to the database file
        db.setDatabaseName("./Database/Client.db")
        # Show message box when there is a connection issue
        if not db.open():
            from os import mkdir
            mkdir("./Database")
            QMessageBox.critical(
                None,
                'QTableView Example - Error!',
                'Database Error: %s.\nDatabase folder has been created.\nPlease try again' % db.lastError().databaseText(),
            )
            return False
        # Create a query and execute it right away using .exec()
        query = """CREATE TABLE IF NOT EXISTS SecureShell (
            Name TEXT NOT NULL, 
            Host TEXT NOT NULL, 
            Port INTEGER NOT NULL, 
            Username VARCHAR(30) NOT NULL, 
            Password TEXT NOT NULL, 
            Timeout INTEGER NOT NULL)"""
        QSqlQuery(query=query, db=db)
        return True

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.passwordMap.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_shown = True
            self.button_showpassword.setText('Hide Password')
        else:
            self.passwordMap.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_shown = False
            self.button_showpassword.setText('Show Password')
            
    def togglewidget(self, widget):
        if widget.isHidden():
            widget.setHidden(False)
        else:
            widget.setHidden(True)

    def add_widget(self):
        self.togglewidget(self.editbox)
        self.sshModel.insertRow(0)
        self.sshTable.selectRow(0)

    def edit_widget(self):
        self.togglewidget(self.editbox)
        self.mainLayout.update()
    
    def delete_widegt(self):
        reply = QMessageBox.warning(self, 'Warning', f"Are you sure to delete host:\n{self.hostMap.text()}?", 
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.sshModel.deleteRowFromTable(self.sshTable.currentIndex().row())
            self.searchModel.removeRow(self.sshTable.currentIndex().row())
            self.tableMapper.submit()
            self.sshModel.select()
        else:
            pass

    def save_widget(self):
        self.tableMapper.submit()
        self.editbox.setHidden(True)
        self.sshModel.select()
 
    def get_host(self):
        print(self.sshTable.currentIndex().row(), self.sshTable.currentIndex().siblingAtColumn(1).data())