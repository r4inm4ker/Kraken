
from PySide import QtGui, QtCore


class KColorWidget(QtGui.QLabel):
    """Custom Label widget to display color settings."""

    clicked = QtCore.Signal(bool)
    colorChanged = QtCore.Signal(QtGui.QColor)

    def __init__(self, parent, color):
        super(KColorWidget, self).__init__(parent)
        self.installEventFilter(self)
        self._color = QtGui.QColor(color)

        self.pixmap = QtGui.QPixmap(12, 12)
        self.pixmap.fill(self._color)

        self.setProperty('colorLabel', True)
        self.setFixedSize(24, 24)
        self.setScaledContents(True)
        self.setPixmap(self.pixmap)

        self.createConnections()

    def createConnections(self):
        self.clicked.connect(self.openColorDialog)
        self.colorChanged.connect(self.changeColor)

    def eventFilter(self, object, event):
        if event.type()== QtCore.QEvent.Enter:
            self.setCursor(QtCore.Qt.PointingHandCursor)
            return True

        if event.type()== QtCore.QEvent.Leave:
            self.setCursor(QtCore.Qt.ArrowCursor)
            return True

        if event.type()== QtCore.QEvent.MouseButtonPress:
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            return True

        if event.type()== QtCore.QEvent.MouseButtonRelease:
            self.setCursor(QtCore.Qt.PointingHandCursor)
            self.clicked.emit(True)
            return True

        return False


    def openColorDialog(self):

        colorDialog = QtGui.QColorDialog()
        colorDialog.setOption(QtGui.QColorDialog.DontUseNativeDialog, True)
        newColor = colorDialog.getColor(self._color, self)
        if newColor.isValid():
            self._color = newColor
            self.colorChanged.emit(newColor)

    def changeColor(self, color):
        self.pixmap.fill(color)
        self.setPixmap(self.pixmap)