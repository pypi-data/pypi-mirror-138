# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/JediInterface/RefactoringPreviewDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RefactoringPreviewDialog(object):
    def setupUi(self, RefactoringPreviewDialog):
        RefactoringPreviewDialog.setObjectName("RefactoringPreviewDialog")
        RefactoringPreviewDialog.resize(600, 600)
        RefactoringPreviewDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(RefactoringPreviewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(RefactoringPreviewDialog)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.previewEdit = QtWidgets.QPlainTextEdit(RefactoringPreviewDialog)
        self.previewEdit.setTabChangesFocus(True)
        self.previewEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.previewEdit.setReadOnly(True)
        self.previewEdit.setObjectName("previewEdit")
        self.verticalLayout.addWidget(self.previewEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(RefactoringPreviewDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RefactoringPreviewDialog)
        self.buttonBox.accepted.connect(RefactoringPreviewDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(RefactoringPreviewDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(RefactoringPreviewDialog)

    def retranslateUi(self, RefactoringPreviewDialog):
        _translate = QtCore.QCoreApplication.translate
        RefactoringPreviewDialog.setWindowTitle(_translate("RefactoringPreviewDialog", "Preview Changes"))
