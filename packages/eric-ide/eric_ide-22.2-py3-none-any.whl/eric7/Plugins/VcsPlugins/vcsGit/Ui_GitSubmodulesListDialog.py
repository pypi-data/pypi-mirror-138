# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsGit/GitSubmodulesListDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GitSubmodulesListDialog(object):
    def setupUi(self, GitSubmodulesListDialog):
        GitSubmodulesListDialog.setObjectName("GitSubmodulesListDialog")
        GitSubmodulesListDialog.resize(500, 300)
        GitSubmodulesListDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitSubmodulesListDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.submodulesList = QtWidgets.QTreeWidget(GitSubmodulesListDialog)
        self.submodulesList.setAlternatingRowColors(True)
        self.submodulesList.setRootIsDecorated(False)
        self.submodulesList.setItemsExpandable(False)
        self.submodulesList.setExpandsOnDoubleClick(False)
        self.submodulesList.setObjectName("submodulesList")
        self.submodulesList.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.submodulesList)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitSubmodulesListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitSubmodulesListDialog)
        self.buttonBox.accepted.connect(GitSubmodulesListDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GitSubmodulesListDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GitSubmodulesListDialog)

    def retranslateUi(self, GitSubmodulesListDialog):
        _translate = QtCore.QCoreApplication.translate
        GitSubmodulesListDialog.setWindowTitle(_translate("GitSubmodulesListDialog", "Defined Submodules"))
        self.submodulesList.headerItem().setText(0, _translate("GitSubmodulesListDialog", "Name"))
        self.submodulesList.headerItem().setText(1, _translate("GitSubmodulesListDialog", "Path"))
        self.submodulesList.headerItem().setText(2, _translate("GitSubmodulesListDialog", "URL"))
        self.submodulesList.headerItem().setText(3, _translate("GitSubmodulesListDialog", "Branch"))
