"""Kraken - objects.locator module.

Classes:
Locator -- Locator representation.

"""

from kraken.core.objects.scene_item import SceneItem


class Locator(SceneItem):
    """Locator object."""

    __kType__ = "Locator"

    def __init__(self, name, parent=None):
        super(Locator, self).__init__(name, parent=parent)


    # =============
    # Name methods
    # =============
    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """

        if self.getParent() is not None:
            if self.getParent().getName() == "inputs":
                return super(Locator, self).getBuildName() + '_srtIn'
            elif self.getParent().getName() == "outputs":
                return super(Locator, self).getBuildName() + '_srtOut'
            else:
                return super(Locator, self).getBuildName() + '_null'
        else:
            return super(Locator, self).getBuildName() + '_null'