# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to generate a requirements file for conda.
"""

import os

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QAbstractButton, QApplication
)

from EricWidgets import EricMessageBox, EricFileDialog
from EricWidgets.EricPathPicker import EricPathPickerModes
from EricWidgets.EricApplication import ericApp
from EricGui.EricOverrideCursor import EricOverrideCursor

from .Ui_CondaExportDialog import Ui_CondaExportDialog


class CondaExportDialog(QDialog, Ui_CondaExportDialog):
    """
    Class implementing a dialog to generate a requirements file for conda.
    """
    def __init__(self, conda, envName, envPrefix, parent=None):
        """
        Constructor
        
        @param conda reference to the master object
        @type Conda
        @param envName name of the environment to create the requirements
            file from
        @type str
        @param envPrefix prefix of the environment to create the requirements
            file from
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.__refreshButton = self.buttonBox.addButton(
            self.tr("&Refresh"), QDialogButtonBox.ButtonRole.ActionRole)
        
        self.requirementsFilePicker.setMode(EricPathPickerModes.SAVE_FILE_MODE)
        self.requirementsFilePicker.setFilters(
            self.tr("Text Files (*.txt);;All Files (*)"))
        
        self.__conda = conda
        self.__prefix = envPrefix
        
        self.environmentLabel.setText("<b>{0}</b>".format(envName))
        
        self.__requirementsEdited = False
        self.__requirementsAvailable = False
        
        self.__updateButtons()
    
    def closeEvent(self, e):
        """
        Protected slot implementing a close event handler.
        
        @param e close event
        @type QCloseEvent
        """
        e.accept()
    
    @pyqtSlot(str)
    def on_requirementsFilePicker_textChanged(self, txt):
        """
        Private slot handling a change of the requirements file name.
        
        @param txt name of the requirements file
        @type str
        """
        self.__updateButtons()
    
    @pyqtSlot()
    def on_requirementsEdit_textChanged(self):
        """
        Private slot handling changes of the requirements text.
        """
        self.__requirementsEdited = True
    
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked
        @type QAbstractButton
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
        elif button == self.__refreshButton:
            self.__refresh()
    
    def __refresh(self):
        """
        Private slot to refresh the displayed list.
        """
        ok = (
            EricMessageBox.yesNo(
                self,
                self.tr("Generate Requirements"),
                self.tr("""The requirements were changed. Do you want"""
                        """ to overwrite these changes?"""))
            if self.__requirementsEdited else
            True
        )
        if ok:
            self.start()
    
    def start(self):
        """
        Public method to start the command.
        """
        self.requirementsEdit.clear()
        self.__requirementsAvailable = False
        
        args = [
            "list",
            "--export",
            "--prefix",
            self.__prefix,
        ]
        
        with EricOverrideCursor():
            success, output = self.__conda.runProcess(args)
            
            if success:
                self.requirementsEdit.setPlainText(output)
                self.__requirementsAvailable = True
            else:
                self.requirementsEdit.setPlainText(
                    self.tr("No output generated by conda."))
        
        self.__updateButtons()
        
        self.__requirementsEdited = False
    
    def __updateButtons(self):
        """
        Private method to set the state of the various buttons.
        """
        self.saveButton.setEnabled(
            self.__requirementsAvailable and
            bool(self.requirementsFilePicker.text())
        )
        self.saveToButton.setEnabled(self.__requirementsAvailable)
        self.copyButton.setEnabled(self.__requirementsAvailable)
        
        aw = ericApp().getObject("ViewManager").activeWindow()
        if aw and self.__requirementsAvailable:
            self.insertButton.setEnabled(True)
            self.replaceAllButton.setEnabled(True)
            self.replaceSelectionButton.setEnabled(
                aw.hasSelectedText())
        else:
            self.insertButton.setEnabled(False)
            self.replaceAllButton.setEnabled(False)
            self.replaceSelectionButton.setEnabled(False)
    
    def __writeToFile(self, fileName):
        """
        Private method to write the requirements text to a file.
        
        @param fileName name of the file to write to
        @type str
        """
        if os.path.exists(fileName):
            ok = EricMessageBox.warning(
                self,
                self.tr("Generate Requirements"),
                self.tr("""The file <b>{0}</b> already exists. Do you want"""
                        """ to overwrite it?""").format(fileName))
            if not ok:
                return
        
        try:
            with open(fileName, "w") as f:
                f.write(self.requirementsEdit.toPlainText())
        except OSError as err:
            EricMessageBox.critical(
                self,
                self.tr("Generate Requirements"),
                self.tr("""<p>The requirements could not be written"""
                        """ to <b>{0}</b>.</p><p>Reason: {1}</p>""")
                .format(fileName, str(err)))
    
    @pyqtSlot()
    def on_saveButton_clicked(self):
        """
        Private slot to save the requirements text to the requirements file.
        """
        fileName = self.requirementsFilePicker.text()
        self.__writeToFile(fileName)
    
    @pyqtSlot()
    def on_saveToButton_clicked(self):
        """
        Private slot to write the requirements text to a new file.
        """
        fileName, selectedFilter = EricFileDialog.getSaveFileNameAndFilter(
            self,
            self.tr("Generate Requirements"),
            os.path.expanduser("~"),
            self.tr("Text Files (*.txt);;All Files (*)"),
            None,
            EricFileDialog.DontConfirmOverwrite
        )
        if fileName:
            ext = os.path.splitext(fileName)[1]
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fileName += ex
            self.__writeToFile(fileName)
    
    @pyqtSlot()
    def on_copyButton_clicked(self):
        """
        Private slot to copy the requirements text to the clipboard.
        """
        txt = self.requirementsEdit.toPlainText()
        cb = QApplication.clipboard()
        cb.setText(txt)
    
    @pyqtSlot()
    def on_insertButton_clicked(self):
        """
        Private slot to insert the requirements text at the cursor position
        of the current editor.
        """
        aw = ericApp().getObject("ViewManager").activeWindow()
        if aw:
            aw.beginUndoAction()
            cline, cindex = aw.getCursorPosition()
            aw.insertAt(self.requirementsEdit.toPlainText(), cline, cindex)
            aw.endUndoAction()
    
    @pyqtSlot()
    def on_replaceSelectionButton_clicked(self):
        """
        Private slot to replace the selected text of the current editor
        with the requirements text.
        """
        aw = ericApp().getObject("ViewManager").activeWindow()
        if aw:
            aw.beginUndoAction()
            aw.replaceSelectedText(self.requirementsEdit.toPlainText())
            aw.endUndoAction()
    
    @pyqtSlot()
    def on_replaceAllButton_clicked(self):
        """
        Private slot to replace the text of the current editor with the
        requirements text.
        """
        aw = ericApp().getObject("ViewManager").activeWindow()
        if aw:
            aw.setText(self.requirementsEdit.toPlainText())
