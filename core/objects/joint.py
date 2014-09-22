"""Kraken - objects.joint module.

Classes:
Joint -- Joint representation.

"""

from kraken.core.objects.scene_item import SceneItem


class Joint(SceneItem):
    """Joint object."""

    __kType__ = "Joint"

    def __init__(self, name, parent=None):
        super(Joint, self).__init__(name, parent=parent)