import os
import sys
import webbrowser

from PySide import QtGui, QtCore
from kraken.core.kraken_system import KrakenSystem
from kraken.core.configs.config import Config


class KrakenMenu(QtGui.QWidget):
    """Kraken Menu Widget"""

    def __init__(self, parent=None):
        super(KrakenMenu, self).__init__(parent)
        self.setObjectName('menuWidget')

        self.createLayout()
        self.createConnections()

    def createLayout(self):

        self.menuLayout = QtGui.QHBoxLayout()
        self.menuLayout.setContentsMargins(0, 0, 0, 0)
        self.menuLayout.setSpacing(0)

        # Menu
        self.menuBar = QtGui.QMenuBar()

        # File Menu
        self.fileMenu = self.menuBar.addMenu('&File')
        self.newAction = self.fileMenu.addAction('&New')
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setObjectName("newAction")

        self.saveAction = self.fileMenu.addAction('&Save')
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setObjectName("saveAction")

        self.saveAsAction = self.fileMenu.addAction('&Save As')
        self.saveAsAction.setShortcut('Ctrl+Shift+S')
        self.saveAsAction.setObjectName("saveAsAction")

        self.loadAction = self.fileMenu.addAction('&Load')
        self.loadAction.setShortcut('Ctrl+L')
        self.loadAction.setObjectName("loadAction")

        self.fileMenu.addSeparator()

        self.closeAction = self.fileMenu.addAction('&Close')
        self.closeAction.setShortcut('Ctrl+W')
        self.closeAction.setObjectName("closeAction")

        # Edit Menu
        self.editMenu = self.menuBar.addMenu('&Edit')
        self.copyAction = self.editMenu.addAction('&Copy')
        self.copyAction.setShortcut('Ctrl+C')
        self.pasteAction = self.editMenu.addAction('&Paste')
        self.pasteAction.setShortcut('Ctrl+V')
        self.pasteConnectedAction = self.editMenu.addAction('Paste Connected')
        self.pasteConnectedAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_V))
        self.editMenu.addSeparator()
        self.pasteMirroredAction = self.editMenu.addAction('Paste Mirrored')
        self.pasteMirroredConnectedAction = self.editMenu.addAction('Paste Mirrored Connected')
        self.editMenu.addSeparator()
        self.editRigNameAction = self.editMenu.addAction('&Rig Name')
        self.editRigNameAction.setObjectName("editRigNameAction")

        # Build Menu
        self.buildMenu = self.menuBar.addMenu('&Build')
        self.buildGuideAction = self.buildMenu.addAction('Build &Guide')
        self.buildGuideAction.setShortcut('Ctrl+G')
        self.buildGuideAction.setObjectName("buildGuideAction")

        self.buildRigAction = self.buildMenu.addAction('Build &Rig')
        self.buildRigAction.setShortcut('Ctrl+B')
        self.buildRigAction.setObjectName("buildRigAction")

        # Panel Menu
        self.panelsMenu = self.menuBar.addMenu('&Panels')
        self.compLibAction = self.panelsMenu.addAction('Component &Library')
        self.compLibAction.setShortcut('Ctrl+Tab')

        # Help Menu
        self.helpMenu = self.menuBar.addMenu('&Help')
        self.onlineHelpAction = self.helpMenu.addAction('Online &Help')
        self.onlineHelpAction.setShortcut('Ctrl+H')

        # Logo
        logoWidget = QtGui.QLabel()
        logoWidget.setObjectName('logoWidget')
        logoWidget.setMinimumHeight(20)
        logoWidget.setMinimumWidth(110)

        logoPixmap = QtGui.QPixmap(':/images/KrakenUI_Logo.png')
        logoWidget.setPixmap(logoPixmap)

        # Config Widget
        self.configsParent = QtGui.QFrame(self)
        self.configsParent.setObjectName('configParent')
        self.configsParent.setFrameStyle(QtGui.QFrame.NoFrame)
        self.configsParent.setMinimumWidth(160)

        self.configsLayout = QtGui.QVBoxLayout()
        self.configsLayout.setContentsMargins(0, 0, 0, 0)
        self.configsLayout.setSpacing(0)

        self.configsWidget = QtGui.QComboBox()
        self.configsWidget.setAutoFillBackground(True)
        self.configsWidget.setObjectName('configWidget')
        self.configsWidget.setMinimumWidth(160)
        self.configsWidget.addItem('Default Config')

        self.configsLayout.addWidget(self.configsWidget)
        self.configsParent.setLayout(self.configsLayout)

        configs = KrakenSystem.getInstance().getConfigClassNames()
        for config in configs:
            self.configsWidget.addItem(config.split('.')[-1])

        self.rigNameLabel = RigNameLabel('Rig Name:')

        # Add Widgets
        self.menuLayout.addWidget(logoWidget, 0)
        self.menuLayout.addWidget(self.menuBar, 3)
        self.menuLayout.addWidget(self.configsParent, 0)
        self.menuLayout.addWidget(self.rigNameLabel, 0)

        self.setLayout(self.menuLayout)


    def openHelp(self):
        webbrowser.open_new_tab('http://fabric-engine.github.io/Kraken')


    def createConnections(self):

        krakenUIWidget = self.parentWidget().getKrakenUI()
        graphViewWidget = krakenUIWidget.graphViewWidget

        # File Menu Connections
        self.newAction.triggered.connect(graphViewWidget.newRigPreset)
        self.newAction.triggered.connect(self.updateRigNameLabel)

        self.saveAction.triggered.connect(graphViewWidget.saveRigPreset)
        self.saveAsAction.triggered.connect(graphViewWidget.saveAsRigPreset)
        self.loadAction.triggered.connect(graphViewWidget.loadRigPreset)
        self.loadAction.triggered.connect(self.updateRigNameLabel)
        self.closeAction.triggered.connect(self.window().close)

        # Edit Menu Connections
        self.copyAction.triggered.connect(graphViewWidget.copy)
        self.pasteAction.triggered.connect(graphViewWidget.pasteUnconnected)
        self.pasteConnectedAction.triggered.connect(graphViewWidget.paste)
        self.pasteMirroredAction.triggered.connect(graphViewWidget.pasteMirrored)
        self.pasteMirroredConnectedAction.triggered.connect(graphViewWidget.pasteMirroredConnected)
        self.editRigNameAction.triggered.connect(graphViewWidget.editRigName)

        # Build Menu Connections
        self.buildGuideAction.triggered.connect(graphViewWidget.buildGuideRig)
        self.buildRigAction.triggered.connect(graphViewWidget.buildRig)

        # Panels Menu Connections
        self.compLibAction.triggered.connect(krakenUIWidget.resizeSplitter)

        # Help Menu Connections
        self.onlineHelpAction.triggered.connect(self.openHelp)

        self.configsWidget.currentIndexChanged.connect(self.setCurrentConfig)

        # Rig Name Label
        self.rigNameLabel.clicked.connect(graphViewWidget.editRigName)


    # =======
    # Events
    # =======
    def updateRigNameLabel(self):
        krakenUIWidget = self.window().getKrakenUI()

        graphViewWidget = krakenUIWidget.graphViewWidget
        newRigName = graphViewWidget.guideRig.getName()

        self.rigNameLabel.setText('Rig Name: ' + newRigName)


    def setCurrentConfig(self, index = None):
        if index is None:
            index = self.configsWidget.currentIndex()
        else:
            self.configsWidget.setCurrentIndex(index)

        if index == 0:
            Config.makeCurrent()
        else:
            ks = KrakenSystem.getInstance()
            configs = ks.getConfigClassNames()
            configClass = ks.getConfigClass(configs[index-1])
            configClass.makeCurrent()


    def writeSettings(self, settings):
        settings.beginGroup("KrakenMenu")
        settings.setValue("currentConfig", self.configsWidget.currentIndex())
        settings.endGroup()


    def readSettings(self, settings):
        settings.beginGroup("KrakenMenu")
        if settings.contains('currentConfig'):
            currentConfig = int(settings.value("currentConfig", 0))
            self.setCurrentConfig(currentConfig)
        settings.endGroup()



class RigNameLabel(QtGui.QLabel):

    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(RigNameLabel, self).__init__(parent)
        self.setObjectName('rigNameLabel')
        self.setToolTip('Double Click to Edit')

    def mouseDoubleClickEvent(self, event):
        self.clicked.emit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    KrakenMenu()

    sys.exit(app.exec_())