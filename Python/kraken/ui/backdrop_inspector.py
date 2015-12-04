
#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#

#pylint: disable-msg=W0613,R0201
import sys
from PySide import QtGui, QtCore
from DataTypeWidgets import AttributeWidget
from kraken.core.kraken_system import KrakenSystem


class BackdropInspector(QtGui.QDialog):
    """A widget providing the ability to nest """

    def __init__(self, parent=None, nodeItem=None):

        # constructors of base classes
        super(BackdropInspector, self).__init__(parent)
        self.setObjectName('BackdropInspector')

        self.parent = parent
        self.nodeItem = nodeItem

        self.setWindowTitle( self.nodeItem.getName() )
        self.setWindowFlags( QtCore.Qt.Dialog )
        self.resize( 600, 300 )

        # layout
        self._mainLayout = QtGui.QVBoxLayout()
        self._mainLayout.setContentsMargins(10, 10, 10, 10)

        self._commentTextEdit = QtGui.QTextEdit(self)
        self._commentTextEdit.setText(self.nodeItem.getComment())
        self._commentTextEdit.setMinimumHeight(20)
        self._commentTextEdit.setMaximumHeight(40)

        # OK and Cancel buttons
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        buttons.accepted.connect(self.acceptClose)
        buttons.rejected.connect(self.close)

        self._mainLayout.addWidget(self._commentTextEdit)
        self._mainLayout.addStretch(1)
        self._mainLayout.addWidget(buttons)

        self.setLayout(self._mainLayout)


    def acceptClose(self):

        self.nodeItem.setComment(self._commentTextEdit.toPlainText())
        self.nodeItem.adjustSize()
        self.close()

    ##############################
    ## Events

    def closeEvent(self, event):
        if self.nodeItem is not None:
            self.nodeItem.inspectorClosed()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    from kraken_examples.arm_component import ArmComponentGuide, ArmComponentRig
    armGuide = ArmComponentGuide("arm")

    widget = BackdropInspector(component=armGuide)
    widget.show()
    sys.exit(app.exec_())

