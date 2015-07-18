"""Kraken - objects.components.component_input module.

Classes:
ComponentOutput -- ComponentOutput representation.

"""

from kraken.core.objects.object_3d import Object3D


class ComponentOutput(Object3D):
    """ComponentOutput object."""

    def __init__(self, name, parent=None):
        super(ComponentOutput, self).__init__(name, parent=parent)
