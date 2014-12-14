"""Kraken - maths.math_object module.

Classes:
MathObject -- A base class for all math types.
"""

import FabricEngine.Core
import json


class MathObject(object):
    """MathObject object. A base class for all math types"""


    def __init__(self):
        """Initialize the base math object."""
        super(MathObject, self).__init__()


    def clientTypes(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        client = KC.getInstance().getCoreClient()

        return client.RT.types


    def typeName(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return str(json.loads(self.rtval.type("Type").jsonDesc("String"))['name'])


    def getTypeName(self, value=None):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        if value is None:
            value = self.rtval

        isRTVal = str(type(value)) == "<type 'PyRTValObject'>"
        if isRTVal:
            return json.loads(value.type("Type").jsonDesc("String"))['name']

        return str(type(value))


    def jsonEncode(self):
        """Encodes object to JSON.

        Return:
        JSON string.

        """
        d = {
                "__class__":self.__class__.__name__,
            }

        attrs = {}
        for eachItem in self.__dict__.items():
            if isinstance(eachItem[1], MathObject):
                attrs[eachItem[0]] = eachItem[1].jsonEncode()
            else:
                attrs[eachItem[0]] = eachItem[1]

        d.update(attrs)

        return d


    def jsonDecode(self, jsonData, loader):
        """Encodes object to JSON.

        Return:
        True of the decode was successful

        """

        if jsonData["__class__"] != self.__class__.__name__:
            raise Exception("Error in jsonDecode. Json data specifies a different class:" + jsonData["__class__"] + "!==" + self.__class__.__name__)

        for key, value in jsonData.iteritems():
            if key == '__class__': continue
            if type(value) is dict:
                setattr(self, key, loader.decodeValue(value))
            else:
                setattr(self, key, value)

        return True