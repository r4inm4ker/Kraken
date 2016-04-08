import os
import sys
import json

from PySide import QtGui, QtCore

from kraken.ui import images_rc
from kraken.ui.kraken_menu import KrakenMenu
from kraken.ui.kraken_ui import KrakenUI
from kraken.ui.preferences import Preferences
from kraken.plugins.logger import OutputLog


class KrakenWindow(QtGui.QMainWindow):
    """Main Kraken Window that loads the UI."""

    def __init__(self, parent=None):
        super(KrakenWindow, self).__init__(parent)
        self.setObjectName('KrakenMainWindow')
        self.setWindowTitle('Kraken Editor')
        self.setWindowIcon(QtGui.QIcon(':/images/Kraken_Icon.png'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Set system output to write to output log object
        self.outputLog = OutputLog()
        sys.stdout = self.outputLog

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

        # Setup Status Bar
        statusBar = self.statusBar()
        self.outputLogButton = QtGui.QPushButton('Log', self)
        self.outputLogButton.setObjectName('outputLog_button')
        statusBar.insertPermanentWidget(0, self.outputLogButton)

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

        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)

        self.statusBar().showMessage('Ready', 2000)

        self.setGeometry(250, 150, 800, 475)
        self.center()

        self.readSettings()


    def createConnections(self):
        self.outputLogButton.clicked.connect(self.showOutputLog)
        self.krakenMenu.newAction.triggered.connect(self.krakenUI.graphViewWidget.newRigPreset)
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

            self.statusBar().showMessage('Closing')

        self.writeSettings()

    def showOutputLog(self):
        outputDialog = OutputLogDialog(self)
        outputDialog.show()
        outputDialog.setText(self.outputLog.getLog())
        outputDialog.textWidget.moveCursor(QtGui.QTextCursor.End)


class OutputLogDialog(QtGui.QDialog):
    """Output Dialog"""

    def __init__(self, parent=None):
        super(OutputLogDialog, self).__init__(parent)
        self.setObjectName('outputLog')
        self.resize(700, 300)
        self.setWindowTitle('Kraken Output Log')

        self.createLayout()
        self.createConnections()


    def createLayout(self):
        """Sets up the layout for the dialog."""

        self.textWidget = QtGui.QTextEdit()
        self.textWidget.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textWidget.setReadOnly(True)
        self.textWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.outputLogLayout = QtGui.QVBoxLayout(self)
        self.outputLogLayout.addWidget(self.textWidget)

        self.setLayout(self.outputLogLayout)


    def createConnections(self):
        """Connects widgets to methods or other signals."""

        self.textWidget.customContextMenuRequested.connect(self.createContextMenu)


    def setText(self, text):
        """Sets the text of the text widget."""

        self.textWidget.setText(text)


    # =============
    # Context Menu
    # =============
    def createContextMenu(self):
        self.contextMenu = QtGui.QMenu(self)
        selectAllAction = self.contextMenu.addAction("Select All")
        copyAction = self.contextMenu.addAction("Copy")
        self.contextMenu.addSeparator()
        clearAction = self.contextMenu.addAction("Clear")

        selectAllAction.triggered.connect(self.contextSelectAll)
        copyAction.triggered.connect(self.contextCopy)
        clearAction.triggered.connect(self.contextClear)

        self.contextMenu.exec_(QtGui.QCursor.pos())

    def contextSelectAll(self):
        self.textWidget.selectAll()

    def contextCopy(self):
        self.textWidget.copy()

    def contextClear(self):
        outputLog = self.parent().outputLog
        outputLog.clear()
        self.textWidget.clear()



def createSplash(app):
    """Creates a splash screen object to show while the Window is loading.

    Return:
    SplashScreen object.

    """

    splashPixmap = QtGui.QPixmap(':/images/KrakenUI_Splash.png')

    splash = QtGui.QSplashScreen(splashPixmap)
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
