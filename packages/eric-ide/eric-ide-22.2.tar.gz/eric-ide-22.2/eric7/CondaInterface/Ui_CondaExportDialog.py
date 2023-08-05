# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/CondaInterface/CondaExportDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CondaExportDialog(object):
    def setupUi(self, CondaExportDialog):
        CondaExportDialog.setObjectName("CondaExportDialog")
        CondaExportDialog.resize(600, 550)
        CondaExportDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CondaExportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(CondaExportDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.environmentLabel = QtWidgets.QLabel(CondaExportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.environmentLabel.sizePolicy().hasHeightForWidth())
        self.environmentLabel.setSizePolicy(sizePolicy)
        self.environmentLabel.setObjectName("environmentLabel")
        self.gridLayout_2.addWidget(self.environmentLabel, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(CondaExportDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.requirementsFilePicker = EricPathPicker(CondaExportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requirementsFilePicker.sizePolicy().hasHeightForWidth())
        self.requirementsFilePicker.setSizePolicy(sizePolicy)
        self.requirementsFilePicker.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.requirementsFilePicker.setObjectName("requirementsFilePicker")
        self.gridLayout_2.addWidget(self.requirementsFilePicker, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.saveButton = QtWidgets.QPushButton(CondaExportDialog)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 0, 1, 1, 1)
        self.saveToButton = QtWidgets.QPushButton(CondaExportDialog)
        self.saveToButton.setObjectName("saveToButton")
        self.gridLayout.addWidget(self.saveToButton, 1, 1, 1, 1)
        self.copyButton = QtWidgets.QPushButton(CondaExportDialog)
        self.copyButton.setObjectName("copyButton")
        self.gridLayout.addWidget(self.copyButton, 2, 1, 1, 1)
        self.insertButton = QtWidgets.QPushButton(CondaExportDialog)
        self.insertButton.setObjectName("insertButton")
        self.gridLayout.addWidget(self.insertButton, 3, 1, 1, 1)
        self.replaceSelectionButton = QtWidgets.QPushButton(CondaExportDialog)
        self.replaceSelectionButton.setObjectName("replaceSelectionButton")
        self.gridLayout.addWidget(self.replaceSelectionButton, 4, 1, 1, 1)
        self.replaceAllButton = QtWidgets.QPushButton(CondaExportDialog)
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.gridLayout.addWidget(self.replaceAllButton, 5, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        self.requirementsEdit = QtWidgets.QPlainTextEdit(CondaExportDialog)
        self.requirementsEdit.setTabChangesFocus(True)
        self.requirementsEdit.setObjectName("requirementsEdit")
        self.gridLayout.addWidget(self.requirementsEdit, 0, 0, 7, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(CondaExportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CondaExportDialog)
        self.buttonBox.accepted.connect(CondaExportDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(CondaExportDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(CondaExportDialog)
        CondaExportDialog.setTabOrder(self.requirementsFilePicker, self.requirementsEdit)
        CondaExportDialog.setTabOrder(self.requirementsEdit, self.saveButton)
        CondaExportDialog.setTabOrder(self.saveButton, self.saveToButton)
        CondaExportDialog.setTabOrder(self.saveToButton, self.copyButton)
        CondaExportDialog.setTabOrder(self.copyButton, self.insertButton)
        CondaExportDialog.setTabOrder(self.insertButton, self.replaceSelectionButton)
        CondaExportDialog.setTabOrder(self.replaceSelectionButton, self.replaceAllButton)

    def retranslateUi(self, CondaExportDialog):
        _translate = QtCore.QCoreApplication.translate
        CondaExportDialog.setWindowTitle(_translate("CondaExportDialog", "Generate Requirements"))
        self.label_2.setText(_translate("CondaExportDialog", "Conda Environment:"))
        self.label.setText(_translate("CondaExportDialog", "Requirements File:"))
        self.saveButton.setToolTip(_translate("CondaExportDialog", "Press to save to the requirements file"))
        self.saveButton.setText(_translate("CondaExportDialog", "Save"))
        self.saveToButton.setToolTip(_translate("CondaExportDialog", "Save to a new file"))
        self.saveToButton.setText(_translate("CondaExportDialog", "Save To"))
        self.copyButton.setToolTip(_translate("CondaExportDialog", "Copy the requirements text to the clipboard"))
        self.copyButton.setText(_translate("CondaExportDialog", "Copy"))
        self.insertButton.setToolTip(_translate("CondaExportDialog", "Insert the requirements text at the cursor position"))
        self.insertButton.setText(_translate("CondaExportDialog", "Insert"))
        self.replaceSelectionButton.setToolTip(_translate("CondaExportDialog", "Replace the current selection with the requirements text"))
        self.replaceSelectionButton.setText(_translate("CondaExportDialog", "Replace Selection"))
        self.replaceAllButton.setToolTip(_translate("CondaExportDialog", "Replace all text with the requirements text"))
        self.replaceAllButton.setText(_translate("CondaExportDialog", "Replace All"))
from EricWidgets.EricPathPicker import EricPathPicker
