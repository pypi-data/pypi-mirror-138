# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/WebBrowser/Network/SendRefererWhitelistDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SendRefererWhitelistDialog(object):
    def setupUi(self, SendRefererWhitelistDialog):
        SendRefererWhitelistDialog.setObjectName("SendRefererWhitelistDialog")
        SendRefererWhitelistDialog.resize(500, 350)
        SendRefererWhitelistDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SendRefererWhitelistDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.searchEdit = QtWidgets.QLineEdit(SendRefererWhitelistDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchEdit.sizePolicy().hasHeightForWidth())
        self.searchEdit.setSizePolicy(sizePolicy)
        self.searchEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.searchEdit.setClearButtonEnabled(True)
        self.searchEdit.setObjectName("searchEdit")
        self.gridLayout_2.addWidget(self.searchEdit, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        self.addButton = QtWidgets.QPushButton(SendRefererWhitelistDialog)
        self.addButton.setAutoDefault(False)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(SendRefererWhitelistDialog)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 1, 1, 1)
        self.removeButton = QtWidgets.QPushButton(SendRefererWhitelistDialog)
        self.removeButton.setAutoDefault(False)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 2, 1, 1, 1)
        self.removeAllButton = QtWidgets.QPushButton(SendRefererWhitelistDialog)
        self.removeAllButton.setAutoDefault(False)
        self.removeAllButton.setObjectName("removeAllButton")
        self.gridLayout.addWidget(self.removeAllButton, 3, 1, 1, 1)
        self.whitelist = EricListView(SendRefererWhitelistDialog)
        self.whitelist.setAlternatingRowColors(True)
        self.whitelist.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.whitelist.setObjectName("whitelist")
        self.gridLayout.addWidget(self.whitelist, 0, 0, 5, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(SendRefererWhitelistDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SendRefererWhitelistDialog)
        self.buttonBox.accepted.connect(SendRefererWhitelistDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SendRefererWhitelistDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SendRefererWhitelistDialog)
        SendRefererWhitelistDialog.setTabOrder(self.searchEdit, self.whitelist)
        SendRefererWhitelistDialog.setTabOrder(self.whitelist, self.addButton)
        SendRefererWhitelistDialog.setTabOrder(self.addButton, self.removeButton)
        SendRefererWhitelistDialog.setTabOrder(self.removeButton, self.removeAllButton)
        SendRefererWhitelistDialog.setTabOrder(self.removeAllButton, self.buttonBox)

    def retranslateUi(self, SendRefererWhitelistDialog):
        _translate = QtCore.QCoreApplication.translate
        SendRefererWhitelistDialog.setWindowTitle(_translate("SendRefererWhitelistDialog", "Send Referer Whitelist"))
        self.searchEdit.setToolTip(_translate("SendRefererWhitelistDialog", "Enter search term for hosts"))
        self.addButton.setToolTip(_translate("SendRefererWhitelistDialog", "Press to add site to the whitelist"))
        self.addButton.setText(_translate("SendRefererWhitelistDialog", "&Add..."))
        self.removeButton.setToolTip(_translate("SendRefererWhitelistDialog", "Press to remove the selected entries"))
        self.removeButton.setText(_translate("SendRefererWhitelistDialog", "&Remove"))
        self.removeAllButton.setToolTip(_translate("SendRefererWhitelistDialog", "Press to remove all entries"))
        self.removeAllButton.setText(_translate("SendRefererWhitelistDialog", "R&emove All"))
from EricWidgets.EricListView import EricListView
