from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget


class OptionWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(OptionWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        hbox = QtGui.QHBoxLayout()

        self._widget = QtGui.QLineEdit(self)
        hbox.addWidget(self._widget, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.updateWidgetValue()


        if self.isEditable():
            # we get lots of 'editingFinished' events,
            # so filter to only generate undos for important ones.

            client = self.getController().getClient()
            kLType = getattr(client.RT.types, 'String')
            self._value = kLType(self._widget.text())
            def invokeSetter():
                value = self._widget.text()
                if self._value != value:
                    self._value = kLType(value)
                    self._invokeSetter()
            self._widget.textChanged.connect(self._invokeSetter)

            def openContextMenu():
                contextMenu = QtGui.QMenu(self)

                def setRangeOption():
                    self._widget.setText("Range={ 'min': 0, 'max': 100 }")
                contextMenu.addAction("Slider Range").triggered.connect(setRangeOption)

                def setComboOption():
                    self._widget.setText("Combo=['X', 'Y', 'Z']")
                contextMenu.addAction("Combo Dropdown").triggered.connect(setComboOption)

                def setMultilineOption():
                    self._widget.setText("Multiline= { 'numLines': 5 }")
                contextMenu.addAction("Multiline String").triggered.connect(setMultilineOption)

                def setReadFileOption():
                    self._widget.setText("ReadFile={ 'Title': 'Choose file...', 'Folder': '~', 'Filter': 'All files(*.*)' }")
                contextMenu.addAction("Read File").triggered.connect(setReadFileOption)

                def setWriteFileOption():
                    self._widget.setText("WriteFile={ 'Title': 'Choose file...', 'Folder': '~', 'Filter': 'All files(*.*)' }")
                contextMenu.addAction("Write File").triggered.connect(setWriteFileOption)

                contextMenu.popup(presetOptionButton.mapToGlobal(QtCore.QPoint(0, 30)))
            presetOptionButton = QtGui.QPushButton('set', self)
            presetOptionButton.clicked.connect(openContextMenu)
            hbox.addWidget(presetOptionButton, 0)
        else:
            self._widget.setReadOnly(True)


    def getWidgetValue(self):
        client = self.getController().getClient()
        kLType = getattr(client.RT.types, 'String')
        return kLType(self._widget.text())

    def setWidgetValue(self, value):
        self._widget.setText(value)

    def getColumnSpan(self):
        """Returns the number of columns in the layout grid this widget takes up. Wide widgets can return values greater than 1 to modify thier alignment relative to the label."""
        return 2

    @classmethod
    def canDisplay(cls, attribute):
        if attribute.getDataType() == 'Option':
            return True
        return False



OptionWidget.registerPortWidget()

