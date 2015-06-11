"""Kraken - objects.component_group module.

Classes:
ComponentGroup -- Hiearchy group representation.

"""

from kraken.core.objects.object_3d import Object3D


class ComponentGroup(Object3D):
    """ComponentGroup object."""

    def __init__(self, name, component, parent=None):
        super(ComponentGroup, self).__init__(name, parent=parent)

        self.setComponent(component)

        self.setShapeVisibility(False)
        self.lockRotation(True, True, True)
        self.lockScale(True, True, True)
        self.lockTranslation(True, True, True)

    # =============
    # Name Methods
    # =============


    def getName(self):
        """Gets the decorated name of the object.

        Return:
        String, decorated name of the object.

        """

        # The ComponentGroup's name should always match the component's name.
        return self.getComponent().getName()


    def getDecoratedName(self):
        """Gets the decorated name of the object.

        Return:
        String, decorated name of the object.

        """

        return self.getComponent().getDecoratedName()
