# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsGit/GitSubmodulesSyncDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GitSubmodulesSyncDialog(object):
    def setupUi(self, GitSubmodulesSyncDialog):
        GitSubmodulesSyncDialog.setObjectName("GitSubmodulesSyncDialog")
        GitSubmodulesSyncDialog.resize(400, 300)
        GitSubmodulesSyncDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitSubmodulesSyncDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(GitSubmodulesSyncDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.submodulesList = QtWidgets.QListWidget(GitSubmodulesSyncDialog)
        self.submodulesList.setAlternatingRowColors(True)
        self.submodulesList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.submodulesList.setObjectName("submodulesList")
        self.verticalLayout.addWidget(self.submodulesList)
        self.recursiveCheckBox = QtWidgets.QCheckBox(GitSubmodulesSyncDialog)
        self.recursiveCheckBox.setObjectName("recursiveCheckBox")
        self.verticalLayout.addWidget(self.recursiveCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitSubmodulesSyncDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitSubmodulesSyncDialog)
        self.buttonBox.accepted.connect(GitSubmodulesSyncDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GitSubmodulesSyncDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GitSubmodulesSyncDialog)

    def retranslateUi(self, GitSubmodulesSyncDialog):
        _translate = QtCore.QCoreApplication.translate
        GitSubmodulesSyncDialog.setWindowTitle(_translate("GitSubmodulesSyncDialog", "Synchronize Submodule URLs"))
        self.label.setText(_translate("GitSubmodulesSyncDialog", "Selected Submodules:"))
        self.submodulesList.setToolTip(_translate("GitSubmodulesSyncDialog", "Select the submodules to be synchronized"))
        self.recursiveCheckBox.setToolTip(_translate("GitSubmodulesSyncDialog", "Select to perform a recursive synchronization"))
        self.recursiveCheckBox.setText(_translate("GitSubmodulesSyncDialog", "Recursive Operation"))
