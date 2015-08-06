
#
# Copyright 2010-2015
#


import json
from PySide import QtGui, QtCore


class IndexSpinBox(QtGui.QSpinBox):
    def __init__(self, parent):
        super(IndexSpinBox, self).__init__(parent)

    def focusOutEvent(self, event):
        self.parent().close()


class EditIndexWidget(QtGui.QWidget):

    def __init__(self, componentInput, pos, parent):
        super(EditIndexWidget, self).__init__(parent)

        self.componentInput = componentInput
        self.setWindowTitle( "Edit " + self.componentInput.getName() + " Index" )
        self.setWindowFlags( QtCore.Qt.Window )

        # self.setObjectName('componentInspector') # TODO: Style me pretty...
        self.setFixedSize(150, 60)

        self.spinBoxWidget = IndexSpinBox(self)
        self.spinBoxWidget.setMinimum(0)
        self.spinBoxWidget.setValue(self.componentInput.getIndex())
        self.spinBoxWidget.valueChanged.connect(self.__setIndex)

        grid = QtGui.QVBoxLayout(self)
        grid.addWidget(self.spinBoxWidget, 0)

        self.move(pos)
        self.show()
        self.spinBoxWidget.setFocus()

    def __setIndex(self, index):
        self.componentInput.setIndex(index)


    def focusOutEvent(self, event):
        self.close()

