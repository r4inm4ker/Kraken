from rigging.dcc.si.utils import *

from PySide import QtGui, QtCore

import kraken
from kraken.ui import kraken_ui
reload(kraken_ui)
from kraken.ui.kraken_ui import KrakenUI

import SIQt
SIQt.initialize()

class KrakenMainWindow( QtGui.QMainWindow):
    def __init__(self, parent):
        super(KrakenMainWindow, self).__init__(parent)
        self.setWindowTitle('Kraken Editor')
        self.setCentralWidget(KrakenUI())
        self.setAutoFillBackground(True)

        self.setStyleSheet("background-color: #151515;")


sianchor = Application.getQtSoftimageAnchor()
sianchor = SIQt.wrapinstance( long(sianchor), QtGui.QWidget )
dialog = KrakenMainWindow(sianchor)
dialog.show()