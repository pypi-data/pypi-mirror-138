# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/EricWidgets/EricComboSelectionDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EricComboSelectionDialog(object):
    def setupUi(self, EricComboSelectionDialog):
        EricComboSelectionDialog.setObjectName("EricComboSelectionDialog")
        EricComboSelectionDialog.resize(400, 100)
        EricComboSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EricComboSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageLabel = QtWidgets.QLabel(EricComboSelectionDialog)
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setObjectName("messageLabel")
        self.verticalLayout.addWidget(self.messageLabel)
        self.selectionComboBox = QtWidgets.QComboBox(EricComboSelectionDialog)
        self.selectionComboBox.setObjectName("selectionComboBox")
        self.verticalLayout.addWidget(self.selectionComboBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(EricComboSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EricComboSelectionDialog)
        self.buttonBox.accepted.connect(EricComboSelectionDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(EricComboSelectionDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EricComboSelectionDialog)

    def retranslateUi(self, EricComboSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        EricComboSelectionDialog.setWindowTitle(_translate("EricComboSelectionDialog", "Select from List"))
        self.messageLabel.setText(_translate("EricComboSelectionDialog", "Select from the list below:"))
