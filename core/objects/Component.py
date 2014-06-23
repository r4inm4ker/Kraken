"""Kraken - objects.compoent module.

Classes:
Component -- Component representation.

"""

from collections import OrderedDict
from SceneItem import SceneItem



class Component(SceneItem):
    """docstring for Component"""

    def __init__(self, name, parent=None):
        super(Component, self).__init__(name, parent)
        self.inputs = []
        self.outputs = []


    # ==================
    # Component Methods
    # ==================
    def getComponent(self, index):
        return self.getChildrenByType(Component)[index]


    def getNumComponents(self):
        return len(self.getChildrenByType(Component))



    def addComponent(self, component):
        pass


    def removeComponent(self, componentName):
        pass


    # ==============
    # Input Methods
    # ==============
    def addInput(self, input):
        pass


    def removeInputByIndex(self):
        pass