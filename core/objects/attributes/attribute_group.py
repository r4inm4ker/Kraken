"""Kraken - objects.Attributes.attribute_group module.

Classes:
AttributeGroup - Attribute Group.

"""

class AttributeGroup(object):
    """Attribute Group that attributes belong to."""

    __kType__ = "AttributeGroup"

    def __init__(self, name, parent = None):
        super(AttributeGroup, self).__init__()
        self.name = name
        self.attributes = []
        self.parent = parent


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


    # ===============
    # Parent Methods
    # ===============
    def setParent(self, parent):
        """Sets the paret of this attribute.

        Arguments:
        parent -- Object, parent object of this attribute.

        Return:
        True if successful.

        """

        self.parent = parent

        return True


    def getParent(self):
        """Returns the paret of this attribute.

        Return:
        Parent object of this attribute.

        """

        return self.parent


    # ==============
    # kType Methods
    # ==============
    def getKType(self):
        """Returns the kType of this object.

        Return:
        True if successful.

        """

        return self.__kType__


    # ==================
    # Attribute Methods
    # ==================
    def checkAttributeIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, attribute index to check.

        Return:
        True if successful.

        """

        if index > len(self.attributes):
            raise IndexError("'" + str(index) + "' is out of the range of 'attributes' array.")

        return True


    def addAttribute(self, attribute):
        """Adds an attribute to this object.

        Arguments:
        attribute -- Object, attribute object to add to this object.

        Return:
        True if successful.

        """

        if attribute.getName() in [x.getName() for x in self.attributes]:
            raise IndexError("Child with " + attribute.getName() + " already exists as a attribute.")

        self.attributes.append(attribute)
        attribute.setParent(self)

        return True


    def removeAttributeByIndex(self, index):
        """Removes attribute at specified index.

        Arguments:
        index -- Integer, index of attribute to remove.

        Return:
        True if successful.

        """

        if self.checkAttributeIndex(index) is not True:
            return False

        del self.attributes[index]

        return True


    def removeAttributeByName(self, name):
        """Removes the attribute with the specified name.

        Arguments:
        name -- String, name of the attribute to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachAttribute in enumerate(self.attributes):
            if eachAttribute.getName() == name:
                removeIndex = i

        if removeIndex is None:
            return False

        self.removeAttributeByIndex(removeIndex)

        return True


    def getNumAttributes(self):
        """Returns the number of attributes as an integer.

        Return:
        Integer of the number of attributes on this object.

        """

        return len(self.attributes)


    def getAttributeByIndex(self, index):
        """Returns the attribute at the specified index.

        Arguments:
        index -- Integer, index of the attribute to return.

        Return:
        Attribute at the specified index.
        False if not a valid index.

        """

        if self.checkAttributeIndex(index) is not True:
            return False

        return self.attributes[index]


    def getAttributeByName(self, name):
        """Return the attribute with the specified name.

        Arguments:
        name -- String, name of the attribute to return.

        Return:
        Attribute with the specified name.
        None if not found.

        """

        for eachAttribute in self.attributes:
            if eachAttribute.getName() == name:
                return eachAttribute

        return None




    # ================
    # Persistence Methods
    # ================

    def jsonEncode(self, saver):
        """Returns the data for this object encoded as a JSON hierarchy.

        Arguments:

        Return:
        A JSON structure containing the data for this SceneItem.

        """

        jsonData = {
            '__kType__': self.__kType__,
            'name': self.name,
            'parent': self.parent.getName(),
            'attributes': []
        }
        for attr in self.attributes:
            jsonData['attributes'].append(attr.jsonEncode(saver))

        return jsonData


    def jsonDecode(self, loader, jsonData):
        """Returns the color of the object.

        Return:
        the decoded object.

        """

        self.parent =  loader.resolveSceneItem(jsonData['parent'])

        for attr in jsonData['attributeGroups']:
            self.addAttributeGroup(loader.construct(attr))

        return self.color
