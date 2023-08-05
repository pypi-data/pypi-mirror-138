# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing an import or import from node.
"""

#
# adapted from flake8-alphabetize v0.0.17
#

import ast
from functools import total_ordering

from .ImportsEnums import GroupEnum, NodeTypeEnum


class ImportNodeException(Exception):
    """
    Class representing an exception for an invalid import node.
    """
    pass


@total_ordering
class ImportNode:
    """
    Class representing an import or import from node.
    """
    def __init__(self, appNames, astNode, checker):
        """
        Constructor
        
        @param appNames list of application package names
        @type list of str
        @param astNode reference to the ast node
        @type ast.AST
        @param checker reference to the checker object
        @type ImportsChecker
        @exception ImportNodeException raised to indicate an invalid node was
            given to this class
        """
        if not isinstance(astNode, (ast.Import, ast.ImportFrom)):
            raise ImportNodeException(
                "Node type {0} not recognized".format(type(astNode))
            )
        
        self.node = astNode
        self.error = None
        level = None
        group = None
        
        if isinstance(astNode, ast.Import):
            self.nodeType = NodeTypeEnum.IMPORT
            names = astNode.names

            self.moduleName = names[0].name
            level = 0
        
        elif isinstance(astNode, ast.ImportFrom):
            module = astNode.module
            self.moduleName = "" if module is None else module
            self.nodeType = NodeTypeEnum.IMPORT_FROM

            names = [n.name for n in astNode.names]
            expectedNames = sorted(names)
            if names != expectedNames:
                self.error = (self.node, "I202", ", ".join(expectedNames))
            level = astNode.level
        
        if self.moduleName == "__future__":
            group = GroupEnum.FUTURE
        elif self.moduleName in checker.getStandardModules():
            group = GroupEnum.STDLIB
        elif level > 0:
            group = GroupEnum.APPLICATION
        else:
            group = GroupEnum.THIRD_PARTY
            for name in appNames:
                if (
                    name == self.moduleName or
                    self.moduleName.startswith("{0}.".format(name))
                ):
                    group = GroupEnum.APPLICATION
                    break
        
        if group == GroupEnum.STDLIB:
            self.sorter = group, self.nodeType, self.moduleName
        else:
            m = self.moduleName
            dotIndex = m.find(".")
            topName = m if dotIndex == -1 else m[:dotIndex]
            self.sorter = group, level, topName, self.nodeType, m
    
    def __eq__(self, other):
        """
        Special method implementing the equality operator.
        
        @param other reference to the object to compare
        @type ImportNode
        @return flag indicating equality
        @rtype bool
        """
        return self.sorter == other.sorter
    
    def __lt__(self, other):
        """
        Special method implementing the less than operator.
        
        @param other reference to the object to compare
        @type ImportNode
        @return flag indicating a less than situation
        @rtype bool
        """
        return self.sorter < other.sorter
    
    def __str__(self):
        """
        Special method to create a string representation of the instance.
        
        @return string representation of the instance
        @rtype str
        @exception ImportNodeException raised to indicate an invalid node was
            given to this class
        """
        if (
            self.nodeType not in (NodeTypeEnum.IMPORT,
                                  NodeTypeEnum.IMPORT_FROM)
        ):
            raise ImportNodeException(
                "The node type {0} is not recognized.".format(self.nodeType)
            )
        
        if self.nodeType == NodeTypeEnum.IMPORT:
            return "import {0}".format(self.moduleName)
        elif self.nodeType == NodeTypeEnum.IMPORT_FROM:
            level = self.node.level
            levelStr = "" if level == 0 else "." * level
            names = [
                n.name + ("" if n.asname is None else
                          " as {0}".format(n.asname))
                for n in self.node.names
            ]
            return "from {0}{1} import {2}".format(
                levelStr, self.moduleName, ", ".join(names))
        
        return None
