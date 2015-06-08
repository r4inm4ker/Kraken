"""Kraken - objects.scene_item module.

Classes:
SceneItem - Base SceneItem Object.

"""


class SceneItem(object):
    """Kraken base object type for any 3D object."""

    def __init__(self, name, parent=None):
        super(SceneItem, self).__init__()
        self._name = name
        self._parent = parent


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

        # # Check for existing objects with that name and type.
        # parent = self.getParent()
        # if parent is not None:
        #     foundChild = parent.findChild(name, childType=self.getTypeName())
        #     if foundChild is not None:
        #         raise Exception("Child with the same name already exists: '" +
        #                         name + "'")

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


    def getDecoratedName(self):
        """Gets the decorated name of the object.

        Return:
        String, decorated name of the object.

        """

        return self.getName()


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
