# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to display profile data.
"""

import os
import pickle       # secok

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QMenu, QHeaderView, QTreeWidgetItem,
    QApplication
)

from EricWidgets import EricMessageBox

from .Ui_PyProfileDialog import Ui_PyProfileDialog
import Utilities


class ProfileTreeWidgetItem(QTreeWidgetItem):
    """
    Class implementing a custom QTreeWidgetItem to allow sorting on numeric
    values.
    """
    def __getNC(self, itm):
        """
        Private method to get the value to compare on for the first column.
        
        @param itm item to operate on (ProfileTreeWidgetItem)
        @return comparison value for the first column (integer)
        """
        s = itm.text(0)
        return int(s.split('/')[0])
        
    def __lt__(self, other):
        """
        Special method to check, if the item is less than the other one.
        
        @param other reference to item to compare against
            (ProfileTreeWidgetItem)
        @return true, if this item is less than other (boolean)
        """
        column = self.treeWidget().sortColumn()
        if column == 0:
            return self.__getNC(self) < self.__getNC(other)
        if column == 6:
            return int(self.text(column)) < int(other.text(column))
        return self.text(column) < other.text(column)
        

class PyProfileDialog(QDialog, Ui_PyProfileDialog):
    """
    Class implementing a dialog to display the results of a profiling run.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        self.cancelled = False
        self.exclude = True
        self.ericpath = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        self.pyLibPath = Utilities.getPythonLibPath()
        
        self.summaryList.headerItem().setText(
            self.summaryList.columnCount(), "")
        self.resultList.headerItem().setText(self.resultList.columnCount(), "")
        self.resultList.header().setSortIndicator(
            0, Qt.SortOrder.DescendingOrder)
        
        self.__menu = QMenu(self)
        self.filterItm = self.__menu.addAction(
            self.tr('Exclude Python Library'),
            self.__filter)
        self.__menu.addSeparator()
        self.__menu.addAction(
            self.tr('Erase Profiling Info'), self.__eraseProfile)
        self.__menu.addAction(
            self.tr('Erase Timing Info'), self.__eraseTiming)
        self.__menu.addSeparator()
        self.__menu.addAction(self.tr('Erase All Infos'), self.__eraseAll)
        self.resultList.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.resultList.customContextMenuRequested.connect(
            self.__showContextMenu)
        self.summaryList.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.summaryList.customContextMenuRequested.connect(
            self.__showContextMenu)
        
    def __createResultItem(self, calls, totalTime, totalTimePerCall,
                           cumulativeTime, cumulativeTimePerCall, file, line,
                           functionName):
        """
        Private method to create an entry in the result list.
        
        @param calls number of calls (integer)
        @param totalTime total time (double)
        @param totalTimePerCall total time per call (double)
        @param cumulativeTime cumulative time (double)
        @param cumulativeTimePerCall cumulative time per call (double)
        @param file filename of file (string)
        @param line linenumber (integer)
        @param functionName function name (string)
        """
        itm = ProfileTreeWidgetItem(self.resultList, [
            calls,
            "{0: 8.3f}".format(totalTime),
            totalTimePerCall,
            "{0: 8.3f}".format(cumulativeTime),
            cumulativeTimePerCall,
            file,
            str(line),
            functionName
        ])
        for col in [0, 1, 2, 3, 4, 6]:
            itm.setTextAlignment(col, Qt.AlignmentFlag.AlignRight)
        
    def __createSummaryItem(self, label, contents):
        """
        Private method to create an entry in the summary list.
        
        @param label text of the first column (string)
        @param contents text of the second column (string)
        """
        itm = QTreeWidgetItem(self.summaryList, [label, contents])
        itm.setTextAlignment(1, Qt.AlignmentFlag.AlignRight)
        
    def __resortResultList(self):
        """
        Private method to resort the tree.
        """
        self.resultList.sortItems(self.resultList.sortColumn(),
                                  self.resultList.header()
                                  .sortIndicatorOrder())
        
    def __populateLists(self, exclude=False):
        """
        Private method used to populate the listviews.
        
        @param exclude flag indicating whether files residing in the
                Python library should be excluded
        """
        self.resultList.clear()
        self.summaryList.clear()
        
        self.checkProgress.setMaximum(len(self.stats))
        QApplication.processEvents()
        
        total_calls = 0
        prim_calls = 0
        total_tt = 0
        
        try:
            # disable updates of the list for speed
            self.resultList.setUpdatesEnabled(False)
            self.resultList.setSortingEnabled(False)
            
            # now go through all the files
            for progress, (func, (cc, nc, tt, ct, _callers)) in enumerate(
                list(self.stats.items()), start=1
            ):
                if self.cancelled:
                    return
                
                if (
                    not (self.ericpath and
                         func[0].startswith(self.ericpath)) and
                    not func[0].startswith("DebugClients") and
                    func[0] != "profile" and
                    not (exclude and (func[0].startswith(self.pyLibPath) or
                                      func[0] == "")
                         ) and
                    (self.file is None or
                     func[0].startswith(self.file) or
                     func[0].startswith(self.pyLibPath))
                ):
                    # calculate the totals
                    total_calls += nc
                    prim_calls += cc
                    total_tt += tt
                    
                    if nc != cc:
                        c = "{0:d}/{1:d}".format(nc, cc)
                    else:
                        c = str(nc)
                    if nc == 0:
                        tpc = "{0: 8.3f}".format(0.0)
                    else:
                        tpc = "{0: 8.3f}".format(tt / nc)
                    if cc == 0:
                        cpc = "{0: 8.3f}".format(0.0)
                    else:
                        cpc = "{0: 8.3f}".format(ct / cc)
                    self.__createResultItem(c, tt, tpc, ct, cpc, func[0],
                                            func[1], func[2])
                    
                self.checkProgress.setValue(progress)
                QApplication.processEvents()
        finally:
            # reenable updates of the list
            self.resultList.setSortingEnabled(True)
            self.resultList.setUpdatesEnabled(True)
        self.__resortResultList()
        
        # now do the summary stuff
        self.__createSummaryItem(self.tr("function calls"),
                                 str(total_calls))
        if total_calls != prim_calls:
            self.__createSummaryItem(self.tr("primitive calls"),
                                     str(prim_calls))
        self.__createSummaryItem(self.tr("CPU seconds"),
                                 "{0:.3f}".format(total_tt))
        
    def start(self, pfn, fn=None):
        """
        Public slot to start the calculation of the profile data.
        
        @param pfn basename of the profiling file (string)
        @param fn file to display the profiling data for (string)
        """
        self.basename = os.path.splitext(pfn)[0]
        
        fname = "{0}.profile".format(self.basename)
        if not os.path.exists(fname):
            EricMessageBox.warning(
                self,
                self.tr("Profile Results"),
                self.tr("""<p>There is no profiling data"""
                        """ available for <b>{0}</b>.</p>""")
                .format(pfn))
            self.close()
            return
        try:
            with open(fname, 'rb') as f:
                self.stats = pickle.load(f)     # secok
        except (OSError, pickle.PickleError, EOFError):
            EricMessageBox.critical(
                self,
                self.tr("Loading Profiling Data"),
                self.tr("""<p>The profiling data could not be"""
                        """ read from file <b>{0}</b>.</p>""")
                .format(fname))
            self.close()
            return
        
        self.file = fn
        self.__populateLists()
        self.__finish()
        
    def __finish(self):
        """
        Private slot called when the action finished or the user pressed the
        button.
        """
        self.cancelled = True
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        QApplication.processEvents()
        self.resultList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.resultList.header().setStretchLastSection(True)
        self.summaryList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.summaryList.header().setStretchLastSection(True)
        
    def __unfinish(self):
        """
        Private slot called to revert the effects of the __finish slot.
        """
        self.cancelled = False
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
        elif button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            self.__finish()
        
    def __showContextMenu(self, coord):
        """
        Private slot to show the context menu of the listview.
        
        @param coord the position of the mouse pointer (QPoint)
        """
        self.__menu.popup(self.mapToGlobal(coord))
        
    def __eraseProfile(self):
        """
        Private slot to handle the Erase Profile context menu action.
        """
        fname = "{0}.profile".format(self.basename)
        if os.path.exists(fname):
            os.remove(fname)
        
    def __eraseTiming(self):
        """
        Private slot to handle the Erase Timing context menu action.
        """
        fname = "{0}.timings".format(self.basename)
        if os.path.exists(fname):
            os.remove(fname)
        
    def __eraseAll(self):
        """
        Private slot to handle the Erase All context menu action.
        """
        self.__eraseProfile()
        self.__eraseTiming()
        
    def __filter(self):
        """
        Private slot to handle the Exclude/Include Python Library context menu
        action.
        """
        self.__unfinish()
        if self.exclude:
            self.exclude = False
            self.filterItm.setText(self.tr('Include Python Library'))
            self.__populateLists(True)
        else:
            self.exclude = True
            self.filterItm.setText(self.tr('Exclude Python Library'))
            self.__populateLists(False)
        self.__finish()
