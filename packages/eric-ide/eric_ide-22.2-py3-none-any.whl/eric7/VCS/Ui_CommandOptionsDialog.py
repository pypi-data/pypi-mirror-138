# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/VCS/CommandOptionsDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VcsCommandOptionsDialog(object):
    def setupUi(self, VcsCommandOptionsDialog):
        VcsCommandOptionsDialog.setObjectName("VcsCommandOptionsDialog")
        VcsCommandOptionsDialog.resize(531, 413)
        VcsCommandOptionsDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(VcsCommandOptionsDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.historyLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.historyLabel.setObjectName("historyLabel")
        self.gridlayout.addWidget(self.historyLabel, 8, 0, 1, 1)
        self.addLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.addLabel.setObjectName("addLabel")
        self.gridlayout.addWidget(self.addLabel, 4, 0, 1, 1)
        self.removeLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.removeLabel.setObjectName("removeLabel")
        self.gridlayout.addWidget(self.removeLabel, 5, 0, 1, 1)
        self.tagLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.tagLabel.setObjectName("tagLabel")
        self.gridlayout.addWidget(self.tagLabel, 10, 0, 1, 1)
        self.commitEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.commitEdit.setObjectName("commitEdit")
        self.gridlayout.addWidget(self.commitEdit, 1, 1, 1, 1)
        self.historyEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.historyEdit.setObjectName("historyEdit")
        self.gridlayout.addWidget(self.historyEdit, 8, 1, 1, 1)
        self.diffEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.diffEdit.setObjectName("diffEdit")
        self.gridlayout.addWidget(self.diffEdit, 6, 1, 1, 1)
        self.updateEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.updateEdit.setObjectName("updateEdit")
        self.gridlayout.addWidget(self.updateEdit, 3, 1, 1, 1)
        self.logEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.logEdit.setObjectName("logEdit")
        self.gridlayout.addWidget(self.logEdit, 7, 1, 1, 1)
        self.tagEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.tagEdit.setObjectName("tagEdit")
        self.gridlayout.addWidget(self.tagEdit, 10, 1, 1, 1)
        self.statusEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.statusEdit.setObjectName("statusEdit")
        self.gridlayout.addWidget(self.statusEdit, 9, 1, 1, 1)
        self.diffLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.diffLabel.setObjectName("diffLabel")
        self.gridlayout.addWidget(self.diffLabel, 6, 0, 1, 1)
        self.globalLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.globalLabel.setObjectName("globalLabel")
        self.gridlayout.addWidget(self.globalLabel, 0, 0, 1, 1)
        self.exportEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.exportEdit.setObjectName("exportEdit")
        self.gridlayout.addWidget(self.exportEdit, 11, 1, 1, 1)
        self.addEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.addEdit.setObjectName("addEdit")
        self.gridlayout.addWidget(self.addEdit, 4, 1, 1, 1)
        self.logLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.logLabel.setObjectName("logLabel")
        self.gridlayout.addWidget(self.logLabel, 7, 0, 1, 1)
        self.statusLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.statusLabel.setObjectName("statusLabel")
        self.gridlayout.addWidget(self.statusLabel, 9, 0, 1, 1)
        self.removeEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.removeEdit.setObjectName("removeEdit")
        self.gridlayout.addWidget(self.removeEdit, 5, 1, 1, 1)
        self.checkoutEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.checkoutEdit.setObjectName("checkoutEdit")
        self.gridlayout.addWidget(self.checkoutEdit, 2, 1, 1, 1)
        self.commitLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.commitLabel.setObjectName("commitLabel")
        self.gridlayout.addWidget(self.commitLabel, 1, 0, 1, 1)
        self.exportLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.exportLabel.setObjectName("exportLabel")
        self.gridlayout.addWidget(self.exportLabel, 11, 0, 1, 1)
        self.checkoutLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.checkoutLabel.setObjectName("checkoutLabel")
        self.gridlayout.addWidget(self.checkoutLabel, 2, 0, 1, 1)
        self.updateLabel = QtWidgets.QLabel(VcsCommandOptionsDialog)
        self.updateLabel.setObjectName("updateLabel")
        self.gridlayout.addWidget(self.updateLabel, 3, 0, 1, 1)
        self.globalEdit = QtWidgets.QLineEdit(VcsCommandOptionsDialog)
        self.globalEdit.setObjectName("globalEdit")
        self.gridlayout.addWidget(self.globalEdit, 0, 1, 1, 1)
        self.vboxlayout.addLayout(self.gridlayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(VcsCommandOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)
        self.historyLabel.setBuddy(self.historyEdit)
        self.addLabel.setBuddy(self.addEdit)
        self.removeLabel.setBuddy(self.removeEdit)
        self.tagLabel.setBuddy(self.tagEdit)
        self.diffLabel.setBuddy(self.diffEdit)
        self.globalLabel.setBuddy(self.globalEdit)
        self.logLabel.setBuddy(self.logEdit)
        self.statusLabel.setBuddy(self.statusEdit)
        self.commitLabel.setBuddy(self.commitEdit)
        self.exportLabel.setBuddy(self.exportEdit)
        self.checkoutLabel.setBuddy(self.checkoutEdit)
        self.updateLabel.setBuddy(self.updateEdit)

        self.retranslateUi(VcsCommandOptionsDialog)
        self.buttonBox.accepted.connect(VcsCommandOptionsDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(VcsCommandOptionsDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(VcsCommandOptionsDialog)
        VcsCommandOptionsDialog.setTabOrder(self.globalEdit, self.commitEdit)
        VcsCommandOptionsDialog.setTabOrder(self.commitEdit, self.checkoutEdit)
        VcsCommandOptionsDialog.setTabOrder(self.checkoutEdit, self.updateEdit)
        VcsCommandOptionsDialog.setTabOrder(self.updateEdit, self.addEdit)
        VcsCommandOptionsDialog.setTabOrder(self.addEdit, self.removeEdit)
        VcsCommandOptionsDialog.setTabOrder(self.removeEdit, self.diffEdit)
        VcsCommandOptionsDialog.setTabOrder(self.diffEdit, self.logEdit)
        VcsCommandOptionsDialog.setTabOrder(self.logEdit, self.historyEdit)
        VcsCommandOptionsDialog.setTabOrder(self.historyEdit, self.statusEdit)
        VcsCommandOptionsDialog.setTabOrder(self.statusEdit, self.tagEdit)
        VcsCommandOptionsDialog.setTabOrder(self.tagEdit, self.exportEdit)

    def retranslateUi(self, VcsCommandOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        VcsCommandOptionsDialog.setWindowTitle(_translate("VcsCommandOptionsDialog", "VCS Command Options"))
        VcsCommandOptionsDialog.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>VCS Command Options Dialog</b>\n"
"<p>Enter the options for the different VCS commands. The \"Global Options\" entry applies to all VCS commands.</p>"))
        self.historyLabel.setText(_translate("VcsCommandOptionsDialog", "&History Options:"))
        self.addLabel.setText(_translate("VcsCommandOptionsDialog", "&Add Options:"))
        self.removeLabel.setText(_translate("VcsCommandOptionsDialog", "&Remove Options:"))
        self.tagLabel.setText(_translate("VcsCommandOptionsDialog", "&Tag Options:"))
        self.commitEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the commit command."))
        self.commitEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Commit Options</b>\n"
"<p>Enter the options for the commit command.</p>"))
        self.historyEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the history command."))
        self.historyEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>History Options</b>\n"
"<p>Enter the options for the history command.</p>"))
        self.diffEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the diff command."))
        self.diffEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Diff Options</b>\n"
