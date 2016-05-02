"""Kraken Main Window and Launcher."""

import argparse
import logging
import os
import sys
import json

from PySide import QtGui, QtCore

from kraken.log import getLogger
from kraken.ui import images_rc
from kraken.ui.kraken_menu import KrakenMenu
from kraken.ui.kraken_ui import KrakenUI
from kraken.ui.preferences import Preferences
from kraken.ui.kraken_output_log import OutputLogDialog
from kraken.ui.kraken_statusbar import KrakenStatusBar
from kraken.ui.kraken_splash import KrakenSplash

logger = getLogger('kraken')


class KrakenWindow(QtGui.QMainWindow):
    """Main Kraken Window that loads the UI."""

    def __init__(self, parent=None):
        super(KrakenWindow, self).__init__(parent)
        self.setObjectName('KrakenMainWindow')
        self.setWindowTitle('Kraken Editor')
        self.setWindowIcon(QtGui.QIcon(':/images/Kraken_Icon.png'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        QtCore.QCoreApplication.setOrganizationName("Kraken")
        QtCore.QCoreApplication.setApplicationName("Kraken Editor")
        self.settings = QtCore.QSettings("Kraken", "Kraken Editor")
        self.preferences = Preferences()

        cssPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'kraken_ui.css')

        styleData = ''
        with open(cssPath) as cssFile:
            styleData = cssFile.read()

        self.setStyleSheet(styleData)

        self.createLayout()
        self.createConnections()


    def createLayout(self):

        self.outputDialog = OutputLogDialog(self)

        # Setup Status Bar
        self.statusBar = KrakenStatusBar(self)

        mainWidget = QtGui.QWidget()

        # Main Layout
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.krakenUI = KrakenUI(self)
        self.krakenMenu = KrakenMenu(self)
        self.krakenUI.graphViewWidget.setGuideRigName('MyRig')
        self.krakenMenu.updateRigNameLabel()

        self.mainLayout.addWidget(self.krakenMenu)
        self.mainLayout.addWidget(self.krakenUI, 1)
        self.mainLayout.addWidget(self.statusBar)

        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)

        self.statusBar.showMessage('Ready', 2000)

        self.setGeometry(250, 150, 800, 475)
        self.center()

        self.readSettings()


    def createConnections(self):
        self.statusBar.outputLogButton.clicked.connect(self.showOutputLog)
        self.krakenUI.graphViewWidget.rigLoaded.connect(self.krakenMenu.buildRecentFilesMenu)
        self.krakenUI.graphViewWidget.rigNameChanged.connect(self.krakenMenu.updateRigNameLabel)


    def getKrakenUI(self):
        return self.krakenUI


    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    # =========
    # Settings
    # =========
    def getSettings(self):
        return self.settings

    def writeSettings(self):
        self.settings.beginGroup('MainWindow')
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos', self.pos())
        self.settings.setValue('preferences', json.dumps(self.preferences.getPreferences()))
        self.settings.endGroup()
        self.krakenMenu.writeSettings(self.settings)
        self.krakenUI.writeSettings(self.settings)

    def readSettings(self):
        self.settings.beginGroup('MainWindow')
        self.resize(self.settings.value('size', self.size()))
        self.move(self.settings.value('pos', self.pos()))
        self.preferences.loadPreferences(json.loads(self.settings.value('preferences', '{}')))
        self.settings.endGroup()

        self.krakenMenu.readSettings(self.settings)
        self.krakenUI.readSettings(self.settings)

    # =======
    # Events
    # =======
    def closeEvent(self, event):

        msgBox = QtGui.QMessageBox(self)
        msgBox.setObjectName('SaveMessageBox')
        msgBox.setWindowTitle("Kraken Editor")
        msgBox.setText("You are closing Kraken.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Save)

        ret = msgBox.exec_()

        if ret == QtGui.QMessageBox.Cancel:
            event.ignore()
            return

        elif ret == QtGui.QMessageBox.Save:
            self.kraken_ui.graphViewWidget.saveRigPreset()

            self.statusBar.showMessage('Closing')

        self.writeSettings()

        # Clear widget handler of any widgets otherwise references to deleted
        # widgets remain.
        for handler in logger.handlers:
            if type(handler).__name__ == 'WidgetHandler':
                handler.clearWidgets()

    def showOutputLog(self):

        self.outputDialog.show()
        self.outputDialog.textWidget.moveCursor(QtGui.QTextCursor.End)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    splash = KrakenSplash(app)
    splash.show()

    window = KrakenWindow()
    window.show()

    splash.finish(window)

    sys.exit(app.exec_())
