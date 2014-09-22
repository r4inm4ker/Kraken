"""Kraken - objects.hierarchy_group module.

Classes:
HierarchyGroup -- Hiearchy group representation.

"""

from kraken.core.objects.scene_item import SceneItem


class HierarchyGroup(SceneItem):
    """HierarchyGroup object."""

    __kType__ = "HierarchyGroup"

    def __init__(self, name, parent=None):
        super(HierarchyGroup, self).__init__(name, parent=parent)

        self.setShapeVisibility(False)