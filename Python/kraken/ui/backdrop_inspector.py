
#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#

from PySide import QtGui, QtCore

from kraken.ui.color_widget import KColorWidget


class BackdropInspector(QtGui.QDialog):
    """A widget providing the ability to nest """

    def __init__(self, parent=None, nodeItem=None):

        # constructors of base classes
        super(BackdropInspector, self).__init__(parent)
        self.setObjectName('BackdropInspector')

        self.parent = parent
        self.nodeItem = nodeItem

        self.setWindowTitle(self.nodeItem.getName())
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.resize(600, 300)

        self.createLayout()
        self.createConnections()


    def createLayout(self):
        self._mainLayout = QtGui.QVBoxLayout()
        self._mainLayout.setContentsMargins(10, 10, 10, 10)

        self._commentTextEdit = QtGui.QTextEdit(self)
        self._commentTextEdit.setText(self.nodeItem.getComment())
        self._commentTextEdit.setMinimumHeight(20)
        self._commentTextEdit.setMaximumHeight(40)

        self._settingsLayout = QtGui.QGridLayout()
        self._settingsLayout.setContentsMargins(10, 10, 10, 10)
        self._settingsLayout.setSpacing(3)
        self._settingsLayout.setColumnMinimumWidth(0, 75)
        self._settingsLayout.setColumnStretch(0, 0)
        self._settingsLayout.setColumnStretch(1, 1)

        # Settings widgets
        self._colorLabel = QtGui.QLabel('Color', self)
        self._colorLabel.setObjectName('color_label')
        self._colorLabel.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        self._colorLabel.setMinimumWidth(75)
        self._colorWidget = KColorWidget(self, self.nodeItem.getColor())

        self._settingsLayout.addWidget(self._colorLabel, 0, 0, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self._settingsLayout.addWidget(self._colorWidget, 0, 1, 1, 1, alignment=QtCore.Qt.AlignLeft)

        # OK and Cancel buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        self._mainLayout.addWidget(self._commentTextEdit)
        self._mainLayout.addLayout(self._settingsLayout)
        self._mainLayout.addStretch(1)
        self._mainLayout.addWidget(self.buttons)

        self.setLayout(self._mainLayout)

    def createConnections(self):
        self.buttons.accepted.connect(self.acceptClose)
        self.buttons.rejected.connect(self.close)

        self._colorWidget.colorChanged.connect(self.setNodeColor)

    def acceptClose(self):

        if self.nodeItem.getComment() != self._commentTextEdit.toPlainText():
            self.nodeItem.setComment(self._commentTextEdit.toPlainText())
            self.nodeItem.adjustSize()

        self.close()


    def setNodeColor(self, color):
        self.nodeItem.setColor(QtGui.QColor(color))
        self.nodeItem.setUnselectedColor(self.nodeItem.getColor().darker(125))
        self.nodeItem.setSelectedColor(self.nodeItem.getColor().lighter(175))
        self.nodeItem.setHoveredColor(self.nodeItem.getColor().lighter(110))

    # =======
    # Events
    # =======
    def closeEvent(self, event):
        if self.nodeItem is not None:
            self.nodeItem.inspectorClosed()
