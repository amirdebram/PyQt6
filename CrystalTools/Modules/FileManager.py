#!/usr/bin/env python3

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (QWidget, QGroupBox, QLabel,
QLineEdit, QDateTimeEdit, QCheckBox, QSpinBox, QPushButton,
QGridLayout, QVBoxLayout)


class FileMangerPage(QWidget):
    def __init__(self, parent=None):
        super(FileMangerPage, self).__init__(parent)

        packagesGroup = QGroupBox("Look for packages")

        nameLabel = QLabel("Name:")
        nameEdit = QLineEdit()

        dateLabel = QLabel("Released after:")
        dateEdit = QDateTimeEdit(QDate.currentDate())

        releasesCheckBox = QCheckBox("Releases")
        upgradesCheckBox = QCheckBox("Upgrades")

        hitsSpinBox = QSpinBox()
        hitsSpinBox.setPrefix("Return up to ")
        hitsSpinBox.setSuffix(" results")
        hitsSpinBox.setSpecialValueText("Return only the first result")
        hitsSpinBox.setMinimum(1)
        hitsSpinBox.setMaximum(100)
        hitsSpinBox.setSingleStep(10)

        startQueryButton = QPushButton("Start query")

        packagesLayout = QGridLayout()
        packagesLayout.addWidget(nameLabel, 0, 0)
        packagesLayout.addWidget(nameEdit, 0, 1)
        packagesLayout.addWidget(dateLabel, 1, 0)
        packagesLayout.addWidget(dateEdit, 1, 1)
        packagesLayout.addWidget(releasesCheckBox, 2, 0)
        packagesLayout.addWidget(upgradesCheckBox, 3, 0)
        packagesLayout.addWidget(hitsSpinBox, 4, 0, 1, 2)
        packagesGroup.setLayout(packagesLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(packagesGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(startQueryButton)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)