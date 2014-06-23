"""Kraken - objects.containers module.

Classes:
Container -- Component container representation.

"""

from SceneItem import SceneItem


class Container(SceneItem):
    """docstring for Container"""

    def __init__(self, name):
        super(Container, self).__init__(name, None)


    def getComponent(self, index):
        return self.getChildrenByType(Component)[index]


    def getNumComponents(self):
        return len(self.getChildrenByType(Component))



    def addComponent(self, component):
        pass


    def removeComponent(self, componentName):
        pass