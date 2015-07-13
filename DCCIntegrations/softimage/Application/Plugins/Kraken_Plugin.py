# Kraken_Plugin

import win32com.client
from win32com.client import constants
import os
import inspect

from win32com.client import constants
from multiprocessing import Pool

import webbrowser

import Qt
Qt.initialize()
from Qt.QtGui import QMainWindow
from Qt.QtGui import QWidget

from PySide import QtWebKit
from PySide import QtGui, QtCore


import kraken.ui.kraken_window
reload(kraken.ui.kraken_window)
from kraken.ui.kraken_window import KrakenWindow
from kraken.ui.kraken_window import createSplash

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
def OpenKrakenEditor_Init(in_ctxt):
    cmd = in_ctxt.Source
    cmd.Description = 'Opens the Kraken Editor'
    cmd.SetFlag(constants.siCannotBeUsedInBatch, True)
    cmd.ReturnValue = True

    return True


def OpenKrakenEditor_Execute():

    OpenKrakenEditor()

    return True


# ==========
# Callbacks
# ==========

def OpenKrakenEditor(in_ctxt):

    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance(long(sianchor), QWidget)

    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    for widget in app.topLevelWidgets():
            if widget.objectName() == 'KrakenMainWindow':
                widget.showNormal()

                return

    splash = createSplash(app)
    splash.show()

    window = KrakenWindow(parent=sianchor)
    window.show()

    splash.finish(window)

    return True


def OpenKrakenHelp(in_ctxt):
    menuItem = in_ctxt.source

    webbrowser.open_new_tab('http://fabric-engine.github.io/Kraken')