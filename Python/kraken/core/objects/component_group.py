"""Kraken - objects.component_group module.

Classes:
ComponentGroup -- Hiearchy group representation.

"""

from kraken.core.objects.scene_item import SceneItem


class ComponentGroup(SceneItem):
    """ComponentGroup object."""

    def __init__(self, name, parent=None):
        super(ComponentGroup, self).__init__(name, parent=parent)

        self.setShapeVisibility(False)
        self.lockRotation(True, True, True)
        self.lockScale(True, True, True)
        self.lockTranslation(True, True, True)