# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing an animated widget.
"""

#
# Code was inspired by qupzilla web browser
#

from PyQt6.QtCore import pyqtSlot, QTimeLine, QPoint
from PyQt6.QtWidgets import QWidget


class EricAnimatedWidget(QWidget):
    """
    Class implementing an animated widget.
    """
    DirectionDown = 0
    DirectionUp = 1
    
    def __init__(self, direction=DirectionDown, duration=300, parent=None):
        """
        Constructor
        
        @param direction direction of the animation
        @type int (one of DirectionDown or DirectionUp)
        @param duration duration of the animation
        @type int
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        
        self.__direction = direction
        self.__stepHeight = 0.0
        self.__stepY = 0.0
        self.__startY = 0
        self.__widget = QWidget(self)
        
        self.__timeline = QTimeLine(duration)
        self.__timeline.setFrameRange(0, 100)
        self.__timeline.frameChanged.connect(self.__animateFrame)
        
        self.setMaximumHeight(0)
    
    def widget(self):
        """
        Public method to get a reference to the animated widget.
        
        @return reference to the animated widget
        @rtype QWidget
        """
        return self.__widget
    
    @pyqtSlot()
    def startAnimation(self):
        """
        Public slot to start the animation.
        """
        if self.__timeline.state() == QTimeLine.State.Running:
            return
        
        shown = 0
        hidden = 0
        
        if self.__direction == self.DirectionDown:
            shown = 0
            hidden = -self.__widget.height()
        
        self.__widget.move(QPoint(self.__widget.pos().x(), hidden))
        
        self.__stepY = (hidden - shown) / 100.0
        self.__startY = hidden
        self.__stepHeight = self.__widget.height() / 100.0
        
        self.__timeline.setDirection(QTimeLine.Direction.Forward)
        self.__timeline.start()
    
    @pyqtSlot(int)
    def __animateFrame(self, frame):
        """
        Private slot to animate the next frame.
        
        @param frame frame number
        @type int
        """
        self.setFixedHeight(frame * self.__stepHeight)
        self.__widget.move(self.pos().x(),
                           self.__startY - frame * self.__stepY)
    
    @pyqtSlot()
    def hide(self):
        """
        Public slot to hide the animated widget.
        """
        if self.__timeline.state() == QTimeLine.State.Running:
            return
        
        self.__timeline.setDirection(QTimeLine.Direction.Backward)
        self.__timeline.finished.connect(self.close)
        self.__timeline.start()
        
        p = self.parentWidget()
        if p is not None:
            p.setFocus()
    
    def resizeEvent(self, evt):
        """
        Protected method to handle a resize event.
        
        @param evt reference to the event object
        @type QResizeEvent
        """
        if evt.size().width() != self.__widget.width():
            self.__widget.resize(evt.size().width(), self.__widget.height())
        
        super().resizeEvent(evt)
