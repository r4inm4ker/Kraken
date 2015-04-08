"""KrakenLoader - objects.kraken_loader module.

Classes:
KrakenLoader - Factory for building SceneItems.

"""

from kraken.core.maths import Vec2, Vec3, Vec4, Quat, Xfo
# from kraken.core.maths.matrix import Matrix33, Matrix44

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.container import Container
from kraken.core.objects.curve import Curve
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.joint import Joint
from kraken.core.objects.layer import Layer
from kraken.core.objects.locator import Locator
from kraken.core.objects.control import Control

from kraken.core.objects.attributes.attribute_group import AttributeGroup
# from kraken.core.objects.attributes.base_attribute import BaseAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.components import *

from kraken.core.objects.constraints.orientation_constraint import OrientationConstraint
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.constraints.position_constraint import PositionConstraint
from kraken.core.objects.constraints.scale_constraint import ScaleConstraint


# from operators import *

class KrakenLoader(object):
    """Kraken base object type for any 3D object."""


    def __init__(self):
        super(KrakenLoader, self).__init__()

        # A dictionary of all the built elements during loading.
        self.builtItems = {}
        # the most recent item build during loading. This item is the parent
        # of subsequently built items.
        self.parentItems = []
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
            val = Vec2()
            val.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Vec3':
            val = Vec3()
            val.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Vec4':
            val = Vec4()
            val.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Euler':
            val = Euler()
            val.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Quat':
            val = Quat()
            val.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Xfo':
            val = Xfo()
            val.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Matrix33':
            val = Matrix33()
            val.jsonDecode(jsonData, self)
        elif jsonData['__class__'] == 'Matrix44':
            val = Matrix44()
            val.jsonDecode(jsonData, self)
        else:
            raise Exception("Unsupported Math type:" + jsonData['__class__'])

        return val


    def getParentItem(self):
        """Returns the item that was constructed prior to the current item.

        Return:
        The stored parent item.

        """

        if len(self.parentItems) < 2:
            return None

        return self.parentItems[-2]


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

        # =========
        # Controls
        # =========
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

        # ===========
        # Attributes
        # ===========
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

        # ============
        # Constraints
        # ============
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


        # ==========
        # Operators
        # ==========
        elif "Operator" in jsonData['__typeHierarchy__']:
            item = Operator(jsonData['name'])

        elif "OperatorBinding" in jsonData['__typeHierarchy__']:
            item = OperatorBinding(jsonData['name'])


        # ============
        # Scene Items
        # ============
        elif "Group" in jsonData['__typeHierarchy__']:
            item = Group(jsonData['name'])

        elif "Null" in jsonData['__typeHierarchy__']:
            item = Null(jsonData['name'])

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

        # Before registering or decoding, set the parent so that the full name contains the entire path. 
        if len(self.parentItems) > 0:
            item.setParent(self.parentItems[-1])

        self.registerItem(item)
        # Store the item as the parent item before decoding the object
        # which in turn decodes the children items.
        self.parentItems.append(item)
        
        item.jsonDecode(self, jsonData)

        # Pop the parent item stack, which reverts the current parent item
        # to the previous value.
        self.parentItems.pop()

        return item


    def registerItem(self, item):
        """Register an item to the loader. If an item is constructed automatically,
        then it can be registered so the loader can provide it during resolveSceneItem.

        Return:
        None

        """
        if item.getFullName() in self.builtItems:
            # TODO: resolve using a path, instead of the name.
            # This will require that all items have a parent specified
            print "Warning. Non unique names used in Kraken:" + item.getFullName()

        self.builtItems[item.getFullName()] = item

        # Fire any registered callbacks for this item.
        # This enables the loading of objects already created,
        # but dependent on this object to be completed.
        if item.getFullName() in self.callbacks:
            for callback in self.callbacks[item.getFullName()]:
                callback(item)


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