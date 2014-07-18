"""Kraken - objects.locator module.

Classes:
Locator -- Locator representation.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.components.base_component import BaseComponent


class Locator(SceneItem):
    """Locator object."""

    __kType__ = "Locator"

    def __init__(self, name):
        super(Locator, self).__init__(name, None)