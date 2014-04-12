"""Kraken - Layers."""

from kraken.core.objects import elements
from kraken.core.components.arm import ArmComponent

class Layer(elements.SceneObject):
    """Base Layer object."""

    __kType__ = "Layer"

    def __init__(self, name, component):
        super(Layer, self).__init__(name, component)
        self.component = component