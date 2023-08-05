# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Plugins/CheckerPlugins/SyntaxChecker/SyntaxCheckerDialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SyntaxCheckerDialog(object):
    def setupUi(self, SyntaxCheckerDialog):
        SyntaxCheckerDialog.setObjectName("SyntaxCheckerDialog")
        SyntaxCheckerDialog.resize(650, 500)
        SyntaxCheckerDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SyntaxCheckerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filterFrame = QtWidgets.QFrame(SyntaxCheckerDialog)
        self.filterFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.filterFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.filterFrame.setObjectName("filterFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.filterFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.filterFrame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.excludeFilesEdit = QtWidgets.QLineEdit(self.filterFrame)
        self.excludeFilesEdit.setClearButtonEnabled(True)
        self.excludeFilesEdit.setObjectName("excludeFilesEdit")
        self.horizontalLayout.addWidget(self.excludeFilesEdit)
        self.line = QtWidgets.QFrame(self.filterFrame)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.startButton = QtWidgets.QPushButton(self.filterFrame)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.verticalLayout.addWidget(self.filterFrame)
        self.resultList = QtWidgets.QTreeWidget(SyntaxCheckerDialog)
        self.resultList.setAlternatingRowColors(True)
        self.resultList.setObjectName("resultList")
        self.verticalLayout.addWidget(self.resultList)
        self.checkProgressLabel = EricSqueezeLabelPath(SyntaxCheckerDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkProgressLabel.sizePolicy().hasHeightForWidth())
        self.checkProgressLabel.setSizePolicy(sizePolicy)
        self.checkProgressLabel.setText("")
        self.checkProgressLabel.setObjectName("checkProgressLabel")
        self.verticalLayout.addWidget(self.checkProgressLabel)
        self.checkProgress = QtWidgets.QProgressBar(SyntaxCheckerDialog)
        self.checkProgress.setProperty("value", 0)
        self.checkProgress.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.checkProgress.setObjectName("checkProgress")
        self.verticalLayout.addWidget(self.checkProgress)
        self.buttonBox = QtWidgets.QDialogButtonBox(SyntaxCheckerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SyntaxCheckerDialog)
        QtCore.QMetaObject.connectSlotsByName(SyntaxCheckerDialog)
        SyntaxCheckerDialog.setTabOrder(self.startButton, self.excludeFilesEdit)
        SyntaxCheckerDialog.setTabOrder(self.excludeFilesEdit, self.resultList)
        SyntaxCheckerDialog.setTabOrder(self.resultList, self.buttonBox)

    def retranslateUi(self, SyntaxCheckerDialog):
        _translate = QtCore.QCoreApplication.translate
        SyntaxCheckerDialog.setWindowTitle(_translate("SyntaxCheckerDialog", "Syntax Check Result"))
        SyntaxCheckerDialog.setWhatsThis(_translate("SyntaxCheckerDialog", "<b>Syntax Check Results</b>\n"
"<p>This dialog shows the results of the syntax check. Double clicking an\n"
"entry will open an editor window and position the cursor at the respective line.</p>"))
        self.label_2.setText(_translate("SyntaxCheckerDialog", "Exclude Files:"))
        self.excludeFilesEdit.setToolTip(_translate("SyntaxCheckerDialog", "Enter filename patterns of files to be excluded separated by a comma"))
        self.startButton.setToolTip(_translate("SyntaxCheckerDialog", "Press to start the syntax check run"))
        self.startButton.setText(_translate("SyntaxCheckerDialog", "Start"))
        self.resultList.setWhatsThis(_translate("SyntaxCheckerDialog", "<b>Result List</b>\n"
"<p>This list shows the results of the syntax check. Double clicking\n"
"an entry will open this entry in an editor window and position the cursor at\n"
"the respective line.</p>"))
        self.resultList.setSortingEnabled(True)
        self.resultList.headerItem().setText(0, _translate("SyntaxCheckerDialog", "File/Line"))
        self.resultList.headerItem().setText(1, _translate("SyntaxCheckerDialog", "Message"))
        self.resultList.headerItem().setText(2, _translate("SyntaxCheckerDialog", "Source"))
        self.checkProgress.setToolTip(_translate("SyntaxCheckerDialog", "Shows the progress of the syntax check action"))
        self.checkProgress.setFormat(_translate("SyntaxCheckerDialog", "%v/%m Files"))
from EricWidgets.EricSqueezeLabels import EricSqueezeLabelPath
