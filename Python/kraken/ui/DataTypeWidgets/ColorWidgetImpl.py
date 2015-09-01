from PySide import QtGui
from AttributeWidgetImpl import AttributeWidget


class ColorWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(ColorWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        hbox = QtGui.QHBoxLayout()
        self._widgets = []

        self._qgraphcsScene = QtGui.QGraphicsScene(self)
        self._qgraphcsView = QtGui.QGraphicsView(self)
        self._qgraphcsView.setScene(self._qgraphcsScene)
        self._qgraphcsView.setFixedSize(100, 20)
        self._qgraphcsView.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        hbox.addWidget(self._qgraphcsView, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.updateWidgetValue()

    def getWidgetValue(self):
        client = self.getController().getClient()
        scalarKLType = getattr(client.RT.types, 'Scalar')
        colorKLType = getattr(client.RT.types, 'Color')
        return colorKLType(
            scalarKLType(self.__color.redF()),
            scalarKLType(self.__color.greenF()),
            scalarKLType(self.__color.blueF())
            )

    def setWidgetValue(self, value):
        self.__color = QtGui.QColor(value.r*255, value.g*255, value.b*255)
        self._qgraphcsView.setBackgroundBrush(self.__color)
        self._qgraphcsView.update()

    def mousePressEvent(self, event):
        if self.isEditable():
            self.__backupColor = self.__color
            self.beginInteraction()
            dialog = QtGui.QColorDialog(self.__color, self)
            dialog.currentColorChanged.connect(self.__onColorChanged)
            dialog.accepted.connect(self.__onAccepted)
            dialog.rejected.connect(self.__onCanceled)
            dialog.setModal(True)
            dialog.show()

    def __onColorChanged(self, qcolor):
        self.__color = QtGui.QColor(qcolor.redF()*255, qcolor.greenF()*255, qcolor.blueF()*255)
        self._qgraphcsView.setBackgroundBrush(self.__color)
        self._invokeSetter()

    def __onAccepted(self):
        self.endInteraction()

    def __onCanceled(self):
        self.endInteraction()

        undoManager = UndoRedoManager.getCurrentUndoManager()
        if undoManager and undoManager.canUndo():
            undoManager.undo()
        else:
            self.__onColorChanged(self.__backupColor)

    @classmethod
    def canDisplay(cls, attribute):
        if attribute.getDataType() == 'Color':
            return True
        return False

ColorWidget.registerPortWidget()
