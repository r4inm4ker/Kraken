import FabricEngine.Core

from kraken.plugins.maya_plugin.utils import *


def getClient():
    contextID = cmds.fabricSplice('getClientContextID')
    if contextID == '':
        cmds.fabricSplice('constructClient')
        contextID = cmds.fabricSplice('getClientContextID')

    return FabricEngine.Core.createClient({"contextID": contextID})