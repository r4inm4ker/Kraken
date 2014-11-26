"""KrakenCore - objects.kraken_core module.

Classes:
KrakenCore - Class for constructing the Fabric Engine Core client. 

"""
from kraken.core.maths.math_object import MathObject

import FabricEngine.Core

class KrakenCore(object):
    """Kraken base object type for any 3D object."""

    __instance = None

    def __init__(self):
        super(KrakenCore, self).__init__()
        self.client = FabricEngine.Core.createClient()
        self.client.loadExtension('Math')

    def getCoreClient(self):
        return self.client


    def constructRTVal(self, dataType, defaultValue=None):

        klType = getattr(self.client.RT.types, dataType)
        if defaultValue is not None:
            if hasattr(defaultValue, 'rtval'):
                return defaultValue.rtval
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
        return self.constructRTVal(dataType, defaultValue)

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = KrakenCore()
        return cls.__instance

    @classmethod
    def inst(cls):
        return cls.getInstance()

