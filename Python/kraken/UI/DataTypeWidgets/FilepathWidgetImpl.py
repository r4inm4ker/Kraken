import os.path
from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget

class FilepathWidget(AttributeWidget):


    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(FilepathWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self._line = QtGui.QLineEdit(self)
        self._browse = QtGui.QPushButton(' ... ', self)

        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self._line)
        hbox.addWidget(self._browse)

        self.setLayout(hbox)

        self._saveFile = attribute.hasOption('WriteFile')
        if self._saveFile:
            self._options = attribute.getOption('WriteFile', {
                'Title': 'Choose file...',
                'Folder': '~',
                'Filter': '"All files(*.*)'
                })
        else:
            self._options = attribute.getOption('ReadFile', {
                'Title': 'Choose file...',
                'Folder': '~',
                'Filter': '"All files(*.*)'
                })

        if attribute.getPortType() == 'In':
            def localSetter(value):
                self._invokeSetter()
            self._line.textEdited.connect(localSetter)

        def __onBrowse():
            if self._saveFile:
                (filename, filter) = QtGui.QFileDialog.getSaveFileName(None, self.getName(), self._folder, self._options['Filter'])
            else:
                (filename, filter) = QtGui.QFileDialog.getOpenFileName(None, self.getName(), self._folder, self._options['Filter'])
            if filename is None or len(filename) == 0:
                return
            self.setWidgetValue(self._klType(filename))
            self._invokeSetter()

        self._browse.clicked.connect(__onBrowse)
        self.updateWidgetValue()

    def getWidgetValue(self):
        return self._klType(self._line.text())

    def setWidgetValue(self, value):
        self._line.setText(value)
        filename = self._line.text()
        if os.path.isdir(filename):
            self._folder = filename
        else:
            self._folder = os.path.split(filename)[0]


    @classmethod
    def canDisplay(cls, attribute):
        dataType = attribute.getDataType()
        return dataType == 'String' and (attribute.hasOption('ReadFile') or attribute.hasOption('WriteFile'))

FilepathWidget.registerPortWidget()
