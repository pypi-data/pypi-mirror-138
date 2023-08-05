# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing an abstract base class to be subclassed by all specific
VCS interfaces.
"""

import contextlib
import json
import os

from PyQt6.QtCore import (
    QObject, QThread, QMutex, QProcess, Qt, pyqtSignal, QCoreApplication,
    QLockFile
)
from PyQt6.QtWidgets import QApplication

from EricWidgets import EricMessageBox
from EricWidgets.EricApplication import ericApp

import Preferences


class VersionControl(QObject):
    """
    Class implementing an abstract base class to be subclassed by all specific
    VCS interfaces.
    
    It defines the vcs interface to be implemented by subclasses
    and the common methods.
    
    @signal committed() emitted after the commit action has completed
    @signal vcsStatusMonitorData(list of str) emitted to update the VCS status
    @signal vcsStatusMonitorAllData(dict) emitted to signal all VCS status
        (key is project relative file name, value is status)
    @signal vcsStatusMonitorStatus(str, str) emitted to signal the status of
        the monitoring thread (ok, nok, op, off) and a status message
    @signal vcsStatusMonitorInfo(str) emitted to signal some info of the
        monitoring thread
    @signal vcsStatusChanged() emitted to indicate a change of the overall
        VCS status
    """
    committed = pyqtSignal()
    vcsStatusMonitorData = pyqtSignal(list)
    vcsStatusMonitorAllData = pyqtSignal(dict)
    vcsStatusMonitorStatus = pyqtSignal(str, str)
    vcsStatusMonitorInfo = pyqtSignal(str)
    vcsStatusChanged = pyqtSignal()
    
    canBeCommitted = 1  # Indicates that a file/directory is in the vcs.
    canBeAdded = 2      # Indicates that a file/directory is not in vcs.
    
    commitHistoryLock = "commitHistory.lock"
    commitHistoryData = "commitHistory.json"
    
    def __init__(self, parent=None, name=None):
        """
        Constructor
        
        @param parent parent widget (QWidget)
        @param name name of this object (string)
        """
        super().__init__(parent)
        if name:
            self.setObjectName(name)
        self.defaultOptions = {
            'global': [''],
            'commit': [''],
            'checkout': [''],
            'update': [''],
            'add': [''],
            'remove': [''],
            'diff': [''],
            'log': [''],
            'history': [''],
            'status': [''],
            'tag': [''],
            'export': ['']
        }
        self.interestingDataKeys = []
        self.options = {}
        self.otherData = {}
        self.canDetectBinaries = True
        
        self.statusMonitorThread = None
        self.vcsExecutionMutex = QMutex()
        
    def vcsShutdown(self):
        """
        Public method used to shutdown the vcs interface.
        
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsExists(self):
        """
        Public method used to test for the presence of the vcs.
        
        @return tuple of flag indicating the existence and a string
            giving an error message in case of failure
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return (False, "")
        
    def vcsInit(self, vcsDir, noDialog=False):
        """
        Public method used to initialize the vcs.
        
        @param vcsDir name of the VCS directory (string)
        @param noDialog flag indicating quiet operations (boolean)
        @return flag indicating success (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
        
    def vcsConvertProject(self, vcsDataDict, project, addAll=True):
        """
        Public method to convert an uncontrolled project to a version
        controlled project.
        
        @param vcsDataDict dictionary of data required for the conversion
        @type dict
        @param project reference to the project object
        @type Project
        @param addAll flag indicating to add all files to the repository
        @type bool
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsImport(self, vcsDataDict, projectDir, noDialog=False, addAll=True):
        """
        Public method used to import the project into the vcs.
        
        @param vcsDataDict dictionary of data required for the import
        @type dict
        @param projectDir project directory (string)
        @type str
        @param noDialog flag indicating quiet operations
        @type bool
        @param addAll flag indicating to add all files to the repository
        @type bool
        @return tuple containing a flag indicating an execution without errors
            and a flag indicating the version control status
        @rtype tuple of (bool, bool)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return (False, False)
        
    def vcsCheckout(self, vcsDataDict, projectDir, noDialog=False):
        """
        Public method used to check the project out of the vcs.
        
        @param vcsDataDict dictionary of data required for the checkout
        @param projectDir project directory to create (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating an execution without errors (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
        
    def vcsExport(self, vcsDataDict, projectDir):
        """
        Public method used to export a directory from the vcs.
        
        @param vcsDataDict dictionary of data required for the export
        @param projectDir project directory to create (string)
        @return flag indicating an execution without errors (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
        
    def vcsCommit(self, name, message, noDialog=False):
        """
        Public method used to make the change of a file/directory permanent in
        the vcs.
        
        @param name file/directory name to be committed (string)
        @param message message for this operation (string)
        @param noDialog flag indicating quiet operations (boolean)
        @return flag indicating success (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
    
    def vcsCommitMessages(self):
        """
        Public method to get the list of saved commit messages.
        
        @return list of saved commit messages
        @rtype list of str
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return []
    
    def _vcsProjectCommitMessages(self):
        """
        Protected method to get the list of saved commit messages.
        
        @return list of saved commit messages
        @rtype list of str
        """
        messages = []
        if Preferences.getVCS("PerProjectCommitHistory"):
            projectMgmtDir = (
                ericApp().getObject("Project").getProjectManagementDir()
            )
            with contextlib.suppress(OSError, json.JSONDecodeError):
                with open(os.path.join(projectMgmtDir,
                                       VersionControl.commitHistoryData),
                          "r") as f:
                    jsonString = f.read()
                messages = json.loads(jsonString)
        
        return messages
    
    def vcsAddCommitMessage(self, message):
        """
        Public method to add a commit message to the list of saved messages.
        
        @param message message to be added
        @type str
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
    
    def _vcsAddProjectCommitMessage(self, message):
        """
        Protected method to add a commit message to the list of project
        specific saved messages.
        
        @param message message to be added
        @type str
        @return flag indicating success
        @rtype bool
        """
        if Preferences.getVCS("PerProjectCommitHistory"):
            projectMgmtDir = (
                ericApp().getObject("Project").getProjectManagementDir()
            )
            lockFile = QLockFile(
                os.path.join(projectMgmtDir, VersionControl.commitHistoryLock))
            if lockFile.lock():
                noMessages = Preferences.getVCS("CommitMessages")
                messages = self.vcsCommitMessages()
                if message in messages:
                    messages.remove(message)
                messages.insert(0, message)
                del messages[noMessages:]
                
                with contextlib.suppress(TypeError, OSError):
                    jsonString = json.dumps(messages, indent=2)
                    with open(os.path.join(projectMgmtDir,
                                           VersionControl.commitHistoryData),
                              "w") as f:
                        f.write(jsonString)
                lockFile.unlock()
                return True
        
        return False
    
    def vcsClearCommitMessages(self):
        """
        Public method to clear the list of saved messages.
        
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
    
    def _vcsClearProjectCommitMessages(self):
        """
        Protected method to clear the list of project specific saved messages.
        
        @return flag indicating success
        @rtype bool
        """
        if Preferences.getVCS("PerProjectCommitHistory"):
            projectMgmtDir = (
                ericApp().getObject("Project").getProjectManagementDir()
            )
            lockFile = QLockFile(
                os.path.join(projectMgmtDir, VersionControl.commitHistoryLock))
            if lockFile.lock():
                with contextlib.suppress(TypeError, OSError):
                    jsonString = json.dumps([], indent=2)
                    with open(os.path.join(projectMgmtDir,
                                           VersionControl.commitHistoryData),
                              "w") as f:
                        f.write(jsonString)
                lockFile.unlock()
                return True
        
        return False
    
    def vcsUpdate(self, name, noDialog=False):
        """
        Public method used to update a file/directory in the vcs.
        
        @param name file/directory name to be updated (string)
        @param noDialog flag indicating quiet operations (boolean)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
        
    def vcsAdd(self, name, isDir=False, noDialog=False):
        """
        Public method used to add a file/directory in the vcs.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        @param noDialog flag indicating quiet operations (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsAddBinary(self, name, isDir=False):
        """
        Public method used to add a file/directory in binary mode in the vcs.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsAddTree(self, path):
        """
        Public method to add a directory tree rooted at path in the vcs.
        
        @param path root directory of the tree to be added (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsRemove(self, name, project=False, noDialog=False):
        """
        Public method used to add a file/directory in the vcs.
        
        @param name file/directory name to be removed (string)
        @param project flag indicating deletion of a project tree (boolean)
        @param noDialog flag indicating quiet operations
        @return flag indicating success (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
        
    def vcsMove(self, name, project, target=None, noDialog=False):
        """
        Public method used to move a file/directory.
        
        @param name file/directory name to be moved (string)
        @param project reference to the project object
        @param target new name of the file/directory (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating successfull operation (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
        
    def vcsLogBrowser(self, name, isFile=False):
        """
        Public method used to view the log of a file/directory in the vcs
        with a log browser dialog.
        
        @param name file/directory name to show the log for (string)
        @param isFile flag indicating log for a file is to be shown
            (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsDiff(self, name):
        """
        Public method used to view the diff of a file/directory in the vcs.
        
        @param name file/directory name to be diffed (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
    
    def vcsSbsDiff(self, name, extended=False, revisions=None):
        """
        Public method used to view the difference of a file to the Mercurial
        repository side-by-side.
        
        @param name file name to be diffed
        @type str
        @param extended flag indicating the extended variant
        @type bool
        @param revisions tuple of two revisions
        @type tuple of two str
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
    
    def vcsStatus(self, name):
        """
        Public method used to view the status of a file/directory in the vcs.
        
        @param name file/directory name to show the status for (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsTag(self, name):
        """
        Public method used to set the tag of a file/directory in the vcs.
        
        @param name file/directory name to be tagged (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsRevert(self, name):
        """
        Public method used to revert changes made to a file/directory.
        
        @param name file/directory name to be reverted
        @type str
        @return flag indicating, that the update contained an add
            or delete
        @rtype bool
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
    
    def vcsForget(self, name):
        """
        Public method used to remove a file from the repository.
        
        @param name file/directory name to be removed
        @type str or list of str
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
    
    def vcsSwitch(self, name):
        """
        Public method used to switch a directory to a different tag/branch.
        
        @param name directory name to be switched (string)
        @return flag indicating, that the switch contained an add
            or delete (boolean)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return False
        
    def vcsMerge(self, name):
        """
        Public method used to merge a tag/branch into the local project.
        
        @param name file/directory name to be merged (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsRegisteredState(self, name):
        """
        Public method used to get the registered state of a file in the vcs.
        
        @param name filename to check (string)
        @return a combination of canBeCommited and canBeAdded or
            0 in order to signal an error
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return 0
        
    def vcsAllRegisteredStates(self, names, dname):
        """
        Public method used to get the registered states of a number of files
        in the vcs.
        
        @param names dictionary with all filenames to be checked as keys
        @param dname directory to check in (string)
        @return the received dictionary completed with a combination of
            canBeCommited and canBeAdded or None in order to signal an error
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return {}
        
    def vcsName(self):
        """
        Public method returning the name of the vcs.
        
        @return name of the vcs (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return ""
        
    def vcsCleanup(self, name):
        """
        Public method used to cleanup the local copy.
        
        @param name directory name to be cleaned up (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsCommandLine(self, name):
        """
        Public method used to execute arbitrary vcs commands.
        
        @param name directory name of the working directory (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsOptionsDialog(self, project, archive, editable=False, parent=None):
        """
        Public method to get a dialog to enter repository info.
        
        @param project reference to the project object
        @param archive name of the project in the repository (string)
        @param editable flag indicating that the project name is editable
            (boolean)
        @param parent parent widget (QWidget)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsNewProjectOptionsDialog(self, parent=None):
        """
        Public method to get a dialog to enter repository info for getting a
        new project.
        
        @param parent parent widget (QWidget)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
    def vcsRepositoryInfos(self, ppath):
        """
        Public method to retrieve information about the repository.
        
        @param ppath local path to get the repository infos (string)
        @return string with ready formated info for display (string)
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return ""
        
    def vcsGetProjectBrowserHelper(self, browser, project,
                                   isTranslationsBrowser=False):
        """
        Public method to instanciate a helper object for the different
        project browsers.
        
        @param browser reference to the project browser object
        @param project reference to the project object
        @param isTranslationsBrowser flag indicating, the helper is requested
            for the translations browser (this needs some special treatment)
        @return the project browser helper object
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return None                         # __IGNORE_WARNING_M831__
        
    def vcsGetProjectHelper(self, project):
        """
        Public method to instanciate a helper object for the project.
        
        @param project reference to the project object
        @return the project helper object
        @exception RuntimeError to indicate that this method must be
            implemented by a subclass
        """
        raise RuntimeError('Not implemented')
        
        return None                         # __IGNORE_WARNING_M831__
    
    #####################################################################
    ## methods above need to be implemented by a subclass
    #####################################################################
    
    def clearStatusCache(self):
        """
        Public method to clear the status cache.
        """
        pass
        
    def vcsInitConfig(self, project):
        """
        Public method to initialize the VCS configuration.
        
        This method could ensure, that certain files or directories are
        exclude from being version controlled.
        
        @param project reference to the project (Project)
        """
        pass
        
    def vcsSupportCommandOptions(self):
        """
        Public method to signal the support of user settable command options.
        
        @return flag indicating the support  of user settable command options
            (boolean)
        """
        return True
    
    def vcsSetOptions(self, options):
        """
        Public method used to set the options for the vcs.
        
        @param options a dictionary of option strings with keys as
                defined by the default options
        """
        if self.vcsSupportCommandOptions():
            for key in options:
                with contextlib.suppress(KeyError):
                    self.options[key] = options[key]
        
    def vcsGetOptions(self):
        """
        Public method used to retrieve the options of the vcs.
        
        @return a dictionary of option strings that can be passed to
            vcsSetOptions.
        """
        if self.vcsSupportCommandOptions():
            return self.options
        else:
            return self.defaultOptions
        
    def vcsSetOtherData(self, data):
        """
        Public method used to set vcs specific data.
        
        @param data a dictionary of vcs specific data
        """
        for key in data:
            with contextlib.suppress(KeyError):
                self.otherData[key] = data[key]
        
    def vcsGetOtherData(self):
        """
        Public method used to retrieve vcs specific data.
        
        @return a dictionary of vcs specific data
        """
        return self.otherData
        
    def vcsSetData(self, key, value):
        """
        Public method used to set an entry in the otherData dictionary.
        
        @param key the key of the data (string)
        @param value the value of the data
        """
        if key in self.interestingDataKeys:
            self.otherData[key] = value
        
    def vcsSetDataFromDict(self, dictionary):
        """
        Public method used to set entries in the otherData dictionary.
        
        @param dictionary dictionary to pick entries from
        """
        for key in self.interestingDataKeys:
            if key in dictionary:
                self.otherData[key] = dictionary[key]
    
    def vcsResolved(self, name):
        """
        Public method used to resolve conflicts of a file/directory.
        
        @param name file/directory name to be resolved
        @type str
        """
        # default implementation just refreshes the status
        self.checkVCSStatus()
    
    #####################################################################
    ## below are some utility methods
    #####################################################################
    
    def startSynchronizedProcess(self, proc, program, arguments,
                                 workingDir=None):
        """
        Public method to start a synchroneous process.
        
        This method starts a process and waits
        for its end while still serving the Qt event loop.
        
        @param proc process to start (QProcess)
        @param program path of the executable to start (string)
        @param arguments list of arguments for the process (list of strings)
        @param workingDir working directory for the process (string)
        @return flag indicating normal exit (boolean)
        """
        if proc is None:
            return False
            
        if workingDir:
            proc.setWorkingDirectory(workingDir)
        proc.start(program, arguments)
        procStarted = proc.waitForStarted(5000)
        if not procStarted:
            EricMessageBox.critical(
                None,
                QCoreApplication.translate(
                    "VersionControl", 'Process Generation Error'),
                QCoreApplication.translate(
                    "VersionControl",
                    'The process {0} could not be started. '
                    'Ensure, that it is in the search path.'
                ).format(program))
            return False
        else:
            while proc.state() == QProcess.ProcessState.Running:
                QApplication.processEvents()
                QThread.msleep(300)
                QApplication.processEvents()
            return (
                (proc.exitStatus() == QProcess.ExitStatus.NormalExit) and
                (proc.exitCode() == 0)
            )
        
    def splitPath(self, name):
        """
        Public method splitting name into a directory part and a file part.
        
        @param name path name (string)
        @return a tuple of 2 strings (dirname, filename).
        """
        if os.path.isdir(name):
            dn = os.path.abspath(name)
            fn = "."
        else:
            dn, fn = os.path.split(name)
        return (dn, fn)
    
    def splitPathList(self, names):
        """
        Public method splitting the list of names into a common directory part
        and a file list.
        
        @param names list of paths (list of strings)
        @return a tuple of string and list of strings (dirname, filenamelist)
        """
        dname = os.path.commonprefix(names)
        if dname:
            if not dname.endswith(os.sep):
                dname = os.path.dirname(dname) + os.sep
            fnames = [n.replace(dname, '') for n in names]
            dname = os.path.dirname(dname)
            return (dname, fnames)
        else:
            return ("/", names)

    def addArguments(self, args, argslist):
        """
        Public method to add an argument list to the already present
        arguments.
        
        @param args current arguments list (list of strings)
        @param argslist list of arguments (list of strings)
        """
        for arg in argslist:
            if arg != '':
                args.append(arg)
    
    ###########################################################################
    ## VCS status monitor thread related methods
    ###########################################################################
    
    def __statusMonitorStatus(self, status, statusMsg):
        """
        Private slot to receive the status monitor status.
        
        It simply re-emits the received status.
        
        @param status status of the monitoring thread
        @type str (one of ok, nok or off)
        @param statusMsg explanotory text for the signaled status
        @type str
        """
        self.vcsStatusMonitorStatus.emit(status, statusMsg)
        QCoreApplication.processEvents()

    def __statusMonitorData(self, statusList):
        """
        Private method to receive the status monitor data update.
        
        It simply re-emits the received status list.
        
        @param statusList list of status records
        @type list of str
        """
        self.vcsStatusMonitorData.emit(statusList)
        QCoreApplication.processEvents()
    
    def __statusMonitorAllData(self, statusDict):
        """
        Private method to receive all status monitor data.
        
        It simply re-emits the received status list.
        
        @param statusDict dictionary of status records
        @type dict
        """
        self.vcsStatusMonitorAllData.emit(statusDict)
        QCoreApplication.processEvents()
    
    def __statusMonitorInfo(self, info):
        """
        Private slot to receive the status monitor info message.
        
        It simply re-emits the received info message.
        
        @param info received info message
        @type str
        """
        self.vcsStatusMonitorInfo.emit(info)
        QCoreApplication.processEvents()
    
    def startStatusMonitor(self, project):
        """
        Public method to start the VCS status monitor thread.
        
        @param project reference to the project object
        @return reference to the monitor thread (QThread)
        """
        vcsStatusMonitorInterval = (
            project.pudata["VCSSTATUSMONITORINTERVAL"]
            if project.pudata["VCSSTATUSMONITORINTERVAL"] else
            Preferences.getVCS("StatusMonitorInterval")
        )
        if vcsStatusMonitorInterval > 0:
            self.statusMonitorThread = self._createStatusMonitorThread(
                vcsStatusMonitorInterval, project)
            if self.statusMonitorThread is not None:
                self.statusMonitorThread.vcsStatusMonitorData.connect(
                    self.__statusMonitorData,
                    Qt.ConnectionType.QueuedConnection)
                self.statusMonitorThread.vcsStatusMonitorAllData.connect(
                    self.__statusMonitorAllData,
                    Qt.ConnectionType.QueuedConnection)
                self.statusMonitorThread.vcsStatusMonitorStatus.connect(
                    self.__statusMonitorStatus,
                    Qt.ConnectionType.QueuedConnection)
                self.statusMonitorThread.vcsStatusMonitorInfo.connect(
                    self.__statusMonitorInfo,
                    Qt.ConnectionType.QueuedConnection)
                self.statusMonitorThread.setAutoUpdate(
                    Preferences.getVCS("AutoUpdate"))
                self.statusMonitorThread.start()
        else:
            self.statusMonitorThread = None
        return self.statusMonitorThread
    
    def stopStatusMonitor(self):
        """
        Public method to stop the VCS status monitor thread.
        """
        if self.statusMonitorThread is not None:
            self.__statusMonitorData(["--RESET--"])
            self.statusMonitorThread.vcsStatusMonitorData.disconnect(
                self.__statusMonitorData)
            self.statusMonitorThread.vcsStatusMonitorAllData.disconnect(
                self.__statusMonitorAllData)
            self.statusMonitorThread.vcsStatusMonitorStatus.disconnect(
                self.__statusMonitorStatus)
            self.statusMonitorThread.vcsStatusMonitorInfo.disconnect(
                self.__statusMonitorInfo)
            self.statusMonitorThread.stop()
            self.statusMonitorThread.wait(10000)
            if not self.statusMonitorThread.isFinished():
                self.statusMonitorThread.terminate()
                self.statusMonitorThread.wait(10000)
            self.statusMonitorThread = None
            self.__statusMonitorStatus(
                "off",
                QCoreApplication.translate(
                    "VersionControl",
                    "Repository status checking is switched off"))
            self.__statusMonitorInfo("")
    
    def setStatusMonitorInterval(self, interval, project):
        """
        Public method to change the monitor interval.
        
        @param interval new interval in seconds (integer)
        @param project reference to the project object
        """
        if self.statusMonitorThread is not None:
            if interval == 0:
                self.stopStatusMonitor()
            else:
                self.statusMonitorThread.setInterval(interval)
        else:
            self.startStatusMonitor(project)
    
    def getStatusMonitorInterval(self):
        """
        Public method to get the monitor interval.
        
        @return interval in seconds (integer)
        """
        if self.statusMonitorThread is not None:
            return self.statusMonitorThread.getInterval()
        else:
            return 0
    
    def setStatusMonitorAutoUpdate(self, auto):
        """
        Public method to enable the auto update function.
        
        @param auto status of the auto update function (boolean)
        """
        if self.statusMonitorThread is not None:
            self.statusMonitorThread.setAutoUpdate(auto)
    
    def getStatusMonitorAutoUpdate(self):
        """
        Public method to retrieve the status of the auto update function.
        
        @return status of the auto update function (boolean)
        """
        if self.statusMonitorThread is not None:
            return self.statusMonitorThread.getAutoUpdate()
        else:
            return False
    
    def checkVCSStatus(self):
        """
        Public method to wake up the VCS status monitor thread.
        """
        self.vcsStatusChanged.emit()
        
        if self.statusMonitorThread is not None:
            self.statusMonitorThread.checkStatus()
    
    def clearStatusMonitorCachedState(self, name):
        """
        Public method to clear the cached VCS state of a file/directory.
        
        @param name name of the entry to be cleared (string)
        """
        if self.statusMonitorThread is not None:
            self.statusMonitorThread.clearCachedState(name)
        
    def _createStatusMonitorThread(self, interval, project):
        """
        Protected method to create an instance of the VCS status monitor
        thread.
        
        Note: This method should be overwritten in subclasses in order to
        support VCS status monitoring.
        
        @param interval check interval for the monitor thread in seconds
            (integer)
        @param project reference to the project object
        @return reference to the monitor thread (QThread)
        """
        return None     # __IGNORE_WARNING_M831__
