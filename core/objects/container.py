"""Kraken - objects.container module.

Classes:
Container -- Component container representation.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.components.base_component import BaseComponent


class Container(SceneItem):
    """Container object."""

    __kType__ = "Container"

    def __init__(self, name):
        super(Container, self).__init__(name, None)

        self.setShapeVisibility(False)


    # =============
    # Name methods
    # =============

    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """

        # The container is generally the root node in the rig.
        return self.getName()


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

        component.setParent(self)
        return self.addChild(component)


    def removeComponent(self, componentName):
        """Removes a component from the container by name.

        Arguments:
        componentName -- String, name of the component to remove from the container.

        Return:
        True if successful.

        """

        component.setParent(None)
        return self.removeChild(componentName)