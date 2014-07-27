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
from attributes.attribute_group import AttributeGroup
# from attributes.base_attribute import BaseAttribute
from attributes.float_attribute import FloatAttribute
from attributes.integer_attribute import IntegerAttribute
from attributes.string_attribute import StringAttribute

from components import * 

from constraints.orientation_constraint import OrientationConstraint
from constraints.pose_constraint import PoseConstraint
from constraints.position_constraint import PositionConstraint
from constraints.scale_constraint import ScaleConstraint


# from constraints import * 
# from operators import * 

class KrakenFactory(object):
    """Kraken base object type for any 3D object."""


    def __init__(self):

        # A dictionary of all the built elements during loading.
        self.parentItem = None
        self.builtItems = {}

    def encodeValue(self, value):
        if isinstance(value, MathObject):
            return value.encodeValue()
        else:
            return value

    def decodeValue(self, jsonData):
        """Returns a constructed scene item based on the provided name.

        Return:
        The constructed scene item.

        """
        if type(jsonData) is not dict:
            return jsonData

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
        if name is None:
            return None
        if name in self.builtItems:
            return self.builtItems[name]
        raise Exception("SceneItem not found:" + str(name))


    def construct(self, jsonData):
        """Returns a constructed scene item based on the provided json data.

        Return:
        The constructed scene item.

        """
        if '__kType__' not in jsonData or 'name' not in jsonData:
            raise Exception("Invalid JSON data for constructing scene item:" + str(jsonData));

        print "construct:" + str(jsonData['__kTypeHierarchy__']) + ":" + jsonData['name']

        ##########################
        ## Controls.

        if "ArrowControl" in jsonData['__kTypeHierarchy__']:
            item = ArrowControl(jsonData['name'])

        elif "ArrowsControl" in jsonData['__kTypeHierarchy__']:
            item = ArrowsControl(jsonData['name'])

        elif "CircleControl" in jsonData['__kTypeHierarchy__']:
            item = CircleControl(jsonData['name'])

        elif "CubeControl" in jsonData['__kTypeHierarchy__']:
            item = CubeControl(jsonData['name'])

        elif "NullControl" in jsonData['__kTypeHierarchy__']:
            item = NullControl(jsonData['name'])

        elif "PinControl" in jsonData['__kTypeHierarchy__']:
            item = PinControl(jsonData['name'])

        elif "SphereControl" in jsonData['__kTypeHierarchy__']:
            item = SphereControl(jsonData['name'])

        elif "SquareControl" in jsonData['__kTypeHierarchy__']:
            item = SquareControl(jsonData['name'])

        elif "TriangleControl" in jsonData['__kTypeHierarchy__']:
            item = TriangleControl(jsonData['name'])

        elif "BaseControl" in jsonData['__kTypeHierarchy__']:
            item = BaseControl(jsonData['name'])

        ##########################
        ## Attributes.

        elif "AttributeGroup" in jsonData['__kTypeHierarchy__']:
            item = AttributeGroup(jsonData['name'])

        elif "BoolAttribute" in jsonData['__kTypeHierarchy__']:
            item = BoolAttribute(jsonData['name'])

        elif "FloatAttribute" in jsonData['__kTypeHierarchy__']:
            item = FloatAttribute(jsonData['name'])

        elif "IntegerAttribute" in jsonData['__kTypeHierarchy__']:
            item = IntegerAttribute(jsonData['name'])

        elif "StringAttribute" in jsonData['__kTypeHierarchy__']:
            item = StringAttribute(jsonData['name'])

        elif "Attribute" in jsonData['__kTypeHierarchy__']:
            item = Attribute(jsonData['name'])

        elif "ComponentInput" in jsonData['__kTypeHierarchy__']:
            item = ComponentInput(jsonData['name'])

        elif "ComponentOutput" in jsonData['__kTypeHierarchy__']:
            item = ComponentOutput(jsonData['name'])

        ##########################
        ## Constraints.

        elif "OrientationConstraint" in jsonData['__kTypeHierarchy__']:
            item = OrientationConstraint(jsonData['name'])

        elif "PoseConstraint" in jsonData['__kTypeHierarchy__']:
            item = PoseConstraint(jsonData['name'])

        elif "PositionConstraint" in jsonData['__kTypeHierarchy__']:
            item = PositionConstraint(jsonData['name'])

        elif "ScaleConstraint" in jsonData['__kTypeHierarchy__']:
            item = ScaleConstraint(jsonData['name'])

        elif "BaseConstraint" in jsonData['__kTypeHierarchy__']:
            item = BaseConstraint(jsonData['name'])


        ##########################
        ## Constraints.

        elif "Operator" in jsonData['__kTypeHierarchy__']:
            item = Operator(jsonData['name'])

        elif "OperatorBinding" in jsonData['__kTypeHierarchy__']:
            item = OperatorBinding(jsonData['name'])

        ##########################
        ## SceneItems.

        elif "Group" in jsonData['__kTypeHierarchy__']:
            item = Group(jsonData['name'])

        elif "Null" in jsonData['__kTypeHierarchy__']:
            item = Null(jsonData['name'])

        elif "Control" in jsonData['__kTypeHierarchy__']:
            item = Control(jsonData['name'])

        elif "Chain" in jsonData['__kTypeHierarchy__']:
            item = Chain(jsonData['name'])

        elif "Joint" in jsonData['__kTypeHierarchy__']:
            item = Joint(jsonData['name'])

        elif "Container" in jsonData['__kTypeHierarchy__']:
            item = Container(jsonData['name'])

        elif "Curve" in jsonData['__kTypeHierarchy__']:
            item = Curve(jsonData['name'])

        elif "HierarchyGroup" in jsonData['__kTypeHierarchy__']:
            item = HierarchyGroup(jsonData['name'])

        elif "Joint" in jsonData['__kTypeHierarchy__']:
            item = Joint(jsonData['name'])

        elif "Layer" in jsonData['__kTypeHierarchy__']:
            item = Layer(jsonData['name'])

        elif "Locator" in jsonData['__kTypeHierarchy__']:
            item = Locator(jsonData['name'])

        elif "SceneItem" in jsonData['__kTypeHierarchy__']:
            item = SceneItem(jsonData['name'])

        else:
            raise Exception("KrakenFactory does not support the given type:" + __kType__)

        self.registerItem(item)
        print "self.builtItems:" + str(self.builtItems.keys())
        item.jsonDecode(self, jsonData)
        return item

    def registerItem(self, item):
        self.builtItems[item.getName()] = item
