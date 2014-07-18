"""Kraken - objects.container module.

Classes:
Container -- Component container representation.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.components.base_component import BaseComponent


class Container(SceneItem):
    """Container object."""

    __kType__ = "Container"

    def __init__(self, name):
        super(Container, self).__init__(name, None)

        self.setShapeVisibility(False)




    # def buildRig(self):

    #     container = Container(self.getName())

    #     for