# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsSubversion/SvnBlameDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SvnBlameDialog(object):
    def setupUi(self, SvnBlameDialog):
        SvnBlameDialog.setObjectName("SvnBlameDialog")
        SvnBlameDialog.resize(690, 750)
        SvnBlameDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(SvnBlameDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.blameList = QtWidgets.QTreeWidget(SvnBlameDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.blameList.sizePolicy().hasHeightForWidth())
        self.blameList.setSizePolicy(sizePolicy)
        self.blameList.setAlternatingRowColors(True)
        self.blameList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.blameList.setRootIsDecorated(False)
        self.blameList.setItemsExpandable(False)
        self.blameList.setObjectName("blameList")
        self.blameList.header().setStretchLastSection(False)
        self.vboxlayout.addWidget(self.blameList)
        self.errorGroup = QtWidgets.QGroupBox(SvnBlameDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout1.addWidget(self.errors)
        self.vboxlayout.addWidget(self.errorGroup)
        self.inputGroup = QtWidgets.QGroupBox(SvnBlameDialog)
        self.inputGroup.setObjectName("inputGroup")
        self.gridlayout = QtWidgets.QGridLayout(self.inputGroup)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtWidgets.QSpacerItem(327, 29, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.inputGroup)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton, 1, 2, 1, 1)
        self.input = QtWidgets.QLineEdit(self.inputGroup)
        self.input.setObjectName("input")
        self.gridlayout.addWidget(self.input, 0, 0, 1, 3)
        self.passwordCheckBox = QtWidgets.QCheckBox(self.inputGroup)
        self.passwordCheckBox.setObjectName("passwordCheckBox")
        self.gridlayout.addWidget(self.passwordCheckBox, 1, 0, 1, 1)
        self.vboxlayout.addWidget(self.inputGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(SvnBlameDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(SvnBlameDialog)
        QtCore.QMetaObject.connectSlotsByName(SvnBlameDialog)
        SvnBlameDialog.setTabOrder(self.blameList, self.errors)
        SvnBlameDialog.setTabOrder(self.errors, self.input)
        SvnBlameDialog.setTabOrder(self.input, self.passwordCheckBox)
        SvnBlameDialog.setTabOrder(self.passwordCheckBox, self.sendButton)
        SvnBlameDialog.setTabOrder(self.sendButton, self.buttonBox)

    def retranslateUi(self, SvnBlameDialog):
        _translate = QtCore.QCoreApplication.translate
        SvnBlameDialog.setWindowTitle(_translate("SvnBlameDialog", "Subversion Blame"))
        self.blameList.headerItem().setText(0, _translate("SvnBlameDialog", "Revision"))
        self.blameList.headerItem().setText(1, _translate("SvnBlameDialog", "Author"))
        self.blameList.headerItem().setText(2, _translate("SvnBlameDialog", "Line"))
        self.errorGroup.setTitle(_translate("SvnBlameDialog", "Errors"))
        self.inputGroup.setTitle(_translate("SvnBlameDialog", "Input"))
        self.sendButton.setToolTip(_translate("SvnBlameDialog", "Press to send the input to the subversion process"))
        self.sendButton.setText(_translate("SvnBlameDialog", "&Send"))
        self.sendButton.setShortcut(_translate("SvnBlameDialog", "Alt+S"))
        self.input.setToolTip(_translate("SvnBlameDialog", "Enter data to be sent to the subversion process"))
        self.passwordCheckBox.setToolTip(_translate("SvnBlameDialog", "Select to switch the input field to password mode"))
        self.passwordCheckBox.setText(_translate("SvnBlameDialog", "&Password Mode"))
        self.passwordCheckBox.setShortcut(_translate("SvnBlameDialog", "Alt+P"))
