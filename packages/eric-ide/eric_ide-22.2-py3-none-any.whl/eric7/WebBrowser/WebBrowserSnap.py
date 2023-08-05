# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing functions to generate page previews.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter


def renderTabPreview(view, w, h):
    """
    Public function to render a pixmap of a page.
    
    @param view reference to the view to be previewed (QWebEngineView)
    @param w width of the preview pixmap (integer)
    @param h height of the preview pixmap (integer)
    @return preview pixmap (QPixmap)
    """
    pageImage = __render(view, view.width(), view.height())
    return pageImage.scaled(
        w, h,
        Qt.AspectRatioMode.IgnoreAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )


def __render(view, w, h):
    """
    Private function to render a pixmap of given size for a web page.
    
    @param view reference to the view to be previewed (QWebEngineView)
    @param w width of the pixmap (integer)
    @param h height of the pixmap (integer)
    @return rendered pixmap (QPixmap)
    """
    # create the page image
    pageImage = QPixmap(w, h)
    pageImage.fill(Qt.GlobalColor.transparent)
    
    # render it
    p = QPainter(pageImage)
    view.render(p)
    p.end()
    
    return pageImage
