"""Kraken - objects.joint module.

Classes:
Joint -- Joint representation.

"""

from kraken.core.objects.scene_item import SceneItem


class Joint(SceneItem):
    """Joint object."""

    __kType__ = "Joint"

    def __init__(self, name, parent=None):
        super(Joint, self).__init__(name, parent=parent)


    # =============
    # Name methods
    # =============

    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """

        return super(Joint, self).getBuildName() + '_def'