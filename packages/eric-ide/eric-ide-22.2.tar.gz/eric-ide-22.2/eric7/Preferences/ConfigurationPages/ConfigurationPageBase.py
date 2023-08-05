# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the base class for all configuration pages.
"""

from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtWidgets import QWidget, QColorDialog, QFontDialog, QDialog


class ConfigurationPageBase(QWidget):
    """
    Class implementing the base class for all configuration pages.
    
    @signal colourChanged(str, QColor) To inform about a new colour selection
    """
    colourChanged = pyqtSignal(str, QColor)
    
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        
        self.__coloursDict = {}
        
    def polishPage(self):
        """
        Public slot to perform some polishing actions.
        """
        return
        
    def saveState(self):
        """
        Public method to save the current state of the widget.
        """
        return
        
    def setState(self, state):
        """
        Public method to set the state of the widget.
        
        @param state state data generated by saveState
        """
        return
        
    def initColour(self, colourKey, button, prefMethod, byName=False,
                   hasAlpha=False):
        """
        Public method to initialize a colour selection button.
        
        @param colourKey key of the colour resource (string)
        @param button reference to a button to show the colour on (QPushButton)
        @param prefMethod preferences method to get the colour
        @param byName flag indicating to retrieve/save by colour name
            (boolean)
        @param hasAlpha flag indicating to allow alpha channel (boolean)
        """
        colour = QColor(prefMethod(colourKey))
        size = button.size()
        pm = QPixmap(size.width() // 2, size.height() // 2)
        pm.fill(colour)
        button.setIconSize(pm.size())
        button.setIcon(QIcon(pm))
        button.setProperty("colorKey", colourKey)
        button.setProperty("hasAlpha", hasAlpha)
        button.clicked.connect(lambda: self.__selectColourSlot(button))
        self.__coloursDict[colourKey] = [colour, byName]
        self.colourChanged.emit(colourKey, colour)
        
    @pyqtSlot()
    def __selectColourSlot(self, button):
        """
        Private slot to select a color.
        
        @param button reference to the button been pressed
        @type QPushButton
        """
        colorKey = button.property("colorKey")
        hasAlpha = button.property("hasAlpha")
        
        colDlg = QColorDialog(self)
        if hasAlpha:
            colDlg.setOptions(QColorDialog.ColorDialogOption.ShowAlphaChannel)
        # Set current color last to avoid conflicts with alpha channel
        colDlg.setCurrentColor(self.__coloursDict[colorKey][0])
        colDlg.currentColorChanged.connect(
            lambda col: self.colourChanged.emit(colorKey, col))
        colDlg.exec()
        
        if colDlg.result() == QDialog.DialogCode.Accepted:
            colour = colDlg.selectedColor()
            size = button.iconSize()
            pm = QPixmap(size.width(), size.height())
            pm.fill(colour)
            button.setIcon(QIcon(pm))
            self.__coloursDict[colorKey][0] = colour
        
        # Update color selection
        self.colourChanged.emit(colorKey, self.__coloursDict[colorKey][0])
        
    def saveColours(self, prefMethod):
        """
        Public method to save the colour selections.
        
        @param prefMethod preferences method to set the colour
        """
        for key in self.__coloursDict:
            if self.__coloursDict[key][1]:
                prefMethod(key, self.__coloursDict[key][0].name())
            else:
                prefMethod(key, self.__coloursDict[key][0])
        
    def selectFont(self, fontSample, fontVar, showFontInfo=False,
                   options=None):
        """
        Public method used by the font selection buttons.
        
        @param fontSample reference to the font sample widget (QLineEdit)
        @param fontVar reference to the variable containing the font (QFont)
        @param showFontInfo flag indicating to show some font info
            as the sample (boolean)
        @param options options for the font dialog
            (QFontDialog.FontDialogOption)
        @return selected font (QFont)
        """
        if options is None:
            options = QFontDialog.FontDialogOption(0)
        font, ok = QFontDialog.getFont(fontVar, self, "", options)
        if ok:
            fontSample.setFont(font)
            if showFontInfo:
                fontSample.setText(
                    "{0} {1}".format(font.family(), font.pointSize()))
        else:
            font = fontVar
        return font  # __IGNORE_WARNING_M834__
