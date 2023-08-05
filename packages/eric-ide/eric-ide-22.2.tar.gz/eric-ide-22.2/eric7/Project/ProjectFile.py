# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the project JSON file.
"""

import json
import time
import contextlib
import typing

from PyQt6.QtCore import QObject

from EricWidgets import EricMessageBox
from EricGui.EricOverrideCursor import EricOverridenCursor

import Preferences
import Utilities

Project = typing.TypeVar("Project")


class ProjectFile(QObject):
    """
    Class representing the project JSON file.
    """
    def __init__(self, project: Project, parent: QObject = None):
        """
        Constructor
        
        @param project reference to the project object
        @type Project
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super().__init__(parent)
        self.__project = project
    
    def writeFile(self, filename: str) -> bool:
        """
        Public method to write the project data to a project JSON file.
        
        @param filename name of the project file
        @type str
        @return flag indicating a successful write
        @rtype bool
        """
        projectDict = {}
        projectDict["header"] = {
            "comment": "eric project file for project {0}".format(
                self.__project.getProjectName()),
            "copyright": "Copyright (C) {0} {1}, {2}".format(
                time.strftime('%Y'),
                self.__project.pdata["AUTHOR"],
                self.__project.pdata["EMAIL"])
        }
        
        if Preferences.getProject("TimestampFile"):
            projectDict["header"]["saved"] = (
                time.strftime('%Y-%m-%d, %H:%M:%S')
            )
        
        projectDict["project"] = self.__project.pdata
        
        # modify paths to contain universal separators
        for key in (
            "SOURCES", "FORMS", "TRANSLATIONS", "TRANSLATIONEXCEPTIONS",
            "RESOURCES", "INTERFACES", "PROTOCOLS", "OTHERS"
        ):
            with contextlib.suppress(KeyError):
                projectDict["project"][key] = [
                    Utilities.fromNativeSeparators(f)
                    for f in projectDict["project"][key]
                ]
        for key in (
            "SPELLWORDS", "SPELLEXCLUDES", "TRANSLATIONPATTERN",
            "TRANSLATIONSBINPATH", "MAINSCRIPT"
        ):
            with contextlib.suppress(KeyError):
                projectDict["project"][key] = Utilities.fromNativeSeparators(
                    projectDict["project"][key])
        
        try:
            jsonString = json.dumps(projectDict, indent=2, sort_keys=True)
            with open(filename, "w", newline="") as f:
                f.write(jsonString)
        except (TypeError, OSError) as err:
            with EricOverridenCursor():
                EricMessageBox.critical(
                    None,
                    self.tr("Save Project File"),
                    self.tr(
                        "<p>The project file <b>{0}</b> could not be "
                        "written.</p><p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the project data from a project JSON file.
        
        @param filename name of the project file
        @type str
        @return flag indicating a successful read
        @rtype bool
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            projectDict = json.loads(jsonString)
        except (OSError, json.JSONDecodeError) as err:
            EricMessageBox.critical(
                None,
                self.tr("Read Project File"),
                self.tr(
                    "<p>The project file <b>{0}</b> could not be "
                    "read.</p><p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return False
        
        # modify paths to contain native separators
        for key in (
            "SOURCES", "FORMS", "TRANSLATIONS", "TRANSLATIONEXCEPTIONS",
            "RESOURCES", "INTERFACES", "PROTOCOLS", "OTHERS"
        ):
            with contextlib.suppress(KeyError):
                projectDict["project"][key] = [
                    Utilities.toNativeSeparators(f)
                    for f in projectDict["project"][key]
                ]
        for key in (
            "SPELLWORDS", "SPELLEXCLUDES", "TRANSLATIONPATTERN",
            "TRANSLATIONSBINPATH", "MAINSCRIPT"
        ):
            with contextlib.suppress(KeyError):
                projectDict["project"][key] = Utilities.toNativeSeparators(
                    projectDict["project"][key])
        
        self.__project.pdata = projectDict["project"]
        
        return True
