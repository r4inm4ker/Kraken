"""Kraken - objects.containers module.

Classes:
Container -- Component container representation.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.component import BaseComponent


class Container(SceneItem):
    """docstring for Container"""

    def __init__(self, name):
        super(Container, self).__init__(name, None)


    # ==================
    # Component Methods
    # ==================
    def getComponent(self, index):
        return self.getChildrenByType(BaseComponent)[index]


    def getNumComponents(self):
        return len(self.getChildrenByType(BaseComponent))


    def addComponent(self, component):
        return self.addChild(component)


    def removeComponent(self, componentName):
        return self.removeChild(componentName)