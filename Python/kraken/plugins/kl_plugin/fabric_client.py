import FabricEngine.Core

from kraken.log.utils import fabricCallback

def getClient():

    options = {
        'contextID': contextID,
        'reportCallback': fabricCallback,
        'guarded': True
    }

    return FabricEngine.Core.createClient(options)