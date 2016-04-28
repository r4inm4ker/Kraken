"""Kraken - objects.scene_item module.

Classes:
SceneItem - Base SceneItem Object.

"""


class SceneItem(object):
    """Kraken base object type for any 3D object."""

    __maxId = 0

    def __init__(self, name, parent=None):
        super(SceneItem, self).__init__()
        self._parent = parent
        self._name = name
        self._component = None
        self._sources = []
        self._id = SceneItem.__maxId
        SceneItem.__maxId = SceneItem.__maxId + 1

    # ==============
    # Type Methods
    # ==============
    def getId(self):
        """Returns the unique Id of this object.

        Returns:
            int: Unique id.

        """

        return self._id


    def getTypeName(self):
        """Returns the class name of this object.

        Returns:
            bool: True if successful.

        """

        return self.__class__.__name__


    def getTypeHierarchyNames(self):
        """Returns the class name of this object.

        Returns:
            bool: True if successful.

        """

        khierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break
            khierarchy.append(cls.__name__)

        return khierarchy


    def isTypeOf(self, typeName):
        """Returns the class name of this object.

        Returns:
            bool: True if the scene item is of the given type.

        """

        for cls in type.mro(type(self)):
            if cls.__name__ == typeName:
                return True

        return False


    def isOfAnyType(self, typeNames):
        """Returns true if this item has any of the given type names

        Returns:
            bool: True if the scene item is of the given type.

        """
        for typeName in typeNames:
            if self.isTypeOf(typeName):
                return True
        return False


    # =============
    # Name methods
    # =============
    def getName(self):
        """Returns the name of the object as a string.

        Returns:
            str: Object's name.

        """

        return self._name


    def setName(self, name):
        """Sets the name of the object with a string.

        Arguments:
            name (str): The new name for the item.

        Returns:
            bool: True if successful.

        """

        self._name = name

        return True


    def getPath(self):
        """Returns the full hierarchical path to this object.

        Returns:
            str: Full name of the object.

        """

        if self.getParent() is not None:
            return self.getParent().getPath() + '.' + self.getName()

        return self.getName()


    def getNameDecoration(self):
        """Gets the decorated name of the object.

        Returns:
            str: Decorated name of the object.

        """

        return ""


    def getDecoratedName(self):
        """Gets the decorated name of the object.

        Returns:
            str: Decorated name of the object.

        """

        return self.getName() + self.getNameDecoration()


    def getDecoratedPath(self):
        """Gets the decorated path of the object.

        Returns:
            str: Decorated path  of the object.

        """


        if self.getParent() is not None:
            return self.getParent().getDecoratedPath() + '.' + self.getDecoratedName()

        return self.getDecoratedName()


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the parent of the object as an object.

        Returns:
            Object: Parent of this object.

        """

        return self._parent


    def setParent(self, parent):
        """Sets the parent attribute of this object.

        Arguments:
        parent (Object): Object that is the parent of this one.

        Returns:
            bool: True if successful.

        """

        self._parent = parent
        self.addSource(parent)

        return True

    # ===============
    # Source Methods
    # ===============
    def getSources(self):
        """Returns the sources of the object.

        Returns:
            list: All sources of this object.

        """

        return self._sources


    def getCurrentSource(self):
        """Returns the source of the object which is currently driving it.

        Returns:
            Object: source of this object

        """
        if len(self.getSources()) > 0:
            return self.getSources()[-1]
        return None


    def addSource(self, source):
        """Adds another source to this object.

        Arguments:
        source (Object): Object that is the source of this one.

        Returns:
            int: Index of the source used

        """

        if not isinstance(source, SceneItem):
            return False

        for prevSource in self._sources:
            if prevSource.getId() == source.getId():
                return False

        self._sources.append(source)
        return True


    def setSource(self, index, source):
        """Sets the source of this object.

        Arguments:
        index (int): The index of the source to update.
        source (Object): Object that is the source of this one.

        """

        self._sources[index] = source
        return True


    # ==================
    # Component Methods
    # ==================
    def getComponent(self):
        """Returns the component of the object as an object.

        Returns:
            Object: Component of this object.

        """

        return self._component

    def setComponent(self, component):
        """Sets the component attribute of this object.

        Args:
            component (Object): Object that is the component of this one.

        Returns:
            bool: True if successful.

        """

        self._component = component

        return True
