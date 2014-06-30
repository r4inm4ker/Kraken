"""Kraken - objects.SceneItem module.

Classes:
SceneItem - Base SceneItem Object.

"""

from kraken.core.maths import *


class SceneItem(object):
    """Kraken base object type for any 3D object."""

    def __init__(self, name, parent=None):
        super(SceneItem, self).__init__()
        self.name = name
        self.parent = parent
        self.children = []
        self.attributes = []
        self.xfo = Xfo()


    def getName(self):
        """Returns the name of the object as a string."""

        return self.name


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the parent of the object as an object."""

        return self.parent


    def setParent(self, parent):
        """Sets the parent attribute of this object.

        Arguments:
        parent -- Object, object that is the paret of this one.

        Return:
        True if successful.
        """

        self.parent = parent

        return True


    # ==============
    # Child Methods
    # ==============
    def checkChildIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, child index to check.
        """

        if index > len(self.children):
            raise IndexError("'" + str(index) + "' is out of the range of 'children' array.")
            return False

        return True


    def addChild(self, child):
        """Adds a child to this object.

        Arguments:
        child -- Object, object that will be a child of this object.

        Return:
        True if successful.
        """

        if child.name in [x.name for x in self.children]:
            raise IndexError("Child with " + child.name + " already exists as a child.")

        self.children.append(child)
        child.setParent(self)

        return True


    def removeChildByIndex(self, index):
        """Removes a child from this object by index.

        Arguments:
        index -- Integer, index of child to remove.
        """

        if self.checkChildIndex(index) is not True:
            return False

        del self.children[index]

        return True


    def removeChildByName(self, name):
        """Removes a child from this object by name.

        Arguments:
        name -- String, name of child to remove.
        """

        removeIndex = None

        for i, eachChild in enumerate(self.children):
            if eachChild.name == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid child of this object.")
            return False

        self.removeChildByIndex(i)

        return True


    def getNumChildren(self):
        """Returns the number of children this object has as an integer."""

        return len(self.children)


    def getChildByIndex(self, index):
        """Returns the child object at specified index."""

        if self.checkChildIndex(index) is not True:
            return False

        return self.children[index]


    def getChildByName(self, name):
        """Returns the child object with the specified name.

        Return:
        Object if found.
        None if not found.
        """

        for eachChild in self.children:
            if eachChild.name == name:
                return eachChild

        return None


    def getChildrenByType(self, type):
        """Returns all children that are of the specified type.

        Return:
        Child objects of the specified type.
        None if no objects of specified type are found.
        """

        childrenOfType = None

        # Do magic here

        return childrenOfType


    # ==================
    # Attribute Methods
    # ==================
    def checkAttributeIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, attribute index to check.
        """

        if index > len(self.attributes):
            raise IndexError("'" + str(index) + "' is out of the range of 'attributes' array.")
            return False

        return True

    def addAttribute(self, attribute):
        """Adds an attribute to this object.

        Arguments:
        attribute -- Object, attribute object to add to this object.

        Return:
        True if successful.
        """

        if attribute.name in [x.name for x in self.attributes]:
            raise IndexError("Child with " + attribute.name + " already exists as a attribute.")

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
            if eachAttribute.name == name:
                removeIndex = i

        if removeIndex is None:
            return False

        self.removeAttributeByIndex(removeIndex)

        return True


    def getNumAttributes(self):
        """Returns the number of attributes as an integer."""

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
            if eachAttribute.name == name:
                return eachAttribute

        return None