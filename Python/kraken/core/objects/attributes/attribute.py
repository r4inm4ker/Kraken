"""Kraken - objects.Attributes.Attribute module.

Classes:
Attribute - Base Attribute.

"""
from kraken.core.objects.base_item import BaseItem

class Attribute(BaseItem):
    """Attribute object."""

    def __init__(self, name, value, parent=None, keyable=None, lock=None):
        super(Attribute, self).__init__(name, parent)
        self._value = value
        self._connection = None
        self._keyable = None
        self._lock = None

        if keyable is not None:
            self.setKeyable(keyable)

        if lock is not None:
            self.setLock(lock)


    # ==============
    # Value Methods
    # ==============
    def getValue(self):
        """Returns the value of the attribute.

        Return:
        Value of the attribute.

        """

        return self._value


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        self._value = value

        return True


    def getKeyable(self):
        """Returns the keyable state of the attribute.

        Return:
        Keyable state of the attribute.

        """

        return self._keyable


    def setKeyable(self, value):
        """Sets the keyable state of the attribute.

        Arguments:
        value -- Bool, keyable state.

        Return:
        True if successful.

        """

        if type(value) is bool:
            self._keyable = value
        else:
            raise TypeError("Value is not of type 'bool'.")

        return True


    def getLock(self):
            """Returns the Lock state of the attribute.

            Return:
            Lock state of the attribute.

            """

            return self._lock


    def setLock(self, value):
        """Sets the lock state of the attribute.

        Arguments:
        value -- Bool, lock state.

        Return:
        True if successful.

        """

        if type(value) is bool:
            self._lock = value
        else:
            raise TypeError("Value is not of type 'bool'.")

        return True


    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Return:
        RTVal

        """
        raise Exception("getRTVal must be implemented by concrete attribute classes")

    # ===================
    # Connection Methods
    # ===================
    def isConnected(self):
        """Returns whether the attribute is connected or not.

        Return:
        True if successful.

        """

        if self._connection is None:
            return False

        return True


    def getConnection(self):
        """Returns the connected attribute.

        Return:
        Object, attribute driving this attribute.

        """

        return self._connection


    def connect(self, attribute):
        """Connects this attribute with another.

        Arguments:
        attribute -- Object, attribute that will drive this one.

        Return:
        True if successful.

        """

        self._connection = attribute

        return True


    def disconnect(self):
        """Clears the connection of this attribute.

        Return:
        True if successful.

        """

        self._connection = None

        return True

    # ====================
    # Persistence Methods
    # ====================
    def jsonEncode(self, saver):
        """Sets the color of this object.

        Arguments:

        Return:
        A JSON structure containing the data for this SceneItem.

        """

        classHierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break;
            classHierarchy.append(cls.__name__)

        jsonData = {
            '__typeHierarchy__': classHierarchy,
            'name': self.name,
            'value': saver.encodeValue(self._value),
            'parent': None
        }

        if self.parent is not None:
            jsonData['parent'] = self.parent.getName()

        return jsonData


    def jsonDecode(self, loader, jsonData):
        """Returns the color of the object.

        Return:
        True if decoding was successful

        """
        self.name =  jsonData['name']
        self._value =  loader.decodeValue(jsonData['value'])

        return True
