"""Kraken - objects.layer module.

Classes:
Layer - Layer object that gets added to containers for organizing the rig.

"""

from kraken.core.objects.scene_item import SceneItem


class Layer(SceneItem):
    """Layer object."""

    def __init__(self, name, parent=None):
        super(Layer, self).__init__(name, parent=parent)

        self.setShapeVisibility(False)