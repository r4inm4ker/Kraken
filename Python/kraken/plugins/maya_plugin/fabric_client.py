import FabricEngine.Core

from kraken.log.utils import fabricCallback
from kraken.plugins.maya_plugin.utils import *


def getClient():
    contextID = cmds.fabricSplice('getClientContextID')
    if contextID == '':
        cmds.fabricSplice('constructClient')
        contextID = cmds.fabricSplice('getClientContextID')

    options = {
        'contextID': contextID,
        'reportCallback': fabricCallback,
        'guarded': True
    }

    client = FabricEngine.Core.createClient(options)

    return client
