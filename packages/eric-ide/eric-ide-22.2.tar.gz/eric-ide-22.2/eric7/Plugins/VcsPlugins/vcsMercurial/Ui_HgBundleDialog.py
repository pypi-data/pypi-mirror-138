# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsMercurial/HgBundleDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgBundleDialog(object):
    def setupUi(self, HgBundleDialog):
        HgBundleDialog.setObjectName("HgBundleDialog")
        HgBundleDialog.resize(450, 452)
        HgBundleDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgBundleDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(HgBundleDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.multipleButton = QtWidgets.QRadioButton(self.groupBox)
        self.multipleButton.setObjectName("multipleButton")
        self.gridLayout.addWidget(self.multipleButton, 0, 0, 1, 1)
        self.multipleEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.multipleEdit.setEnabled(False)
        self.multipleEdit.setTabChangesFocus(True)
        self.multipleEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.multipleEdit.setObjectName("multipleEdit")
        self.gridLayout.addWidget(self.multipleEdit, 0, 1, 1, 1)
        self.tagButton = QtWidgets.QRadioButton(self.groupBox)
        self.tagButton.setObjectName("tagButton")
        self.gridLayout.addWidget(self.tagButton, 1, 0, 1, 1)
        self.tagCombo = QtWidgets.QComboBox(self.groupBox)
        self.tagCombo.setEnabled(False)
        self.tagCombo.setEditable(True)
        self.tagCombo.setObjectName("tagCombo")
        self.gridLayout.addWidget(self.tagCombo, 1, 1, 1, 1)
        self.branchButton = QtWidgets.QRadioButton(self.groupBox)
        self.branchButton.setObjectName("branchButton")
        self.gridLayout.addWidget(self.branchButton, 2, 0, 1, 1)
        self.branchCombo = QtWidgets.QComboBox(self.groupBox)
        self.branchCombo.setEnabled(False)
        self.branchCombo.setEditable(True)
        self.branchCombo.setObjectName("branchCombo")
        self.gridLayout.addWidget(self.branchCombo, 2, 1, 1, 1)
        self.bookmarkButton = QtWidgets.QRadioButton(self.groupBox)
        self.bookmarkButton.setObjectName("bookmarkButton")
        self.gridLayout.addWidget(self.bookmarkButton, 3, 0, 1, 1)
        self.bookmarkCombo = QtWidgets.QComboBox(self.groupBox)
        self.bookmarkCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarkCombo.sizePolicy().hasHeightForWidth())
        self.bookmarkCombo.setSizePolicy(sizePolicy)
        self.bookmarkCombo.setEditable(True)
        self.bookmarkCombo.setObjectName("bookmarkCombo")
        self.gridLayout.addWidget(self.bookmarkCombo, 3, 1, 1, 1)
        self.noneButton = QtWidgets.QRadioButton(self.groupBox)
        self.noneButton.setChecked(True)
        self.noneButton.setObjectName("noneButton")
        self.gridLayout.addWidget(self.noneButton, 4, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(HgBundleDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.baseRevisionsEdit = QtWidgets.QPlainTextEdit(HgBundleDialog)
        self.baseRevisionsEdit.setTabChangesFocus(True)
        self.baseRevisionsEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.baseRevisionsEdit.setObjectName("baseRevisionsEdit")
        self.horizontalLayout_2.addWidget(self.baseRevisionsEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(HgBundleDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.compressionCombo = QtWidgets.QComboBox(HgBundleDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.compressionCombo.sizePolicy().hasHeightForWidth())
        self.compressionCombo.setSizePolicy(sizePolicy)
        self.compressionCombo.setObjectName("compressionCombo")
        self.horizontalLayout.addWidget(self.compressionCombo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.allCheckBox = QtWidgets.QCheckBox(HgBundleDialog)
        self.allCheckBox.setObjectName("allCheckBox")
        self.verticalLayout.addWidget(self.allCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgBundleDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgBundleDialog)
        self.buttonBox.accepted.connect(HgBundleDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgBundleDialog.reject) # type: ignore
        self.tagButton.toggled['bool'].connect(self.tagCombo.setEnabled) # type: ignore
        self.branchButton.toggled['bool'].connect(self.branchCombo.setEnabled) # type: ignore
        self.bookmarkButton.toggled['bool'].connect(self.bookmarkCombo.setEnabled) # type: ignore
        self.multipleButton.toggled['bool'].connect(self.multipleEdit.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgBundleDialog)
        HgBundleDialog.setTabOrder(self.multipleButton, self.multipleEdit)
        HgBundleDialog.setTabOrder(self.multipleEdit, self.tagButton)
        HgBundleDialog.setTabOrder(self.tagButton, self.tagCombo)
        HgBundleDialog.setTabOrder(self.tagCombo, self.branchButton)
        HgBundleDialog.setTabOrder(self.branchButton, self.branchCombo)
        HgBundleDialog.setTabOrder(self.branchCombo, self.bookmarkButton)
        HgBundleDialog.setTabOrder(self.bookmarkButton, self.bookmarkCombo)
        HgBundleDialog.setTabOrder(self.bookmarkCombo, self.noneButton)
        HgBundleDialog.setTabOrder(self.noneButton, self.baseRevisionsEdit)
        HgBundleDialog.setTabOrder(self.baseRevisionsEdit, self.compressionCombo)
        HgBundleDialog.setTabOrder(self.compressionCombo, self.allCheckBox)
        HgBundleDialog.setTabOrder(self.allCheckBox, self.buttonBox)

    def retranslateUi(self, HgBundleDialog):
        _translate = QtCore.QCoreApplication.translate
        HgBundleDialog.setWindowTitle(_translate("HgBundleDialog", "Mercurial Bundle"))
        self.groupBox.setTitle(_translate("HgBundleDialog", "Revision"))
        self.multipleButton.setToolTip(_translate("HgBundleDialog", "Select to specify multiple revisions"))
        self.multipleButton.setText(_translate("HgBundleDialog", "Revisions:"))
        self.multipleEdit.setToolTip(_translate("HgBundleDialog", "Enter revisions by number, id, range or revset expression one per line"))
        self.tagButton.setToolTip(_translate("HgBundleDialog", "Select to specify a revision by a tag"))
        self.tagButton.setText(_translate("HgBundleDialog", "Tag:"))
        self.tagCombo.setToolTip(_translate("HgBundleDialog", "Enter a tag name"))
        self.branchButton.setToolTip(_translate("HgBundleDialog", "Select to specify a revision by a branch"))
        self.branchButton.setText(_translate("HgBundleDialog", "Branch:"))
        self.branchCombo.setToolTip(_translate("HgBundleDialog", "Enter a branch name"))
        self.bookmarkButton.setToolTip(_translate("HgBundleDialog", "Select to specify a revision by a bookmark"))
        self.bookmarkButton.setText(_translate("HgBundleDialog", "Bookmark:"))
        self.bookmarkCombo.setToolTip(_translate("HgBundleDialog", "Enter a bookmark name"))
        self.noneButton.setToolTip(_translate("HgBundleDialog", "Select to not specify a specific revision"))
        self.noneButton.setText(_translate("HgBundleDialog", "No revision selected"))
        self.label_2.setText(_translate("HgBundleDialog", "Base Revisions:"))
        self.baseRevisionsEdit.setToolTip(_translate("HgBundleDialog", "Enter changesets by number, id, range or revset expression one per line"))
        self.label.setText(_translate("HgBundleDialog", "Compression:"))
        self.compressionCombo.setToolTip(_translate("HgBundleDialog", "Select the compression type (empty for default)"))
        self.allCheckBox.setToolTip(_translate("HgBundleDialog", "Select to bundle all changesets"))
        self.allCheckBox.setText(_translate("HgBundleDialog", "Bundle all changesets"))
