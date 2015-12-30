
#
# Copyright 2015 Horde Software Inc. All rights reserved.
#

#pylint: disable-msg=W0613,R0201
import os
import sys

from PySide import QtGui, QtCore
from widget_factory import EditorFactory

class BaseInspector(QtGui.QWidget):
    """A widget providing the ability to nest """

    def __init__(self, objectname='inspector', parent=None):

        # constructors of base classes
        super(BaseInspector, self).__init__(parent)

        # Note: we must set the object name before constructing the layout.
        self.setObjectName(objectname)

        # layout
        self.mainLayout = QtGui.QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.paramsFrame = QtGui.QScrollArea(self)
        self.paramsFrame.setWidgetResizable(True)
        self.paramsFrame.setEnabled(True)
        self.paramsFrame.setSizePolicy(sizePolicy)
        # self.paramsFrame.setFrameStyle(QtGui.QFrame.NoFrame)
        self.paramsFrame.setFrameStyle(QtGui.QFrame.StyledPanel)

        self.paramsGroup = QtGui.QWidget(self.paramsFrame)
        self.paramsFrame.setWidget(self.paramsGroup)

        self.paramsLayout = QtGui.QGridLayout()
        self.paramsLayout.setAlignment(QtCore.Qt.AlignTop)

        self.paramsGroup.setLayout(self.paramsLayout)

        self.mainLayout.addWidget(self.paramsFrame)
        self.widgets = []
        self.controllers = []
        self.gridRow = 0


    def addButton(self, button, columnSpan=1):
        if columnSpan==1:
            self.paramsLayout.addWidget(button, self.gridRow, 1)
            self.gridRow += 1
        else:
            self.paramsLayout.addWidget(button, self.gridRow+1, 0, 1, columnSpan)
            self.gridRow += 2

        self.widgets.append(button)


    def addEditor(self, name, widget, columnSpan=1):

        label = None
        widgetColumn = 0
        if name != None:
            label = QtGui.QLabel(name, self.paramsGroup)
            label.setContentsMargins(0, 5, 0, 0)
            self.paramsLayout.addWidget(label, self.gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self.gridRow += 1
            widgetColumn = 1

        if widget is not None:
            if columnSpan==1:
                self.paramsLayout.addWidget(widget, self.gridRow-1, widgetColumn)
            else:
                self.paramsLayout.addWidget(widget, self.gridRow, 0, 1, columnSpan)
                self.gridRow += 1

            self.widgets.append(widget)

    def addControllerEditor(self, valueController, columnSpan=None):
        widget = EditorFactory.constructEditor(valueController, parent=self)
        if columnSpan is None:
            columnSpan = widget.getColumnSpan()
        self.addEditor(valueController.getName(), widget, columnSpan)

        # we hold a reference to the controller here so it doesn't get deleted.
        # Usefull for testing only.
        self.controllers.append(valueController)

        return widget

    def addSeparator(self, name=None):

        separatorEditor = QtGui.QFrame(self.paramsGroup)
        separatorEditor.setFrameShape(QtGui.QFrame.HLine)
        separatorEditor.setObjectName('separatorFrame')
        if name is not None:
            labelEditor = QtGui.QLabel(name, self.paramsGroup)
            labelEditor.setObjectName('separatorLabel')

            self.paramsLayout.addWidget(labelEditor, self.gridRow, 0)
            self.paramsLayout.addWidget(separatorEditor, self.gridRow, 1, QtCore.Qt.AlignBottom)
            self.gridRow += 1
        else:
            self.paramsLayout.addWidget(separatorEditor, self.gridRow, 0, 1, 2)
            self.gridRow += 1


    def addStretch(self, stretch):
        self.paramsLayout.addWidget(QtGui.QWidget(self), self.gridRow, 0, 1, 2)
        self.paramsLayout.setRowStretch(self.gridRow, stretch)
        self.gridRow += 1


    def clear(self):
        while self.paramsLayout.count():
            self.paramsLayout.takeAt(0).widget().deleteLater()
        self.widgets = []
        self.gridRow = 0


