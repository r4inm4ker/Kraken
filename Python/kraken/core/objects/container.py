"""Kraken - objects.container module.

Classes:
Container -- Component container representation.

"""

from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.components.base_example_component import BaseExampleComponent


class Container(Object3D):
    """Container object."""

    def __init__(self, name):
        super(Container, self).__init__(name, None)

        self.setShapeVisibility(False)
        self.lockRotation(x=True, y=True, z=True)
        self.lockScale(x=True, y=True, z=True)
        self.lockTranslation(x=True, y=True, z=True)
