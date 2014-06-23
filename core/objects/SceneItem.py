from kraken.core.maths import *


class SceneItem(object):
    """docstring for SceneItem"""


    def __init__(self, name, parent=None):
        super(SceneItem, self).__init__()
        self.name = name
        self.parent = parent
        self.children = []
        self.attributes = []
        self.xfo = Xfo()


    def getName(self):
        return self.name


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        return self.parent


    def setParent(self, parent):
        self.parent = parent


    # ==============
    # Child Methods
    # ==============
    def addChild(self, child):

        if child.name in [x.name for x in self.children]:
            raise IndexError("Child with " + child.name + " already exists as a child.")

        self.children.append(child)
        child.setParent(self)

        return True


    def removeChildByIndex(self, index):
        pass


    def removeChildByName(self, name):
        pass


    def getNumChildren(self):
        return len(self.children)


    def getChildByIndex(self, index):
        return self.children[index]


    def getChildByName(self, name):

        for eachChild in self.children:
            if eachChild.name == name:
                return eachChild

        return None

    def getChildrenByType(self, type):
        pass


    # ==================
    # Attribute Methods
    # ==================
    def addAttribute(self, attribute):

        if attribute.name in [x.name for x in self.attributes]:
            raise IndexError("Child with " + attribute.name + " already exists as a attribute.")

        self.attributes.append(attribute)
        attribute.setParent(self)

        return True


    def removeAttributeByIndex(self, index):
        pass


    def removeAttributeByName(self, name):
        pass


    def getNumAttributes(self):
        return len(self.attributes)


    def getAttributeByIndex(self, index):
        return self.attributes[index]


    def getAttributeByName(self, name):

        for eachAttribute in self.attributes:
            if eachAttribute.name == name:
                return eachAttribute

        return None