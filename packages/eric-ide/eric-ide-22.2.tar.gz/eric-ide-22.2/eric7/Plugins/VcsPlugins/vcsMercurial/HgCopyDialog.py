# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a copy or rename operation.
"""

import os.path

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_HgCopyDialog import Ui_HgCopyDialog


class HgCopyDialog(QDialog, Ui_HgCopyDialog):
    """
    Class implementing a dialog to enter the data for a copy or rename
    operation.
    """
    def __init__(self, source, parent=None, move=False):
        """
        Constructor
        
        @param source name of the source file/directory (string)
        @param parent parent widget (QWidget)
        @param move flag indicating a move operation (boolean)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.source = source
        if os.path.isdir(self.source):
            self.targetPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        else:
            self.targetPicker.setMode(EricPathPickerModes.SAVE_FILE_MODE)
        
        if move:
            self.setWindowTitle(self.tr('Mercurial Move'))
        else:
            self.forceCheckBox.setEnabled(False)
        
        self.sourceEdit.setText(source)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def getData(self):
        """
        Public method to retrieve the copy data.
        
        @return the target name (string) and a flag indicating
            the operation should be enforced (boolean)
        """
        target = self.targetPicker.text()
        if not os.path.isabs(target):
            sourceDir = os.path.dirname(self.sourceEdit.text())
            target = os.path.join(sourceDir, target)
        return target, self.forceCheckBox.isChecked()
    
    @pyqtSlot(str)
    def on_targetPicker_textChanged(self, txt):
        """
        Private slot to handle changes of the target.
        
        @param txt contents of the target edit (string)
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            os.path.isabs(txt) or os.path.dirname(txt) == "")
