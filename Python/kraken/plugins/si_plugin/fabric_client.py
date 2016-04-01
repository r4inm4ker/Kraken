import FabricEngine.Core

from kraken.plugins.si_plugin.utils import *


def getClient():
    contextID = si.fabricSplice('getClientContextID')
    if contextID == '':
        si.fabricSplice('constructClient')
        contextID = si.fabricSplice('getClientContextID')

    return FabricEngine.Core.createClient({"contextID": contextID})