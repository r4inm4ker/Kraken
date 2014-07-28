"""KrakenLoader - objects.kraken_loader module.

Classes:
KrakenLoader - Factory for building SceneItems.

"""

from kraken.core.maths.vec import Vec2, Vec3, Vec4
from kraken.core.maths.rotation import Euler, Quat
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.matrix import Matrix33, Matrix44

from container import Container
from curve import Curve
from hierarchy_group import HierarchyGroup
from joint import Joint
from layer import Layer
from locator import Locator
from scene_item import SceneItem

from attributes.attribute_group import AttributeGroup
# from attributes.base_attribute import BaseAttribute
from attributes.bool_attribute import BoolAttribute
from attributes.float_attribute import FloatAttribute
from attributes.integer_attribute import IntegerAttribute
from attributes.string_attribute import StringAttribute

from components import * 

from controls.arrow_control import ArrowControl
from controls.arrows_control import ArrowsControl
from controls.circle_control import CircleControl
from controls.cube_control import CubeControl
from controls.null_control import NullControl
from controls.pin_control import PinControl
from controls.sphere_control import SphereControl
from controls.square_control import SquareControl
from controls.triangle_control import TriangleControl
from controls.base_control import BaseControl

from constraints.orientation_constraint import OrientationConstraint
from constraints.pose_constraint import PoseConstraint
from constraints.position_constraint import PositionConstraint
from constraints.scale_constraint import ScaleConstraint


# from operators import * 

class KrakenLoader(object):
    """Kraken base object type for any 3D object."""


    def __init__(self):
        super(KrakenLoader, self).__init__()

        # A dictionary of all the built elements during loading.
        self.parentItem = None
        self.builtItems = {}
        self.callbacks = {}

    def decodeValue(self, jsonData):
        """Returns a constructed math value based on the provided json data.

        Return:
        The constructed math value

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

    def getParentItem(self):
        return self.parentItem

    def resolveSceneItem(self, name):
        """Returns a constructed scene item based on the provided name.

        Return:
        The resolved scene item.

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
        if '__typeHierarchy__' not in jsonData or 'name' not in jsonData:
            raise Exception("Invalid JSON data for constructing scene item:" + str(jsonData));

        ##########################
        ## Controls.

        if "ArrowControl" in jsonData['__typeHierarchy__']:
            item = ArrowControl(jsonData['name'])

        elif "ArrowsControl" in jsonData['__typeHierarchy__']:
            item = ArrowsControl(jsonData['name'])

        elif "CircleControl" in jsonData['__typeHierarchy__']:
            item = CircleControl(jsonData['name'])

        elif "CubeControl" in jsonData['__typeHierarchy__']:
            item = CubeControl(jsonData['name'])

        elif "NullControl" in jsonData['__typeHierarchy__']:
            item = NullControl(jsonData['name'])

        elif "PinControl" in jsonData['__typeHierarchy__']:
            item = PinControl(jsonData['name'])

        elif "SphereControl" in jsonData['__typeHierarchy__']:
            item = SphereControl(jsonData['name'])

        elif "SquareControl" in jsonData['__typeHierarchy__']:
            item = SquareControl(jsonData['name'])

        elif "TriangleControl" in jsonData['__typeHierarchy__']:
            item = TriangleControl(jsonData['name'])

        elif "BaseControl" in jsonData['__typeHierarchy__']:
            item = BaseControl(jsonData['name'])

        ##########################
        ## Attributes.

        elif "AttributeGroup" in jsonData['__typeHierarchy__']:
            item = AttributeGroup(jsonData['name'])

        elif "BoolAttribute" in jsonData['__typeHierarchy__']:
            item = BoolAttribute(jsonData['name'])

        elif "FloatAttribute" in jsonData['__typeHierarchy__']:
            item = FloatAttribute(jsonData['name'])

        elif "IntegerAttribute" in jsonData['__typeHierarchy__']:
            item = IntegerAttribute(jsonData['name'])

        elif "StringAttribute" in jsonData['__typeHierarchy__']:
            item = StringAttribute(jsonData['name'])

        elif "Attribute" in jsonData['__typeHierarchy__']:
            item = Attribute(jsonData['name'])

        elif "ComponentInput" in jsonData['__typeHierarchy__']:
            item = ComponentInput(jsonData['name'])

        elif "ComponentOutput" in jsonData['__typeHierarchy__']:
            item = ComponentOutput(jsonData['name'])

        ##########################
        ## Constraints.

        elif "OrientationConstraint" in jsonData['__typeHierarchy__']:
            item = OrientationConstraint(jsonData['name'])

        elif "PoseConstraint" in jsonData['__typeHierarchy__']:
            item = PoseConstraint(jsonData['name'])

        elif "PositionConstraint" in jsonData['__typeHierarchy__']:
            item = PositionConstraint(jsonData['name'])

        elif "ScaleConstraint" in jsonData['__typeHierarchy__']:
            item = ScaleConstraint(jsonData['name'])

        elif "BaseConstraint" in jsonData['__typeHierarchy__']:
            item = BaseConstraint(jsonData['name'])


        ##########################
        ## Constraints.

        elif "Operator" in jsonData['__typeHierarchy__']:
            item = Operator(jsonData['name'])

        elif "OperatorBinding" in jsonData['__typeHierarchy__']:
            item = OperatorBinding(jsonData['name'])

        ##########################
        ## SceneItems.

        elif "Group" in jsonData['__typeHierarchy__']:
            item = Group(jsonData['name'])

        elif "Null" in jsonData['__typeHierarchy__']:
            item = Null(jsonData['name'])

        elif "Control" in jsonData['__typeHierarchy__']:
            item = Control(jsonData['name'])

        elif "Chain" in jsonData['__typeHierarchy__']:
            item = Chain(jsonData['name'])

        elif "Joint" in jsonData['__typeHierarchy__']:
            item = Joint(jsonData['name'])

        elif "Container" in jsonData['__typeHierarchy__']:
            item = Container(jsonData['name'])

        elif "Curve" in jsonData['__typeHierarchy__']:
            item = Curve(jsonData['name'])

        elif "HierarchyGroup" in jsonData['__typeHierarchy__']:
            item = HierarchyGroup(jsonData['name'])

        elif "Joint" in jsonData['__typeHierarchy__']:
            item = Joint(jsonData['name'])

        elif "Layer" in jsonData['__typeHierarchy__']:
            item = Layer(jsonData['name'])

        elif "Locator" in jsonData['__typeHierarchy__']:
            item = Locator(jsonData['name'])

        elif "SceneItem" in jsonData['__typeHierarchy__']:
            item = SceneItem(jsonData['name'])

        else:
            raise Exception("KrakenLoader does not support the given type:" + __kType__)

        self.registerItem(item)
        # Store the item as the parent item before decoding the object
        # which in turn decodes the children items. 
        self.parentItem = item
        item.jsonDecode(self, jsonData)

        # Fire any registered callbacks for this item. 
        # This enables the loading of objects already created,
        # but dependent on this object to be completed.
        if item.getName() in self.callbacks:
            for callback in self.callbacks[item.getName()]:
                callback(item)

        return item

    def registerItem(self, item):
        self.builtItems[item.getName()] = item

    def registerConstructionCallback(self, name, callback):
        """Register a callback to be invoked when the requested item is constructed.

        Return:
        None

        """

        if name in self.builtItems:
            callback(self.builtItems[name])
        else:
            if name not in self.callbacks:
                self.callbacks[name] = []
            self.callbacks[name].append(callback)