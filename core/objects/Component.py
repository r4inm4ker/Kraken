"""Kraken - objects.compoent module.

Classes:
Component -- Component representation.

"""

from collections import OrderedDict
from kraken.core.maths import *
from SceneItem import SceneItem



class Component(SceneItem):
    """docstring for Component"""

    def __init__(self, name, parent=None, side='M'):
        super(Component, self).__init__(name, parent)
        self.side = side
        self.componentXfos = []
        self.inputs = []
        self.outputs = []


    # =============
    # Side Methods
    # =============
    def getSide(self):
        return self.side


    def setSide(self, side):
        if side not in ["L", "M", "R"]:
            raise ValueError("'" + side + "' is not a valid side.")

        self.side = side

        return True


    # ======================
    # Component Xfo Methods
    # ======================
    def checkComponentXfoIndex(self, index):

        if index > len(self.componentXfos):
            raise IndexError("'" + str(index) + "' is out of the range of 'componentXfos'.")
            return False

        return True


    def addComponentXfo(self, xfo=None):

        if xfo is None:
            xfo = Xfo()

        self.componentXfos.append(xfo)

        return self.componentXfos[-1]


    def removeComponentXfo(self, index):

        if self.checkComponentXfoIndex(index) is not True:
            return False

        del self.componentXfos[index]

        return True


    def getNumComponentXfos(self):
        return len(self.componentXfos)


    def getComponentXfos(self):
        return self.componentXfos


    def getComponentXfoByIndex(self, index):

        if self.checkComponentXfoIndex(index) is not True:
            return False

        return self.componentXfos[index]


    def setComponentXfo(self, index, xfo):

        if self.checkComponentXfoIndex(index) is not True:
            return False

        self.componentXfos[index] = xfo

        return True


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