# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/VcsPlugins/vcsMercurial/QueuesExtension/HgQueuesHeaderDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgQueuesHeaderDialog(object):
    def setupUi(self, HgQueuesHeaderDialog):
        HgQueuesHeaderDialog.setObjectName("HgQueuesHeaderDialog")
        HgQueuesHeaderDialog.resize(400, 300)
        HgQueuesHeaderDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgQueuesHeaderDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageEdit = QtWidgets.QPlainTextEdit(HgQueuesHeaderDialog)
        self.messageEdit.setReadOnly(True)
        self.messageEdit.setObjectName("messageEdit")
        self.verticalLayout.addWidget(self.messageEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgQueuesHeaderDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgQueuesHeaderDialog)
        QtCore.QMetaObject.connectSlotsByName(HgQueuesHeaderDialog)
        HgQueuesHeaderDialog.setTabOrder(self.messageEdit, self.buttonBox)

    def retranslateUi(self, HgQueuesHeaderDialog):
        _translate = QtCore.QCoreApplication.translate
        HgQueuesHeaderDialog.setWindowTitle(_translate("HgQueuesHeaderDialog", "Commit Message"))
