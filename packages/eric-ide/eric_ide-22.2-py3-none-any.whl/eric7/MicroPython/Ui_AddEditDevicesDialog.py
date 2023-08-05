# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/MicroPython/AddEditDevicesDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddEditDevicesDialog(object):
    def setupUi(self, AddEditDevicesDialog):
        AddEditDevicesDialog.setObjectName("AddEditDevicesDialog")
        AddEditDevicesDialog.resize(500, 270)
        AddEditDevicesDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(AddEditDevicesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(AddEditDevicesDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.vidEdit = QtWidgets.QLineEdit(AddEditDevicesDialog)
        self.vidEdit.setReadOnly(True)
        self.vidEdit.setObjectName("vidEdit")
        self.gridLayout.addWidget(self.vidEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(AddEditDevicesDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pidEdit = QtWidgets.QLineEdit(AddEditDevicesDialog)
        self.pidEdit.setReadOnly(True)
        self.pidEdit.setObjectName("pidEdit")
        self.gridLayout.addWidget(self.pidEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(AddEditDevicesDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.descriptionEdit = QtWidgets.QLineEdit(AddEditDevicesDialog)
        self.descriptionEdit.setReadOnly(True)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridLayout.addWidget(self.descriptionEdit, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(AddEditDevicesDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.deviceTypeComboBox = QtWidgets.QComboBox(AddEditDevicesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceTypeComboBox.sizePolicy().hasHeightForWidth())
        self.deviceTypeComboBox.setSizePolicy(sizePolicy)
        self.deviceTypeComboBox.setObjectName("deviceTypeComboBox")
        self.gridLayout.addWidget(self.deviceTypeComboBox, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(AddEditDevicesDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.dataVolumeEdit = QtWidgets.QLineEdit(AddEditDevicesDialog)
        self.dataVolumeEdit.setClearButtonEnabled(True)
        self.dataVolumeEdit.setObjectName("dataVolumeEdit")
        self.gridLayout.addWidget(self.dataVolumeEdit, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(AddEditDevicesDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.flashVolumeEdit = QtWidgets.QLineEdit(AddEditDevicesDialog)
        self.flashVolumeEdit.setClearButtonEnabled(True)
        self.flashVolumeEdit.setObjectName("flashVolumeEdit")
        self.gridLayout.addWidget(self.flashVolumeEdit, 5, 1, 1, 1)
        self.reportButton = QtWidgets.QPushButton(AddEditDevicesDialog)
        self.reportButton.setObjectName("reportButton")
        self.gridLayout.addWidget(self.reportButton, 6, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddEditDevicesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)

        self.retranslateUi(AddEditDevicesDialog)
        self.buttonBox.accepted.connect(AddEditDevicesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(AddEditDevicesDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AddEditDevicesDialog)
        AddEditDevicesDialog.setTabOrder(self.vidEdit, self.pidEdit)
        AddEditDevicesDialog.setTabOrder(self.pidEdit, self.descriptionEdit)
        AddEditDevicesDialog.setTabOrder(self.descriptionEdit, self.deviceTypeComboBox)
        AddEditDevicesDialog.setTabOrder(self.deviceTypeComboBox, self.dataVolumeEdit)
        AddEditDevicesDialog.setTabOrder(self.dataVolumeEdit, self.flashVolumeEdit)
        AddEditDevicesDialog.setTabOrder(self.flashVolumeEdit, self.reportButton)

    def retranslateUi(self, AddEditDevicesDialog):
        _translate = QtCore.QCoreApplication.translate
        AddEditDevicesDialog.setWindowTitle(_translate("AddEditDevicesDialog", "Add Unknown Device"))
        self.label.setText(_translate("AddEditDevicesDialog", "Vendor ID:"))
        self.label_2.setText(_translate("AddEditDevicesDialog", "Product ID:"))
        self.label_3.setText(_translate("AddEditDevicesDialog", "Description:"))
        self.label_4.setText(_translate("AddEditDevicesDialog", "Device Type:"))
        self.deviceTypeComboBox.setToolTip(_translate("AddEditDevicesDialog", "Select the device type"))
        self.label_5.setText(_translate("AddEditDevicesDialog", "Data Volume:"))
        self.dataVolumeEdit.setToolTip(_translate("AddEditDevicesDialog", "Enter the volume name used for direct acces to the device"))
        self.label_6.setText(_translate("AddEditDevicesDialog", "Flash Volume:"))
        self.flashVolumeEdit.setToolTip(_translate("AddEditDevicesDialog", "Enter the volume name used for flashing if this device supports UF2"))
        self.reportButton.setToolTip(_translate("AddEditDevicesDialog", "Press to report the entered data via email"))
        self.reportButton.setText(_translate("AddEditDevicesDialog", "Report Data"))
