"""Kraken - objects.joint module.

Classes:
Joint -- Joint representation.

"""

from kraken.core.objects.scene_item import SceneItem


class Joint(SceneItem):
    """Joint object."""

    __kType__ = "Joint"

    def __init__(self, name):
        super(Joint, self).__init__(name, None)


    # =============
    # Name methods
    # =============

    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """
        
        return super(Joint, self).getBuildName() + '_def'