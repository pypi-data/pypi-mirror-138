# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a manager for open search engines.
"""

import os
import contextlib

from PyQt6.QtCore import (
    pyqtSignal, QObject, QUrl, QFile, QDir, QIODevice, QUrlQuery
)
from PyQt6.QtWidgets import QLineEdit, QInputDialog
from PyQt6.QtNetwork import QNetworkRequest, QNetworkReply

from EricWidgets.EricApplication import ericApp
from EricWidgets import EricMessageBox

from Utilities.AutoSaver import AutoSaver
import Utilities
import Preferences


class OpenSearchManager(QObject):
    """
    Class implementing a manager for open search engines.
    
    @signal changed() emitted to indicate a change
    @signal currentEngineChanged() emitted to indicate a change of
            the current search engine
    """
    changed = pyqtSignal()
    currentEngineChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent object (QObject)
        """
        if parent is None:
            parent = ericApp()
        super().__init__(parent)
        
        self.__replies = []
        self.__engines = {}
        self.__keywords = {}
        self.__current = ""
        self.__loading = False
        self.__saveTimer = AutoSaver(self, self.save)
        
        self.changed.connect(self.__saveTimer.changeOccurred)
        
        self.load()
    
    def close(self):
        """
        Public method to close the open search engines manager.
        """
        self.__saveTimer.saveIfNeccessary()
    
    def currentEngineName(self):
        """
        Public method to get the name of the current search engine.
        
        @return name of the current search engine (string)
        """
        return self.__current
    
    def setCurrentEngineName(self, name):
        """
        Public method to set the current engine by name.
        
        @param name name of the new current engine (string)
        """
        if name not in self.__engines:
            return
        
        self.__current = name
        self.currentEngineChanged.emit()
        self.changed.emit()
    
    def currentEngine(self):
        """
        Public method to get a reference to the current engine.
        
        @return reference to the current engine (OpenSearchEngine)
        """
        if not self.__current or self.__current not in self.__engines:
            return None
        
        return self.__engines[self.__current]
    
    def setCurrentEngine(self, engine):
        """
        Public method to set the current engine.
        
        @param engine reference to the new current engine (OpenSearchEngine)
        """
        if engine is None:
            return
        
        for engineName in self.__engines:
            if self.__engines[engineName] == engine:
                self.setCurrentEngineName(engineName)
                break
    
    def engine(self, name):
        """
        Public method to get a reference to the named engine.
        
        @param name name of the engine (string)
        @return reference to the engine (OpenSearchEngine)
        """
        if name not in self.__engines:
            return None
        
        return self.__engines[name]
    
    def engineExists(self, name):
        """
        Public method to check, if an engine exists.
        
        @param name name of the engine (string)
        @return flag indicating an existing engine (boolean)
        """
        return name in self.__engines
    
    def allEnginesNames(self):
        """
        Public method to get a list of all engine names.
        
        @return sorted list of all engine names (list of strings)
        """
        return sorted(self.__engines.keys())
    
    def enginesCount(self):
        """
        Public method to get the number of available engines.
        
        @return number of engines (integer)
        """
        return len(self.__engines)
    
    def addEngine(self, engine):
        """
        Public method to add a new search engine.
        
        @param engine URL of the engine definition file (QUrl) or
            name of a file containing the engine definition (string)
            or reference to an engine object (OpenSearchEngine)
        @return flag indicating success (boolean)
        """
        from .OpenSearchEngine import OpenSearchEngine
        if isinstance(engine, QUrl):
            return self.__addEngineByUrl(engine)
        elif isinstance(engine, OpenSearchEngine):
            return self.__addEngineByEngine(engine)
        else:
            return self.__addEngineByFile(engine)
    
    def __addEngineByUrl(self, url):
        """
        Private method to add a new search engine given its URL.
        
        @param url URL of the engine definition file (QUrl)
        @return flag indicating success (boolean)
        """
        if not url.isValid():
            return False
        
        from WebBrowser.WebBrowserWindow import WebBrowserWindow

        reply = WebBrowserWindow.networkManager().get(QNetworkRequest(url))
        reply.finished.connect(lambda: self.__engineFromUrlAvailable(reply))
        reply.setParent(self)
        self.__replies.append(reply)
        
        return True
    
    def __addEngineByFile(self, filename):
        """
        Private method to add a new search engine given a filename.
        
        @param filename name of a file containing the engine definition
            (string)
        @return flag indicating success (boolean)
        """
        file_ = QFile(filename)
        if not file_.open(QIODevice.OpenModeFlag.ReadOnly):
            return False
        
        from .OpenSearchReader import OpenSearchReader
        reader = OpenSearchReader()
        engine = reader.read(file_)
        
        if not self.__addEngineByEngine(engine):
            return False
        
        return True
    
    def __addEngineByEngine(self, engine):
        """
        Private method to add a new search engine given a reference to an
        engine.
        
        @param engine reference to an engine object (OpenSearchEngine)
        @return flag indicating success (boolean)
        """
        if engine is None:
            return False
        
        if not engine.isValid():
            return False
        
        if engine.name() in self.__engines:
            return False
        
        engine.setParent(self)
        self.__engines[engine.name()] = engine
        
        self.changed.emit()
        
        return True
    
    def addEngineFromForm(self, res, view):
        """
        Public method to add a new search engine from a form.
        
        @param res result of the JavaScript run on by
            WebBrowserView.__addSearchEngine()
        @type dict or None
        @param view reference to the web browser view
        @type WebBrowserView
        """
        if not res:
            return
        
        method = res["method"]
        actionUrl = QUrl(res["action"])
        inputName = res["inputName"]
        
        if method != "get":
            EricMessageBox.warning(
                self,
                self.tr("Method not supported"),
                self.tr(
                    """{0} method is not supported.""").format(method.upper()))
            return
        
        if actionUrl.isRelative():
            actionUrl = view.url().resolved(actionUrl)
        
        searchUrlQuery = QUrlQuery(actionUrl)
        searchUrlQuery.addQueryItem(inputName, "{searchTerms}")
        
        inputFields = res["inputs"]
        for inputField in inputFields:
            name = inputField[0]
            value = inputField[1]
            
            if not name or name == inputName or not value:
                continue
            
            searchUrlQuery.addQueryItem(name, value)
        
        engineName, ok = QInputDialog.getText(
            view,
            self.tr("Engine name"),
            self.tr("Enter a name for the engine"),
            QLineEdit.EchoMode.Normal)
        if not ok:
            return
        
        actionUrl.setQuery(searchUrlQuery)
        
        from .OpenSearchEngine import OpenSearchEngine
        engine = OpenSearchEngine()
        engine.setName(engineName)
        engine.setDescription(engineName)
        engine.setSearchUrlTemplate(
            actionUrl.toDisplayString(
                QUrl.ComponentFormattingOption.FullyDecoded))
        engine.setImage(view.icon().pixmap(16, 16).toImage())
        
        self.__addEngineByEngine(engine)
    
    def removeEngine(self, name):
        """
        Public method to remove an engine.
        
        @param name name of the engine (string)
        """
        if len(self.__engines) <= 1:
            return
        
        if name not in self.__engines:
            return
        
        engine = self.__engines[name]
        for keyword in [k for k in self.__keywords
                        if self.__keywords[k] == engine]:
            del self.__keywords[keyword]
        del self.__engines[name]
        
        file_ = QDir(self.enginesDirectory()).filePath(
            self.generateEngineFileName(name))
        QFile.remove(file_)
        
        if name == self.__current:
            self.setCurrentEngineName(list(self.__engines.keys())[0])
        
        self.changed.emit()
    
    def generateEngineFileName(self, engineName):
        """
        Public method to generate a valid engine file name.
        
        @param engineName name of the engine (string)
        @return valid engine file name (string)
        """
        fileName = ""
        
        # strip special characters
        for c in engineName:
            if c.isspace():
                fileName += '_'
                continue
            
            if c.isalnum():
                fileName += c
        
        fileName += ".xml"
        
        return fileName
    
    def saveDirectory(self, dirName):
        """
        Public method to save the search engine definitions to files.
        
        @param dirName name of the directory to write the files to (string)
        """
        qdir = QDir()
        if not qdir.mkpath(dirName):
            return
        qdir.setPath(dirName)
        
        from .OpenSearchWriter import OpenSearchWriter
        writer = OpenSearchWriter()
        
        for engine in list(self.__engines.values()):
            name = self.generateEngineFileName(engine.name())
            fileName = qdir.filePath(name)
            
            file = QFile(fileName)
            if not file.open(QIODevice.OpenModeFlag.WriteOnly):
                continue
            
            writer.write(file, engine)
    
    def save(self):
        """
        Public method to save the search engines configuration.
        """
        if self.__loading:
            return
        
        self.saveDirectory(self.enginesDirectory())
        
        Preferences.setWebBrowser("WebSearchEngine", self.__current)
        keywords = []
        for k in self.__keywords:
            if self.__keywords[k]:
                keywords.append((k, self.__keywords[k].name()))
        Preferences.setWebBrowser("WebSearchKeywords", keywords)
    
    def loadDirectory(self, dirName):
        """
        Public method to load the search engine definitions from files.
        
        @param dirName name of the directory to load the files from (string)
        @return flag indicating success (boolean)
        """
        if not QFile.exists(dirName):
            return False
        
        success = False
        
        qdir = QDir(dirName)
        for name in qdir.entryList(["*.xml"]):
            fileName = qdir.filePath(name)
            if self.__addEngineByFile(fileName):
                success = True
        
        return success
    
    def load(self):
        """
        Public method to load the search engines configuration.
        """
        self.__loading = True
        self.__current = Preferences.getWebBrowser("WebSearchEngine")
        keywords = Preferences.getWebBrowser("WebSearchKeywords")
        
        if not self.loadDirectory(self.enginesDirectory()):
            self.restoreDefaults()
        
        for keyword, engineName in keywords:
            self.__keywords[keyword] = self.engine(engineName)
        
        if (
            self.__current not in self.__engines and
            len(self.__engines) > 0
        ):
            self.__current = list(self.__engines.keys())[0]
        
        self.__loading = False
        self.currentEngineChanged.emit()
    
    def restoreDefaults(self):
        """
        Public method to restore the default search engines.
        """
        from .OpenSearchReader import OpenSearchReader

        reader = OpenSearchReader()
        defaultEnginesDirectory = os.path.join(os.path.dirname(__file__),
                                               "DefaultSearchEngines")
        for engineFileName in (
            QDir(defaultEnginesDirectory, "*.xml").entryList()
        ):
            engineFile = QFile(os.path.join(defaultEnginesDirectory,
                                            engineFileName))
            if not engineFile.open(QIODevice.OpenModeFlag.ReadOnly):
                continue
            engine = reader.read(engineFile)
            self.__addEngineByEngine(engine)
    
    def enginesDirectory(self):
        """
        Public method to determine the directory containing the search engine
        descriptions.
        
        @return directory name (string)
        """
        return os.path.join(
            Utilities.getConfigDir(), "web_browser", "searchengines")
    
    def __confirmAddition(self, engine):
        """
        Private method to confirm the addition of a new search engine.
        
        @param engine reference to the engine to be added (OpenSearchEngine)
        @return flag indicating the engine shall be added (boolean)
        """
        if engine is None or not engine.isValid():
            return False
        
        host = QUrl(engine.searchUrlTemplate()).host()
        
        res = EricMessageBox.yesNo(
            None,
            "",
            self.tr(
                """<p>Do you want to add the following engine to your"""
                """ list of search engines?<br/><br/>Name: {0}<br/>"""
                """Searches on: {1}</p>""").format(engine.name(), host))
        return res
    
    def __engineFromUrlAvailable(self, reply):
        """
        Private slot to add a search engine from the net.
        
        @param reply reference to the network reply
        @type QNetworkReply
        """
        reply.close()
        if reply in self.__replies:
            self.__replies.remove(reply)
        
        if reply.error() == QNetworkReply.NetworkError.NoError:
            from .OpenSearchReader import OpenSearchReader
            reader = OpenSearchReader()
            engine = reader.read(reply)
            
            if not engine.isValid():
                return
            
            if self.engineExists(engine.name()):
                return
            
            if not self.__confirmAddition(engine):
                return
            
            if not self.__addEngineByEngine(engine):
                return
        else:
            # some error happened
            from WebBrowser.WebBrowserWindow import WebBrowserWindow
            WebBrowserWindow.getWindow().statusBar().showMessage(
                reply.errorString(), 10000)
    
    def convertKeywordSearchToUrl(self, keywordSearch):
        """
        Public method to get the search URL for a keyword search.
        
        @param keywordSearch search string for keyword search (string)
        @return search URL (QUrl)
        """
        try:
            keyword, term = keywordSearch.split(" ", 1)
        except ValueError:
            return QUrl()
        
        if not term:
            return QUrl()
        
        engine = self.engineForKeyword(keyword)
        if engine:
            return engine.searchUrl(term)
        
        return QUrl()
    
    def engineForKeyword(self, keyword):
        """
        Public method to get the engine for a keyword.
        
        @param keyword keyword to get engine for (string)
        @return reference to the search engine object (OpenSearchEngine)
        """
        if keyword and keyword in self.__keywords:
            return self.__keywords[keyword]
        
        return None
    
    def setEngineForKeyword(self, keyword, engine):
        """
        Public method to set the engine for a keyword.
        
        @param keyword keyword to get engine for (string)
        @param engine reference to the search engine object (OpenSearchEngine)
            or None to remove the keyword
        """
        if not keyword:
            return
        
        if engine is None:
            with contextlib.suppress(KeyError):
                del self.__keywords[keyword]
        else:
            self.__keywords[keyword] = engine
        
        self.changed.emit()
    
    def keywordsForEngine(self, engine):
        """
        Public method to get the keywords for a given engine.
        
        @param engine reference to the search engine object (OpenSearchEngine)
        @return list of keywords (list of strings)
        """
        return [k for k in self.__keywords if self.__keywords[k] == engine]
    
    def setKeywordsForEngine(self, engine, keywords):
        """
        Public method to set the keywords for an engine.
        
        @param engine reference to the search engine object (OpenSearchEngine)
        @param keywords list of keywords (list of strings)
        """
        if engine is None:
            return
        
        for keyword in self.keywordsForEngine(engine):
            del self.__keywords[keyword]
        
        for keyword in keywords:
            if not keyword:
                continue
            
            self.__keywords[keyword] = engine
        
        self.changed.emit()
    
    def enginesChanged(self):
        """
        Public slot to tell the search engine manager, that something has
        changed.
        """
        self.changed.emit()
