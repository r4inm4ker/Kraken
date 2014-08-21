"""Kraken - objects.locator module.

Classes:
SrtBuffer -- SrtBuffer representation.

"""

from kraken.core.objects.scene_item import SceneItem


class SrtBuffer(SceneItem):
    """SrtBuffer object."""

    __kType__ = "SrtBuffer"

    def __init__(self, name, parent=None):
        super(SrtBuffer, self).__init__(name, parent=parent)
        self.setShapeVisibility(False)


    # =============
    # Name methods
    # =============
    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """

        return super(SrtBuffer, self).getBuildName() + '_srtBuffer'