import json
from PySide import QtCore, QtGui

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor

class Image2DEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):

        super(Image2DEditor, self).__init__(valueController, parent=parent)

        self._grid = QtGui.QGridLayout()
        self._grid.setContentsMargins(0, 0, 0, 0)

        self.__value = self._invokeGetter()

        # format
        formatLabelEditor = QtGui.QLabel("format", self)
        formatLabelEditor.setMinimumWidth(20)
        self._formatEditor = QtGui.QLineEdit(self)
        self._formatEditor.setText(self.__value.pixelFormat)
        self._formatEditor.setReadOnly(True)

        self._grid.addWidget(formatLabelEditor, 0, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(self._formatEditor, 0, 1)

        # width
        widthLabelEditor = QtGui.QLabel("width", self)
        widthLabelEditor.setMinimumWidth(20)
        self._widthEditor = QtGui.QSpinBox(self)
        self._widthEditor.setMinimum(0)
        self._widthEditor.setMaximum(9999999)
        self._widthEditor.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self._widthEditor.setValue(self.__value.width)
        self._widthEditor.setReadOnly(True)

        self._grid.addWidget(widthLabelEditor, 1, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(self._widthEditor, 1, 1)

        # height
        heightLabelEditor = QtGui.QLabel("height", self)
        heightLabelEditor.setMinimumWidth(20)
        self._heightEditor = QtGui.QSpinBox(self)
        self._heightEditor.setMinimum(0)
        self._heightEditor.setMaximum(9999999)
        self._heightEditor.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self._heightEditor.setValue(self.__value.height)
        self._heightEditor.setReadOnly(True)

        self._grid.addWidget(heightLabelEditor, 2, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(self._heightEditor, 2, 1)

        self._thumbnailSize = 40
        self.tumbnailEditor = QtGui.QLabel()
        self.tumbnailEditor.setBackgroundRole(QtGui.QPalette.Base)
        self.tumbnailEditor.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.tumbnailEditor.setScaledContents(True)

        self._updateThumbnail()

        self.setLayout(self._grid)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)

        # self.updateEditorValue()


    def _updateThumbnail(self):
        if self.__value.width > 0 and self.__value.height > 0:
                self._qimage = QtGui.QImage(self._thumbnailSize, self._thumbnailSize, QtGui.QImage.Format_RGB32)
                for i in range(self._thumbnailSize):
                    for j in range(self._thumbnailSize):
                        if self.__value.pixelFormat == "RGB":
                                pixelColor = self.__value.sampleRGB("""RGB""", float(i)/(self._thumbnailSize - 1.0), float(j)/(self._thumbnailSize - 1.0))
                        elif self.__value.pixelFormat == "RGBA":
                                pixelColor = self.__value.sampleRGBA("""RGBA""", float(i)/(self._thumbnailSize - 1.0), float(j)/(self._thumbnailSize - 1.0))
                        pixelValue = QtGui.qRgb(pixelColor.r, pixelColor.g, pixelColor.b)
                        self._qimage.setPixel(i, j, pixelValue)

                self.tumbnailEditor.setPixmap(QtGui.QPixmap.fromImage(self._qimage))


        self._grid.addWidget(self.tumbnailEditor, 3, 0, 2, 2)
        self._grid.setRowStretch(4, 2)


    def getEditorValue(self):
        return self.__value


    def setEditorValue(self, value):
        self.__value = value
        self._formatEditor.setText(self.__value.pixelFormat)
        self._widthEditor.setValue(self.__value.width)
        self._heightEditor.setValue(self.__value.height)
        self._updateThumbnail()


    @classmethod
    def canDisplay(cls, valueController):
        return valueController.getDataType() == 'Image2D'


EditorFactory.registerEditorClass(Image2DEditor)