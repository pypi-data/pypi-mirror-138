# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsMercurial/PurgeExtension/HgPurgeListDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgPurgeListDialog(object):
    def setupUi(self, HgPurgeListDialog):
        HgPurgeListDialog.setObjectName("HgPurgeListDialog")
        HgPurgeListDialog.resize(500, 400)
        HgPurgeListDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgPurgeListDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.purgeList = QtWidgets.QListWidget(HgPurgeListDialog)
        self.purgeList.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.purgeList.setAlternatingRowColors(True)
        self.purgeList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.purgeList.setTextElideMode(QtCore.Qt.TextElideMode.ElideLeft)
        self.purgeList.setObjectName("purgeList")
        self.verticalLayout.addWidget(self.purgeList)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgPurgeListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgPurgeListDialog)
        self.buttonBox.accepted.connect(HgPurgeListDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgPurgeListDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgPurgeListDialog)
        HgPurgeListDialog.setTabOrder(self.purgeList, self.buttonBox)

    def retranslateUi(self, HgPurgeListDialog):
        _translate = QtCore.QCoreApplication.translate
        HgPurgeListDialog.setWindowTitle(_translate("HgPurgeListDialog", "Purge List"))
