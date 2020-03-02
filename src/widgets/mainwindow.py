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
import inspect
import pathlib
import sys
import shutil
from importlib import import_module
from widgets.flatbutton import FlatButton
from widgets.expander import Expander
from widgets.hyperlink import HyperLink
from widgets.dashboard import Dashboard
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QMainWindow, QWidget, QScrollArea, QDockWidget, QUndoStack, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QUrl, QRect, QCoreApplication, QDir, QSettings, QByteArray, QEvent, QPoint, QAbstractAnimation, QPropertyAnimation
from PyQt5.QtQml import QQmlEngine, QQmlComponent

import resources

class MainWindow(QMainWindow):
    siteLoaded = pyqtSignal(object)

    def __init__(self):
        QMainWindow.__init__(self)
        self.initGui()
        self.readSettings()
        self.dashboard.setExpanded(True)
        self.showDashboard()
        self.statusBar().showMessage("Ready")
    
    def initGui(self):
        self.installEventFilter(self)
        self.dashboard = Expander("Dashboard", ":/images/dashboard_normal.png", ":/images/dashboard_hover.png", ":/images/dashboard_selected.png")
        self.content = Expander("Clients", ":/images/clients_normal.png", ":/images/clients_hover.png", ":/images/clients_selected.png")
        self.settings = Expander("Settings", ":/images/settings_normal.png", ":/images/settings_hover.png", ":/images/settings_selected.png")

        self.setWindowTitle(QCoreApplication.applicationName() + " " + QCoreApplication.applicationVersion())
        vbox = QVBoxLayout()
        vbox.addWidget(self.dashboard)
        vbox.addWidget(self.content)
        vbox.addWidget(self.settings)
        vbox.addStretch()

        content_box = QVBoxLayout()
        #pages_button = HyperLink("Pages")
        #posts_button = HyperLink("Posts")
        #content_box.addWidget(pages_button)
        #content_box.addWidget(posts_button)
        self.content.addLayout(content_box)

        scroll_content = QWidget()
        scroll_content.setLayout(vbox)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(200)
        scroll.setMinimumWidth(200)

        self.navigationdock = QDockWidget("Navigation", self)
        self.navigationdock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.navigationdock.setWidget(scroll)
        self.navigationdock.setObjectName("Navigation")

        self.addDockWidget(Qt.LeftDockWidgetArea, self.navigationdock)

        self.showDock = FlatButton(":/images/edit_normal.png", ":/images/edit_hover.png")
        self.showDock.setToolTip("Show Navigation")
        self.statusBar().addPermanentWidget(self.showDock)

        self.dashboard.expanded.connect(self.dashboardExpanded)
        self.dashboard.clicked.connect(self.showDashboard)
        self.content.expanded.connect(self.contentExpanded)
        
        self.settings.expanded.connect(self.settingsExpanded)
        
        self.showDock.clicked.connect(self.showMenu)
        self.navigationdock.visibilityChanged.connect(self.dockVisibilityChanged)

    def showDashboard(self):
        db = Dashboard()
        db.createSite.connect(self.createSite)
        self.setCentralWidget(db)

    def setCentralWidget(self, widget):
        old_widget = self.takeCentralWidget()
        super().setCentralWidget(widget)
        widget.show()

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def writeSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
       
    def readSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        geometry = settings.value("geometry", QByteArray())
        if geometry.isEmpty():
            availableGeometry = QApplication.desktop().availableGeometry(self)
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
            self.move(int(((availableGeometry.width() - self.width()) / 2)), int((availableGeometry.height() - self.height()) / 2))
        else:
            self.restoreGeometry(geometry)
            self.restoreState(settings.value("state"))

    def dashboardExpanded(self, value):
        if value:
            self.content.setExpanded(False)
            self.settings.setExpanded(False)

    def contentExpanded(self, value):
        if value:
            self.dashboard.setExpanded(False)
            self.settings.setExpanded(False)

    def settingsExpanded(self, value):
        if value:
            self.dashboard.setExpanded(False)
            self.content.setExpanded(False)

    def showMenu(self):
        self.navigationdock.setVisible(True)

    def dockVisibilityChanged(self, visible):
        self.showDock.setVisible(not visible)

    def createSite(self):
       pass

    def animate(self, item):
        panel = self.centralWidget()
        self.list = item.tableWidget()
        self.row = item.row()

        # create a cell widget to get the right position in the table
        self.cellWidget = QWidget()
        self.cellWidget.setMaximumHeight(0)
        self.list.setCellWidget(self.row, 1, self.cellWidget)
        pos = self.cellWidget.mapTo(panel, QPoint(0, 0))

        self.editor.setParent(panel)
        self.editor.move(pos)
        self.editor.resize(self.cellWidget.size())
        self.editor.show()

        self.animation = QPropertyAnimation(self.editor, "geometry".encode("utf-8"))
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(pos.x(), pos.y(), self.cellWidget.size().width(), self.cellWidget.size().height()))
        self.animation.setEndValue(QRect(0, 0, panel.size().width(), panel.size().height()))
        self.animation.start()

    def editorClosed(self):
        pos = self.cellWidget.mapTo(self.centralWidget(), QPoint(0, 0))
        # correct end values in case of resizing the window
        self.animation.setStartValue(QRect(pos.x(), pos.y(), self.cellWidget.size().width(), self.cellWidget.size().height()))
        self.animation.finished.connect(self.animationFineshedZoomOut)
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()

    def animationFineshedZoomOut(self):
        self.list.removeCellWidget(self.row, 1)
        del self.animation

        # in the case self.editor was a MenuEditor, we have to unregister it in the MenuList
        # should be refactored some day :-)
        list = self.centralWidget()
        if list is MenuEditor:
            list.unregisterMenuEditor()

        del self.editor
        self.editor = None

        if self.method_after_animation == "showDashboard":
            self.showDashboard()
            self.method_after_animation = ""
        elif self.method_after_animation == "showSettings":
            self.showSettings()

        if self.content_after_animation:
            self.previewSite(self.content_after_animation)
            self.content_after_animation = None
