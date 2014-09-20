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