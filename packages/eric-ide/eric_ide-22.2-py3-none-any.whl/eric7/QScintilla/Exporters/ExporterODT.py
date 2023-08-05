# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing an exporter for ODT.
"""

from PyQt6.QtGui import QTextDocument, QTextDocumentWriter

from EricWidgets import EricMessageBox
from EricGui.EricOverrideCursor import EricOverrideCursor

from .ExporterBase import ExporterBase
from .ExporterHTML import HTMLGenerator

import Preferences


class ExporterODT(ExporterBase):
    """
    Class implementing an exporter for ODT.
    """
    def __init__(self, editor, parent=None):
        """
        Constructor
        
        @param editor reference to the editor object (QScintilla.Editor.Editor)
        @param parent parent object of the exporter (QObject)
        """
        ExporterBase.__init__(self, editor, parent)
    
    def exportSource(self):
        """
        Public method performing the export.
        """
        filename = self._getFileName(self.tr("ODT Files (*.odt)"))
        if not filename:
            return
        
        tabSize = self.editor.getEditorConfig("TabWidth")
        if tabSize == 0:
            tabSize = 4
        wysiwyg = Preferences.getEditorExporter("ODT/WYSIWYG")
        onlyStylesUsed = Preferences.getEditorExporter("ODT/OnlyStylesUsed")
        tabs = Preferences.getEditorExporter("ODT/UseTabs")
        
        with EricOverrideCursor():
            # generate HTML of the source
            generator = HTMLGenerator(self.editor)
            html = generator.generate(
                tabSize=tabSize,
                useTabs=tabs,
                wysiwyg=wysiwyg,
                folding=False,
                onlyStylesUsed=onlyStylesUsed,
                titleFullPath=False
            )
            
            # convert HTML to ODT
            doc = QTextDocument()
            doc.setHtml(html)
            writer = QTextDocumentWriter(filename)
            ok = writer.write(doc)
        
        if not ok:
            EricMessageBox.critical(
                self.editor,
                self.tr("Export source"),
                self.tr(
                    """<p>The source could not be exported to"""
                    """ <b>{0}</b>.</p>""").format(filename))
