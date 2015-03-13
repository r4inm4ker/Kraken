"""KrakenSystem - objects.kraken_core module.

Classes:
KrakenSystem - Class for constructing the Fabric Engine Core client.

"""

import imp
from kraken.core.maths.math_object import MathObject
import FabricEngine.Core

class KrakenSystem(object):
    """Kraken base object type for any 3D object."""

    __instance = None

    def __init__(self):
        """Initializes the Kraken System object."""

        super(KrakenSystem, self).__init__()

        self.client = None

    def getCoreClient(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """
        if self.client == None:
            print "getCoreClient:"
            try:
                imp.find_module('cmds')
                host = 'Maya'
            except ImportError:
                try:
                    imp.find_module('sipyutils')
                    host = 'Softimage'
                except ImportError:
                    host = 'Python'
                    
            print "host:" + host
            if host == "Python":
                self.client = FabricEngine.Core.createClient()
                self.client.loadExtension('Math')

            elif host == "Maya":
                contextID = cmds.fabricSplice('getClientContextID')
                if contextID == '':
                    cmds.fabricSplice('constructClient')
                    contextID = cmds.fabricSplice('getClientContextID')

                # Pull out the Splice client.
                self.client = FabricEngine.Core.createClient({"contextID": contextID})

            elif host == "Softimage":
                from win32com.client.dynamic import Dispatch
                si = Dispatch("XSI.Application").Application
                contextID = si.fabricSplice('getClientContextID')
                if contextID == '':
                    si.fabricSplice('constructClient')
                    contextID = si.fabricSplice('getClientContextID')

                # Pull out the Splice client.
                self.client = FabricEngine.Core.createClient({"contextID": contextID})

        return self.client


    def constructRTVal(self, dataType, defaultValue=None):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """
        client = self.getCoreClient()

        klType = getattr(self.client.RT.types, dataType)
        if defaultValue is not None:
            if hasattr(defaultValue, '_rtval'):
                return defaultValue._rtval

            typeDesc = self.client.RT.getRegisteredTypes()[dataType]
            if 'members' in typeDesc:
                try:
                    value = klType.create()
                except:
                    value = klType()
                for i in range(0, len(typeDesc['members'])):
                    memberName = typeDesc['members'][i]['name']
                    memberType = typeDesc['members'][i]['type']
                    if memberName in defaultValue:
                        setattr(value, memberName, self.constructRTVal(memberType, getattr(defaultValue, memberName)))
                return value

            else:
                return klType(defaultValue)

        else:
            try:
                return klType.create()
            except:
                return klType()


    def rtVal(self, dataType, defaultValue=None):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.constructRTVal(dataType, defaultValue)


    @classmethod
    def getInstance(cls):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        if cls.__instance is None:
            cls.__instance = KrakenSystem()

        return cls.__instance


    @classmethod
    def inst(cls):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return cls.getInstance()