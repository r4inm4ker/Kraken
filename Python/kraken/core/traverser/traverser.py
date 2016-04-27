"""Kraken - traverser.traverser module.

Classes:
Traverser - Base Traverser.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.components.component import Component
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.constraints.constraint import Constraint
from kraken.core.objects.operators.operator import Operator

class Traverser(object):
    """Kraken base traverser for any scene item."""

    def __init__(self, name = 'Traverser'):
        self._rootItems = []
        self.reset()
        self._items = []

    # ==================
    # Property Methods
    # ==================
    @property
    def rootItems(self):
        """Gets the root items of this Traverser.

        Returns:
            []: The root items of this Traverser.

        """

        return self._xfo


    def addRootItem(self, item):
        """Adds a new root object to this Traverser

        Args:
            item (SceneItem): The SceneItem to add as a root item.

        Returns:
            bool: True if successful.

        """

        for rootItem in self._rootItems:
            if rootItem.getId() == item.getId():
                return False

        self._rootItems.append(item)

        return True

    def addRootItems(self, items):
        """Adds a bunch of root items to this Traverser

        Args:
            items (SceneItem[]): The SceneItems to add as root items.

        Returns:
            bool: True if successful.

        """

        for item in items:
            self.addRootItem(item)

        return True


    @property
    def items(self):
        """Gets the traversed items of this Traverser.

        Returns:
            []: The traversed items of this Traverser.

        """

        return self._items


    def getItemsOfType(self, typeName):
        """Gets only the traversed items of a given type.

        Args:
            typeName (str): The name of the type to look for.

        Returns:
            []: The items in the total items list matching the given type.
        """

        result = []
        for item in self._items:
            if not item.isTypeOf(typeName):
                continue
            result.append(item)
        return result


    # =============
    # Traverse Methods
    # =============
    def reset(self):
        """Resets all internal structures of this Traverser.

        """

        self._visited = {}
        self._items = []


    def traverse(self, itemCallback = None, discoverCallback = None, discoveredItemsFirst = True):
        """Visits all objects within this Traverser based on the root items.

        Args:
            itemCallback (func): A callback function to be invoked for each item visited.
            discoverCallback (func): A callback to return an array of children for each item.
        """

        self.reset()

        if discoverCallback is None:
            discoverCallback = self.discoverBySource

        for item in self._rootItems:
            self.__visitItem(item, itemCallback, discoverCallback, discoveredItemsFirst)

        return self.items

    def __collectVisitedItem(self, item, itemCallback):
        if not itemCallback is None:
            itemCallback(item = item, traverser = self)
        self._items.append(item)

    def __visitItem(self, item, itemCallback, discoverCallback, discoveredItemsFirst):

        if self._visited.get(item.getId(), False):
            return False

        self._visited[item.getId()] = True

        sourcedByConstraintOrOperator = False
        if discoveredItemsFirst:
            for source in item.getSources():
                if isinstance(source, Constraint) or isinstance(source, Operator):
                    sourcedByConstraintOrOperator = True
                    break

        if not discoveredItemsFirst or sourcedByConstraintOrOperator:
            self.__collectVisitedItem(item, itemCallback)

        if discoverCallback:
            discoveredItems = discoverCallback(item)
            if discoveredItems:
                for discoveredItem in discoveredItems:
                    self.__visitItem(discoveredItem, itemCallback, discoverCallback, discoveredItemsFirst)

        if discoveredItemsFirst and not sourcedByConstraintOrOperator:
            self.__collectVisitedItem(item, itemCallback)

        return True

    def discoverChildren(self, item):
        result = []

        if isinstance(item, Component):
            result += item.getItems().values()
        
        if isinstance(item, Object3D):
            for i in xrange(item.getNumAttributeGroups()):
                if item.getAttributeGroupByIndex(i).getName() == 'implicitAttrGrp':
                    continue
                result.append(item.getAttributeGroupByIndex(i))
            result += item.getChildren()

        if isinstance(item, AttributeGroup):
            for i in xrange(item.getNumAttributes()):
                result.append(item.getAttributeByIndex(i))

        return result

    def discoverBySource(self, item):
        result = []

        for source in item.getSources():
            if isinstance(source, Operator):
                for outputName in source.getOutputNames():
                    operatorOutputs = source.getOutput(outputName)
                    if not isinstance(operatorOutputs, list):
                        operatorOutputs = [operatorOutputs]
                    for operatorOutput in operatorOutputs:
                        if not isinstance(operatorOutput, SceneItem):
                            continue
                        result.append(operatorOutput)

            result.append(source)

        return result
