"""Kraken - maths.math_object module.

Classes:
MathObject -- A base class for all math types.
"""

import json
import FabricEngine.Core


class MathObject(object):
    """MathObject object. A base class for all math types"""


    def __init__(self):
        """Initialize the base math object."""
        super(MathObject, self).__init__()
        self._rtval = None


    def getRTVal(self):
        """Returns the internal RTVal object owned by the math object.

        Return:
        RTVal

        """

        return self._rtval


    def setRTVal(self, rtval):
        """Sets the internal RTVal object owned by the math object.

        Arguments:
        rtval -- rtval, the internal RTVal object owned by the math object.

        """

        self._rtval = rtval


    def jsonEncode(self):
        """Encodes object to JSON.

        Return:
        JSON string.

        """

        d = {
             "__mathObjectClass__": self.__class__.__name__,
            }

        public_attrs = (name for name in dir(self) if not name.startswith('_') and not callable(getattr(self,name)) and name)
        for name in public_attrs:
            item = getattr(self, name)
            if isinstance(item, MathObject):
                d[name] = item.jsonEncode()
            else:
                d[name] = item

        return d


    def jsonDecode(self, jsonData, decodeFn):
        """Encodes object to JSON.

        Arguments:
        jsonData -- dict, the JSON data used to populate the math object.
        decodeFn -- decodeFn, the decodeFn that can construct the math objects.

        Return:
        True of the decode was successful

        """

        if jsonData["__mathObjectClass__"] != self.__class__.__name__:
            raise Exception("Error in jsonDecode. Json data specifies a \
                            different class:" + jsonData["__class__"] + "!==" +
                            self.__class__.__name__)

        for key, value in jsonData.iteritems():
            if key == '__mathObjectClass__': continue
            if type(value) is dict:
                setattr(self, key, decodeFn(value))
            else:
                setattr(self, key, value)

        return True


