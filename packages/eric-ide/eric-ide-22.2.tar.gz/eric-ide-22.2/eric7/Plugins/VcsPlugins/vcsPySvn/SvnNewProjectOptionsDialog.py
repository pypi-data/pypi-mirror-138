# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Subversion Options Dialog for a new project from the
repository.
"""

import os

from PyQt6.QtCore import QDir, pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_SvnNewProjectOptionsDialog import Ui_SvnNewProjectOptionsDialog
from .Config import ConfigSvnProtocols

import Utilities
import Preferences


class SvnNewProjectOptionsDialog(QDialog, Ui_SvnNewProjectOptionsDialog):
    """
    Class implementing the Options Dialog for a new project from the
    repository.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the version control object
        @param parent parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.vcsProjectDirPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.vcsUrlPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        
        self.protocolCombo.addItems(ConfigSvnProtocols)
        
        hd = Utilities.toNativeSeparators(QDir.homePath())
        hd = os.path.join(hd, 'subversionroot')
        self.vcsUrlPicker.setText(hd)
        
        self.vcs = vcs
        
        self.localPath = hd
        self.networkPath = "localhost/"
        self.localProtocol = True
        
        ipath = (
            Preferences.getMultiProject("Workspace") or
            Utilities.getHomeDir()
        )
        self.__initPaths = [
            Utilities.fromNativeSeparators(ipath),
            Utilities.fromNativeSeparators(ipath) + "/",
        ]
        self.vcsProjectDirPicker.setText(self.__initPaths[0])
        
        self.resize(self.width(), self.minimumSizeHint().height())
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    @pyqtSlot(str)
    def on_vcsProjectDirPicker_textChanged(self, txt):
        """
        Private slot to handle a change of the project directory.
        
        @param txt name of the project directory (string)
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(txt) and
            Utilities.fromNativeSeparators(txt) not in self.__initPaths)
        
    @pyqtSlot()
    def on_vcsUrlPicker_pickerButtonClicked(self):
        """
        Private slot to display a repository browser dialog.
        """
        from .SvnRepoBrowserDialog import SvnRepoBrowserDialog
        dlg = SvnRepoBrowserDialog(self.vcs, mode="select", parent=self)
        dlg.start(
            self.protocolCombo.currentText() + self.vcsUrlPicker.text())
        if dlg.exec() == QDialog.DialogCode.Accepted:
            url = dlg.getSelectedUrl()
            if url:
                protocol = url.split("://")[0]
                path = url.split("://")[1]
                self.protocolCombo.setCurrentIndex(
                    self.protocolCombo.findText(protocol + "://"))
                self.vcsUrlPicker.setText(path)
        
    def on_layoutCheckBox_toggled(self, checked):
        """
        Private slot to handle the change of the layout checkbox.
        
        @param checked flag indicating the state of the checkbox (boolean)
        """
        self.vcsTagLabel.setEnabled(checked)
        self.vcsTagEdit.setEnabled(checked)
        if not checked:
            self.vcsTagEdit.clear()
        
    @pyqtSlot(int)
    def on_protocolCombo_activated(self, index):
        """
        Private slot to switch the status of the directory selection button.
        
        @param index index of the selected entry
        @type int
        """
        protocol = self.protocolCombo.itemText(index)
        if protocol == "file://":
            self.networkPath = self.vcsUrlPicker.text()
            self.vcsUrlPicker.setText(self.localPath)
            self.vcsUrlLabel.setText(self.tr("Pat&h:"))
            self.localProtocol = True
            self.vcsUrlPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        else:
            if self.localProtocol:
                self.localPath = self.vcsUrlPicker.text()
                self.vcsUrlPicker.setText(self.networkPath)
                self.vcsUrlLabel.setText(self.tr("&URL:"))
                self.localProtocol = False
                self.vcsUrlPicker.setMode(EricPathPickerModes.CUSTOM_MODE)
    
    @pyqtSlot(str)
    def on_vcsUrlPicker_textChanged(self, txt):
        """
        Private slot to handle changes of the URL.
        
        @param txt current text of the line edit (string)
        """
        enable = "://" not in txt
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enable)
        
    def getData(self):
        """
        Public slot to retrieve the data entered into the dialog.
        
        @return a tuple of a string (project directory) and a dictionary
            containing the data entered.
        """
        scheme = self.protocolCombo.currentText()
        url = self.vcsUrlPicker.text()
        vcsdatadict = {
            "url": '{0}{1}'.format(scheme, url),
            "tag": self.vcsTagEdit.text(),
            "standardLayout": self.layoutCheckBox.isChecked(),
        }
        return (self.vcsProjectDirPicker.text(), vcsdatadict)
