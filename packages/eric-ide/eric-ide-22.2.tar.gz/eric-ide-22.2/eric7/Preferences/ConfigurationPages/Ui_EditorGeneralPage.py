# Form implementation generated from reading ui file '/home/detlev/Development/Python/Eric/eric7-22.2/eric/eric7/Preferences/ConfigurationPages/EditorGeneralPage.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditorGeneralPage(object):
    def setupUi(self, EditorGeneralPage):
        EditorGeneralPage.setObjectName("EditorGeneralPage")
        EditorGeneralPage.resize(550, 1000)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(EditorGeneralPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.headerLabel = QtWidgets.QLabel(EditorGeneralPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_3.addWidget(self.headerLabel)
        self.line2 = QtWidgets.QFrame(EditorGeneralPage)
        self.line2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line2.setObjectName("line2")
        self.verticalLayout_3.addWidget(self.line2)
        self.groupBox_5 = QtWidgets.QGroupBox(EditorGeneralPage)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.autoindentCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.autoindentCheckBox.setObjectName("autoindentCheckBox")
        self.gridLayout_2.addWidget(self.autoindentCheckBox, 0, 0, 1, 1)
        self.tabforindentationCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.tabforindentationCheckBox.setObjectName("tabforindentationCheckBox")
        self.gridLayout_2.addWidget(self.tabforindentationCheckBox, 0, 1, 1, 1)
        self.tabindentsCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.tabindentsCheckBox.setObjectName("tabindentsCheckBox")
        self.gridLayout_2.addWidget(self.tabindentsCheckBox, 1, 0, 1, 1)
        self.converttabsCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.converttabsCheckBox.setObjectName("converttabsCheckBox")
        self.gridLayout_2.addWidget(self.converttabsCheckBox, 1, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.TextLabel13_3 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel13_3.setObjectName("TextLabel13_3")
        self.gridLayout_4.addWidget(self.TextLabel13_3, 0, 0, 1, 1)
        self.tabwidthSlider = QtWidgets.QSlider(self.groupBox_5)
        self.tabwidthSlider.setMinimum(1)
        self.tabwidthSlider.setMaximum(20)
        self.tabwidthSlider.setProperty("value", 4)
        self.tabwidthSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.tabwidthSlider.setTickInterval(1)
        self.tabwidthSlider.setObjectName("tabwidthSlider")
        self.gridLayout_4.addWidget(self.tabwidthSlider, 0, 1, 1, 1)
        self.tabwidthLCD = QtWidgets.QLCDNumber(self.groupBox_5)
        self.tabwidthLCD.setDigitCount(2)
        self.tabwidthLCD.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.tabwidthLCD.setProperty("value", 4.0)
        self.tabwidthLCD.setObjectName("tabwidthLCD")
        self.gridLayout_4.addWidget(self.tabwidthLCD, 0, 2, 1, 1)
        self.TextLabel13_2_3 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel13_2_3.setObjectName("TextLabel13_2_3")
        self.gridLayout_4.addWidget(self.TextLabel13_2_3, 1, 0, 1, 1)
        self.indentwidthSlider = QtWidgets.QSlider(self.groupBox_5)
        self.indentwidthSlider.setMinimum(1)
        self.indentwidthSlider.setMaximum(20)
        self.indentwidthSlider.setProperty("value", 4)
        self.indentwidthSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.indentwidthSlider.setTickInterval(1)
        self.indentwidthSlider.setObjectName("indentwidthSlider")
        self.gridLayout_4.addWidget(self.indentwidthSlider, 1, 1, 1, 1)
        self.indentwidthLCD = QtWidgets.QLCDNumber(self.groupBox_5)
        self.indentwidthLCD.setDigitCount(2)
        self.indentwidthLCD.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.indentwidthLCD.setProperty("value", 4.0)
        self.indentwidthLCD.setObjectName("indentwidthLCD")
        self.gridLayout_4.addWidget(self.indentwidthLCD, 1, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.languageOverrideWidget = QtWidgets.QTreeWidget(self.groupBox_5)
        self.languageOverrideWidget.setAlternatingRowColors(True)
        self.languageOverrideWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.languageOverrideWidget.setRootIsDecorated(False)
        self.languageOverrideWidget.setItemsExpandable(False)
        self.languageOverrideWidget.setObjectName("languageOverrideWidget")
        self.languageOverrideWidget.headerItem().setText(3, " ")
        self.horizontalLayout_2.addWidget(self.languageOverrideWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.addButton = QtWidgets.QToolButton(self.groupBox_5)
        self.addButton.setObjectName("addButton")
        self.verticalLayout_2.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QToolButton(self.groupBox_5)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout_2.addWidget(self.deleteButton)
        self.editButton = QtWidgets.QToolButton(self.groupBox_5)
        self.editButton.setObjectName("editButton")
        self.verticalLayout_2.addWidget(self.editButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.groupBox_5)
        self.sourceOutlineGroupBox = QtWidgets.QGroupBox(EditorGeneralPage)
        self.sourceOutlineGroupBox.setCheckable(True)
        self.sourceOutlineGroupBox.setObjectName("sourceOutlineGroupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.sourceOutlineGroupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.sourceOutlineGroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.sourceOutlineWidthSpinBox = QtWidgets.QSpinBox(self.sourceOutlineGroupBox)
        self.sourceOutlineWidthSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.sourceOutlineWidthSpinBox.setMinimum(50)
        self.sourceOutlineWidthSpinBox.setMaximum(498)
        self.sourceOutlineWidthSpinBox.setSingleStep(50)
        self.sourceOutlineWidthSpinBox.setObjectName("sourceOutlineWidthSpinBox")
        self.gridLayout_3.addWidget(self.sourceOutlineWidthSpinBox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.sourceOutlineGroupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)
        self.sourceOutlineWidthStepSpinBox = QtWidgets.QSpinBox(self.sourceOutlineGroupBox)
        self.sourceOutlineWidthStepSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.sourceOutlineWidthStepSpinBox.setMinimum(10)
        self.sourceOutlineWidthStepSpinBox.setMaximum(100)
        self.sourceOutlineWidthStepSpinBox.setSingleStep(10)
        self.sourceOutlineWidthStepSpinBox.setObjectName("sourceOutlineWidthStepSpinBox")
        self.gridLayout_3.addWidget(self.sourceOutlineWidthStepSpinBox, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(345, 17, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 4, 1, 1)
        self.sourceOutlineShowCodingCheckBox = QtWidgets.QCheckBox(self.sourceOutlineGroupBox)
        self.sourceOutlineShowCodingCheckBox.setObjectName("sourceOutlineShowCodingCheckBox")
        self.gridLayout_3.addWidget(self.sourceOutlineShowCodingCheckBox, 1, 0, 1, 5)
        self.verticalLayout_3.addWidget(self.sourceOutlineGroupBox)
        self.groupBox = QtWidgets.QGroupBox(EditorGeneralPage)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.comment0CheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.comment0CheckBox.setObjectName("comment0CheckBox")
        self.gridLayout.addWidget(self.comment0CheckBox, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(EditorGeneralPage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 1)
        self.docstringStyleComboBox = QtWidgets.QComboBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.docstringStyleComboBox.sizePolicy().hasHeightForWidth())
        self.docstringStyleComboBox.setSizePolicy(sizePolicy)
        self.docstringStyleComboBox.setObjectName("docstringStyleComboBox")
        self.gridLayout_6.addWidget(self.docstringStyleComboBox, 0, 1, 1, 1)
        self.docstringCompletionCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.docstringCompletionCheckBox.setObjectName("docstringCompletionCheckBox")
        self.gridLayout_6.addWidget(self.docstringCompletionCheckBox, 1, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.mouseHoverHelpGroupBox = QtWidgets.QGroupBox(EditorGeneralPage)
        self.mouseHoverHelpGroupBox.setCheckable(True)
        self.mouseHoverHelpGroupBox.setObjectName("mouseHoverHelpGroupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.mouseHoverHelpGroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.mouseHoverHelpGroupBox)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.mouseDwellTimeSpinBox = QtWidgets.QSpinBox(self.mouseHoverHelpGroupBox)
        self.mouseDwellTimeSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.mouseDwellTimeSpinBox.setMinimum(100)
        self.mouseDwellTimeSpinBox.setMaximum(1000)
        self.mouseDwellTimeSpinBox.setSingleStep(50)
        self.mouseDwellTimeSpinBox.setProperty("value", 500)
        self.mouseDwellTimeSpinBox.setObjectName("mouseDwellTimeSpinBox")
        self.horizontalLayout.addWidget(self.mouseDwellTimeSpinBox)
        spacerItem3 = QtWidgets.QSpacerItem(347, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_3.addWidget(self.mouseHoverHelpGroupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(EditorGeneralPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.vsSelectionCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.vsSelectionCheckBox.setObjectName("vsSelectionCheckBox")
        self.verticalLayout.addWidget(self.vsSelectionCheckBox)
        self.vsUserCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.vsUserCheckBox.setObjectName("vsUserCheckBox")
        self.verticalLayout.addWidget(self.vsUserCheckBox)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.TextLabel13_3.setBuddy(self.tabwidthSlider)
        self.TextLabel13_2_3.setBuddy(self.indentwidthSlider)

        self.retranslateUi(EditorGeneralPage)
        self.tabwidthSlider.valueChanged['int'].connect(self.tabwidthLCD.display) # type: ignore
        self.indentwidthSlider.valueChanged['int'].connect(self.indentwidthLCD.display) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EditorGeneralPage)
        EditorGeneralPage.setTabOrder(self.autoindentCheckBox, self.tabforindentationCheckBox)
        EditorGeneralPage.setTabOrder(self.tabforindentationCheckBox, self.tabindentsCheckBox)
        EditorGeneralPage.setTabOrder(self.tabindentsCheckBox, self.converttabsCheckBox)
        EditorGeneralPage.setTabOrder(self.converttabsCheckBox, self.tabwidthSlider)
        EditorGeneralPage.setTabOrder(self.tabwidthSlider, self.indentwidthSlider)
        EditorGeneralPage.setTabOrder(self.indentwidthSlider, self.languageOverrideWidget)
        EditorGeneralPage.setTabOrder(self.languageOverrideWidget, self.addButton)
        EditorGeneralPage.setTabOrder(self.addButton, self.deleteButton)
        EditorGeneralPage.setTabOrder(self.deleteButton, self.editButton)
        EditorGeneralPage.setTabOrder(self.editButton, self.sourceOutlineGroupBox)
        EditorGeneralPage.setTabOrder(self.sourceOutlineGroupBox, self.sourceOutlineWidthSpinBox)
        EditorGeneralPage.setTabOrder(self.sourceOutlineWidthSpinBox, self.sourceOutlineWidthStepSpinBox)
        EditorGeneralPage.setTabOrder(self.sourceOutlineWidthStepSpinBox, self.sourceOutlineShowCodingCheckBox)
        EditorGeneralPage.setTabOrder(self.sourceOutlineShowCodingCheckBox, self.comment0CheckBox)
        EditorGeneralPage.setTabOrder(self.comment0CheckBox, self.docstringStyleComboBox)
        EditorGeneralPage.setTabOrder(self.docstringStyleComboBox, self.docstringCompletionCheckBox)
        EditorGeneralPage.setTabOrder(self.docstringCompletionCheckBox, self.mouseHoverHelpGroupBox)
        EditorGeneralPage.setTabOrder(self.mouseHoverHelpGroupBox, self.mouseDwellTimeSpinBox)
        EditorGeneralPage.setTabOrder(self.mouseDwellTimeSpinBox, self.vsSelectionCheckBox)
        EditorGeneralPage.setTabOrder(self.vsSelectionCheckBox, self.vsUserCheckBox)

    def retranslateUi(self, EditorGeneralPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EditorGeneralPage", "<b>Configure general editor settings</b>"))
        self.groupBox_5.setTitle(_translate("EditorGeneralPage", "Tabs && Indentation"))
        self.autoindentCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether autoindentation shall be enabled"))
        self.autoindentCheckBox.setText(_translate("EditorGeneralPage", "Auto indentation"))
        self.tabforindentationCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether tab characters are used for indentations."))
        self.tabforindentationCheckBox.setText(_translate("EditorGeneralPage", "Use tabs for indentations"))
        self.tabindentsCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether pressing the tab key indents."))
        self.tabindentsCheckBox.setText(_translate("EditorGeneralPage", "Tab key indents"))
        self.converttabsCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether tabs shall be converted upon opening the file"))
        self.converttabsCheckBox.setText(_translate("EditorGeneralPage", "Convert tabs upon open"))
        self.TextLabel13_3.setText(_translate("EditorGeneralPage", "Tab width:"))
        self.tabwidthSlider.setToolTip(_translate("EditorGeneralPage", "Move to set the tab width."))
        self.tabwidthLCD.setToolTip(_translate("EditorGeneralPage", "Displays the selected tab width."))
        self.TextLabel13_2_3.setText(_translate("EditorGeneralPage", "Indentation width:"))
        self.indentwidthSlider.setToolTip(_translate("EditorGeneralPage", "Move to set the indentation width."))
        self.indentwidthLCD.setToolTip(_translate("EditorGeneralPage", "Displays the selected indentation width."))
        self.languageOverrideWidget.headerItem().setText(0, _translate("EditorGeneralPage", "Language"))
        self.languageOverrideWidget.headerItem().setText(1, _translate("EditorGeneralPage", "Tab Width"))
        self.languageOverrideWidget.headerItem().setText(2, _translate("EditorGeneralPage", "Indent Width"))
        self.addButton.setToolTip(_translate("EditorGeneralPage", "Press to add a language specific override"))
        self.deleteButton.setToolTip(_translate("EditorGeneralPage", "Press to delete the selected language specific override"))
        self.editButton.setToolTip(_translate("EditorGeneralPage", "Press to edit the selected language specific override"))
        self.sourceOutlineGroupBox.setToolTip(_translate("EditorGeneralPage", "Select to enable the source code outline view"))
        self.sourceOutlineGroupBox.setTitle(_translate("EditorGeneralPage", "Source Code Outline"))
        self.label_2.setText(_translate("EditorGeneralPage", "Default Width:"))
        self.sourceOutlineWidthSpinBox.setToolTip(_translate("EditorGeneralPage", "Enter the default width of the source code outline view"))
        self.label_3.setText(_translate("EditorGeneralPage", "Width Step Size:"))
        self.sourceOutlineWidthStepSpinBox.setToolTip(_translate("EditorGeneralPage", "Enter the amount of pixels the width of the outline should be increased or decreased"))
        self.sourceOutlineShowCodingCheckBox.setToolTip(_translate("EditorGeneralPage", "Select to show the source code encoding"))
        self.sourceOutlineShowCodingCheckBox.setText(_translate("EditorGeneralPage", "Show source file encoding"))
        self.groupBox.setTitle(_translate("EditorGeneralPage", "Comments"))
        self.comment0CheckBox.setToolTip(_translate("EditorGeneralPage", "Select to insert the comment sign at column 0"))
        self.comment0CheckBox.setWhatsThis(_translate("EditorGeneralPage", "<b>Insert comment at column 0</b><p>Select to insert the comment sign at column 0. Otherwise, the comment sign is inserted at the first non-whitespace position.</p>"))
        self.comment0CheckBox.setText(_translate("EditorGeneralPage", "Insert comment at column 0"))
        self.groupBox_3.setTitle(_translate("EditorGeneralPage", "Docstring"))
        self.label_4.setText(_translate("EditorGeneralPage", "Docstring Style:"))
        self.docstringStyleComboBox.setToolTip(_translate("EditorGeneralPage", "Select the docstring style to be used"))
        self.docstringCompletionCheckBox.setToolTip(_translate("EditorGeneralPage", "Select this to generate a docstring when the docstring start sequence was entered (e.g. \"\"\" for Python)."))
        self.docstringCompletionCheckBox.setText(_translate("EditorGeneralPage", "Generate Docstring when Docstring start is entered"))
        self.mouseHoverHelpGroupBox.setToolTip(_translate("EditorGeneralPage", "Select to enable the support for mouse hover help text"))
        self.mouseHoverHelpGroupBox.setWhatsThis(_translate("EditorGeneralPage", "<b>Mouse Hover Help</b><p>Enable this option to show some information about the symbol the mouse is hovering over. An information provider plug-in (e.g. Jedi) must be installed for this to work.</p>"))
        self.mouseHoverHelpGroupBox.setTitle(_translate("EditorGeneralPage", "Mouse Hover Help"))
        self.label_5.setText(_translate("EditorGeneralPage", "Wait time:"))
        self.mouseDwellTimeSpinBox.setToolTip(_translate("EditorGeneralPage", "Enter the time to wait before help information is shown"))
        self.mouseDwellTimeSpinBox.setSuffix(_translate("EditorGeneralPage", " ms"))
        self.groupBox_2.setTitle(_translate("EditorGeneralPage", "Virtual Space"))
        self.label.setText(_translate("EditorGeneralPage", "Virtual space is the space after the last character of a line. It is not allocated unless some text is entered or copied into it. Usage of virtual space can be configured with these selections."))
        self.vsSelectionCheckBox.setToolTip(_translate("EditorGeneralPage", "Select to enable a rectangular selection to extend into virtual space"))
        self.vsSelectionCheckBox.setText(_translate("EditorGeneralPage", "Selection may access virtual space"))
        self.vsUserCheckBox.setToolTip(_translate("EditorGeneralPage", "Select to allow the cursor to be moved into virtual space"))
        self.vsUserCheckBox.setText(_translate("EditorGeneralPage", "Cursor can move into virtual space"))
