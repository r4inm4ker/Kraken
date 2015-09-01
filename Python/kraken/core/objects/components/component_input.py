"""Kraken - objects.components.component_input module.

Classes:
ComponentInput -- ComponentInput representation.

"""

from kraken.core.objects.object_3d import Object3D


class ComponentInput(Object3D):
    """ComponentInput object."""

    def __init__(self, name, parent=None):
        super(ComponentInput, self).__init__(name, parent=parent)
        self.setShapeVisibility(False)