# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Project/NewPythonPackageDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_NewPythonPackageDialog(object):
    def setupUi(self, NewPythonPackageDialog):
        NewPythonPackageDialog.setObjectName("NewPythonPackageDialog")
        NewPythonPackageDialog.resize(400, 95)
        self.vboxlayout = QtWidgets.QVBoxLayout(NewPythonPackageDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.label_2 = QtWidgets.QLabel(NewPythonPackageDialog)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)
        self.packageEdit = QtWidgets.QLineEdit(NewPythonPackageDialog)
        self.packageEdit.setObjectName("packageEdit")
        self.vboxlayout.addWidget(self.packageEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewPythonPackageDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(NewPythonPackageDialog)
        self.buttonBox.accepted.connect(NewPythonPackageDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(NewPythonPackageDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(NewPythonPackageDialog)

    def retranslateUi(self, NewPythonPackageDialog):
        _translate = QtCore.QCoreApplication.translate
        NewPythonPackageDialog.setWindowTitle(_translate("NewPythonPackageDialog", "Add new Python package"))
        self.label_2.setText(_translate("NewPythonPackageDialog", "Enter the dotted name of the new package"))
        self.packageEdit.setToolTip(_translate("NewPythonPackageDialog", "Enter the dotted package name"))
