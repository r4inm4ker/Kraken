import sys, json

from PySide import QtGui

import kraken.ui
from kraken.ui.kraken_ui import KrakenUI

from maya import cmds
# import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

try:
  # Maya 2013 with custom pyside build
  import PySide.shiboken as shiboken
except:
  # Maya 2014 and higher
  import shiboken



# Command
class OpenKrakenEditorCommand(OpenMayaMPx.MPxCommand):
  def __init__(self):
    OpenMayaMPx.MPxCommand.__init__(self)

  # Invoked when the command is run.
  def doIt(self,argList):
    parent = OpenMayaUI.MQtUtil.mainWindow()
    parent = shiboken.wrapInstance(long(parent), QtGui.QWidget)
    dfgApp = KrakenUI(parent)

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
    SingletonHost.getController().redo()
    return 0

  def undoIt(self):
    SingletonHost.getController().undo()
    return 0

  @staticmethod
  def creator():
    return OpenMayaMPx.asMPxPtr( KrakenUndoableCmd() )


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

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
  mplugin = OpenMayaMPx.MFnPlugin(mobject)

  try:
    mplugin.deregisterCommand( 'openKrakenEditor' )
  except:
    sys.stderr.write( 'Failed to unregister command: openKrakenEditor' )


  try:
    mplugin.deregisterCommand( 'krakenUndoableCmd' )
  except:
    sys.stderr.write( 'Failed to unregister command: krakenUndoableCmd' )
