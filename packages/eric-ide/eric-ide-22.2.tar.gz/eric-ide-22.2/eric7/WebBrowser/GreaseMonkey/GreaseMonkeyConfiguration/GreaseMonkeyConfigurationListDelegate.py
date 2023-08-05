# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a delegate for the special list widget for GreaseMonkey
scripts.
"""

from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QFontMetrics, QPalette, QFont
from PyQt6.QtWidgets import QStyle, QStyledItemDelegate, QApplication
from PyQt6.QtWidgets import QStyleOptionViewItem

import UI.PixmapCache
import Globals


class GreaseMonkeyConfigurationListDelegate(QStyledItemDelegate):
    """
    Class implementing a delegate for the special list widget for GreaseMonkey
    scripts.
    """
    IconSize = 32
    RemoveIconSize = 16
    CheckBoxSize = 18
    MinPadding = 5
    ItemWidth = 200
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent object (QObject)
        """
        super().__init__(parent)
        
        self.__removePixmap = UI.PixmapCache.getIcon(
            "greaseMonkeyTrash").pixmap(
                GreaseMonkeyConfigurationListDelegate.RemoveIconSize)
        self.__rowHeight = 0
        self.__padding = 0
    
    def padding(self):
        """
        Public method to get the padding used.
        
        @return padding used (integer)
        """
        return self.__padding
    
    def paint(self, painter, option, index):
        """
        Public method to paint the specified list item.
        
        @param painter painter object to paint to (QPainter)
        @param option style option used for painting (QStyleOptionViewItem)
        @param index model index of the item (QModelIndex)
        """
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        
        widget = opt.widget
        style = widget.style() if widget is not None else QApplication.style()
        height = opt.rect.height()
        center = height // 2 + opt.rect.top()
        
        # Prepare title font
        titleFont = QFont(opt.font)
        titleFont.setBold(True)
        titleFont.setPointSize(titleFont.pointSize() + 1)
        
        titleMetrics = QFontMetrics(titleFont)
        colorRole = (
            QPalette.ColorRole.Text
            if Globals.isWindowsPlatform() else
            (QPalette.ColorRole.HighlightedText
             if opt.state & QStyle.StateFlag.State_Selected else
             QPalette.ColorRole.Text)
        )
        
        leftPos = self.__padding
        rightPos = (
            opt.rect.right() - self.__padding -
            GreaseMonkeyConfigurationListDelegate.RemoveIconSize
        )
        
        # Draw background
        style.drawPrimitive(
            QStyle.PrimitiveElement.PE_PanelItemViewItem, opt, painter, widget)
        
        # Draw checkbox
        checkBoxYPos = (
            center -
            GreaseMonkeyConfigurationListDelegate.CheckBoxSize // 2
        )
        opt2 = QStyleOptionViewItem(opt)
        if opt2.checkState == Qt.CheckState.Checked:
            opt2.state |= QStyle.StateFlag.State_On
        else:
            opt2.state |= QStyle.StateFlag.State_Off
        styleCheckBoxRect = style.subElementRect(
            QStyle.SubElement.SE_ViewItemCheckIndicator, opt2, widget)
        opt2.rect = QRect(
            leftPos, checkBoxYPos,
            styleCheckBoxRect.width(), styleCheckBoxRect.height())
        style.drawPrimitive(
            QStyle.PrimitiveElement.PE_IndicatorViewItemCheck, opt2, painter,
            widget)
        leftPos = opt2.rect.right() + self.__padding
        
        # Draw icon
        iconYPos = center - GreaseMonkeyConfigurationListDelegate.IconSize // 2
        iconRect = QRect(leftPos, iconYPos,
                         GreaseMonkeyConfigurationListDelegate.IconSize,
                         GreaseMonkeyConfigurationListDelegate.IconSize)
        pixmap = index.data(Qt.ItemDataRole.DecorationRole).pixmap(
            GreaseMonkeyConfigurationListDelegate.IconSize)
        painter.drawPixmap(iconRect, pixmap)
        leftPos = iconRect.right() + self.__padding
        
        # Draw script name
        name = index.data(Qt.ItemDataRole.DisplayRole)
        leftTitleEdge = leftPos + 2
        rightTitleEdge = rightPos - self.__padding
        try:
            leftPosForVersion = (
                titleMetrics.horizontalAdvance(name) + self.__padding
            )
        except AttributeError:
            leftPosForVersion = titleMetrics.width(name) + self.__padding
        nameRect = QRect(leftTitleEdge, opt.rect.top() + self.__padding,
                         rightTitleEdge - leftTitleEdge, titleMetrics.height())
        painter.setFont(titleFont)
        style.drawItemText(
            painter, nameRect,
            Qt.AlignmentFlag.AlignLeft, opt.palette, True,
            name, colorRole)
        
        # Draw version
        version = index.data(Qt.ItemDataRole.UserRole)
        versionRect = QRect(
            nameRect.x() + leftPosForVersion, nameRect.y(),
            rightTitleEdge - leftTitleEdge, titleMetrics.height())
        versionFont = titleFont
        painter.setFont(versionFont)
        style.drawItemText(
            painter, versionRect,
            Qt.AlignmentFlag.AlignLeft, opt.palette,
            True, version, colorRole)
        
        # Draw description
        infoYPos = nameRect.bottom() + opt.fontMetrics.leading()
        infoRect = QRect(
            nameRect.x(), infoYPos,
            nameRect.width(), opt.fontMetrics.height())
        info = opt.fontMetrics.elidedText(
            index.data(Qt.ItemDataRole.UserRole + 1),
            Qt.TextElideMode.ElideRight, infoRect.width())
        painter.setFont(opt.font)
        style.drawItemText(
            painter, infoRect,
            Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextSingleLine,
            opt.palette, True, info, colorRole)
        
        # Draw remove button
        removeIconYPos = (
            center -
            GreaseMonkeyConfigurationListDelegate.RemoveIconSize // 2
        )
        removeIconRect = QRect(
            rightPos, removeIconYPos,
            GreaseMonkeyConfigurationListDelegate.RemoveIconSize,
            GreaseMonkeyConfigurationListDelegate.RemoveIconSize)
        painter.drawPixmap(removeIconRect, self.__removePixmap)
    
    def sizeHint(self, option, index):
        """
        Public method to get a size hint for the specified list item.
        
        @param option style option used for painting (QStyleOptionViewItem)
        @param index model index of the item (QModelIndex)
        @return size hint (QSize)
        """
        if not self.__rowHeight:
            opt = QStyleOptionViewItem(option)
            self.initStyleOption(opt, index)
            
            widget = opt.widget
            style = (
                widget.style() if widget is not None
                else QApplication.style()
            )
            padding = style.pixelMetric(
                QStyle.PixelMetric.PM_FocusFrameHMargin) + 1
            
            titleFont = opt.font
            titleFont.setBold(True)
            titleFont.setPointSize(titleFont.pointSize() + 1)
            
            self.__padding = (
                padding
                if padding > GreaseMonkeyConfigurationListDelegate.MinPadding
                else GreaseMonkeyConfigurationListDelegate.MinPadding
            )
            
            titleMetrics = QFontMetrics(titleFont)
            
            self.__rowHeight = (
                2 * self.__padding +
                opt.fontMetrics.leading() +
                opt.fontMetrics.height() +
                titleMetrics.height()
            )
        
        return QSize(GreaseMonkeyConfigurationListDelegate.ItemWidth,
                     self.__rowHeight)
