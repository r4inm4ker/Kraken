"""Kraken - objects.hierarchy_group module.

Classes:
HierarchyGroup -- Hiearchy group representation.

"""

from kraken.core.objects.scene_item import SceneItem


class HierarchyGroup(SceneItem):
    """HierarchyGroup object."""

    def __init__(self, name, parent=None):
        super(HierarchyGroup, self).__init__(name, parent=parent)

        self.setShapeVisibility(False)
        self.lockRotation(x=True, y=True, z=True)
        self.lockScale(x=True, y=True, z=True)
        self.lockTranslation(x=True, y=True, z=True)
