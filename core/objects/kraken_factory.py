"""KrakenFactory - objects.kraken_factory module.

Classes:
KrakenFactory - Factory for building SceneItems.

"""
from kraken.core.maths import *

from container import Container
from curve import Curve
from hierarchy_group import HierarchyGroup
from joint import Joint
from layer import Layer
from locator import Locator
from scene_item import SceneItem
from attributes import * 
from components import * 
# from constraints import * 
# from operators import * 

class KrakenFactory(object):
    """Kraken base object type for any 3D object."""


    def __init__(self):

        # A dictionary of all the built elements during loading.
        self.builtItems = {}

    def decodeValue(self, jsonData):
        """Returns a constructed scene item based on the provided name.

        Return:
        The constructed scene item.

        """
        if '__class__' not in jsonData:
            raise Exception("Invalid JSON data for constructing value:" + str(jsonData));

        if jsonData['__class__'] == 'Vec2':
            item = Vec2()
            item.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Vec3':
            item = Vec3()
            item.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Vec4':
            item = Vec4()
            item.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Euler':
            item = Euler()
            item.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Quat':
            item = Quat()
            item.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Xfo':
            item = Xfo()
            item.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Matrix33':
            item = Matrix33()
            item.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Matrix44':
            item = Matrix44()
            item.jsonDecode(jsonData, self)
        else:
            raise Exception("Unsupported Math type:" + jsonData['__class__'])
        return item


    def resolveSceneItem(self, name):
        """Returns a constructed scene item based on the provided name.

        Return:
        The constructed scene item.

        """
        if name in self.builtItems:
            return self.builtItems[name]
        raise Exception("SceneItem not found:" + name)


    def construct(self, jsonData):
        """Returns a constructed scene item based on the provided json data.

        Return:
        The constructed scene item.

        """
        if '__kType__' not in jsonData or 'name' not in jsonData:
            raise Exception("Invalid JSON data for constructing scene item:" + str(jsonData));

        if jsonData['__kType__'] == "Group":
            item = Group(jsonData['name'])

        elif jsonData['__kType__'] == "Null":
            item = Null(jsonData['name'])

        elif jsonData['__kType__'] == "Control":
            item = Control(jsonData['name'])

        elif jsonData['__kType__'] == "Chain":
            item = Chain(jsonData['name'])

        elif jsonData['__kType__'] == "Joint":
            item = Joint(jsonData['name'])

        elif jsonData['__kType__'] == "Container":
            item = Container(jsonData['name'])

        elif jsonData['__kType__'] == "Curve":
            item = Curve(jsonData['name'])

        elif jsonData['__kType__'] == "HierarchyGroup":
            item = HierarchyGroup(jsonData['name'])

        elif jsonData['__kType__'] == "Joint":
            item = Joint(jsonData['name'])

        elif jsonData['__kType__'] == "Layer":
            item = Layer(jsonData['name'])

        elif jsonData['__kType__'] == "Locator":
            item = Locator(jsonData['name'])

        elif jsonData['__kType__'] == "SceneItem":
            item = SceneItem(jsonData['name'])

        elif jsonData['__kType__'] == "AttributeGroup":
            item = AttributeGroup(jsonData['name'])

        elif jsonData['__kType__'] == "Attribute":
            item = Attribute(jsonData['name'])

        elif jsonData['__kType__'] == "BoolAttribute":
            item = BoolAttribute(jsonData['name'])

        elif jsonData['__kType__'] == "FloatAttribute":
            item = FloatAttribute(jsonData['name'])

        elif jsonData['__kType__'] == "IntegerAttribute":
            item = IntegerAttribute(jsonData['name'])

        elif jsonData['__kType__'] == "StringAttribute":
            item = StringAttribute(jsonData['name'])

        elif jsonData['__kType__'] == "Component":
            item = Component(jsonData['name'])

        elif jsonData['__kType__'] == "ComponentInput":
            item = ComponentInput(jsonData['name'])

        elif jsonData['__kType__'] == "ComponentOutput":
            item = ComponentOutput(jsonData['name'])

        elif jsonData['__kType__'] == "BaseConstraint":
            item = BaseConstraint(jsonData['name'])

        elif jsonData['__kType__'] == "OrientationConstraint":
            item = OrientationConstraint(jsonData['name'])

        elif jsonData['__kType__'] == "PoseConstraint":
            item = PoseConstraint(jsonData['name'])

        elif jsonData['__kType__'] == "PositionConstraint":
            item = PositionConstraint(jsonData['name'])

        elif jsonData['__kType__'] == "ScaleConstraint":
            item = ScaleConstraint(jsonData['name'])

        elif jsonData['__kType__'] == "Control":
            item = Control(jsonData['name'])

        elif jsonData['__kType__'] == "Operator":
            item = Operator(jsonData['name'])

        elif jsonData['__kType__'] == "OperatorBinding":
            item = OperatorBinding(jsonData['name'])
        else:
            raise Exception("KrakenFactory does not support the given type:" + __kType__)

        item.jsonDecode(jsonData)
        self.builtItems[item.getName()] = item
        return item