"""Kraken SI - Utils module."""

from win32com.client import constants
from win32com.client.dynamic import Dispatch

from kraken.plugins.si_plugin import logger as siLogger


si = Dispatch("XSI.Application").Application
sel = si.Selection
log = si.LogMessage
logger = siLogger.getLogger("siLogger")

XSIMath = Dispatch("XSI.Math")
XSIUtils = Dispatch("XSI.Utils")
XSIUIToolkit = Dispatch("XSI.UIToolkit")
XSIFactory = Dispatch("XSI.Factory")


def getCollection():
    """Returns an XSICollection object."""

    return Dispatch("XSI.Collection")


def lockObjXfo(dccSceneItem):

    localXfoParams = ['posx', 'posy', 'posz', 'rotx', 'roty', 'rotz', 'sclx', 'scly', 'sclz']
    for eachParam in localXfoParams:
        param = dccSceneItem.Parameters(eachParam)
        if param.IsLocked():
            continue

        param.SetLock(constants.siLockLevelManipulation)

    si.SetKeyableAttributes(dccSceneItem, "kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty,kine.local.ori.euler.rotz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz", constants.siKeyableAttributeClear)