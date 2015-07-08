import os
import sys
import json

from PySide import QtGui, QtCore

import types

import kraken
import kraken.ui.kraken_window
from kraken.ui.kraken_window import KrakenWindow
from kraken.ui.kraken_window import createSplash

import maya
from maya import cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

import pymel.core as pm

try:
  # Maya 2013 with custom pyside build
  import PySide.shiboken as shiboken
except:
  # Maya 2014 and higher
  import shiboken


def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtGui.QWidget)


# Command
class OpenKrakenEditorCommand(OpenMayaMPx.MPxCommand):
  def __init__(self):
    OpenMayaMPx.MPxCommand.__init__(self)

  # Invoked when the command is run.
  def doIt(self,argList):

    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    splash = createSplash(app)

    window = KrakenWindow(parent=getMayaWindow())
    window.show()

    splash.finish(window)

  # Creator
  @staticmethod
  def creator():
    return OpenMayaMPx.asMPxPtr( OpenKrakenEditorCommand() )


class KrakenUndoableCmd(OpenMayaMPx.MPxCommand):

  def __init__(self):
    OpenMayaMPx.MPxCommand.__init__(self)

  def isUndoable(self):
    return True

  def doIt(self, argList):
    return 0

  def redoIt(self):
    print "TODO: provide undoable command here."
    return 0

  def undoIt(self):
    print "TODO: provide undoable command here."
    return 0

  @staticmethod
  def creator():
    return OpenMayaMPx.asMPxPtr( KrakenUndoableCmd() )


def setupKrakenMenu():
    mainWindow = maya.mel.eval('$tmpVar=$gMainWindow')

    menuName = 'Kraken'
    lMenus = pm.window(mainWindow, q=True, ma=True)
    if menuName in lMenus:
        return

    krakenMenu = pm.menu(menuName, parent=mainWindow, label=menuName, to=True)

    # menuEditor = pm.menuItem("KrakenEditorMenuItem", parent=krakenMenu, label="Open Kraken Editor", to=True, subMenu=True)

    pm.menuItem(parent=krakenMenu, label="Open Kraken Editor", c="from maya import cmds; cmds.openKrakenEditor()")
    pm.menuItem(parent=krakenMenu, divider=True)
    pm.menuItem(parent=krakenMenu, label="Help", c="import webbrowser; webbrowser.open_new_tab('http://fabric-engine.github.io/Kraken')")


# Initialize the script plug-in
def initializePlugin(mobject):
  mplugin = OpenMayaMPx.MFnPlugin(mobject)

  try:
    mplugin.registerCommand( 'openKrakenEditor', OpenKrakenEditorCommand.creator )
  except:
    sys.stderr.write( 'Failed to register DFG commands:openKrakenEditor' )
    raise

  try:
    mplugin.registerCommand( 'krakenUndoableCmd', KrakenUndoableCmd.creator )
  except:
    sys.stderr.write( 'Failed to register DFG commands:krakenUndoableCmd' )
    raise


  setupKrakenMenu();

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
  mplugin = OpenMayaMPx.MFnPlugin(mobject)

  unloadMenu();

  try:
    mplugin.deregisterCommand( 'openKrakenEditor' )
  except:
    sys.stderr.write( 'Failed to unregister command: openKrakenEditor' )


  try:
    mplugin.deregisterCommand( 'krakenUndoableCmd' )
  except:
    sys.stderr.write( 'Failed to unregister command: krakenUndoableCmd' )
