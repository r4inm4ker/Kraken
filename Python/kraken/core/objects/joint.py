"""Kraken - objects.joint module.

Classes:
Joint -- Joint representation.

"""

from kraken.core.objects.object_3d import Object3D


class Joint(Object3D):
    """Joint object."""

    def __init__(self, name, parent=None):
        super(Joint, self).__init__(name, parent=parent)
