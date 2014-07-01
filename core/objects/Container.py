"""Kraken - objects.containers module.

Classes:
Container -- Component container representation.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.component import BaseComponent


class Container(SceneItem):
    """docstring for Container"""

    def __init__(self, name):
        super(Container, self).__init__(name, None)


    # ==================
    # Component Methods
    # ==================
    def getComponent(self, index):
        """Get the component at the specified index..

        Arguments:
        index -- Integer, index of the connection to return.

        Return:
        The component at the specified index.

        """

        return self.getChildrenByType(BaseComponent)[index]


    def getNumComponents(self):
        """Gets the number of components for this object.

        Return:
        The number of components.

        """

        return len(self.getChildrenByType(BaseComponent))


    def addComponent(self, component):
        """Adds a component to the container.

        Arguments:
        component -- Object, component to add to the container.

        Return:
        True if successful.

        """

        return self.addChild(component)


    def removeComponent(self, componentName):
        """Removes a component from the container by name.

        Arguments:
        componentName -- String, name of the component to remove from the container.

        Return:
        True if successful.

        """

        return self.removeChild(componentName)