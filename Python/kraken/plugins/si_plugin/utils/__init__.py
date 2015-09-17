"""Kraken SI - Utils module."""

from win32com.client import constants
from win32com.client.dynamic import Dispatch


si = Dispatch("XSI.Application").Application
sel = si.Selection
log = si.LogMessage

XSIMath = Dispatch("XSI.Math")
XSIUtils = Dispatch("XSI.Utils")
XSIUIToolkit = Dispatch("XSI.UIToolkit")
XSIFactory = Dispatch("XSI.Factory")


def getCollection():
    """Returns an XSICollection object."""

    newCollection = Dispatch("XSI.Collection")
    newCollection.Unique = True

    return newCollection


def lockObjXfo(dccSceneItem):
    """Locks the dccSceneItem's transform parameters.

    Args:
        dccSceneItem (object): DCC object to lock transform parameters on.

    Returns:
        bool: True if successful.

    """

    localXfoParams = ['posx', 'posy', 'posz', 'rotx', 'roty', 'rotz', 'sclx', 'scly', 'sclz']
    for eachParam in localXfoParams:
        param = dccSceneItem.Parameters(eachParam)
        if param.IsLocked():
            continue

        param.SetLock(constants.siLockLevelManipulation)

    si.SetKeyableAttributes(dccSceneItem, "kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty,kine.local.ori.euler.rotz,kine.local.sc.sclx,kine.local.sc.scly,kine.local.sc.sclz", constants.siKeyableAttributeClear)

    return True