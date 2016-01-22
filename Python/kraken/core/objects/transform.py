"""Kraken - objects.transform module.

Classes:
Transform -- Transform representation.

"""

from kraken.core.objects.object_3d import Object3D


class Transform(Object3D):
    """Transform object."""

    def __init__(self, name, parent=None):
        super(Transform, self).__init__(name, parent=parent)

