"""Kraken - objects.locator module.

Classes:
Locator -- Locator representation.

"""

from kraken.core.objects.scene_item import SceneItem


class Locator(SceneItem):
    """Locator object."""

    __kType__ = "Locator"

    def __init__(self, name):
        super(Locator, self).__init__(name, None)


    # =============
    # Name methods
    # =============

    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """
        
        return super(Locator, self).getBuildName() + '_null'