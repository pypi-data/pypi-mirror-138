# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsMercurial/HgRepoConfigDataDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgRepoConfigDataDialog(object):
    def setupUi(self, HgRepoConfigDataDialog):
        HgRepoConfigDataDialog.setObjectName("HgRepoConfigDataDialog")
        HgRepoConfigDataDialog.resize(500, 436)
        HgRepoConfigDataDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgRepoConfigDataDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(HgRepoConfigDataDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.defaultUrlEdit = QtWidgets.QLineEdit(self.groupBox)
        self.defaultUrlEdit.setClearButtonEnabled(True)
        self.defaultUrlEdit.setObjectName("defaultUrlEdit")
        self.gridLayout.addWidget(self.defaultUrlEdit, 0, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.defaultUserEdit = QtWidgets.QLineEdit(self.groupBox)
        self.defaultUserEdit.setClearButtonEnabled(True)
        self.defaultUserEdit.setObjectName("defaultUserEdit")
        self.gridLayout.addWidget(self.defaultUserEdit, 1, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.defaultPasswordEdit = QtWidgets.QLineEdit(self.groupBox)
        self.defaultPasswordEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.defaultPasswordEdit.setClearButtonEnabled(True)
        self.defaultPasswordEdit.setObjectName("defaultPasswordEdit")
        self.gridLayout.addWidget(self.defaultPasswordEdit, 2, 1, 1, 1)
        self.defaultShowPasswordButton = QtWidgets.QToolButton(self.groupBox)
        self.defaultShowPasswordButton.setCheckable(True)
        self.defaultShowPasswordButton.setObjectName("defaultShowPasswordButton")
        self.gridLayout.addWidget(self.defaultShowPasswordButton, 2, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(HgRepoConfigDataDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.defaultPushUrlEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.defaultPushUrlEdit.setClearButtonEnabled(True)
        self.defaultPushUrlEdit.setObjectName("defaultPushUrlEdit")
        self.gridLayout_2.addWidget(self.defaultPushUrlEdit, 0, 1, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.defaultPushUserEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.defaultPushUserEdit.setClearButtonEnabled(True)
        self.defaultPushUserEdit.setObjectName("defaultPushUserEdit")
        self.gridLayout_2.addWidget(self.defaultPushUserEdit, 1, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.defaultPushPasswordEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.defaultPushPasswordEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.defaultPushPasswordEdit.setClearButtonEnabled(True)
        self.defaultPushPasswordEdit.setObjectName("defaultPushPasswordEdit")
        self.gridLayout_2.addWidget(self.defaultPushPasswordEdit, 2, 1, 1, 1)
        self.defaultPushShowPasswordButton = QtWidgets.QToolButton(self.groupBox_2)
        self.defaultPushShowPasswordButton.setCheckable(True)
        self.defaultPushShowPasswordButton.setObjectName("defaultPushShowPasswordButton")
        self.gridLayout_2.addWidget(self.defaultPushShowPasswordButton, 2, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.largefilesGroup = QtWidgets.QGroupBox(HgRepoConfigDataDialog)
        self.largefilesGroup.setObjectName("largefilesGroup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.largefilesGroup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_8 = QtWidgets.QLabel(self.largefilesGroup)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.lfFileSizeSpinBox = QtWidgets.QSpinBox(self.largefilesGroup)
        self.lfFileSizeSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lfFileSizeSpinBox.setMinimum(1)
        self.lfFileSizeSpinBox.setProperty("value", 10)
        self.lfFileSizeSpinBox.setObjectName("lfFileSizeSpinBox")
        self.gridLayout_3.addWidget(self.lfFileSizeSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(215, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.largefilesGroup)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.lfFilePatternsEdit = QtWidgets.QLineEdit(self.largefilesGroup)
        self.lfFilePatternsEdit.setObjectName("lfFilePatternsEdit")
        self.gridLayout_3.addWidget(self.lfFilePatternsEdit, 1, 1, 1, 2)
        self.verticalLayout.addWidget(self.largefilesGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgRepoConfigDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgRepoConfigDataDialog)
        self.buttonBox.accepted.connect(HgRepoConfigDataDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgRepoConfigDataDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgRepoConfigDataDialog)
        HgRepoConfigDataDialog.setTabOrder(self.defaultUrlEdit, self.defaultUserEdit)
        HgRepoConfigDataDialog.setTabOrder(self.defaultUserEdit, self.defaultPasswordEdit)
        HgRepoConfigDataDialog.setTabOrder(self.defaultPasswordEdit, self.defaultShowPasswordButton)
        HgRepoConfigDataDialog.setTabOrder(self.defaultShowPasswordButton, self.defaultPushUrlEdit)
        HgRepoConfigDataDialog.setTabOrder(self.defaultPushUrlEdit, self.defaultPushUserEdit)
        HgRepoConfigDataDialog.setTabOrder(self.defaultPushUserEdit, self.defaultPushPasswordEdit)
        HgRepoConfigDataDialog.setTabOrder(self.defaultPushPasswordEdit, self.defaultPushShowPasswordButton)
        HgRepoConfigDataDialog.setTabOrder(self.defaultPushShowPasswordButton, self.lfFileSizeSpinBox)
        HgRepoConfigDataDialog.setTabOrder(self.lfFileSizeSpinBox, self.lfFilePatternsEdit)
        HgRepoConfigDataDialog.setTabOrder(self.lfFilePatternsEdit, self.buttonBox)

    def retranslateUi(self, HgRepoConfigDataDialog):
        _translate = QtCore.QCoreApplication.translate
        HgRepoConfigDataDialog.setWindowTitle(_translate("HgRepoConfigDataDialog", "Mercurial Repository Configuration"))
        self.groupBox.setTitle(_translate("HgRepoConfigDataDialog", "Default"))
        self.label_2.setText(_translate("HgRepoConfigDataDialog", "Upstream URL:"))
        self.defaultUrlEdit.setToolTip(_translate("HgRepoConfigDataDialog", "Enter the URL of the upstream repository"))
        self.label_3.setText(_translate("HgRepoConfigDataDialog", "Username:"))
        self.defaultUserEdit.setToolTip(_translate("HgRepoConfigDataDialog", "Enter user name to acces the upstream repository"))
        self.label_4.setText(_translate("HgRepoConfigDataDialog", "Password:"))
        self.defaultPasswordEdit.setToolTip(_translate("HgRepoConfigDataDialog", "Enter the password to acces the upstream repository"))
        self.defaultShowPasswordButton.setToolTip(_translate("HgRepoConfigDataDialog", "Press to show the password"))
        self.groupBox_2.setTitle(_translate("HgRepoConfigDataDialog", "Default Push"))
        self.label_5.setText(_translate("HgRepoConfigDataDialog", "Upstream URL:"))
        self.defaultPushUrlEdit.setToolTip(_translate("HgRepoConfigDataDialog", "Enter the URL of the upstream (push) repository"))
        self.label_7.setText(_translate("HgRepoConfigDataDialog", "Username:"))
        self.defaultPushUserEdit.setToolTip(_translate("HgRepoConfigDataDialog", "Enter user name to acces the upstream (push) repository"))
        self.label_6.setText(_translate("HgRepoConfigDataDialog", "Password:"))
        self.defaultPushPasswordEdit.setToolTip(_translate("HgRepoConfigDataDialog", "Enter the password to acces the upstream (push) repository"))
        self.defaultPushShowPasswordButton.setToolTip(_translate("HgRepoConfigDataDialog", "Press to show the password"))
        self.largefilesGroup.setTitle(_translate("HgRepoConfigDataDialog", "Large Files"))
        self.label_8.setText(_translate("HgRepoConfigDataDialog", "Minimum file size:"))
        self.lfFileSizeSpinBox.setToolTip(_translate("HgRepoConfigDataDialog", "Enter the minimum file size in MB for files to be treated as Large Files"))
        self.lfFileSizeSpinBox.setSuffix(_translate("HgRepoConfigDataDialog", " MB"))
        self.label_9.setText(_translate("HgRepoConfigDataDialog", "Patterns:"))
        self.lfFilePatternsEdit.setToolTip(_translate("HgRepoConfigDataDialog", "Enter file patterns (space separated) for files to be treated as Large Files"))
