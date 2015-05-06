"""Kraken - objects.scene_item module.

Classes:
BaseItem - Base BaseItem Object.

"""


class BaseItem(object):
    """Kraken base object type for any 3D object."""

    def __init__(self, name, parent=None):
        super(BaseItem, self).__init__()
        self.name = name
        self.parent = parent

    # ==============
    # Type Methods
    # ==============
    def getTypeName(self):
        """Returns the class name of this object.

        Return:
        True if successful.

        """

        return self.__class__.__name__


    def getTypeHierarchyNames(self):
        """Returns the class name of this object.

        Return:
        True if successful.

        """

        khierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break;
            khierarchy.append(cls.__name__)

        return khierarchy


    def isTypeOf(self, typeName):
        """Returns the class name of this object.

        Return:
        True if the scene item is of the given type.

        """

        for cls in type.mro(type(self)):
            if cls.__name__ == typeName:
                return True

        return False

    # =============
    # Name methods
    # =============
    def getName(self):
        """Returns the name of the object as a string.

        Return:
        String of the object's name.

        """

        return self.name


    def getFullName(self):
        """Returns the full hierarchical path to this object.

        Return:
        String, full name of the object.

        """

        if self.parent is not None:
            return self.parent.getFullName() + '.' + self.getName()

        return self.getName()


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the parent of the object as an object.

        Return:
        Parent of this object.

        """

        return self.parent


    def setParent(self, parent):
        """Sets the parent attribute of this object.

        Arguments:
        parent -- Object, object that is the parent of this one.

        Return:
        True if successful.

        """

        self.parent = parent

        return True
