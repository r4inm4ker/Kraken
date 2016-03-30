"""Kraken - objects.container module.

Classes:
Container -- Component container representation.

"""

from kraken.core.objects.object_3d import Object3D
# from kraken.core.objects.components.base_example_component import BaseExampleComponent

# Note: does a container need to inherit off 'Object3D'?
# These items exist only to structure a rig as a graph. 
# The never get built.
class Container(object):
    """Container object."""

    def __init__(self, name, container=None):
        super(Container, self).__init__()

        self._name = name
        self._items = {}
        self._containter = container
        
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

        if self._containter is not None:
            return self._containter.getPath() + '.' + self.getName()

        return self.getName()

    # ==============
    # Item Methods
    # ==============
    def addItem(self, name, item):
        """Adds a child to the component and sets the object's component attribute.

        Args:
            child (Object): Object to add as a child.

        Returns:
            bool: True if successful.

        """



        # Assign the child self as the component.
        item.setComponent(self)

        self._items[name] = item

        return True

    def getItems(self):
        """Returns all items for this component.

        Returns:
            list: Items for this component.

        """

        return dict(self._items)


    # ==================
    # Hierarchy Methods
    # ==================
    def getContainer(self):
        """Returns the Container the object belongs to.

        Returns:
            Object: Container.

        """

        parent = self.getParent()
        while (parent is not None and 'Container' not in parent.getTypeHierarchyNames()):
            parent = parent.getParent()

        return parent