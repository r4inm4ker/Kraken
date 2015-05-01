"""Kraken - objects.locator module.

Classes:
SrtBuffer -- SrtBuffer representation.

"""

from kraken.core.objects.scene_item import SceneItem


class SrtBuffer(SceneItem):
    """SrtBuffer object."""

    def __init__(self, name, parent=None):
        super(SrtBuffer, self).__init__(name, parent=parent)
        self.setShapeVisibility(False)
