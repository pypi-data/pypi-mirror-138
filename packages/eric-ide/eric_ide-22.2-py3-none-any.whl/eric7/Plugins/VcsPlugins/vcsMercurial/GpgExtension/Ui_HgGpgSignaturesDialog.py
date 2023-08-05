# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsMercurial/GpgExtension/HgGpgSignaturesDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgGpgSignaturesDialog(object):
    def setupUi(self, HgGpgSignaturesDialog):
        HgGpgSignaturesDialog.setObjectName("HgGpgSignaturesDialog")
        HgGpgSignaturesDialog.resize(700, 600)
        HgGpgSignaturesDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgGpgSignaturesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.categoryCombo = QtWidgets.QComboBox(HgGpgSignaturesDialog)
        self.categoryCombo.setObjectName("categoryCombo")
        self.categoryCombo.addItem("")
        self.categoryCombo.addItem("")
        self.horizontalLayout_2.addWidget(self.categoryCombo)
        self.rxEdit = QtWidgets.QLineEdit(HgGpgSignaturesDialog)
        self.rxEdit.setClearButtonEnabled(True)
        self.rxEdit.setObjectName("rxEdit")
        self.horizontalLayout_2.addWidget(self.rxEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.signaturesList = QtWidgets.QTreeWidget(HgGpgSignaturesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.signaturesList.sizePolicy().hasHeightForWidth())
        self.signaturesList.setSizePolicy(sizePolicy)
        self.signaturesList.setAlternatingRowColors(True)
        self.signaturesList.setRootIsDecorated(False)
        self.signaturesList.setHeaderHidden(True)
        self.signaturesList.setObjectName("signaturesList")
        self.signaturesList.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.signaturesList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verifyButton = QtWidgets.QPushButton(HgGpgSignaturesDialog)
        self.verifyButton.setEnabled(False)
        self.verifyButton.setObjectName("verifyButton")
        self.horizontalLayout.addWidget(self.verifyButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.errorGroup = QtWidgets.QGroupBox(HgGpgSignaturesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout.setObjectName("vboxlayout")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout.addWidget(self.errors)
        self.verticalLayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgGpgSignaturesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgGpgSignaturesDialog)
        QtCore.QMetaObject.connectSlotsByName(HgGpgSignaturesDialog)
        HgGpgSignaturesDialog.setTabOrder(self.categoryCombo, self.rxEdit)
        HgGpgSignaturesDialog.setTabOrder(self.rxEdit, self.signaturesList)
        HgGpgSignaturesDialog.setTabOrder(self.signaturesList, self.verifyButton)
        HgGpgSignaturesDialog.setTabOrder(self.verifyButton, self.errors)
        HgGpgSignaturesDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, HgGpgSignaturesDialog):
        _translate = QtCore.QCoreApplication.translate
        HgGpgSignaturesDialog.setWindowTitle(_translate("HgGpgSignaturesDialog", "Signed Changesets"))
        self.categoryCombo.setToolTip(_translate("HgGpgSignaturesDialog", "Select the category to filter on"))
        self.categoryCombo.setItemText(0, _translate("HgGpgSignaturesDialog", "Revision"))
        self.categoryCombo.setItemText(1, _translate("HgGpgSignaturesDialog", "Signature"))
        self.rxEdit.setToolTip(_translate("HgGpgSignaturesDialog", "Enter the regular expression to filter on"))
        self.verifyButton.setToolTip(_translate("HgGpgSignaturesDialog", "Press to verify the signatures of the selected revision"))
        self.verifyButton.setText(_translate("HgGpgSignaturesDialog", "&Verify..."))
        self.errorGroup.setTitle(_translate("HgGpgSignaturesDialog", "Errors"))
        self.errors.setWhatsThis(_translate("HgGpgSignaturesDialog", "<b>Mercurial errors</b><p>This shows possible error messages.</p>"))
