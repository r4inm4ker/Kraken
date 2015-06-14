import os

from PySide import QtGui, QtCore


class KrakenSplash(QtGui.QWidget):
    """Kraken Splash Screen Widget"""

    def __init__(self, parent=None):
        super(KrakenSplash, self).__init__(parent)

        self.setObjectName('KrakenSplash')
        self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)

        styleSheet = """

        QWidget#KrakenSplash {
            background-color: #151515;
            color: white;

            margin: 0px;
            padding: 0px;
        }

        QLabel {
            margin: 0px;
            padding: 0px;
        }

        QLabel#KrakenSplashStatus {
            background-color: #151515;
            color: white;

            padding: 5px;
        }

        """

        self.setStyleSheet(styleSheet)

        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        splashPixmap = QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', 'KrakenUI_Splash.png'))
        splaceLabel = QtGui.QLabel()
        splaceLabel.setMinimumWidth(700)
        splaceLabel.setMinimumHeight(350)
        splaceLabel.setPixmap(splashPixmap)

        messageLabel = QtGui.QLabel()
        messageLabel.setObjectName('KrakenSplashStatus')
        messageLabel.setText('Loading Extensions...')

        layout.addWidget(splaceLabel, 0)
        layout.addWidget(messageLabel, 0)
        layout.addStretch(1)