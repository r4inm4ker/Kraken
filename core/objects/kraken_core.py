"""KrakenSaver - objects.kraken_saver module.

Classes:
KrakenSaver - Helper class for saving Kraken rigs to JSON representations .

"""
from kraken.core.maths.math_object import MathObject

import FabricEngine.Core

class KrakenCore(object):
    """Kraken base object type for any 3D object."""

    __instance = None

    def __init__(self):
        super(KrakenSaver, self).__init__()
        this.client = FabricEngine.Core.createClient()
        self.client.loadExtension('Math')

    def getCoreClient(self):
        return client


    def constructRTVal(self, dataType, defaultValue=None):

        klType = getattr(self.client.RT.types, dataType)
        if defaultValue is not None:
            if hasattr(defaultValue, 'rtval'):
                return defaultValue.rtVal
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
                        setattr(value, memberName, self.constructRTVal(memberType, getattr(defaultValue, memberName))
                return value
            else:
                return klType(defaultValue)
        else:
            try:
                return klType.create()
            except:
                return klType()

    def rtVal(self):
        return self.constructRTVal()

    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = KrakenCore()
        return cls.__instance

    def inst(cls):
        return cls.getInstance()

