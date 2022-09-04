#!/usr/bin/env python3

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtWidgets import (QWidget, QGroupBox, QCheckBox, 
QListWidget, QListWidgetItem, QPushButton, QVBoxLayout)


class RocketD3Page(QWidget):
    def __init__(self, parent=None):
        super(RocketD3Page, self).__init__(parent)

        updateGroup = QGroupBox("Package selection")
        systemCheckBox = QCheckBox("Update system")
        appsCheckBox = QCheckBox("Update applications")
        docsCheckBox = QCheckBox("Update documentation")

        packageGroup = QGroupBox("Existing packages")

        packageList = QListWidget()
        qtItem = QListWidgetItem(packageList)
        qtItem.setText("Qt")
        qsaItem = QListWidgetItem(packageList)
        qsaItem.setText("QSA")
        teamBuilderItem = QListWidgetItem(packageList)
        teamBuilderItem.setText("Teambuilder")

        startUpdateButton = QPushButton("Start update")

        updateLayout = QVBoxLayout()
        updateLayout.addWidget(systemCheckBox)
        updateLayout.addWidget(appsCheckBox)
        updateLayout.addWidget(docsCheckBox)
        updateGroup.setLayout(updateLayout)

        packageLayout = QVBoxLayout()
        packageLayout.addWidget(packageList)
        packageGroup.setLayout(packageLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(updateGroup)
        mainLayout.addWidget(packageGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(startUpdateButton)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)