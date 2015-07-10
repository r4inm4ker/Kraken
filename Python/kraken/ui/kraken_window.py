import os
import sys
import inspect

from PySide import QtGui, QtCore

import kraken.ui.kraken_ui
reload(kraken.ui.kraken_ui)
from kraken.ui.kraken_menu import KrakenMenu
from kraken.ui.kraken_ui import KrakenUI


class KrakenWindow(QtGui.QMainWindow):
    """Main Kraken Window that loads the UI."""

    def __init__(self, parent=None):
        super(KrakenWindow, self).__init__(parent)
        self.setObjectName('KrakenMainWindow')
        self.setWindowTitle('Kraken Editor')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        cssPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'kraken_ui.css')

        with open(cssPath) as cssFile:
            styleData = cssFile.read()

        self.setStyleSheet(styleData)

        uiDir = os.path.dirname(inspect.getfile(KrakenUI))
        iconPath = os.path.join(uiDir, 'images', 'Kraken_Icon.png')
        self.setWindowIcon(QtGui.QIcon(iconPath))

        self.createLayout()
        self.createConnections()


    def createLayout(self):

        mainWidget = QtGui.QWidget()

        # Main Layout
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.kraken_ui = KrakenUI(self)
        self.krakenMenu = KrakenMenu(self)
        self.kraken_ui.graphViewWidget.setRigName('MyRig')
        self.krakenMenu.updateRigNameLabel()

        self.mainLayout.addWidget(self.krakenMenu)
        self.mainLayout.addWidget(self.kraken_ui, 1)

        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)

        self.statusBar().showMessage('Ready')


    def createConnections(self):
        self.krakenMenu.newAction.triggered.connect(self.kraken_ui.graphViewWidget.newRigPreset)

        self.kraken_ui.graphViewWidget.rigNameChanged.connect(self.krakenMenu.updateRigNameLabel)


    # =======
    # Events
    # =======
    def closeUI(self):

        self.statusBar().showMessage('Closing')
        self.close()


def createSplash(app):
    """Creates a splash screen object to show while the Window is loading.

    Return:
    SplashScreen object.

    """

    uiDir = os.path.dirname(inspect.getfile(KrakenUI))
    splashPixmap = QtGui.QPixmap()
    splashImgPath = os.path.join(uiDir, 'images', 'KrakenUI_Splash.png')
    splashPixmap.load(splashImgPath)

    splash = QtGui.QSplashScreen(splashPixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splashPixmap.mask())
    splash.showMessage("Loading Extensions...",
                       QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft,
                       QtCore.Qt.white)

    splash.show()

    app.processEvents()

    return splash


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    splash = createSplash(app)

    window = KrakenWindow()
    window.show()

    splash.finish(window)

    sys.exit(app.exec_())
