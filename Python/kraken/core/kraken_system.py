"""KrakenSystem - objects.kraken_core module.

Classes:
KrakenSystem - Class for constructing the Fabric Engine Core client.

"""

import json
from kraken.core.maths.math_object import MathObject
import FabricEngine.Core


class KrakenSystem(object):
    """The KrakenSystem is a singleton object used to provide an interface with the FabricEngine Core and RTVal system."""

    __instance = None

    def __init__(self):
        """Initializes the Kraken System object."""

        super(KrakenSystem, self).__init__()
        self.client = FabricEngine.Core.createClient()
        self.client.loadExtension('Math')


    def getCoreClient(self):
        """Returns the Fabric Engine Core Client owned by the KrakenSystem

        Return:
        The Fabric Engine Core Client

        """

        return self.client


    def constructRTVal(self, dataType, defaultValue=None):
        """Constructs a new RTVal using the given name and optional devault value.

        Arguments:
        dataType -- The name of the data type to construct.
        defaultValue -- The default value to use to initialize the RTVal

        Return:
        The constructed RTval.

        """

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
        """Constructs a new RTVal using the given name and optional devault value.

        Arguments:
        dataType -- The name of the data type to construct.
        defaultValue -- The default value to use to initialize the RTVal

        Return:
        The constructed RTval.

        """

        return self.constructRTVal(dataType, defaultValue)


    def isRTVal(self, value):
        """Returns true if the given value is an RTVal.

        Arguments:
        value -- value to test.

        Return:
        True if successful.

        """

        return str(type(value)) == "<type 'PyRTValObject'>"


    def getRTValTypeName(self, rtval):
        """Returns the name of the type, handling extracting the name from KL RTVals.

        Arguments:
        rtval -- the rtval to extract the name from.

        Return:
        True if successful.

        """
        if ks.isRTVal(rtval): 
            return json.loads(rtval.type("Type").jsonDesc("String"))['name']
        else:
            return "None"

    @classmethod
    def getInstance(cls):
        """This class method returns the singleton instance for the KrakenSystem

        Return:
        The singleton instance.

        """

        if cls.__instance is None:
            cls.__instance = KrakenSystem()

        return cls.__instance

ks = KrakenSystem.getInstance()