import json
from PySide import QtCore, QtGui

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor
from ..core.value_controller import MemberController

class NestedEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):

        super(NestedEditor, self).__init__(valueController, parent=parent)

        self._value = self._invokeGetter()
        self._labels = {}
        self._editors = {}
        self._gridRow = 0
        self._grid = QtGui.QGridLayout()
        self._grid.setColumnStretch(1, 1)

        if self._valueController.hasOption('displayGroupbox'):
            groupBox = QtGui.QGroupBox(self._valueController.getDataType())
            groupBox.setLayout(self._grid)
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(groupBox)
            self.setLayout(vbox)
        else:
            self._grid.setContentsMargins(0, 0, 0, 0)
            self.setLayout(self._grid)


    def addValueEditor(self, name, widget):

        # widget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        label = QtGui.QLabel(name, self)
        # label.setMaximumWidth(200)
        # label.setContentsMargins(0, 5, 0, 0)
        # label.setMinimumWidth(60)
        # label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        # label.setAlignment(QtCore.Qt.AlignRight)
        # label.adjustSize()

        rowSpan = widget.getRowSpan()
        columnSpan = widget.getColumnSpan()
        # if columnSpan==1:
        self._grid.addWidget(label, self._gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(widget, self._gridRow, 1)#, QtCore.Qt.AlignLeft)
        self._gridRow += 1
        # else:
        #     self._grid.addWidget(label, self._gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        #     self._grid.addWidget(widget, self._gridRow+1, 0, rowSpan, columnSpan)
        #     self._gridRow += 2

        self._labels[name] = label
        self._editors[name] = widget


    def addMemberEditor(self, memberName, memberType):
        memberController = MemberController(memberName, memberType, owner=self._value, editable=self.isEditable())
        # memberController = self._valueController.getMemberController(memberName)
        widget = EditorFactory.constructEditor(memberController, parent=self)
        if widget is None:
            return
        self.addValueEditor(memberName, widget)


    def getEditorValue(self):
        return self._value


    def setEditorValue(self, value):
        raise Exception("This method must be implimented by the derived widget:" + self.__class__.__name__)


    def clear(self):
        """
        When the widget is being removed from the inspector,
        this method must be called to unregister the event handlers
        """
        for label, widget in self._labels.iteritems():
            widget.deleteLater()
        for label, widget in self._editors.iteritems():
            widget.deleteLater()


