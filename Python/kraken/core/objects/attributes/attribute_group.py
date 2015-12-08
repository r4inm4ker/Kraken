"""Kraken - objects.Attributes.attribute_group module.

Classes:
AttributeGroup - Attribute Group.

"""

from kraken.core.objects.scene_item import SceneItem

# TODO: Attribute group has children in the form of attributes, but doesn's support the object 3d interface
# that provides the getChild* methods. We should clean this up so AttributeGroup supports all the child methods
# A current bug is that an attribute group can have multiple children with the same name.
class AttributeGroup(SceneItem):
    """Attribute Group that attributes belong to."""

    def __init__(self, name, parent=None):
        super(AttributeGroup, self).__init__(name)
        self._attributes = []

        if parent is not None:
            if 'Object3D' not in parent.getTypeHierarchyNames():
                raise ValueError("Parent: " + parent.getName() +
                    " is not of type 'Object3D'!")

            parent.addAttributeGroup(self)


    # ==================
    # Attribute Methods
    # ==================
    def _checkAttributeIndex(self, index):
        """Checks the supplied index is valid.

        Args:
            index (int): attribute index to check.

        Returns:
            bool: True if valid.

        """

        if index > len(self._attributes):
            raise IndexError("'" + str(index) + "' is out of the range of 'attributes' array.")

        return True


    def addAttribute(self, attribute):
        """Adds an attribute to this object..

        Args:
            attribute (Object): attribute object to add to this object.

        Returns:
            bool: True if successful.

        """

        if attribute.getName() in [x.getName() for x in self._attributes]:
            raise IndexError("Child with " + attribute.getName() + " already exists as a attribute.")

        self._attributes.append(attribute)
        attribute.setParent(self)

        return True


    def removeAttributeByIndex(self, index):
        """Removes attribute at specified index..

        Args:
            index (int): index of the attribute to remove.

        Returns:
            bool: True if successful.

        """

        if self._checkAttributeIndex(index) is not True:
            return False

        del self._attributes[index]

        return True


    def removeAttributeByName(self, name):
        """Removes the attribute with the specified name..

        Args:
            name (str): name of the attribute to remove.

        Returns:
            bool: True if successful.

        """

        removeIndex = None

        for i, eachAttribute in enumerate(self._attributes):
            if eachAttribute.getName() == name:
                removeIndex = i

        if removeIndex is None:
            return False

        self.removeAttributeByIndex(removeIndex)

        return True


    def getNumAttributes(self):
        """Returns the number of attributes as an integer.

        Returns:
            int: Number of attributes on this object.

        """

        return len(self._attributes)


    def getAttributeByIndex(self, index):
        """Returns the attribute at the specified index..

        Args:
            index (int): index of the attribute to return.

        Returns:
            Attribute: The attribute at the specified index.

        """

        if self._checkAttributeIndex(index) is not True:
            return False

        return self._attributes[index]


    def getAttributeByName(self, name):
        """Return the attribute with the specified name..

        Args:
            name (str): Name of the attribute to return.

        Returns:
            Attribute: The attribute with the specified name.

        """

        for eachAttribute in self._attributes:
            if eachAttribute.getName() == name:
                return eachAttribute

        return None


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
                break;
            classHierarchy.append(cls.__name__)

        jsonData = {
            '__typeHierarchy__': classHierarchy,
            'name': self.name,
            'parent': self.getParent().getName(),
            'attributes': []
        }
        for attr in self._attributes:
            jsonData['attributes'].append(attr.jsonEncode(saver))

        return jsonData


    def jsonDecode(self, loader, jsonData):
        """Returns the color of the object..

        Args:
            loader (Object): Loader object.
            jsonData (Dict): JSON object structure.

        Returns:
            bool: True if successful.

        """

        for attr in jsonData['attributes']:
            self.addAttribute(loader.construct(attr))

        return True
