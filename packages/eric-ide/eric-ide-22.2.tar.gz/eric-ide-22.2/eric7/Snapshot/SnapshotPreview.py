# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the snapshot preview label.
"""

from PyQt6.QtCore import pyqtSignal, QPoint, Qt
from PyQt6.QtWidgets import QLabel, QApplication


class SnapshotPreview(QLabel):
    """
    Class implementing the snapshot preview label.
    
    @signal startDrag() emitted to indicate the start of a drag operation
    """
    startDrag = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter |
                          Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        
        self.__mouseClickPoint = QPoint(0, 0)
    
    def setPreview(self, preview):
        """
        Public slot to set the preview picture.
        
        @param preview preview picture to be shown (QPixmap)
        """
        pixmap = (
            preview.scaled(
                self.width(), self.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            if not preview.isNull() else
            preview
        )
        self.setPixmap(pixmap)
    
    def mousePressEvent(self, evt):
        """
        Protected method to handle mouse button presses.
        
        @param evt mouse button press event (QMouseEvent)
        """
        if evt.button() == Qt.MouseButton.LeftButton:
            self.__mouseClickPoint = evt.position().toPoint()
    
    def mouseReleaseEvent(self, evt):
        """
        Protected method to handle mouse button releases.
        
        @param evt mouse button release event (QMouseEvent)
        """
        self.__mouseClickPoint = QPoint(0, 0)
    
    def mouseMoveEvent(self, evt):
        """
        Protected method to handle mouse moves.
        
        @param evt mouse move event (QMouseEvent)
        """
        if (
            self.__mouseClickPoint != QPoint(0, 0) and (
                evt.position().toPoint() - self.__mouseClickPoint
            ).manhattanLength() > QApplication.startDragDistance()
        ):
            self.__mouseClickPoint = QPoint(0, 0)
            self.startDrag.emit()
