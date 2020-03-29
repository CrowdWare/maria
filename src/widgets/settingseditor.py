#############################################################################
# Copyright (C) 2020 Olaf Japp
#
# This file is part of Maria.
#
#  Maria is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Maria is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Maria.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import os
import shutil
from PyQt5.QtWidgets import QWidget, QSpinBox, QLineEdit, QComboBox, QGridLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QImage, QFont
import resources


class SettingsEditor(QWidget):
    def __init__(self, win):
        QWidget.__init__(self)
        self.win = win
        title = QLabel("Settings")
        fnt = title.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        title.setFont(fnt)
        self.layout = QGridLayout()
        self.fontSize = QSpinBox()
        self.fontSize.setValue(win.fontSize)
        self.databaseFile = QLineEdit()
        self.databaseFile.setText(win.databaseFile)

        vbox = QVBoxLayout()
        vbox.addStretch()

        self.layout.addWidget(title, 0, 0)
        self.layout.addWidget(QLabel("Font Size"), 1, 0)
        self.layout.addWidget(self.fontSize, 2, 0, 1, 3)
        self.layout.addWidget(QLabel("Database File"), 3, 0)
        self.layout.addWidget(self.databaseFile, 4, 0, 1, 3)
        self.layout.addLayout(vbox, 16, 0)
        self.setLayout(self.layout)

        self.fontSize.valueChanged.connect(self.settingsChanged)
        self.databaseFile.textEdited.connect(self.settingsChanged)

    def settingsChanged(self):
        self.win.fontSize = self.fontSize.value()
        self.win.databaseFile = self.databaseFile.text()

        font = QFont("Sans Serif", self.win.fontSize)
        self.win.app.setFont(font)
