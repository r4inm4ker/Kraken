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

        return str(json.loads(self._rtval.type("Type").jsonDesc("String"))['name'])


    def getTypeName(self, value=None):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        if value is None:
            value = self._rtval
            isRTVal = True
        else:
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
            
        public_attrs = (name for name in dir(self) if not name.startswith('_') and not callable(getattr(self,name)) and name)
        for name in public_attrs:
            item = getattr(self, name)
            if isinstance(item, MathObject):
                d[name] = item.jsonEncode()
            else:
                d[name] = item

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