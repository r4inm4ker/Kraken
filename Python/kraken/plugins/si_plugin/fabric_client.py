import FabricEngine.Core

from win32com.client.dynamic import Dispatch


def getClient():
    si = Dispatch("XSI.Application").Application
    contextID = si.fabricSplice('getClientContextID')
    if contextID == '':
        si.fabricSplice('constructClient')
        contextID = si.fabricSplice('getClientContextID')

    # Pull out the Splice client.
    return FabricEngine.Core.createClient({"contextID": contextID})