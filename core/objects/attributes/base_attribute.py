"""Kraken - objects.Attributes.BaseAttribute module.

Classes:
BaseAttribute - Base Attribute.

"""

class BaseAttribute(object):
    """Base Attribute object."""

    __kType__ = "Attribute"

    def __init__(self, name, value):
        super(BaseAttribute, self).__init__()
        self.name = name
        self.value = value
        self.parent = None


    # =============
    # Name Methods
    # =============
    def setName(self, name):
        """Sets the name of the attribute group.

        Arguments:
        name -- Sting, name of the attribute group.

        Return:
        True if successful.

        """

        self.name = name

        return True


    def getName(self):
        """Returns the name of the attribute.

        Return:
        String of the name of the attribute.

        """

        return self.name


    # ==============
    # Value Methods
    # ==============
    def getValue(self):
        """Returns the value of the attribute.

        Return:
        Value of the attribute.

        """

        return self.value


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        self.value = value

        return True


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the paret of this attribute.

        Return:
        Parent object of this attribute.

        """

        return self.parent


    def setParent(self, parent):
        """Sets the paret of this attribute.

        Arguments:
        parent -- Object, parent object of this attribute.

        Return:
        True if successful.

        """

        self.parent = parent

        return True


    # ==============
    # kType Methods
    # ==============
    def getKType(self):
        """Returns the kType of this object.

        Return:
        True if successful.

        """

        return self.__kType__



    # ================
    # Persistence Methods
    # ================

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
            'value': saver.encodeValue(self.value),
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
        self.value =  loader.decodeValue(jsonData['value'])
        self.parent =  loader.getParentItem()

        return True
