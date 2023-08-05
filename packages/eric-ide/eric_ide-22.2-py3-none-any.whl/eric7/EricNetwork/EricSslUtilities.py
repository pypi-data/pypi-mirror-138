# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing SSL utility functions.
"""


def initSSL():
    """
    Function to initialize some global SSL stuff.
    """
    blacklist = [
        "SRP-AES-256-CBC-SHA",          # open to MitM
        "SRP-AES-128-CBC-SHA",          # open to MitM
    ]
    
    try:
        from PyQt6.QtNetwork import QSslConfiguration
    except ImportError:
        # no SSL available, so there is nothing to initialize
        return
    
    strongCiphers = [c for c in QSslConfiguration.supportedCiphers()
                     if c.name() not in blacklist and c.usedBits() >= 128]
    defaultSslConfiguration = QSslConfiguration.defaultConfiguration()
    defaultSslConfiguration.setCiphers(strongCiphers)
    QSslConfiguration.setDefaultConfiguration(defaultSslConfiguration)
