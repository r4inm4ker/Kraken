import os.path
from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor

class FilepathEditor(BaseValueEditor):


    def __init__(self, valueController, parent=None):
        super(FilepathEditor, self).__init__(valueController, parent=parent)

        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self._line = QtGui.QLineEdit(self)
        self._browse = QtGui.QPushButton(' ... ', self)

        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self._line)
        hbox.addWidget(self._browse)

        self.setLayout(hbox)
        self.__updateOptions()

        def localSetter(value):
            self._setValueToController()
        self._line.textEdited.connect(localSetter)

        def __onBrowse():
            if self._line.text() == '':
                initialDir = self._folder
            else:
                initialDir = os.path.join(self._folder, self._line.text())

            if self._saveFile:
                (filepath, filter) = QtGui.QFileDialog.getSaveFileName(None, caption=self._options['Title'], dir=initialDir, filter=self._options['Filter'])
            else:
                (filepath, filter) = QtGui.QFileDialog.getOpenFileName(None, caption=self._options['Title'], dir=initialDir, filter=self._options['Filter'])

            if filepath is None or len(filepath) == 0:
                return

            if self._folder != '':
                filepath = os.path.relpath(filepath, self._folder)

            self.setEditorValue(filepath)
            self._setValueToController()

        self._browse.clicked.connect(__onBrowse)
        valueController.optionChanged.connect(self.__updateOptions)

        self.updateEditorValue()
        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        self._line.setReadOnly( not editable )
        self._browse.setEnabled( editable )


    def __updateOptions(self, key=None):
        self._saveFile = self._valueController.hasOption('WriteFile')

        if self._saveFile:
            self._options = self._valueController.getOption('WriteFile', defaultValue={
                'Title': 'Choose file...',
                'RootFolder': '',
                'Filter': '"All files(*.*)'
                })
        else:
            self._options = self._valueController.getOption('ReadFile', defaultValue={
                'Title': 'Choose file...',
                'RootFolder': '',
                'Filter': '"All files(*.*)'
                })

        self._folder = self._options.get('RootFolder', '~')


    def getEditorValue(self):
        filepath = self._line.text()
        if self._folder != '':
            filepath = os.path.join(self._folder, filepath)
        if self._dataType == 'FilePath':
            FE.getInstance().types().FilePath.create(filepath)
        else:
            return filepath

    def setEditorValue(self, value):
        if isinstance(value, basestring):
            self._line.setText(value)
        else:
            self._line.setText(value.string('String'))


    @classmethod
    def canDisplay(cls, valueController):
        dataType = valueController.getDataType()
        if dataType == 'String':
            return (valueController.hasOption('ReadFile') or valueController.hasOption('WriteFile'))
        elif dataType == 'FilePath':
            return True


EditorFactory.registerEditorClass(FilepathEditor)
