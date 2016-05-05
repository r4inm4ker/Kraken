
from PySide import QtGui, QtCore

from kraken.log import getLogger

logger = getLogger('kraken')


class KrakenStatusBar(QtGui.QStatusBar):
    """Custom status bar widget for Kraken."""

    def __init__(self, parent=None):
        super(KrakenStatusBar, self).__init__(parent)
        self.setObjectName('krakenStatusBar')

        for handler in logger.handlers:
            if type(handler).__name__ == 'WidgetHandler':
                handler.addWidget(self)

        self.createLayout()

    def createLayout(self):
        self.outputLogButton = QtGui.QPushButton('Log', self)
        self.outputLogButton.setObjectName('outputLog_button')
        self.insertPermanentWidget(0, self.outputLogButton)

    def showMessage(self, message, timeout=0):
        super(KrakenStatusBar, self).showMessage(message, timeout)

    def write(self, msg, level):

        messageConfig = {
            'DEBUG': {
                'color': '#B4EEB4',
                'timeout': 3500
            },
            'INFO': {
                'color': '#FFFFFF',
                'timeout': 3500
            },
            'INFORM': {
                'color': '#009900',
                'timeout': 3500
            },
            'WARNING': {
                'color': '#D89614',
                'timeout': 3500
            },
            'ERROR': {
                'color': '#CC0000',
                'timeout': 0
            },
            'CRITICAL': {
                'color': '#CC0000',
                'timeout': 0
            }
        }

        timeOut = messageConfig[level]['timeout']

        # Remove current labels
        currentLabels = self.findChildren(QtGui.QLabel)
        for label in currentLabels:
            self.removeWidget(label)

        if level == "INFO":
            self.showMessage(msg, timeOut)
        else:
            lines = msg.split("\n")
            if len(lines) > 0:
                msg = lines[0][:120]
            else:
                msg = msg[:120]

            messageLabel = QtGui.QLabel(' ' + msg)
            messageLabel.setStyleSheet("QLabel { border-radius: 3px; background-color: " + messageConfig[level]['color'] + "}")

            def addMessage():
                self.clearMessage()
                self.currentMessage = messageLabel
                self.addWidget(messageLabel, 1)
                self.repaint()
                if timeOut > 0.0:
                    timer.start()

            def endMessage():
                timer.stop()
                self.removeWidget(messageLabel)
                self.repaint()
                self.showMessage('Ready', 2000)

            if timeOut > 0.0:
                timer = QtCore.QTimer()
                timer.setInterval(timeOut)
                timer.timeout.connect(endMessage)

            addMessage()
