#!/usr/bin/env python3

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QDialog,
    QHBoxLayout, QVBoxLayout,
    QListView, QListWidget, QListWidgetItem, QStackedWidget,
    QPushButton
    )
    
from Modules.Clients import ClientsPage
from Modules.FileManager import FileMangerPage
from Modules.Printers import PrinterPage
from Modules.Rocketd3 import RocketD3Page
from Modules.Server import ServerPage

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.sideToolBox = QListWidget()
        self.sideToolBox.setViewMode(QListView.ViewMode.IconMode)
        self.sideToolBox.setIconSize(QSize(90, 80))
        self.sideToolBox.setMovement(QListView.Movement.Static)
        self.sideToolBox.setMaximumWidth(125)
        self.sideToolBox.setMinimumHeight(575)
        self.sideToolBox.setSpacing(12)
        self.sideToolBox.setCurrentRow(0)
        self.sideToolBox.currentItemChanged.connect(self.changePage)

        self.createIcons()

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(ClientsPage())
        self.pagesWidget.addWidget(FileMangerPage())
        self.pagesWidget.addWidget(PrinterPage())
        self.pagesWidget.addWidget(RocketD3Page())
        self.pagesWidget.addWidget(ServerPage())

        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.close)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.sideToolBox)
        horizontalLayout.addWidget(self.pagesWidget, 1)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)
        
        self.setWindowTitle("Crystal Tools")
        self.setWindowIcon(QIcon('.\\res\\Icons\\tool-box.png'))
        self.setFixedSize(900, 600)


    def createIcons(self):
        clientsButton = QListWidgetItem(self.sideToolBox)
        clientsButton.setIcon(QIcon('.\\res\\Icons\\Toolbox\\client.png'))
        clientsButton.setText("Clients")
        clientsButton.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        clientsButton.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        queryButton = QListWidgetItem(self.sideToolBox)
        queryButton.setIcon(QIcon('.\\res\\Icons\\Toolbox\\file.png'))
        queryButton.setText("File Manager")
        queryButton.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        queryButton.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        PrinterButton = QListWidgetItem(self.sideToolBox)
        PrinterButton.setIcon(QIcon('.\\res\\Icons\\Toolbox\\printer.png'))
        PrinterButton.setText("Printers")
        PrinterButton.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        PrinterButton.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        rocketButton = QListWidgetItem(self.sideToolBox)
        rocketButton.setIcon(QIcon('.\\res\\Icons\\Toolbox\\shuttle.png'))
        rocketButton.setText("Rocket D3")
        rocketButton.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        rocketButton.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        updateButton = QListWidgetItem(self.sideToolBox)
        updateButton.setIcon(QIcon('.\\res\\Icons\\Toolbox\\server.png'))
        updateButton.setText("Server")
        updateButton.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        updateButton.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

    def changePage(self, current, previous):
        if not current:
            current = previous
        self.pagesWidget.setCurrentIndex(self.sideToolBox.row(current))
  

if __name__ == '__main__':

    from sys import argv, exit

    app = QApplication(argv)
    if not ClientsPage().createConnection():
        exit(1)

    # Open the style sheet file and read it
    # with open('.\\res\\stylesheets\\style.qss', 'r') as f:
    #     style = f.read()
    # # Set the current style sheet
    # app.setStyleSheet(style)
    # app.setStyle('fusion')
    CrystalTools = MainWindow()
    exit(CrystalTools.exec())    
