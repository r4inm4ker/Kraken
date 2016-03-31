"""Kraken - objects.container module.

Classes:
Container -- Component container representation.

"""

from collections import OrderedDict

from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.components.base_example_component import BaseExampleComponent

# Note: does a container need to inherit off 'Object3D'?
# These items exist only to structure a rig as a graph.
# The never get built.
class Container(Object3D):
    """Container object."""

    def __init__(self, name):
        super(Container, self).__init__(name, None)

        self.setShapeVisibility(False)
        self.lockRotation(x=True, y=True, z=True)
        self.lockScale(x=True, y=True, z=True)
        self.lockTranslation(x=True, y=True, z=True)

        self._items = OrderedDict()

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