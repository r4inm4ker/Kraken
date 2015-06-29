
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
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', 'Kraken_Icon.png')))

        self.styleSheet = """


        QLabel {
            padding-right: 10px;

            color: #e1ffff;
        }

        QToolBar::separator {
            padding: 0 10px;
            width: 1px;
        }

        QLineEdit {
            border: 0px;
            border-radius: 3px;
            padding: 3px;

            color: #e1ffff;
            background-color: #333;
        }

        QLineEdit:hover {
            background-color: #3b3b3b;
        }

        QSplitter::handle:horizontal {
            background: #222;
            width: 13px;
            margin-top: 2px;
            margin-bottom: 2px;
            border-radius: 3px;
        }


        /* ======= */
        /* Main UI */
        /* ======= */
        QWidget#mainUI {
            background-color: #151515;
        }


        /* ============== */
        /* Component Tree */
        /* ============== */
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


        /* =================== */
        /* Component Inspector */
        /* =================== */
        QWidget#componentInspector QWidget {
            background-color: #222;
        }

        QWidget#componentInspector QLineEdit {
            border: 0px;
            border-radius: 3px;
            padding: 3px;

            background-color: #333;
        }

        QWidget#componentInspector QLineEdit:hover {
            background-color: #3b3b3b;
        }

        QWidget#componentInspector QFrame#separatorFrame {
            border-bottom: 1px solid #293b3d;
            border-style: outset;
        }

        QWidget#componentInspector QLabel#separatorLabel {
            border: 1px #293b3d;
            border-style: outset;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            padding: 6px;

            background-color: #293b3d;
            color: #64d7e6;
        }

        QWidget#componentInspector QSlider::groove:horizontal {
            background-color: #3b3b3b;
            height: 8px;
        }

        QWidget#componentInspector QSlider::handle:horizontal {
            border: 1px #438f99;
            border-style: outset;
            margin: -2px 0;
            width: 18px;

            background-color: #438f99;
        }


        /* ==================== */
        /* Contextual Node List */
        /* ==================== */
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

        /* ============ */
        /* Main Toolbar */
        /* ============ */
        QToolbar#mainToolbar {
            spacing: 20px;
        }

        QToolBar#mainToolbar {
            border: 0px;
            border-radius: 3px;
            height: 50px;
            padding: 5px 5px;
            margin: 0;
            spacing: 5px;

            background-color: #222;
        }

        QToolBar#mainToolbar::handle {
            background-color: #FF0000;
        }

        QToolBar#mainToolbar QToolButton {
            width: 65px;
            border: 1px #333;
            border-radius: 3px;
            border-style: outset;
            padding: 5px;

            background-color: #333;
            color: #e1ffff;
        }

        QToolBar#mainToolbar QToolButton:hover {
            background-color: #3b3b3b;
        }

        QToolBar#mainToolbar QToolButton:pressed {
            border-style: inset;
            padding-top: 6px;
            padding-left: 7px;

            background-color: #3b3b3b;
        }

        QLabel#rigNameLabel {
            background-color: #222;
        }

        /* ==== */
        /* Logo */
        /* ==== */
        QLabel#logoWidget {
            margin: 0px;
            padding: 0px 5px;

            background-color: #222;
        }

        /* ========== */
        /* Graph View */
        /* ========== */
        QGraphicsView#graphView {
            border: 0px;
        }


        /* ================ */
        /* Right Click Menu */
        /* ================ */
        QMenu#rightClickContextMenu {
            border: 1px solid #666;
            border-radius: 3px;
            padding: 3px;

            background-color: #333;
            color: #e1ffff;
        }

        QMenu#rightClickContextMenu QAbstractItemView {
            background-color: transparent;
        }

        QMenu#rightClickContextMenu::item{
            color: white;
            padding: 5px;
        }

        QMenu#rightClickContextMenu::item:selected {
            background-color: #438f99;
        }

        QMenu#rightClickContextMenu::item:hover {
            background-color: #438f99;
        }

        """

        self.setStyleSheet(self.styleSheet)

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
