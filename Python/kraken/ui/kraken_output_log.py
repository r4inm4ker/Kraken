
from PySide import QtGui, QtCore

from kraken.ui import images_rc
from kraken.log import getLogger

logger = getLogger('kraken')


class OutputLogDialog(QtGui.QDialog):
    """Output Dialog"""

    def __init__(self, parent=None):
        super(OutputLogDialog, self).__init__(parent)
        self.setObjectName('outputLog')
        self.resize(700, 300)
        self.setWindowTitle('Kraken Output Log')

        for handler in logger.handlers:
            if type(handler).__name__ == 'WidgetHandler':
                handler.addWidget(self)

        self.createLayout()
        self.createConnections()


    def createLayout(self):
        """Sets up the layout for the dialog."""

        self.textWidget = QtGui.QTextEdit(self)
        self.textWidget.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textWidget.setReadOnly(True)
        self.textWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.outputLogLayout = QtGui.QVBoxLayout(self)
        self.outputLogLayout.addWidget(self.textWidget)

        self.setLayout(self.outputLogLayout)

    def createConnections(self):
        """Connects widgets to methods or other signals."""

        self.textWidget.customContextMenuRequested.connect(self.createContextMenu)

    def write(self, msg, level):

        if level == 'DEBUG':
            messageColor = QtGui.QColor("#B4EEB4")
        elif level == 'INFO':
            messageColor = QtGui.QColor(QtCore.Qt.white)
        elif level == 'WARNING':
            messageColor = QtGui.QColor("#CC3300")
        elif level == 'ERROR':
            messageColor = QtGui.QColor("#FF0000")
        elif level == 'CRITICAL':
            messageColor = QtGui.QColor("#FF0000")
        else:
            messageColor = QtGui.QColor(QtCore.Qt.white)

        self.textWidget.setTextColor(messageColor)
        charFormat = self.textWidget.currentCharFormat()
        textCursor = self.textWidget.textCursor()
        textCursor.movePosition(QtGui.QTextCursor.End)
        textCursor.insertText(msg, charFormat)

        self.textWidget.setTextCursor(textCursor)
        self.textWidget.ensureCursorVisible()

    # =============
    # Context Menu
    # =============
    def createContextMenu(self):
        self.contextMenu = QtGui.QMenu(self)
        selectAllAction = self.contextMenu.addAction("Select All")
        copyAction = self.contextMenu.addAction("Copy")
        self.contextMenu.addSeparator()
        clearAction = self.contextMenu.addAction("Clear")

        selectAllAction.triggered.connect(self.contextSelectAll)
        copyAction.triggered.connect(self.contextCopy)
        clearAction.triggered.connect(self.textWidget.clear)

        self.contextMenu.exec_(QtGui.QCursor.pos())

    def contextSelectAll(self):
        self.textWidget.selectAll()

    def contextCopy(self):
        self.textWidget.copy()
