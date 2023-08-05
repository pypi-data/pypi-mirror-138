# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the connection parameters.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox
from PyQt6.QtSql import QSqlDatabase

from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_SqlConnectionDialog import Ui_SqlConnectionDialog


class SqlConnectionDialog(QDialog, Ui_SqlConnectionDialog):
    """
    Class implementing a dialog to enter the connection parameters.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.databasePicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        
        self.okButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok)
        
        drivers = QSqlDatabase.drivers()
        
        # remove compatibility names
        if "QMYSQL3" in drivers:
            drivers.remove("QMYSQL3")
        if "QOCI8" in drivers:
            drivers.remove("QOCI8")
        if "QODBC3" in drivers:
            drivers.remove("QODBC3")
        if "QPSQL7" in drivers:
            drivers.remove("QPSQL7")
        if "QTDS7" in drivers:
            drivers.remove("QTDS7")
        
        self.driverCombo.addItems(drivers)
        
        self.__updateDialog()
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __updateDialog(self):
        """
        Private slot to update the dialog depending on its contents.
        """
        driver = self.driverCombo.currentText()
        if driver.startswith("QSQLITE"):
            self.databasePicker.setPickerEnabled(True)
        else:
            self.databasePicker.setPickerEnabled(False)
        
        if self.databasePicker.text() == "" or driver == "":
            self.okButton.setEnabled(False)
        else:
            self.okButton.setEnabled(True)
    
    @pyqtSlot(int)
    def on_driverCombo_activated(self, index):
        """
        Private slot handling the selection of a database driver.
        
        @param index index of the selected entry
        @type int
        """
        self.__updateDialog()
    
    @pyqtSlot(str)
    def on_databasePicker_textChanged(self, txt):
        """
        Private slot handling the change of the database name.
        
        @param txt text of the edit (string)
        """
        self.__updateDialog()
    
    def getData(self):
        """
        Public method to retrieve the connection data.
        
        @return tuple giving the driver name (string), the database name
            (string), the user name (string), the password (string), the
            host name (string) and the port (integer)
        """
        return (
            self.driverCombo.currentText(),
            self.databasePicker.text(),
            self.usernameEdit.text(),
            self.passwordEdit.text(),
            self.hostnameEdit.text(),
            self.portSpinBox.value(),
        )
