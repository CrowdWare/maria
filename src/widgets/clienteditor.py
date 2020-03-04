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
from widgets.imageselector import ImageSelector
from PyQt5.QtWidgets import QWidget, QDateEdit, QTextEdit, QLineEdit, QComboBox, QGridLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QDate
import resources


class ClientEditor(QWidget):
    def __init__(self, win):
        QWidget.__init__(self)
        self.win = win
        title = QLabel("Client Data")
        fnt = title.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        title.setFont(fnt)
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        self.name = QLineEdit()
        self.email = QLineEdit()
        self.profession = QLineEdit()
        self.address = QLineEdit()
        self.mobile = QLineEdit()
        self.reason = QLineEdit()
        self.how = QLineEdit()
        self.fiscal = QLineEdit()
        self.notes = QTextEdit()
        self.birthday = QDateEdit()
        self.birthday.setCalendarPopup(True)
        self.birthday.setDisplayFormat("dd.MM.yyyy")
        self.firstcontact = QDateEdit(QDate.currentDate())
        self.firstcontact.setDisplayFormat("dd.MM.yyyy")
        self.firstcontact.setCalendarPopup(True)
        
        self.image = ImageSelector()
        self.image.setImage(QImage(":/images/image_placeholder.png"))
        self.image.setMinimumWidth(250)

        self.layout.addWidget(title, 0, 0, 1, 2)
        self.layout.addWidget(QLabel("Name"), 1, 0)
        self.layout.addWidget(self.name, 2, 0)
        self.layout.addWidget(QLabel("Address"), 3, 0)
        self.layout.addWidget(self.address, 4, 0)
        self.layout.addWidget(QLabel("Email"), 5, 0)
        self.layout.addWidget(self.email, 6, 0)
        self.layout.addWidget(QLabel("Mobile"), 7, 0)
        self.layout.addWidget(self.mobile, 8, 0)
        self.layout.addWidget(QLabel("Profession"), 9, 0)
        self.layout.addWidget(self.profession, 10, 0)
        self.layout.addWidget(QLabel("Reason"), 11, 0)
        self.layout.addWidget(self.reason, 12, 0)
        self.layout.addWidget(QLabel("How did you get here?"), 13, 0)
        self.layout.addWidget(self.how, 14, 0)
        self.layout.addWidget(QLabel("Notes"), 15, 0)
        self.layout.addWidget(self.notes, 16, 0, 1, 2)
        self.layout.addWidget(self.image, 2, 1, 7, 1)
        self.layout.addWidget(QLabel("Birhday"), 9, 1)
        self.layout.addWidget(self.birthday, 10, 1)
        self.layout.addWidget(QLabel("First Contact"), 11, 1)
        self.layout.addWidget(self.firstcontact, 12, 1)
        self.layout.addWidget(QLabel("Fiscal"), 13, 1)
        self.layout.addWidget(self.fiscal, 14, 1, 1, 1)
        self.setLayout(self.layout)

        self.reload()

        self.name.textEdited.connect(self.clientChanged)
        self.address.textEdited.connect(self.clientChanged)
        self.email.textEdited.connect(self.clientChanged)
        self.mobile.textEdited.connect(self.clientChanged)
        self.profession.textEdited.connect(self.clientChanged)
        self.reason.textEdited.connect(self.clientChanged)
        self.how.textEdited.connect(self.clientChanged)
        self.notes.textChanged.connect(self.clientChanged)
        self.fiscal.textEdited.connect(self.clientChanged)

    def reload(self):
        if self.win.client:
            self.name.setText(self.win.client["name"])
            self.address.setText(self.win.client["address"])
            self.email.setText(self.win.client["email"])
            self.mobile.setText(self.win.client["mobile"])
            self.profession.setText(self.win.client["profession"])
            self.reason.setText(self.win.client["reason"])
            self.how.setText(self.win.client["how"])
            self.notes.setText(self.win.client["notes"])
            self.birthday.setDate(self.win.client["birthdate_year"])
            self.firstcontact.setDate(self.win.client["firstContact"])
            self.fiscal.setText(self.win.client["fiscal"])
        else:
            self.name.setText("")
            self.address.setText("")
            self.email.setText("")
            self.mobile.setText("")
            self.profession.setText("")
            self.reason.setText("")
            self.how.setText("")
            self.notes.setText("")
            self.fiscal.setText("")
            #self.birthday.setDate(QDate(1900,1,1))
            #self.firstcontact.setDate(QDate(1900,1,1))
            
    def clientChanged(self):
        self.win.client["name"] = self.name.text()
        self.win.client["address"] = self.address.text()
        self.win.client["email"] = self.email.text()
        self.win.client["mobile"] = self.mobile.text()
        self.win.client["profession"] = self.profession.text()
        self.win.client["reason"] = self.reason.text()
        self.win.client["how"] = self.how.text()
        self.win.client["notes"] = self.notes.toPlainText()
        self.win.client["fiscal"] = self.fiscal.text()
        self.win.clients.update(self.win.client, doc_ids=[self.win.client.doc_id])
        self.win.updateClient()
