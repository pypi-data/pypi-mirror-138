# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsMercurial/HgMergeDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgMergeDialog(object):
    def setupUi(self, HgMergeDialog):
        HgMergeDialog.setObjectName("HgMergeDialog")
        HgMergeDialog.resize(372, 305)
        HgMergeDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgMergeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(HgMergeDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.numberButton = QtWidgets.QRadioButton(self.groupBox)
        self.numberButton.setObjectName("numberButton")
        self.gridLayout.addWidget(self.numberButton, 0, 0, 1, 1)
        self.numberSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.numberSpinBox.setEnabled(False)
        self.numberSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.numberSpinBox.setMaximum(999999999)
        self.numberSpinBox.setObjectName("numberSpinBox")
        self.gridLayout.addWidget(self.numberSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(158, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.idButton = QtWidgets.QRadioButton(self.groupBox)
        self.idButton.setObjectName("idButton")
        self.gridLayout.addWidget(self.idButton, 1, 0, 1, 1)
        self.idEdit = QtWidgets.QLineEdit(self.groupBox)
        self.idEdit.setEnabled(False)
        self.idEdit.setObjectName("idEdit")
        self.gridLayout.addWidget(self.idEdit, 1, 1, 1, 2)
        self.tagButton = QtWidgets.QRadioButton(self.groupBox)
        self.tagButton.setObjectName("tagButton")
        self.gridLayout.addWidget(self.tagButton, 2, 0, 1, 1)
        self.tagCombo = QtWidgets.QComboBox(self.groupBox)
        self.tagCombo.setEnabled(False)
        self.tagCombo.setEditable(True)
        self.tagCombo.setObjectName("tagCombo")
        self.gridLayout.addWidget(self.tagCombo, 2, 1, 1, 2)
        self.branchButton = QtWidgets.QRadioButton(self.groupBox)
        self.branchButton.setObjectName("branchButton")
        self.gridLayout.addWidget(self.branchButton, 3, 0, 1, 1)
        self.branchCombo = QtWidgets.QComboBox(self.groupBox)
        self.branchCombo.setEnabled(False)
        self.branchCombo.setEditable(True)
        self.branchCombo.setObjectName("branchCombo")
        self.gridLayout.addWidget(self.branchCombo, 3, 1, 1, 2)
        self.bookmarkButton = QtWidgets.QRadioButton(self.groupBox)
        self.bookmarkButton.setObjectName("bookmarkButton")
        self.gridLayout.addWidget(self.bookmarkButton, 4, 0, 1, 1)
        self.bookmarkCombo = QtWidgets.QComboBox(self.groupBox)
        self.bookmarkCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarkCombo.sizePolicy().hasHeightForWidth())
        self.bookmarkCombo.setSizePolicy(sizePolicy)
        self.bookmarkCombo.setEditable(True)
        self.bookmarkCombo.setObjectName("bookmarkCombo")
        self.gridLayout.addWidget(self.bookmarkCombo, 4, 1, 1, 2)
        self.noneButton = QtWidgets.QRadioButton(self.groupBox)
        self.noneButton.setChecked(True)
        self.noneButton.setObjectName("noneButton")
        self.gridLayout.addWidget(self.noneButton, 5, 0, 1, 3)
        self.verticalLayout.addWidget(self.groupBox)
        self.forceCheckBox = QtWidgets.QCheckBox(HgMergeDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.verticalLayout.addWidget(self.forceCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgMergeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgMergeDialog)
        self.buttonBox.accepted.connect(HgMergeDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgMergeDialog.reject) # type: ignore
        self.numberButton.toggled['bool'].connect(self.numberSpinBox.setEnabled) # type: ignore
        self.idButton.toggled['bool'].connect(self.idEdit.setEnabled) # type: ignore
        self.tagButton.toggled['bool'].connect(self.tagCombo.setEnabled) # type: ignore
        self.branchButton.toggled['bool'].connect(self.branchCombo.setEnabled) # type: ignore
        self.bookmarkButton.toggled['bool'].connect(self.bookmarkCombo.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgMergeDialog)
        HgMergeDialog.setTabOrder(self.numberButton, self.numberSpinBox)
        HgMergeDialog.setTabOrder(self.numberSpinBox, self.idButton)
        HgMergeDialog.setTabOrder(self.idButton, self.idEdit)
        HgMergeDialog.setTabOrder(self.idEdit, self.tagButton)
        HgMergeDialog.setTabOrder(self.tagButton, self.tagCombo)
        HgMergeDialog.setTabOrder(self.tagCombo, self.branchButton)
        HgMergeDialog.setTabOrder(self.branchButton, self.branchCombo)
        HgMergeDialog.setTabOrder(self.branchCombo, self.bookmarkButton)
        HgMergeDialog.setTabOrder(self.bookmarkButton, self.bookmarkCombo)
        HgMergeDialog.setTabOrder(self.bookmarkCombo, self.noneButton)
        HgMergeDialog.setTabOrder(self.noneButton, self.forceCheckBox)
        HgMergeDialog.setTabOrder(self.forceCheckBox, self.buttonBox)

    def retranslateUi(self, HgMergeDialog):
        _translate = QtCore.QCoreApplication.translate
        HgMergeDialog.setWindowTitle(_translate("HgMergeDialog", "Mercurial Merge"))
        self.groupBox.setTitle(_translate("HgMergeDialog", "Revision"))
        self.numberButton.setToolTip(_translate("HgMergeDialog", "Select to specify a revision by number"))
        self.numberButton.setText(_translate("HgMergeDialog", "Number"))
        self.numberSpinBox.setToolTip(_translate("HgMergeDialog", "Enter a revision number"))
        self.idButton.setToolTip(_translate("HgMergeDialog", "Select to specify a revision by changeset id"))
        self.idButton.setText(_translate("HgMergeDialog", "Id:"))
        self.idEdit.setToolTip(_translate("HgMergeDialog", "Enter a changeset id"))
        self.tagButton.setToolTip(_translate("HgMergeDialog", "Select to specify a revision by a tag"))
        self.tagButton.setText(_translate("HgMergeDialog", "Tag:"))
        self.tagCombo.setToolTip(_translate("HgMergeDialog", "Enter a tag name"))
        self.branchButton.setToolTip(_translate("HgMergeDialog", "Select to specify a revision by a branch"))
        self.branchButton.setText(_translate("HgMergeDialog", "Branch:"))
        self.branchCombo.setToolTip(_translate("HgMergeDialog", "Enter a branch name"))
        self.bookmarkButton.setToolTip(_translate("HgMergeDialog", "Select to specify a revision by a bookmark"))
        self.bookmarkButton.setText(_translate("HgMergeDialog", "Bookmark:"))
        self.bookmarkCombo.setToolTip(_translate("HgMergeDialog", "Enter a bookmark name"))
        self.noneButton.setToolTip(_translate("HgMergeDialog", "Select to not specify a specific revision"))
        self.noneButton.setText(_translate("HgMergeDialog", "No revision selected"))
        self.forceCheckBox.setToolTip(_translate("HgMergeDialog", "Select to force the merge operation"))
        self.forceCheckBox.setText(_translate("HgMergeDialog", "Enforce merge"))
