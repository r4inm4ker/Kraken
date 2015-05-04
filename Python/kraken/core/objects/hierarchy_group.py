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
        self.lockRotation(True, True, True)
        self.lockScale(True, True, True)
        self.lockTranslation(True, True, True)

