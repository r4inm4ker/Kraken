import json
from PySide import QtCore, QtGui
from parameter import Parameter
from AttributeWidgetImpl import AttributeWidget

class Image2DWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):

        super(Image2DWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self._grid = QtGui.QGridLayout()
        self._grid.setContentsMargins(0, 0, 0, 0)

        self.__value = self._invokeGetter()

        # format
        formatLabelWidget = QtGui.QLabel("format", self)
        formatLabelWidget.setMinimumWidth(20)
        self._formatWidget = QtGui.QLineEdit(self)
        self._formatWidget.setText(self.__value.pixelFormat)
        self._formatWidget.setReadOnly(True)

        self._grid.addWidget(formatLabelWidget, 0, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(self._formatWidget, 0, 1)

        # width
        widthLabelWidget = QtGui.QLabel("width", self)
        widthLabelWidget.setMinimumWidth(20)
        self._widthWidget = QtGui.QSpinBox(self)
        self._widthWidget.setMinimum(0)
        self._widthWidget.setMaximum(9999999)
        self._widthWidget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self._widthWidget.setValue(self.__value.width)
        self._widthWidget.setReadOnly(True)

        self._grid.addWidget(widthLabelWidget, 1, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(self._widthWidget, 1, 1)

        # height
        heightLabelWidget = QtGui.QLabel("height", self)
        heightLabelWidget.setMinimumWidth(20)
        self._heightWidget = QtGui.QSpinBox(self)
        self._heightWidget.setMinimum(0)
        self._heightWidget.setMaximum(9999999)
        self._heightWidget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self._heightWidget.setValue(self.__value.height)
        self._heightWidget.setReadOnly(True)

        self._grid.addWidget(heightLabelWidget, 2, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(self._heightWidget, 2, 1)

        self._thumbnailSize = 40
        self.tumbnailWidget = QtGui.QLabel()
        self.tumbnailWidget.setBackgroundRole(QtGui.QPalette.Base)
        self.tumbnailWidget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.tumbnailWidget.setScaledContents(True)

        self._updateThumbnail()

        self.setLayout(self._grid)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)

        # self.updateWidgetValue()

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

                self.tumbnailWidget.setPixmap(QtGui.QPixmap.fromImage(self._qimage))


        self._grid.addWidget(self.tumbnailWidget, 3, 0, 2, 2)
        self._grid.setRowStretch(4, 2)
    def getWidgetValue(self):
        return self.__value

    def setWidgetValue(self, value):
        self.__value = value
        self._formatWidget.setText(self.__value.pixelFormat)
        self._widthWidget.setValue(self.__value.width)
        self._heightWidget.setValue(self.__value.height)
        self._updateThumbnail()


    def unregisterNotificationListener(self):
        """
        When the widget is being removed from the inspector,
        this method must be called to unregister the event handlers
        """
        super(Image2DWidget, self).unregisterNotificationListener()

    @classmethod
    def canDisplay(cls, attribute):
        return attribute.getDataType() == 'Image2D'


Image2DWidget.registerPortWidget()