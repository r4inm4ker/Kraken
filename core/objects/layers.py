"""Kraken - Layers."""

from collections import OrderedDict
from kraken.core.objects import elements


class Layer(elements.SceneObject):
    """Base Layer object."""

    __kType__ = "Layer"

    def __init__(self, name, component):
        super(Layer, self).__init__(name, component)
        self.component = component
        self.members = OrderedDict()


    def addMember(self, member):
        """Adds an object to this layer and puts it into the members dictionary.

        Arguments:
        member -- object, member to add to this layer.

        Return:
        True if added successfully.

        """

        if member.name in self.members.keys():
            raise KeyError("Object is already part of the layer: " + member.name)
            return False

        self.members[member.name] = member
        member.layer = self

        return True


    def buildDef(self):
        """Builds the Rig Definition and stores to definition attribute.

        Return:
        Dictionary of object data.
        """

        self.definition = {
                           "elements":{},
                           "io":{}
                          }

        for eachAttrGroup in self.attributes:
            attrGroup = self.attributes[eachAttrGroup]

            for eachAttribute in attrGroup:
                self.definition["io"][attrGroup[eachAttribute].name] = attrGroup[eachAttribute].buildDef()

        for eachChild in self.children:
            self.definition["elements"][eachChild] = self.children[eachChild].buildDef()

        return self.definition