"""Kraken - objects.locator module.

Classes:
Locator -- Locator representation.

"""

from kraken.core.objects.object_3d import Object3D


class Locator(Object3D):
    """Locator object."""

    def __init__(self, name, parent=None):
        super(Locator, self).__init__(name, parent=parent)
