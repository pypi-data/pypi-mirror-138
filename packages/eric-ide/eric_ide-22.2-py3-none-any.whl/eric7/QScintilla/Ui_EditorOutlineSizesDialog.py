# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/QScintilla/EditorOutlineSizesDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditorOutlineSizesDialog(object):
    def setupUi(self, EditorOutlineSizesDialog):
        EditorOutlineSizesDialog.setObjectName("EditorOutlineSizesDialog")
        EditorOutlineSizesDialog.resize(400, 110)
        EditorOutlineSizesDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(EditorOutlineSizesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(EditorOutlineSizesDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.sourceOutlineWidthSpinBox = QtWidgets.QSpinBox(EditorOutlineSizesDialog)
        self.sourceOutlineWidthSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.sourceOutlineWidthSpinBox.setMinimum(50)
        self.sourceOutlineWidthSpinBox.setMaximum(498)
        self.sourceOutlineWidthSpinBox.setSingleStep(50)
        self.sourceOutlineWidthSpinBox.setObjectName("sourceOutlineWidthSpinBox")
        self.gridLayout.addWidget(self.sourceOutlineWidthSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(219, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(EditorOutlineSizesDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.sourceOutlineWidthStepSpinBox = QtWidgets.QSpinBox(EditorOutlineSizesDialog)
        self.sourceOutlineWidthStepSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.sourceOutlineWidthStepSpinBox.setMinimum(10)
        self.sourceOutlineWidthStepSpinBox.setMaximum(100)
        self.sourceOutlineWidthStepSpinBox.setSingleStep(10)
        self.sourceOutlineWidthStepSpinBox.setObjectName("sourceOutlineWidthStepSpinBox")
        self.gridLayout.addWidget(self.sourceOutlineWidthStepSpinBox, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(EditorOutlineSizesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok|QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)

        self.retranslateUi(EditorOutlineSizesDialog)
        self.buttonBox.accepted.connect(EditorOutlineSizesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(EditorOutlineSizesDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EditorOutlineSizesDialog)

    def retranslateUi(self, EditorOutlineSizesDialog):
        _translate = QtCore.QCoreApplication.translate
        EditorOutlineSizesDialog.setWindowTitle(_translate("EditorOutlineSizesDialog", "Editor Outline Sizes"))
        self.label_2.setText(_translate("EditorOutlineSizesDialog", "Default Width:"))
        self.sourceOutlineWidthSpinBox.setToolTip(_translate("EditorOutlineSizesDialog", "Enter the default width of the source code outline view"))
        self.label_3.setText(_translate("EditorOutlineSizesDialog", "Width Step Size:"))
        self.sourceOutlineWidthStepSpinBox.setToolTip(_translate("EditorOutlineSizesDialog", "Enter the amount of pixels the width of the outline should be increased or decreased"))