"<p>Enter the options for the diff command.</p>"))
        self.updateEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the update command."))
        self.updateEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Update Options</b>\n"
"<p>Enter the options for the update command.</p>"))
        self.logEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the log command."))
        self.logEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Log Options</b>\n"
"<p>Enter the options for the log command.</p>"))
        self.tagEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the tag command."))
        self.tagEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Tag Options</b>\n"
"<p>Enter the options for the tag command.</p>"))
        self.statusEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the status command."))
        self.statusEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Status Options</b>\n"
"<p>Enter the options for the status command.</p>"))
        self.diffLabel.setText(_translate("VcsCommandOptionsDialog", "&Diff Options:"))
        self.globalLabel.setText(_translate("VcsCommandOptionsDialog", "&Global Options:"))
        self.exportEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the export command."))
        self.exportEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Export Options</b>\n"
"<p>Enter the options for the export command.</p>"))
        self.addEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the add command."))
        self.addEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Add Options</b>\n"
"<p>Enter the options for the add command.</p>"))
        self.logLabel.setText(_translate("VcsCommandOptionsDialog", "&Log Options:"))
        self.statusLabel.setText(_translate("VcsCommandOptionsDialog", "&StatusOptions:"))
        self.removeEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the remove command."))
        self.removeEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Remove Options</b>\n"
"<p>Enter the options for the remove command.</p>"))
        self.checkoutEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the options for the checkout command."))
        self.checkoutEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Checkout Options</b>\n"
"<p>Enter the options for the checkout command.</p>"))
        self.commitLabel.setText(_translate("VcsCommandOptionsDialog", "Co&mmit Options:"))
        self.exportLabel.setText(_translate("VcsCommandOptionsDialog", "&Export Options:"))
        self.checkoutLabel.setText(_translate("VcsCommandOptionsDialog", "Check&out Options:"))
        self.updateLabel.setText(_translate("VcsCommandOptionsDialog", "&Update Options:"))
        self.globalEdit.setToolTip(_translate("VcsCommandOptionsDialog", "Enter the global options."))
        self.globalEdit.setWhatsThis(_translate("VcsCommandOptionsDialog", "<b>Global Options</b>\n"
"<p>Enter the global options.</p>"))
