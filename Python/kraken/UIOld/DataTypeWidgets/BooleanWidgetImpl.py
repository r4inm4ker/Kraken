from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget


class BooleanWidget(AttributeWidget):

  def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
    super(BooleanWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

    hbox = QtGui.QHBoxLayout()

    self._widget = QtGui.QCheckBox(self)
    hbox.addWidget(self._widget, 1)

    hbox.addStretch(0)
    hbox.setContentsMargins(0, 0, 0, 0)
    self.setLayout(hbox)
    self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

    self.updateWidgetValue()

    if self.isEditable():
      def __stateChanged(value):
        self._invokeSetter()
      self._widget.stateChanged.connect(__stateChanged)
    else:
      self._widget.setEnabled(False)


  def getWidgetValue(self):
    return self._widget.checkState() == QtCore.Qt.Checked

  def setWidgetValue(self, value):
    if value:
      self._widget.setCheckState(QtCore.Qt.Checked)
    else:
      self._widget.setCheckState(QtCore.Qt.Unchecked)

  @classmethod
  def canDisplay(cls, attribute):
    return attribute.getDataType() == 'Boolean'

BooleanWidget.registerPortWidget()

