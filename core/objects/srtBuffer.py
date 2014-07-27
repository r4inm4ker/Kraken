"""Kraken - objects.locator module.

Classes:
SrtBuffer -- SrtBuffer representation.

"""

from kraken.core.objects.scene_item import SceneItem


class SrtBuffer(SceneItem):
    """SrtBuffer object."""

    __kType__ = "SrtBuffer"

    def __init__(self, name):
        super(SrtBuffer, self).__init__(name, None)