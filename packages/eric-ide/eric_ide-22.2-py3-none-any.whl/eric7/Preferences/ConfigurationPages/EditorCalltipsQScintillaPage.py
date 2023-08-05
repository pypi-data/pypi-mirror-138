# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the QScintilla Calltips configuration page.
"""

from PyQt6.Qsci import QsciScintilla

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_EditorCalltipsQScintillaPage import Ui_EditorCalltipsQScintillaPage

import Preferences


class EditorCalltipsQScintillaPage(ConfigurationPageBase,
                                   Ui_EditorCalltipsQScintillaPage):
    """
    Class implementing the QScintilla Calltips configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setupUi(self)
        self.setObjectName("EditorCalltipsQScintillaPage")
        
        # set initial values
        ctContext = Preferences.getEditor("CallTipsStyle")
        if ctContext == QsciScintilla.CallTipsStyle.CallTipsNoContext:
            self.ctNoContextButton.setChecked(True)
        elif (
            ctContext ==
            QsciScintilla.CallTipsStyle.CallTipsNoAutoCompletionContext
        ):
            self.ctNoAutoCompletionButton.setChecked(True)
        elif ctContext == QsciScintilla.CallTipsStyle.CallTipsContext:
            self.ctContextButton.setChecked(True)
        
    def save(self):
        """
        Public slot to save the EditorCalltips configuration.
        """
        if self.ctNoContextButton.isChecked():
            Preferences.setEditor(
                "CallTipsStyle",
                QsciScintilla.CallTipsStyle.CallTipsNoContext)
        elif self.ctNoAutoCompletionButton.isChecked():
            Preferences.setEditor(
                "CallTipsStyle",
                QsciScintilla.CallTipsStyle.CallTipsNoAutoCompletionContext)
        elif self.ctContextButton.isChecked():
            Preferences.setEditor(
                "CallTipsStyle",
                QsciScintilla.CallTipsStyle.CallTipsContext)


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = EditorCalltipsQScintillaPage()
    return page
