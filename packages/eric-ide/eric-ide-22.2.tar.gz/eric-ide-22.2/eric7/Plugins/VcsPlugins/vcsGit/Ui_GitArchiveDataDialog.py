# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsGit/GitArchiveDataDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GitArchiveDataDialog(object):
    def setupUi(self, GitArchiveDataDialog):
        GitArchiveDataDialog.setObjectName("GitArchiveDataDialog")
        GitArchiveDataDialog.resize(553, 308)
        GitArchiveDataDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitArchiveDataDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(GitArchiveDataDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.revButton = QtWidgets.QRadioButton(self.groupBox)
        self.revButton.setObjectName("revButton")
        self.gridLayout.addWidget(self.revButton, 0, 0, 1, 1)
        self.revEdit = QtWidgets.QLineEdit(self.groupBox)
        self.revEdit.setEnabled(False)
        self.revEdit.setObjectName("revEdit")
        self.gridLayout.addWidget(self.revEdit, 0, 1, 1, 2)
        self.tagButton = QtWidgets.QRadioButton(self.groupBox)
        self.tagButton.setObjectName("tagButton")
        self.gridLayout.addWidget(self.tagButton, 1, 0, 1, 1)
        self.tagCombo = QtWidgets.QComboBox(self.groupBox)
        self.tagCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagCombo.sizePolicy().hasHeightForWidth())
        self.tagCombo.setSizePolicy(sizePolicy)
        self.tagCombo.setEditable(True)
        self.tagCombo.setObjectName("tagCombo")
        self.gridLayout.addWidget(self.tagCombo, 1, 1, 1, 2)
        self.branchButton = QtWidgets.QRadioButton(self.groupBox)
        self.branchButton.setObjectName("branchButton")
        self.gridLayout.addWidget(self.branchButton, 2, 0, 1, 1)
        self.branchCombo = QtWidgets.QComboBox(self.groupBox)
        self.branchCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.branchCombo.sizePolicy().hasHeightForWidth())
        self.branchCombo.setSizePolicy(sizePolicy)
        self.branchCombo.setEditable(True)
        self.branchCombo.setObjectName("branchCombo")
        self.gridLayout.addWidget(self.branchCombo, 2, 1, 1, 2)
        self.tipButton = QtWidgets.QRadioButton(self.groupBox)
        self.tipButton.setChecked(True)
        self.tipButton.setObjectName("tipButton")
        self.gridLayout.addWidget(self.tipButton, 3, 0, 1, 3)
        self.verticalLayout.addWidget(self.groupBox)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(GitArchiveDataDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.formatComboBox = QtWidgets.QComboBox(GitArchiveDataDialog)
        self.formatComboBox.setObjectName("formatComboBox")
        self.gridLayout_2.addWidget(self.formatComboBox, 0, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(GitArchiveDataDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.fileEdit = QtWidgets.QLineEdit(GitArchiveDataDialog)
        self.fileEdit.setObjectName("fileEdit")
        self.gridLayout_2.addWidget(self.fileEdit, 1, 1, 1, 1)
        self.fileButton = QtWidgets.QToolButton(GitArchiveDataDialog)
        self.fileButton.setObjectName("fileButton")
        self.gridLayout_2.addWidget(self.fileButton, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(GitArchiveDataDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.prefixEdit = QtWidgets.QLineEdit(GitArchiveDataDialog)
        self.prefixEdit.setObjectName("prefixEdit")
        self.gridLayout_2.addWidget(self.prefixEdit, 2, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitArchiveDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitArchiveDataDialog)
        self.buttonBox.accepted.connect(GitArchiveDataDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GitArchiveDataDialog.reject) # type: ignore
        self.revButton.toggled['bool'].connect(self.revEdit.setEnabled) # type: ignore
        self.tagButton.toggled['bool'].connect(self.tagCombo.setEnabled) # type: ignore
        self.branchButton.toggled['bool'].connect(self.branchCombo.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GitArchiveDataDialog)
        GitArchiveDataDialog.setTabOrder(self.revButton, self.revEdit)
        GitArchiveDataDialog.setTabOrder(self.revEdit, self.tagButton)
        GitArchiveDataDialog.setTabOrder(self.tagButton, self.tagCombo)
        GitArchiveDataDialog.setTabOrder(self.tagCombo, self.branchButton)
        GitArchiveDataDialog.setTabOrder(self.branchButton, self.branchCombo)
        GitArchiveDataDialog.setTabOrder(self.branchCombo, self.tipButton)
        GitArchiveDataDialog.setTabOrder(self.tipButton, self.formatComboBox)
        GitArchiveDataDialog.setTabOrder(self.formatComboBox, self.fileEdit)
        GitArchiveDataDialog.setTabOrder(self.fileEdit, self.fileButton)
        GitArchiveDataDialog.setTabOrder(self.fileButton, self.prefixEdit)

    def retranslateUi(self, GitArchiveDataDialog):
        _translate = QtCore.QCoreApplication.translate
        GitArchiveDataDialog.setWindowTitle(_translate("GitArchiveDataDialog", "Git Archive"))
        self.groupBox.setTitle(_translate("GitArchiveDataDialog", "Revision"))
        self.revButton.setToolTip(_translate("GitArchiveDataDialog", "Select to specify a revision by a revision expression"))
        self.revButton.setText(_translate("GitArchiveDataDialog", "Commit:"))
        self.revEdit.setToolTip(_translate("GitArchiveDataDialog", "Enter a commit id"))
        self.tagButton.setToolTip(_translate("GitArchiveDataDialog", "Select to specify a revision by a tag"))
        self.tagButton.setText(_translate("GitArchiveDataDialog", "Tag:"))
        self.tagCombo.setToolTip(_translate("GitArchiveDataDialog", "Enter a tag name"))
        self.branchButton.setToolTip(_translate("GitArchiveDataDialog", "Select to specify a revision by a branch"))
        self.branchButton.setText(_translate("GitArchiveDataDialog", "Branch:"))
        self.branchCombo.setToolTip(_translate("GitArchiveDataDialog", "Enter a branch name"))
        self.tipButton.setToolTip(_translate("GitArchiveDataDialog", "Select HEAD revision"))
        self.tipButton.setText(_translate("GitArchiveDataDialog", "HEAD"))
        self.label.setText(_translate("GitArchiveDataDialog", "Format:"))
        self.formatComboBox.setToolTip(_translate("GitArchiveDataDialog", "Select the archive format"))
        self.label_3.setText(_translate("GitArchiveDataDialog", "File Name:"))
        self.fileEdit.setToolTip(_translate("GitArchiveDataDialog", "Enter the name of the archive file"))
        self.fileButton.setToolTip(_translate("GitArchiveDataDialog", "Select the archive file via a file selection dialog"))
        self.label_2.setText(_translate("GitArchiveDataDialog", "Prefix:"))
        self.prefixEdit.setToolTip(_translate("GitArchiveDataDialog", "Enter a prefix to be prepended to each file"))
