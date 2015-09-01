"""Kraken - objects.layer module.

Classes:
Layer - Layer object that gets added to containers for organizing the rig.

"""

from kraken.core.objects.object_3d import Object3D


class Layer(Object3D):
    """Layer object."""

    def __init__(self, name, parent=None):
        super(Layer, self).__init__(name, parent=parent)

        self.setShapeVisibility(False)
        self.lockRotation(x=True, y=True, z=True)
        self.lockScale(x=True, y=True, z=True)
        self.lockTranslation(x=True, y=True, z=True)
