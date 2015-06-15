
#
# Copyright 2010-2015
#

import os
import sys

from PySide import QtGui, QtCore

from kraken_splash import KrakenSplash
from component_library import ComponentLibrary
from GraphView.graph_view_widget import GraphViewWidget

from kraken.core.kraken_system import KrakenSystem


class KrakenUI(QtGui.QWidget):
    """A debugger widget hosting an inspector as well as a graph view"""

    def __init__(self, parent=None):

        # constructors of base classes
        super(KrakenUI, self).__init__(parent)
        self.setObjectName('mainUI')

        styleSheet = """

        QWidget#mainUI {
            background-color: #151515;
        }

        QSplitter::handle:horizontal {
            background: #222;
            width: 13px;
            margin-top: 2px;
            margin-bottom: 2px;
            border-radius: 3px;
        }

        QListWidget#ComponentTree {
            border: 0;
            border-radius: 3px;
            padding: 0;
            margin: 0;

            color: #e1ffff;
            background-color: #333;
        }

        QListWidget#ComponentTree::item {
            padding: 5px 0;
            margin: 0;
            spacing: 0;
        }

        QListWidget#ComponentTree::item:hover {
            background-color: #438f99;
        }

        QListWidget#ComponentTree::item:focus {
            color: white;
            background-color: #438f99;
        }

        QListWidget#ComponentTree::item:selected {
            color: white;
            background-color: #438f99;
        }

        QLineEdit {
            border: 0px;
            border-radius: 3px;
            padding: 3px;

            color: #e1ffff;
            background-color: #333;
        }

        /* Contextual Node List */
        QLineEdit#contextNodeListSearchLine {
            border: 1px solid #111;
        }

        QListWidget#contextNodeList {
            background-color: #333;
        }

        QListWidget#contextNodeList::item {
            color: #e1ffff;
        }

        QListWidget#contextNodeList::item:selected {
            color: white;
            background-color: #438f99;
        }

        QListWidget#contextNodeList::item:hover {
            background-color: #438f99;
        }

        /* Toolbar */
        QToolbar#mainToolbar {
            spacing: 20px;
        }

        QToolBar {
            border: 0px;
            border-radius: 3px;
            height: 50px;
            padding: 5px 5px;
            margin: 0;
            spacing: 5px;

            background-color: #222;
        }

        QToolBar::handle {
            background-color: #FF0000;
        }

        QToolButton {
            width: 65px;
            border-radius: 3px;
            padding: 5px;

            background-color: #333;
            color: #e1ffff;
        }

        QToolButton:hover {
            background-color: #3b3b3b;
        }

        QLabel {
            padding-right: 10px;

            color: #e1ffff;
        }

        QLabel#logoWidget {
            margin: 0px;
            padding: 0px 5px;
        }

        QToolBar::separator {
            padding: 0 10px;
            width: 1px;
        }

        QGraphicsView#graphView {
            border: 0px;
        }

        """

        self.setStyleSheet(styleSheet)

        self.setWindowTitle("Kraken Editor")
        self.setAcceptDrops(True)

        self.nodeLibrary = ComponentLibrary(parent=self)
        self.graphViewWidget = GraphViewWidget(parent=self)

        horizontalSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, parent=self)
        horizontalSplitter.addWidget(self.nodeLibrary)
        horizontalSplitter.addWidget(self.graphViewWidget)

        horizontalSplitter.setStretchFactor(0, 0)
        horizontalSplitter.setStretchFactor(1, 1)

        horizontalSplitter.setSizes([0, 100])

        grid = QtGui.QVBoxLayout(self)
        grid.addWidget(horizontalSplitter)

    def closeEvent(self, event):
        self.graphViewWidget.closeEvent(event)

    def showEvent(self, event):

        splash = KrakenSplash(self)
        splash.show()

        krakenSystem = KrakenSystem.getInstance()
        krakenSystem.loadCoreClient()
        krakenSystem.loadExtension('Kraken')

        splash.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    widget = KrakenUI()
    widget.show()

    sys.exit(app.exec_())
