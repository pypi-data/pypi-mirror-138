# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a widget controlling a download.
"""

import enum
import os

from PyQt6.QtCore import (
    pyqtSlot, pyqtSignal, QTime, QUrl, QStandardPaths, QFileInfo, QDateTime
)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QWidget, QStyle, QDialog
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest

from EricWidgets import EricFileDialog
from EricWidgets.EricApplication import ericApp

from .Ui_DownloadItem import Ui_DownloadItem

from .DownloadUtilities import timeString, dataString, speedString
from WebBrowser.WebBrowserWindow import WebBrowserWindow

import UI.PixmapCache
import Utilities.MimeTypes


class DownloadState(enum.Enum):
    """
    Class implementing the various download states.
    """
    Downloading = 0
    Successful = 1
    Cancelled = 2


class DownloadItem(QWidget, Ui_DownloadItem):
    """
    Class implementing a widget controlling a download.
    
    @signal statusChanged() emitted upon a status change of a download
    @signal downloadFinished(success) emitted when a download finished
    @signal progress(int, int) emitted to signal the download progress
    """
    statusChanged = pyqtSignal()
    downloadFinished = pyqtSignal(bool)
    progress = pyqtSignal(int, int)
    
    def __init__(self, downloadRequest=None, pageUrl=None, parent=None):
        """
        Constructor
        
        @param downloadRequest reference to the download object containing the
        download data.
        @type QWebEngineDownloadRequest
        @param pageUrl URL of the calling page
        @type QUrl
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.fileIcon.setStyleSheet("background-color: transparent")
        self.datetimeLabel.setStyleSheet("background-color: transparent")
        self.filenameLabel.setStyleSheet("background-color: transparent")
        if ericApp().usesDarkPalette():
            self.infoLabel.setStyleSheet(
                "color: #c0c0c0; background-color: transparent"
            )      # light gray
        else:
            self.infoLabel.setStyleSheet(
                "color: #808080; background-color: transparent"
            )      # dark gray
        
        self.progressBar.setMaximum(0)
        
        self.pauseButton.setIcon(UI.PixmapCache.getIcon("pause"))
        self.stopButton.setIcon(UI.PixmapCache.getIcon("stopLoading"))
        self.openButton.setIcon(UI.PixmapCache.getIcon("open"))
        self.openButton.setEnabled(False)
        self.openButton.setVisible(False)
        
        self.__state = DownloadState.Downloading
        
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        self.fileIcon.setPixmap(icon.pixmap(48, 48))
        
        self.__downloadRequest = downloadRequest
        if pageUrl is None:
            self.__pageUrl = QUrl()
        else:
            self.__pageUrl = pageUrl
        self.__bytesReceived = 0
        self.__bytesTotal = -1
        self.__downloadTime = QTime()
        self.__fileName = ""
        self.__originalFileName = ""
        self.__finishedDownloading = False
        self.__gettingFileName = False
        self.__canceledFileSelect = False
        self.__autoOpen = False
        self.__downloadedDateTime = QDateTime()
        
        self.__initialize()
    
    def __initialize(self):
        """
        Private method to initialize the widget.
        """
        if self.__downloadRequest is None:
            return
        
        self.__finishedDownloading = False
        self.__bytesReceived = 0
        self.__bytesTotal = -1
        
        # start timer for the download estimation
        self.__downloadTime = QTime.currentTime()
        
        # attach to the download item object
        self.__url = self.__downloadRequest.url()
        self.__downloadRequest.receivedBytesChanged.connect(
            self.__downloadProgress)
        self.__downloadRequest.isFinishedChanged.connect(self.__finished)
        
        # reset info
        self.datetimeLabel.clear()
        self.datetimeLabel.hide()
        self.infoLabel.clear()
        self.progressBar.setValue(0)
        if (
            self.__downloadRequest.state() ==
            QWebEngineDownloadRequest.DownloadState.DownloadRequested
        ):
            self.__getFileName()
            if not self.__fileName:
                self.__downloadRequest.cancel()
            else:
                self.__downloadRequest.setDownloadFileName(self.__fileName)
                self.__downloadRequest.accept()
        else:
            fileName = self.__downloadRequest.downloadFileName()
            self.__setFileName(fileName)
    
    def __getFileName(self):
        """
        Private method to get the file name to save to from the user.
        """
        if self.__gettingFileName:
            return
        
        savePage = self.__downloadRequest.isSavePageDownload()
        
        documentLocation = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation)
        downloadDirectory = (
            WebBrowserWindow.downloadManager().downloadDirectory()
        )
        
        if self.__fileName:
            fileName = self.__fileName
            originalFileName = self.__originalFileName
            self.__toDownload = True
            ask = False
        else:
            defaultFileName, originalFileName = self.__saveFileName(
                documentLocation if savePage else downloadDirectory)
            fileName = defaultFileName
            self.__originalFileName = originalFileName
            ask = True
        self.__autoOpen = False
        
        if not savePage:
            from .DownloadAskActionDialog import DownloadAskActionDialog
            url = self.__downloadRequest.url()
            mimetype = Utilities.MimeTypes.mimeType(originalFileName)
            dlg = DownloadAskActionDialog(
                QFileInfo(originalFileName).fileName(),
                mimetype,
                "{0}://{1}".format(url.scheme(), url.authority()),
                self)
            
            if (
                dlg.exec() == QDialog.DialogCode.Rejected or
                dlg.getAction() == "cancel"
            ):
                self.progressBar.setVisible(False)
                self.on_stopButton_clicked()
                self.filenameLabel.setText(
                    self.tr("Download canceled: {0}").format(
                        QFileInfo(defaultFileName).fileName()))
                self.__canceledFileSelect = True
                self.__setDateTime()
                return
            
            if dlg.getAction() == "scan":
                self.__mainWindow.requestVirusTotalScan(url)
                
                self.progressBar.setVisible(False)
                self.on_stopButton_clicked()
                self.filenameLabel.setText(
                    self.tr("VirusTotal scan scheduled: {0}").format(
                        QFileInfo(defaultFileName).fileName()))
                self.__canceledFileSelect = True
                return
        
            self.__autoOpen = dlg.getAction() == "open"
            
            tempLocation = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.TempLocation)
            fileName = (
                tempLocation + '/' +
                QFileInfo(fileName).completeBaseName()
            )
            
            if ask and not self.__autoOpen:
                self.__gettingFileName = True
                fileName = EricFileDialog.getSaveFileName(
                    None,
                    self.tr("Save File"),
                    defaultFileName,
                    "")
                self.__gettingFileName = False
        
        if not fileName:
            self.progressBar.setVisible(False)
            self.on_stopButton_clicked()
            self.filenameLabel.setText(
                self.tr("Download canceled: {0}")
                    .format(QFileInfo(defaultFileName).fileName()))
            self.__canceledFileSelect = True
            self.__setDateTime()
            return
        
        self.__setFileName(fileName)
    
    def __setFileName(self, fileName):
        """
        Private method to set the file name to save the download into.
        
        @param fileName name of the file to save into
        @type str
        """
        fileInfo = QFileInfo(fileName)
        WebBrowserWindow.downloadManager().setDownloadDirectory(
            fileInfo.absoluteDir().absolutePath())
        self.filenameLabel.setText(fileInfo.fileName())
        
        self.__fileName = fileName
        
        # check file path for saving
        saveDirPath = QFileInfo(self.__fileName).dir()
        if (
            not saveDirPath.exists() and
            not saveDirPath.mkpath(saveDirPath.absolutePath())
        ):
            self.progressBar.setVisible(False)
            self.on_stopButton_clicked()
            self.infoLabel.setText(self.tr(
                "Download directory ({0}) couldn't be created.")
                .format(saveDirPath.absolutePath()))
            self.__setDateTime()
            return
        
        self.filenameLabel.setText(QFileInfo(self.__fileName).fileName())
    
    def __saveFileName(self, directory):
        """
        Private method to calculate a name for the file to download.
        
        @param directory name of the directory to store the file into (string)
        @return proposed filename and original filename (string, string)
        """
        path = self.__downloadRequest.downloadFileName()
        info = QFileInfo(path)
        baseName = info.completeBaseName()
        endName = info.suffix()
        
        origName = baseName
        if endName:
            origName += '.' + endName
        
        name = os.path.join(directory, baseName)
        if endName:
            name += '.' + endName
        return name, origName
    
    @pyqtSlot(bool)
    def on_pauseButton_clicked(self, checked):
        """
        Private slot to pause the download.
        
        @param checked flag indicating the state of the button
        @type bool
        """
        if checked:
            self.__downloadRequest.pause()
        else:
            self.__downloadRequest.resume()
    
    @pyqtSlot()
    def on_stopButton_clicked(self):
        """
        Private slot to stop the download.
        """
        self.cancelDownload()
    
    def cancelDownload(self):
        """
        Public slot to stop the download.
        """
        self.setUpdatesEnabled(False)
        self.stopButton.setEnabled(False)
        self.stopButton.setVisible(False)
        self.openButton.setEnabled(False)
        self.openButton.setVisible(False)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setVisible(False)
        self.setUpdatesEnabled(True)
        self.__state = DownloadState.Cancelled
        self.__downloadRequest.cancel()
        self.__setDateTime()
        self.downloadFinished.emit(False)
    
    @pyqtSlot()
    def on_openButton_clicked(self):
        """
        Private slot to open the downloaded file.
        """
        self.openFile()
    
    def openFile(self):
        """
        Public slot to open the downloaded file.
        """
        info = QFileInfo(self.__fileName)
        url = QUrl.fromLocalFile(info.absoluteFilePath())
        QDesktopServices.openUrl(url)
    
    def openFolder(self):
        """
        Public slot to open the folder containing the downloaded file.
        """
        info = QFileInfo(self.__fileName)
        url = QUrl.fromLocalFile(info.absolutePath())
        QDesktopServices.openUrl(url)
    
    @pyqtSlot()
    def __downloadProgress(self):
        """
        Private slot to show the download progress.
        """
        self.__bytesReceived = self.__downloadRequest.receivedBytes()
        self.__bytesTotal = self.__downloadRequest.totalBytes()
        currentValue = 0
        totalValue = 0
        if self.__bytesTotal > 0:
            currentValue = self.__bytesReceived * 100 // self.__bytesTotal
            totalValue = 100
        self.progressBar.setValue(currentValue)
        self.progressBar.setMaximum(totalValue)
        
        self.progress.emit(currentValue, totalValue)
        self.__updateInfoLabel()
    
    def downloadProgress(self):
        """
        Public method to get the download progress.
        
        @return current download progress
        @rtype int
        """
        return self.progressBar.value()
    
    def bytesTotal(self):
        """
        Public method to get the total number of bytes of the download.
        
        @return total number of bytes (integer)
        """
        if self.__bytesTotal == -1:
            self.__bytesTotal = self.__downloadRequest.totalBytes()
        return self.__bytesTotal
    
    def bytesReceived(self):
        """
        Public method to get the number of bytes received.
        
        @return number of bytes received (integer)
        """
        return self.__bytesReceived
    
    def remainingTime(self):
        """
        Public method to get an estimation for the remaining time.
        
        @return estimation for the remaining time (float)
        """
        if not self.downloading():
            return -1.0
        
        if self.bytesTotal() == -1:
            return -1.0
        
        cSpeed = self.currentSpeed()
        timeRemaining = (
            (self.bytesTotal() - self.bytesReceived()) / cSpeed
            if cSpeed != 0 else
            1
        )
        
        # ETA should never be 0
        if timeRemaining == 0:
            timeRemaining = 1
        
        return timeRemaining
    
    def currentSpeed(self):
        """
        Public method to get an estimation for the download speed.
        
        @return estimation for the download speed (float)
        """
        if not self.downloading():
            return -1.0
        
        return (
            self.__bytesReceived * 1000.0 /
            self.__downloadTime.msecsTo(QTime.currentTime())
        )
    
    def __updateInfoLabel(self):
        """
        Private method to update the info label.
        """
        bytesTotal = self.bytesTotal()
        running = not self.downloadedSuccessfully()
        
        speed = self.currentSpeed()
        timeRemaining = self.remainingTime()
        
        info = ""
        if running:
            remaining = ""
            
            if bytesTotal > 0:
                remaining = timeString(timeRemaining)
            
            info = self.tr(
                "{0} of {1} ({2}/sec) {3}"
            ).format(
                dataString(self.__bytesReceived),
                bytesTotal == -1 and self.tr("?") or
                dataString(bytesTotal),
                speedString(speed),
                remaining
            )
        else:
            if bytesTotal in (self.__bytesReceived, -1):
                info = self.tr(
                    "{0} downloaded"
                ).format(dataString(self.__bytesReceived))
            else:
                info = self.tr(
                    "{0} of {1} - Stopped"
                ).format(dataString(self.__bytesReceived),
                         dataString(bytesTotal))
        self.infoLabel.setText(info)
    
    def downloading(self):
        """
        Public method to determine, if a download is in progress.
        
        @return flag indicating a download is in progress (boolean)
        """
        return self.__state == DownloadState.Downloading
    
    def downloadedSuccessfully(self):
        """
        Public method to check for a successful download.
        
        @return flag indicating a successful download (boolean)
        """
        return self.__state == DownloadState.Successful
    
    def downloadCanceled(self):
        """
        Public method to check, if the download was cancelled.
        
        @return flag indicating a canceled download (boolean)
        """
        return self.__state == DownloadState.Cancelled
    
    def __finished(self):
        """
        Private slot to handle the download finished.
        """
        self.__finishedDownloading = True
        
        noError = (self.__downloadRequest.state() ==
                   QWebEngineDownloadRequest.DownloadState.DownloadCompleted)
        
        self.progressBar.setVisible(False)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setVisible(False)
        self.stopButton.setEnabled(False)
        self.stopButton.setVisible(False)
        self.openButton.setEnabled(noError)
        self.openButton.setVisible(noError)
        self.__state = DownloadState.Successful
        self.__updateInfoLabel()
        self.__setDateTime()
        
        self.__adjustSize()
        
        self.statusChanged.emit()
        self.downloadFinished.emit(True)
        
        if self.__autoOpen:
            self.openFile()
    
    def canceledFileSelect(self):
        """
        Public method to check, if the user canceled the file selection.
        
        @return flag indicating cancellation (boolean)
        """
        return self.__canceledFileSelect
    
    def setIcon(self, icon):
        """
        Public method to set the download icon.
        
        @param icon reference to the icon to be set (QIcon)
        """
        self.fileIcon.setPixmap(icon.pixmap(48, 48))
    
    def fileName(self):
        """
        Public method to get the name of the output file.
        
        @return name of the output file (string)
        """
        return self.__fileName
    
    def absoluteFilePath(self):
        """
        Public method to get the absolute path of the output file.
        
        @return absolute path of the output file (string)
        """
        return QFileInfo(self.__fileName).absoluteFilePath()
    
    def getData(self):
        """
        Public method to get the relevant download data.
        
        @return dictionary containing the URL, save location, done flag,
            the URL of the related web page and the date and time of the
            download
        @rtype dict of {"URL": QUrl, "Location": str, "Done": bool,
            "PageURL": QUrl, "Downloaded": QDateTime}
        """
        return {
            "URL": self.__url,
            "Location": QFileInfo(self.__fileName).filePath(),
            "Done": self.downloadedSuccessfully(),
            "PageURL": self.__pageUrl,
            "Downloaded": self.__downloadedDateTime
        }
    
    def setData(self, data):
        """
        Public method to set the relevant download data.
        
        @param data dictionary containing the URL, save location, done flag,
            the URL of the related web page and the date and time of the
            download
        @type dict of {"URL": QUrl, "Location": str, "Done": bool,
            "PageURL": QUrl, "Downloaded": QDateTime}
        """
        self.__url = data["URL"]
        self.__fileName = data["Location"]
        self.__pageUrl = data["PageURL"]
        
        self.filenameLabel.setText(QFileInfo(self.__fileName).fileName())
        self.infoLabel.setText(self.__fileName)
        
        try:
            self.__setDateTime(data["Downloaded"])
        except KeyError:
            self.__setDateTime(QDateTime())
        
        self.pauseButton.setEnabled(False)
        self.pauseButton.setVisible(False)
        self.stopButton.setEnabled(False)
        self.stopButton.setVisible(False)
        self.openButton.setEnabled(data["Done"])
        self.openButton.setVisible(data["Done"])
        if data["Done"]:
            self.__state = DownloadState.Successful
        else:
            self.__state = DownloadState.Cancelled
        self.progressBar.setVisible(False)
        
        self.__adjustSize()
    
    def getInfoData(self):
        """
        Public method to get the text of the info label.
        
        @return text of the info label (string)
        """
        return self.infoLabel.text()
    
    def getPageUrl(self):
        """
        Public method to get the URL of the download page.
        
        @return URL of the download page (QUrl)
        """
        return self.__pageUrl
    
    def __adjustSize(self):
        """
        Private method to adjust the size of the download item.
        """
        self.ensurePolished()
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __setDateTime(self, dateTime=None):
        """
        Private method to set the download date and time.
        
        @param dateTime date and time to be set
        @type QDateTime
        """
        if dateTime is None:
            self.__downloadedDateTime = QDateTime.currentDateTime()
        else:
            self.__downloadedDateTime = dateTime
        if self.__downloadedDateTime.isValid():
            labelText = self.__downloadedDateTime.toString("yyyy-MM-dd hh:mm")
            self.datetimeLabel.setText(labelText)
            self.datetimeLabel.show()
        else:
            self.datetimeLabel.clear()
            self.datetimeLabel.hide()
