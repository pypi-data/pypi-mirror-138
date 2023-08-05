# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a path picker widget.
"""

import enum
import os

from PyQt6.QtCore import pyqtSignal, Qt, QFileInfo, QCoreApplication, QDir
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QToolButton, QSizePolicy, QLineEdit, QComboBox
)

from . import EricFileDialog
from .EricCompleters import EricFileCompleter, EricDirCompleter

import UI.PixmapCache


class EricPathPickerModes(enum.Enum):
    """
    Class implementing the path picker modes.
    """
    OPEN_FILE_MODE = 0
    OPEN_FILES_MODE = 1
    SAVE_FILE_MODE = 2
    SAVE_FILE_ENSURE_EXTENSION_MODE = 3
    SAVE_FILE_OVERWRITE_MODE = 4
    DIRECTORY_MODE = 5
    DIRECTORY_SHOW_FILES_MODE = 6
    OPEN_FILES_AND_DIRS_MODE = 7
    CUSTOM_MODE = 99
    NO_MODE = 100


class EricPathPickerBase(QWidget):
    """
    Class implementing the base of a path picker widget consisting of a
    line edit or combo box and a tool button to open a file dialog.
    
    @signal textChanged(path) emitted when the entered path has changed
        (line edit based widget)
    @signal editTextChanged(path) emitted when the entered path has changed
        (combo box based widget)
    @signal pathSelected(path) emitted after a path has been selected via the
        file dialog
    @signal aboutToShowPathPickerDialog emitted before the file dialog is shown
    @signal pickerButtonClicked emitted when the picker button was pressed and
        the widget mode is custom
    """
    DefaultMode = EricPathPickerModes.NO_MODE
    
    textChanged = pyqtSignal(str)
    editTextChanged = pyqtSignal(str)
    pathSelected = pyqtSignal(str)
    aboutToShowPathPickerDialog = pyqtSignal()
    pickerButtonClicked = pyqtSignal()
    
    def __init__(self, parent=None, useLineEdit=True):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        @param useLineEdit flag indicating the use of a line edit
        @type bool
        """
        super().__init__(parent)
        
        self.__lineEditKind = useLineEdit
        
        self.__mode = EricPathPicker.DefaultMode
        self.__editorEnabled = True
        
        self._completer = None
        self.__filters = ""
        self.__defaultDirectory = ""
        self.__windowTitle = ""
        
        self.__layout = QHBoxLayout(self)
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)
        
        if useLineEdit:
            self._editor = QLineEdit(self)
            self._editor.setPlaceholderText(QCoreApplication.translate(
                "EricPathPickerBase", "Enter Path Name"))
            self._editor.setClearButtonEnabled(True)
        else:
            self._editor = QComboBox(self)
            self._editor.setEditable(True)
            self._editor.lineEdit().setPlaceholderText(
                QCoreApplication.translate(
                    "EricPathPickerBase", "Enter Path Name"))
            self._editor.lineEdit().setClearButtonEnabled(True)
        
        self.__button = QToolButton(self)
        self.__button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.__button.setIcon(UI.PixmapCache.getIcon("open"))
        
        self.__layout.addWidget(self._editor)
        self.__layout.addWidget(self.__button)
        
        self.__button.clicked.connect(self.__showPathPickerDialog)
        if useLineEdit:
            self._editor.textEdited.connect(self.__pathEdited)
            self._editor.textChanged.connect(self.textChanged)
        else:
            self._editor.editTextChanged.connect(self.editTextChanged)
        
        self.setFocusProxy(self._editor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Preferred)
        
        self.__button.setEnabled(self.__mode != EricPathPickerModes.NO_MODE)
    
    def __pathEdited(self, path):
        """
        Private slot handling editing of the path.
        
        @param path current text of the path line edit
        @type str
        """
        if self._completer and not self._completer.popup().isVisible():
            self._completer.setRootPath(QDir.toNativeSeparators(path))
    
    def setMode(self, mode):
        """
        Public method to set the path picker mode.
        
        @param mode picker mode
        @type EricPathPickerModes
        @exception ValueError raised to indicate a bad parameter value
        """
        if mode not in EricPathPickerModes:
            raise ValueError("Bad value for 'mode' parameter.")
        
        oldMode = self.__mode
        self.__mode = mode
        
        if mode != oldMode or (self.__lineEditKind and not self._completer):
            if self.__lineEditKind and self._completer:
                # Remove current completer
                self._editor.setCompleter(None)
                self._completer = None
            
            if mode != EricPathPickerModes.NO_MODE:
                if self.__lineEditKind:
                    # Set a new completer
                    if mode == EricPathPickerModes.DIRECTORY_MODE:
                        self._completer = EricDirCompleter(self._editor)
                    else:
                        self._completer = EricFileCompleter(self._editor)
                
                # set inactive text
                if mode in (
                    EricPathPickerModes.OPEN_FILES_MODE,
                    EricPathPickerModes.OPEN_FILES_AND_DIRS_MODE,
                ):
                    self._editor.setPlaceholderText(
                        self.tr("Enter Path Names separated by ';'"))
                else:
                    self._editor.setPlaceholderText(
                        self.tr("Enter Path Name"))
        self.__button.setEnabled(self.__mode != EricPathPickerModes.NO_MODE)
    
    def mode(self):
        """
        Public method to get the path picker mode.
        
        @return path picker mode
        @rtype EricPathPickerModes
        """
        return self.__mode
    
    def setPickerEnabled(self, enable):
        """
        Public method to set the enabled state of the file dialog button.
        
        @param enable flag indicating the enabled state
        @type bool
        """
        self.__button.setEnabled(enable)
    
    def isPickerEnabled(self):
        """
        Public method to get the file dialog button enabled state.
        
        @return flag indicating the enabled state
        @rtype bool
        """
        return self.__button.isEnabled()
    
    def clear(self):
        """
        Public method to clear the current path or list of paths.
        """
        self._editor.clear()
    
    def clearEditText(self):
        """
        Public method to clear the current path.
        """
        if not self.__lineEditKind:
            self._editor.clearEditText()
    
    def _setEditorText(self, text):
        """
        Protected method to set the text of the editor.
        
        @param text text to set
        @type str
        """
        if self.__lineEditKind:
            self._editor.setText(text)
        else:
            self._editor.setEditText(text)
            if text and self._editor.findText(text) == -1:
                self._editor.insertItem(0, text)
    
    def _editorText(self):
        """
        Protected method to get the text of the editor.
        
        @return text of the editor
        @rtype str
        """
        if self.__lineEditKind:
            return self._editor.text()
        else:
            return self._editor.currentText()
    
    def setText(self, path, toNative=True):
        """
        Public method to set the current path.
        
        @param path path to be set
        @type str
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        """
        if self.__mode in (
            EricPathPickerModes.OPEN_FILES_MODE,
            EricPathPickerModes.OPEN_FILES_AND_DIRS_MODE,
        ):
            self._setEditorText(path)
        else:
            if toNative:
                path = QDir.toNativeSeparators(path)
            self._setEditorText(path)
            if self._completer:
                self._completer.setRootPath(path)
    
    def text(self, toNative=True):
        """
        Public method to get the current path.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return current path
        @rtype str
        """
        if self.__mode in (
            EricPathPickerModes.OPEN_FILES_MODE,
            EricPathPickerModes.OPEN_FILES_AND_DIRS_MODE,
        ):
            if toNative:
                return ";".join(
                    [QDir.toNativeSeparators(path)
                     for path in self._editorText().split(";")])
            else:
                return self._editorText()
        else:
            if toNative:
                return os.path.expanduser(
                    QDir.toNativeSeparators(self._editorText()))
            else:
                return os.path.expanduser(self._editorText())
    
    def setEditText(self, path, toNative=True):
        """
        Public method to set the current path.
        
        @param path path to be set
        @type str
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        """
        self.setText(path, toNative=toNative)
    
    def currentText(self, toNative=True):
        """
        Public method to get the current path.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return current path
        @rtype str
        """
        return self.text(toNative=toNative)
    
    def setPath(self, path, toNative=True):
        """
        Public method to set the current path.
        
        @param path path to be set
        @type str
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        """
        self.setText(path, toNative=toNative)
    
    def path(self, toNative=True):
        """
        Public method to get the current path.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return current path
        @rtype str
        """
        return self.text(toNative=toNative)
    
    def paths(self, toNative=True):
        """
        Public method to get the list of entered paths.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return entered paths
        @rtype list of str
        """
        if self.__mode in (
            EricPathPickerModes.OPEN_FILES_MODE,
            EricPathPickerModes.OPEN_FILES_AND_DIRS_MODE,
        ):
            return self.path(toNative=toNative).split(";")
        else:
            return [self.path(toNative=toNative)]
    
    def firstPath(self, toNative=True):
        """
        Public method to get the first path of a list of entered paths.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return first path
        @rtype str
        """
        return self.paths(toNative=toNative)[0]
    
    def lastPath(self, toNative=True):
        """
        Public method to get the last path of a list of entered paths.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return last path
        @rtype str
        """
        return self.paths(toNative=toNative)[-1]
    
    def setEditorEnabled(self, enable):
        """
        Public method to set the path editor's enabled state.
        
        @param enable flag indicating the enable state
        @type bool
        """
        if enable != self._editorEnabled:
            self._editorEnabled = enable
            self._editor.setEnabled(enable)
    
    def editorEnabled(self):
        """
        Public method to get the path editor's enabled state.
        
        @return flag indicating the enabled state
        @rtype bool
        """
        return self._editorEnabled
    
    def setDefaultDirectory(self, directory):
        """
        Public method to set the default directory.
        
        @param directory default directory
        @type str
        """
        self.__defaultDirectory = directory
    
    def defaultDirectory(self):
        """
        Public method to get the default directory.
        
        @return default directory
        @rtype str
        """
        return self.__defaultDirectory
    
    def setWindowTitle(self, title):
        """
        Public method to set the path picker dialog window title.
        
        @param title window title
        @type str
        """
        self.__windowTitle = title
    
    def windowTitle(self):
        """
        Public method to get the path picker dialog's window title.
        
        @return window title
        @rtype str
        """
        return self.__windowTitle
    
    def setFilters(self, filters):
        """
        Public method to set the filters for the path picker dialog.
        
        Note: Multiple filters must be separated by ';;'.
        
        @param filters string containing the file filters
        @type str
        """
        self.__filters = filters
    
    def filters(self):
        """
        Public methods to get the filter string.
        
        @return filter string
        @rtype str
        """
        return self.__filters
    
    def setNameFilters(self, filters):
        """
        Public method to set the name filters for the completer.
        
        @param filters list of file name filters
        @type list of str
        """
        if self._completer:
            self._completer.model().setNameFilters(filters)
    
    def setButtonToolTip(self, tooltip):
        """
        Public method to set the tool button tool tip.
        
        @param tooltip text to be set as a tool tip
        @type str
        """
        self.__button.setToolTip(tooltip)
    
    def buttonToolTip(self):
        """
        Public method to get the tool button tool tip.
        
        @return tool tip text
        @rtype str
        """
        return self.__button.toolTip()
    
    def setEditorToolTip(self, tooltip):
        """
        Public method to set the editor tool tip.
        
        @param tooltip text to be set as a tool tip
        @type str
        """
        self._editor.setToolTip(tooltip)
    
    def editorToolTip(self):
        """
        Public method to get the editor tool tip.
        
        @return tool tip text
        @rtype str
        """
        return self._editor.toolTip()
    
    def __showPathPickerDialog(self):
        """
        Private slot to show the path picker dialog.
        """
        if self.__mode == EricPathPickerModes.NO_MODE:
            return
        
        if self.__mode == EricPathPickerModes.CUSTOM_MODE:
            self.pickerButtonClicked.emit()
            return
        
        self.aboutToShowPathPickerDialog.emit()
        
        windowTitle = self.__windowTitle
        if not windowTitle:
            if self.__mode == EricPathPickerModes.OPEN_FILE_MODE:
                windowTitle = self.tr("Choose a file to open")
            elif self.__mode == EricPathPickerModes.OPEN_FILES_MODE:
                windowTitle = self.tr("Choose files to open")
            elif self.__mode == EricPathPickerModes.OPEN_FILES_AND_DIRS_MODE:
                windowTitle = self.tr("Choose files and directories")
            elif self.__mode in [
                EricPathPickerModes.SAVE_FILE_MODE,
                    EricPathPickerModes.SAVE_FILE_ENSURE_EXTENSION_MODE,
                    EricPathPickerModes.SAVE_FILE_OVERWRITE_MODE]:
                windowTitle = self.tr("Choose a file to save")
            elif self.__mode == EricPathPickerModes.DIRECTORY_MODE:
                windowTitle = self.tr("Choose a directory")
        
        directory = self._editorText()
        if not directory and self.__defaultDirectory:
            directory = self.__defaultDirectory
        directory = (
            os.path.expanduser(directory.split(";")[0])
            if self.__mode in (
                EricPathPickerModes.OPEN_FILES_MODE,
                EricPathPickerModes.OPEN_FILES_AND_DIRS_MODE) else
            os.path.expanduser(directory)
        )
        if not os.path.isabs(directory) and self.__defaultDirectory:
            directory = os.path.join(self.__defaultDirectory, directory)
        directory = QDir.fromNativeSeparators(directory)
        
        if self.__mode == EricPathPickerModes.OPEN_FILE_MODE:
            path = EricFileDialog.getOpenFileName(
                self,
                windowTitle,
                directory,
                self.__filters)
            path = QDir.toNativeSeparators(path)
        elif self.__mode == EricPathPickerModes.OPEN_FILES_MODE:
            paths = EricFileDialog.getOpenFileNames(
                self,
                windowTitle,
                directory,
                self.__filters)
            path = ";".join([QDir.toNativeSeparators(path)
                             for path in paths])
        elif self.__mode == EricPathPickerModes.OPEN_FILES_AND_DIRS_MODE:
            paths = EricFileDialog.getOpenFileAndDirNames(
                self,
                windowTitle,
                directory,
                self.__filters)
            path = ";".join([QDir.toNativeSeparators(path)
                             for path in paths])
        elif self.__mode == EricPathPickerModes.SAVE_FILE_MODE:
            path = EricFileDialog.getSaveFileName(
                self,
                windowTitle,
                directory,
                self.__filters,
                EricFileDialog.DontConfirmOverwrite)
            path = QDir.toNativeSeparators(path)
        elif (
            self.__mode == EricPathPickerModes.SAVE_FILE_ENSURE_EXTENSION_MODE
        ):
            path, selectedFilter = EricFileDialog.getSaveFileNameAndFilter(
                self,
                windowTitle,
                directory,
                self.__filters,
                None,
                EricFileDialog.DontConfirmOverwrite)
            path = QDir.toNativeSeparators(path)
            if path:
                ext = QFileInfo(path).suffix()
                if not ext:
                    ex = selectedFilter.split("(*")[1].split(")")[0]
                    if ex:
                        path += ex
        elif self.__mode == EricPathPickerModes.SAVE_FILE_OVERWRITE_MODE:
            path = EricFileDialog.getSaveFileName(
                self,
                windowTitle,
                directory,
                self.__filters)
            path = QDir.toNativeSeparators(path)
        elif self.__mode == EricPathPickerModes.DIRECTORY_MODE:
            path = EricFileDialog.getExistingDirectory(
                self,
                windowTitle,
                directory,
                EricFileDialog.ShowDirsOnly)
            path = QDir.toNativeSeparators(path)
            while path.endswith(os.sep):
                path = path[:-1]
        elif self.__mode == EricPathPickerModes.DIRECTORY_SHOW_FILES_MODE:
            path = EricFileDialog.getExistingDirectory(
                self,
                windowTitle,
                directory,
                EricFileDialog.DontUseNativeDialog)
            path = QDir.toNativeSeparators(path)
            while path.endswith(os.sep):
                path = path[:-1]
        
        if path:
            self._setEditorText(path)
            self.pathSelected.emit(path)
    
    def setReadOnly(self, readOnly):
        """
        Public method to set the path picker to read only mode.
        
        @param readOnly flag indicating read only mode
        @type bool
        """
        try:
            self._editor.setReadOnly(readOnly)
        except AttributeError:
            self._editor.setEditable(not readOnly)
        self.setPickerEnabled(not readOnly)
    
    def isReadOnly(self):
        """
        Public method to check the path picker for read only mode.
        
        @return flg indicating read only mode
        @rtype bool
        """
        try:
            return self._editor.isReadOnly()
        except AttributeError:
            return not self._editor.isEditable()
    
    ##################################################################
    ## Methods below emulate some of the QComboBox API
    ##################################################################
    
    def addItems(self, pathsList):
        """
        Public method to add paths to the current list.
        
        @param pathsList list of paths to add
        @type list of str
        """
        self._editor.addItems(pathsList)
    
    def addItem(self, path):
        """
        Public method to add a paths to the current list.
        
        @param path path to add
        @type str
        """
        self._editor.addItem(path)
    
    def setPathsList(self, pathsList):
        """
        Public method to set the paths list.
        
        @param pathsList list of paths
        @type list of str
        """
        self.clear()
        self.addItems(pathsList)
    
    def setCurrentIndex(self, index):
        """
        Public slot to set the current index.
        
        @param index index of the item to set current
        @type int
        """
        self._editor.setCurrentIndex(index)
    
    def setInsertPolicy(self, policy):
        """
        Public method to set the insertion policy of the combo box.
        
        @param policy insertion policy
        @type QComboBox.InsertPolicy
        """
        self._editor.setInsertPolicy(policy)
    
    def setSizeAdjustPolicy(self, policy):
        """
        Public method to set the size adjust policy of the combo box.
        
        @param policy size adjust policy
        @type QComboBox.SizeAdjustPolicy
        """
        self._editor.setSizeAdjustPolicy(policy)


class EricPathPicker(EricPathPickerBase):
    """
    Class implementing a path picker widget consisting of a line edit and a
    tool button to open a file dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent, useLineEdit=True)


class EricComboPathPicker(EricPathPickerBase):
    """
    Class implementing a path picker widget consisting of a combobox and a
    tool button to open a file dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent, useLineEdit=False)
    
    def getPathItems(self):
        """
        Public method to get the list of remembered paths.
        
        @return list od remembered paths
        @rtype list of str
        """
        paths = []
        for index in range(self._editor.count()):
            paths.append(self._editor.itemText(index))
        return paths
