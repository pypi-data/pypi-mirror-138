# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/HelpViewer/HelpBookmarksImportDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HelpBookmarksImportDialog(object):
    def setupUi(self, HelpBookmarksImportDialog):
        HelpBookmarksImportDialog.setObjectName("HelpBookmarksImportDialog")
        HelpBookmarksImportDialog.resize(500, 98)
        HelpBookmarksImportDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(HelpBookmarksImportDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.replaceCheckBox = QtWidgets.QCheckBox(HelpBookmarksImportDialog)
        self.replaceCheckBox.setObjectName("replaceCheckBox")
        self.gridLayout.addWidget(self.replaceCheckBox, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(HelpBookmarksImportDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.bookmarksPicker = EricPathPicker(HelpBookmarksImportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarksPicker.sizePolicy().hasHeightForWidth())
        self.bookmarksPicker.setSizePolicy(sizePolicy)
        self.bookmarksPicker.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        self.bookmarksPicker.setObjectName("bookmarksPicker")
        self.gridLayout.addWidget(self.bookmarksPicker, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(HelpBookmarksImportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(HelpBookmarksImportDialog)
        self.buttonBox.accepted.connect(HelpBookmarksImportDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HelpBookmarksImportDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HelpBookmarksImportDialog)

    def retranslateUi(self, HelpBookmarksImportDialog):
        _translate = QtCore.QCoreApplication.translate
        HelpBookmarksImportDialog.setWindowTitle(_translate("HelpBookmarksImportDialog", "Import Bookmarks"))
        self.replaceCheckBox.setToolTip(_translate("HelpBookmarksImportDialog", "Select to replace the existing bookmarks"))
        self.replaceCheckBox.setText(_translate("HelpBookmarksImportDialog", "Replace Existing Bookmarks"))
        self.label.setText(_translate("HelpBookmarksImportDialog", "Bookmarks:"))
        self.bookmarksPicker.setToolTip(_translate("HelpBookmarksImportDialog", "Enter the path of the bookmarks file"))
from EricWidgets.EricPathPicker import EricPathPicker
