# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/WebBrowser/QtHelp/QtHelpDocumentationConfigurationDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_QtHelpDocumentationConfigurationDialog(object):
    def setupUi(self, QtHelpDocumentationConfigurationDialog):
        QtHelpDocumentationConfigurationDialog.setObjectName("QtHelpDocumentationConfigurationDialog")
        QtHelpDocumentationConfigurationDialog.resize(600, 500)
        QtHelpDocumentationConfigurationDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(QtHelpDocumentationConfigurationDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(QtHelpDocumentationConfigurationDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.documentsTab = QtWidgets.QWidget()
        self.documentsTab.setObjectName("documentsTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.documentsTab)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.documentationSettingsWidget = QtHelpDocumentationSettingsWidget(self.documentsTab)
        self.documentationSettingsWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.documentationSettingsWidget.setObjectName("documentationSettingsWidget")
        self.verticalLayout.addWidget(self.documentationSettingsWidget)
        self.tabWidget.addTab(self.documentsTab, "")
        self.filtersTab = QtWidgets.QWidget()
        self.filtersTab.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.filtersTab.setObjectName("filtersTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.filtersTab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.filterSettingsWidget = QHelpFilterSettingsWidget(self.filtersTab)
        self.filterSettingsWidget.setObjectName("filterSettingsWidget")
        self.verticalLayout_2.addWidget(self.filterSettingsWidget)
        self.tabWidget.addTab(self.filtersTab, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtHelpDocumentationConfigurationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Apply|QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(QtHelpDocumentationConfigurationDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.rejected.connect(QtHelpDocumentationConfigurationDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(QtHelpDocumentationConfigurationDialog)

    def retranslateUi(self, QtHelpDocumentationConfigurationDialog):
        _translate = QtCore.QCoreApplication.translate
        QtHelpDocumentationConfigurationDialog.setWindowTitle(_translate("QtHelpDocumentationConfigurationDialog", "Manage QtHelp Documentation"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.documentsTab), _translate("QtHelpDocumentationConfigurationDialog", "Registered Documents"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filtersTab), _translate("QtHelpDocumentationConfigurationDialog", "Filters"))
from .QtHelpDocumentationSettingsWidget import QtHelpDocumentationSettingsWidget
from PyQt6.QtHelp import QHelpFilterSettingsWidget
