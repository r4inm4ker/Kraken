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

        Returns:
            str: Decorated name of the object.

        """


        # During construction of the base class, the name is tested before
        # the component is assigned.
        if self.getComponent() is not None:
            # The ComponentGroup's name should always match the component's name.
            return self.getComponent().getName()
        else:
            return super(ComponentGroup, self).getName()


    def getNameDecoration(self):
        """Gets the decorated name of the object.

        Returns:
            str: Decorated name of the object.

        """

        if self.getComponent() is not None:
            # The ComponentGroup's name should always match the component's name.
            return self.getComponent().getNameDecoration()
        else:
            return super(ComponentGroup, self).getNameDecoration()
