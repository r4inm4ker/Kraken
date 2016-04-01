import FabricEngine.Core


def getClient():
    si = Dispatch("XSI.Application").Application
    contextID = si.fabricSplice('getClientContextID')
    if contextID == '':
        si.fabricSplice('constructClient')
        contextID = si.fabricSplice('getClientContextID')

    # Pull out the Splice client.
    return FabricEngine.Core.createClient({"contextID": contextID})