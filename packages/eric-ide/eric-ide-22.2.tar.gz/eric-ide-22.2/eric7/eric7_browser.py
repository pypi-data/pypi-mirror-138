#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Web Browser.

This is the main Python script that performs the necessary initialization
of the web browser and starts the Qt event loop. This is a standalone version
of the integrated web browser. It is based on QtWebEngine.
"""

import sys
import os

sys.path.insert(1, os.path.dirname(__file__))

app = None
SettingsDir = None

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        import Globals
        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt6.QtCore import QSettings
        SettingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(SettingsDir):
            os.makedirs(SettingsDir)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, SettingsDir)
        sys.argv.remove(arg)

try:
    from PyQt6 import QtWebEngineWidgets    # __IGNORE_WARNING__
except ImportError:
    if "--quiet" not in sys.argv:
        from PyQt6.QtCore import QTimer
        from PyQt6.QtWidgets import QApplication
        from EricWidgets import EricMessageBox          # __IGNORE_WARNING__
        app = QApplication([])
        QTimer.singleShot(0, lambda: EricMessageBox.critical(
            None,
            "eric Web Browser",
            "QtWebEngineWidgets is not installed but needed to execute the"
            " web browser."))
        app.exec()
    sys.exit(100)

from PyQt6.QtWebEngineCore import QWebEngineUrlScheme

import Globals
from Globals import AppInfo

from EricWidgets.EricApplication import EricApplication

from Toolbox import Startup

from WebBrowser.WebBrowserSingleApplication import (
    WebBrowserSingleApplicationClient
)


def createMainWidget(argv):
    """
    Function to create the main widget.
    
    @param argv list of command line parameters
    @type list of str
    @return reference to the main widget
    @rtype QWidget
    """
    from WebBrowser.WebBrowserWindow import WebBrowserWindow
    
    searchWord = None
    private = False
    qthelp = False
    single = False
    name = ""
    
    for arg in reversed(argv):
        if arg.startswith("--search="):
            searchWord = argv[1].split("=", 1)[1]
            argv.remove(arg)
        elif arg.startswith("--name="):
            name = arg.replace("--name=", "")
            argv.remove(arg)
        elif arg == "--private":
            private = True
            argv.remove(arg)
        elif arg == "--qthelp":
            qthelp = True
            argv.remove(arg)
        elif arg == "--single":
            single = True
            argv.remove(arg)
        elif (
            arg.startswith(("--newtab=", "--")) or
            arg == "--quiet"
        ):
            # only needed until we reach this point
            argv.remove(arg)
    
    try:
        home = argv[1]
    except IndexError:
        home = ""
    
    browser = WebBrowserWindow(home, '.', None, 'web_browser',
                               searchWord=searchWord, private=private,
                               settingsDir=SettingsDir, qthelp=qthelp,
                               single=single, saname=name)
    return browser


def main():
    """
    Main entry point into the application.
    """
    global app
    
    from PyQt6.QtGui import QGuiApplication
    QGuiApplication.setDesktopFileName("eric7_browser.desktop")
    
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--private", "start the browser in private browsing mode"),
        ("--qthelp", "start the browser with support for QtHelp"),
        ("--quiet", "don't show any startup error messages"),
        ("--search=word", "search for the given word"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
        ("--single", "start the browser as a single application"),
    ]
    appinfo = AppInfo.makeAppInfo(sys.argv,
                                  "eric Web Browser",
                                  "file",
                                  "web browser",
                                  options)
    
    # set the library paths for plugins
    Startup.setLibraryPaths()
    
    scheme = QWebEngineUrlScheme(b"eric")
    scheme.setSyntax(QWebEngineUrlScheme.Syntax.Path)
    scheme.setFlags(QWebEngineUrlScheme.Flag.SecureScheme |
                    QWebEngineUrlScheme.Flag.ContentSecurityPolicyIgnored)
    QWebEngineUrlScheme.registerScheme(scheme)
    if "--qthelp" in sys.argv:
        scheme = QWebEngineUrlScheme(b"qthelp")
        scheme.setSyntax(QWebEngineUrlScheme.Syntax.Path)
        scheme.setFlags(QWebEngineUrlScheme.Flag.SecureScheme)
        QWebEngineUrlScheme.registerScheme(scheme)
    
    app = EricApplication(sys.argv)
    if "--private" not in sys.argv:
        client = WebBrowserSingleApplicationClient()
        res = client.connect()
        if res > 0:
            if len(sys.argv) > 1:
                client.processArgs(sys.argv[1:])
            sys.exit(0)
        elif res < 0:
            print("eric7_browser: {0}".format(client.errstr()))
            # __IGNORE_WARNING_M801__
            sys.exit(res)
    
    res = Startup.simpleAppStartup(sys.argv,
                                   appinfo,
                                   createMainWidget,
                                   installErrorHandler=True,
                                   app=app)
    sys.exit(res)

if __name__ == '__main__':
    main()
