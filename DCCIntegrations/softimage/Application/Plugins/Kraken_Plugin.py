# Kraken_Plugin

import win32com.client
from win32com.client import constants

from win32com.client import constants
from multiprocessing import Pool

import Qt
Qt.initialize()
from Qt.QtGui import QMainWindow
from Qt.QtGui import QWidget
from PySide import QtWebKit
from PySide.QtCore import QUrl


import kraken.ui.kraken_ui
reload(kraken.ui.kraken_ui)
from kraken.ui.kraken_ui import KrakenUI
from kraken.ui.kraken_splash import KrakenSplash

si = Application
log = si.LogMessage


def XSILoadPlugin(in_reg):
    in_reg.Author = 'Eric Thivierge & Phil Taylor'
    in_reg.Name = 'Kraken_Plugin'
    in_reg.Major = 1
    in_reg.Minor = 0

    in_reg.RegisterMenu(constants.siMenuMainTopLevelID, "Kraken", False, False)
    in_reg.RegisterCommand('OpenKrakenEditor', 'OpenKrakenEditor')

    return True

def XSIUnloadPlugin(in_reg):
    log(in_reg.Name + ' has been unloaded.', constants.siVerbose)

    return True

def Kraken_Init( in_ctxt ):

    menu = in_ctxt.source;
    menu.AddCallbackItem( "Open UI", "OpenKrakenEditor")
    menu.AddSeparatorItem();
    menu.AddCallbackItem( "Help", "OpenKrakenHelp" )

# =========
# Commands
# =========


class KrakenMainWindow(QMainWindow):
    def __init__(self, parent):
        super(KrakenMainWindow, self).__init__(parent)
        self.setWindowTitle('Kraken Editor')
        self.setCentralWidget(KrakenUI(showSplash=False))
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #151515;")


class KrakenSplashWindow(QMainWindow):
    def __init__(self, parent):
        super(KrakenSplashWindow, self).__init__(parent)
        self.setWindowTitle('Kraken Splash')
        self.setCentralWidget(KrakenSplash())
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #151515;")


def OpenKrakenEditor( in_ctxt=None ):

    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance( long(sianchor), QWidget )
    
    splash = KrakenSplashWindow(parent=sianchor)
    splash.show()

    window = KrakenMainWindow(parent=sianchor)
    window.show()

    splash.hide()

    return True


def OpenKrakenEditor_Init( in_ctxt ):
    cmd = in_ctxt.Source
    cmd.Description = 'Opens the Kraken Editor'
    cmd.SetFlag(constants.siCannotBeUsedInBatch, True)
    cmd.ReturnValue = True

    return True


def OpenKrakenEditor_Execute(  ):

    OpenKrakenEditor()

    return True


class KrakenHelpWindow(QMainWindow):
    def __init__(self, parent):
        super(KrakenHelpWindow, self).__init__(parent)
        self.setWindowTitle('Kraken Help')

        view = QtWebKit.QWebView(self)
        view.load(QUrl("http://fabric-engine.github.io/Kraken/"))

        self.setCentralWidget(view)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #151515;")


def OpenKrakenHelp( in_ctxt ):
    oMenuItem = in_ctxt.source;
    
    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance( long(sianchor), QWidget )
    window = KrakenHelpWindow(parent=sianchor)
    window.show()


