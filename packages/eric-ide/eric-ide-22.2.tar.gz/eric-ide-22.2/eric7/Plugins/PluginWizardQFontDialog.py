# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the QFontDialog wizard plugin.
"""

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QDialog

from EricWidgets.EricApplication import ericApp
from EricGui.EricAction import EricAction
from EricWidgets import EricMessageBox

import UI.Info

# Start-Of-Header
name = "QFontDialog Wizard Plugin"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = True
deactivateable = True
version = UI.Info.VersionOnly
className = "FontDialogWizard"
packageName = "__core__"
shortDescription = "Show the QFontDialog wizard."
longDescription = """This plugin shows the QFontDialog wizard."""
pyqtApi = 2
# End-Of-Header

error = ""


class FontDialogWizard(QObject):
    """
    Class implementing the QFontDialog wizard plugin.
    """
    def __init__(self, ui):
        """
        Constructor
        
        @param ui reference to the user interface object (UI.UserInterface)
        """
        super().__init__(ui)
        self.__ui = ui

    def activate(self):
        """
        Public method to activate this plugin.
        
        @return tuple of None and activation status (boolean)
        """
        self.__initAction()
        self.__initMenu()
        
        return None, True

    def deactivate(self):
        """
        Public method to deactivate this plugin.
        """
        menu = self.__ui.getMenu("wizards")
        if menu:
            menu.removeAction(self.action)
        self.__ui.removeEricActions([self.action], 'wizards')
    
    def __initAction(self):
        """
        Private method to initialize the action.
        """
        self.action = EricAction(
            self.tr('QFontDialog Wizard'),
            self.tr('QFontDialog Wizard...'), 0, 0, self,
            'wizards_qfontdialog')
        self.action.setStatusTip(self.tr('QFontDialog Wizard'))
        self.action.setWhatsThis(self.tr(
            """<b>QFontDialog Wizard</b>"""
            """<p>This wizard opens a dialog for entering all the parameters"""
            """ needed to create a QFontDialog. The generated code is"""
            """ inserted at the current cursor position.</p>"""
        ))
        self.action.triggered.connect(self.__handle)
        
        self.__ui.addEricActions([self.action], 'wizards')

    def __initMenu(self):
        """
        Private method to add the actions to the right menu.
        """
        menu = self.__ui.getMenu("wizards")
        if menu:
            menu.addAction(self.action)
    
    def __callForm(self, editor):
        """
        Private method to display a dialog and get the code.
        
        @param editor reference to the current editor
        @return the generated code (string)
        """
        from WizardPlugins.FontDialogWizard.FontDialogWizardDialog import (
            FontDialogWizardDialog
        )
        dlg = FontDialogWizardDialog(None)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            line, index = editor.getCursorPosition()
            indLevel = editor.indentation(line) // editor.indentationWidth()
            if editor.indentationsUseTabs():
                indString = '\t'
            else:
                indString = editor.indentationWidth() * ' '
            return (dlg.getCode(indLevel, indString), True)
        else:
            return (None, False)
        
    def __handle(self):
        """
        Private method to handle the wizards action.
        """
        editor = ericApp().getObject("ViewManager").activeWindow()
        
        if editor is None:
            EricMessageBox.critical(
                self.__ui,
                self.tr('No current editor'),
                self.tr('Please open or create a file first.'))
        else:
            code, ok = self.__callForm(editor)
            if ok:
                line, index = editor.getCursorPosition()
                # It should be done on this way to allow undo
                editor.beginUndoAction()
                editor.insertAt(code, line, index)
                editor.endUndoAction()
