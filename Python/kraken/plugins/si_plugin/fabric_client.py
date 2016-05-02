import FabricEngine.Core

from kraken.log.utils import fabricCallback
from kraken.plugins.si_plugin.utils import *


def getClient():
    contextID = si.fabricSplice('getClientContextID')
    if contextID == '':
        si.fabricSplice('constructClient')
        contextID = si.fabricSplice('getClientContextID')

    options = {
        'contextID': contextID,
        'reportCallback': fabricCallback,
        'guarded': True
    }

    client = FabricEngine.Core.createClient(options)

    return client
