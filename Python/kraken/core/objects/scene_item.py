"""Kraken - objects.scene_item module.

Classes:
SceneItem - Base SceneItem Object.

"""


class SceneItem(object):
    """Kraken base object type for any 3D object."""

    def __init__(self, name, parent=None):
        super(SceneItem, self).__init__()
        self._parent = parent
        self._name = name


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

        return self._name


    def setName(self, name):
        """Sets the name of the object with a string.

        Arguments:
        name -- String, the new name for the item.

        Return:
        True if successful.

        """

        self._name = name

        return True


    def getPath(self):
        """Returns the full hierarchical path to this object.

        Return:
        String, full name of the object.

        """

        if self.getParent() is not None:
            return self.getParent().getPath() + '.' + self.getName()

        return self.getName()


    def getNameDecoration(self):
        """Gets the decorated name of the object.

        Return:
        String, decorated name of the object.

        """

        return ""

    def getDecoratedName(self):
        """Gets the decorated name of the object.

        Return:
        String, decorated name of the object.

        """

        return self.getName() + self.getNameDecoration()


    def getDecoratedPath(self):
        """Gets the decorated path of the object.

        Return:
        String, decorated path  of the object.

        """


        if self.getParent() is not None:
            return self.getParent().getDecoratedPath() + '.' + self.getDecoratedName()

        return self.getDecoratedName()


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the parent of the object as an object.

        Return:
        Parent of this object.

        """

        return self._parent


    def setParent(self, parent):
        """Sets the parent attribute of this object.

        Arguments:
        parent -- Object, object that is the parent of this one.

        Return:
        True if successful.

        """

        self._parent = parent

        return True
