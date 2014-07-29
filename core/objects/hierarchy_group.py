"""Kraken - objects.hierarchy_group module.

Classes:
HierarchyGroup -- Hiearchy group representation.

"""

from kraken.core.objects.scene_item import SceneItem


class HierarchyGroup(SceneItem):
    """HierarchyGroup object."""

    __kType__ = "HierarchyGroup"

    def __init__(self, name):
        super(HierarchyGroup, self).__init__(name, None)

        self.setShapeVisibility(False)


    # =============
    # Name methods
    # =============

    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """
        
        return super(HierarchyGroup, self).getBuildName() + '_hrc'