"""Kraken - objects.Attributes.Attribute module.

Classes:
Attribute - Base Attribute.

"""

from kraken.core.objects.scene_item import SceneItem


class Attribute(SceneItem):
    """Attribute object."""

    def __init__(self, name, value, parent=None):
        super(Attribute, self).__init__(name)
        self._value = value
        self._connection = None
        self._keyable = True
        self._lock = False
        self._animatable = True
        self._callback = None

        if parent is not None:
            if parent.getTypeName() != 'AttributeGroup':
                raise ValueError("Parent: " + parent.getName() +
                    " is not an Attribute Group!")

            parent.addAttribute(self)



    # ==============
    # Value Methods
    # ==============
    def getValue(self):
        """Returns the value of the attribute.

        Returns: Attribute Value.

        """

        return self._value


    def setValue(self, value):
        """Sets attribute value.

        Args:
            value: Value to set the attribute to.

        Returns:
            bool: True if successful.

        """

        self._value = value

        if self._callback is not None:
            self._callback(value)

        return True


    def setValueChangeCallback(self, callback):
        """Sets the value of the attribute.


        Args:
            callback: Value to set the attribute to.

        Returns:
            bool: True if successful.

        """

        self._callback = callback

        return True


    def getKeyable(self):
        """Returns the keyable state of the attribute.

        Args:
            argument (Type): description.

        Returns:
            bool: Keyable state of the attribute.

        """

        return self._keyable


    def setKeyable(self, value):
        """Sets the keyable state of the attribute.

        Args:
            value (bool): keyable state.

        Returns:
            bool: True if successful.

        """

        if type(value) is not bool:
            raise TypeError("Value is not of type 'bool'.")

        self._keyable = value

        return True


    def getLock(self):
        """Returns the Lock state of the attribute.

        Returns:
            bool: Lock state of the attribute.

        """

        return self._lock


    def setLock(self, value):
        """Sets the lock state of the attribute..

        Args:
            value (bool): lock state.

        Returns:
            bool: True if successful.

        """

        if type(value) is not bool:
            raise TypeError("Value is not of type 'bool'.")

        self._lock = value

        return True


    def setAnimatable(self, value):
        """Sets the animatable state of the attribute..

        Args:
            value (bool): animatable state.

        Returns:
            bool: True if successful.

        """

        if type(value) is not bool:
            raise TypeError("Value is not of type 'bool'.")

        self._animatable = value

        return True


    def getAnimatable(self):
        """Returns the animatable state of the attribute..

        Returns:
            bool: True if Animatable state of the attribute.

        """

        return self._animatable


    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Note:
            This method should be re-implemented in concrete attribute classes.

        Returns:
            RTVal: RTVal object for this attribute.

        Raises:
            NotImplemented: Must be implemented by concrete attribute classes.

        """

        raise NotImplemented("This method should be re-implemented in concrete attribute classes.")


    def validateValue(self, value):
        """Validates the incoming value is the correct type.

        Note:
            This method should be re-implemented in concrete attribute classes.

        Args:
            value: value to check the type of.

        Returns:
            bool: True if valid.

        Raises:
            NotImplemented: This method should be re-implemented in concrete attribute classes.

        """

        raise NotImplemented("This method should be re-implemented in concrete attribute classes.")


    # ===================
    # Connection Methods
    # ===================
    def isConnected(self):
        """Returns whether the attribute is connected or not.

        Returns:
            bool: True if is connected.

        """

        if self._connection is None:
            return False

        return True


    def getConnection(self):
        """Returns the connected attribute..

        Returns:
            Object: attribute driving this attribute.

        """

        return self._connection


    def connect(self, attribute):
        """Connects this attribute with another..

        Args:
            attribute (Object): attribute that will drive this one.

        Returns:
            bool: True if successful.

        """

        self._connection = attribute

        return True


    def disconnect(self):
        """Clears the connection of this attribute..

        Returns:
            bool: True if successful.

        """

        self._connection = None

        return True

    # ====================
    # Persistence Methods
    # ====================
    def jsonEncode(self, saver):
        """Encodes the object to a JSON structure.

        Args:
            saver (Object): saver object.

        Returns:
            Dict: A JSON structure containing the data for this SceneItem.

        """

        classHierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break
            classHierarchy.append(cls.__name__)

        jsonData = {
            '__typeHierarchy__': classHierarchy,
            'name': self.name,
            'value': saver.encodeValue(self._value),
            'parent': None
        }

        if self.getParent() is not None:
            jsonData['parent'] = self.getParent().getName()

        return jsonData


    def jsonDecode(self, loader, jsonData):
        """Returns the color of the object..

        Args:
            loader (Object): Loader object.
            jsonData (Dict): JSON object structure.

        Returns:
            bool: True if successful.

        """

        self.name =  jsonData['name']
        self._value =  loader.decodeValue(jsonData['value'])

        return True
