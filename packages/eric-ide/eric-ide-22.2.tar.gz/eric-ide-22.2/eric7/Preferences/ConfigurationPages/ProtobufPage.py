# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the protobuf configuration page.
"""

from EricWidgets.EricPathPicker import EricPathPickerModes

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_ProtobufPage import Ui_ProtobufPage

import Preferences


class ProtobufPage(ConfigurationPageBase, Ui_ProtobufPage):
    """
    Class implementing the protobuf configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setupUi(self)
        self.setObjectName("ProtobufPage")
        
        self.protocPicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.protocPicker.setToolTip(self.tr(
            "Press to select the Protobuf compiler via a file selection"
            " dialog."))
        
        self.grpcPythonPicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.grpcPythonPicker.setToolTip(self.tr(
            "Press to select the Python interpreter containing the gRPC"
            " compiler via a file selection dialog."))
        
        # set initial values
        self.protocPicker.setText(Preferences.getProtobuf("protoc"))
        self.grpcPythonPicker.setText(Preferences.getProtobuf("grpcPython"))
        
    def save(self):
        """
        Public slot to save the protobuf configuration.
        """
        Preferences.setProtobuf("protoc", self.protocPicker.text())
        Preferences.setProtobuf("grpcPython", self.grpcPythonPicker.text())
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = ProtobufPage()
    return page
