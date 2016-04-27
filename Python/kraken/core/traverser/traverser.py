"""Kraken - traverser.traverser module.

Classes:
Traverser - Base Traverser.

"""

from kraken.core.objects.scene_item import SceneItem
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


    def traverse(self, itemCallback = None, discoverCallback = None):
        """Visits all objects within this Traverser based on the root items.

        Args:
            itemCallback (func): A callback function to be invoked for each item visited.
            discoverCallback (func): A callback to return an array of children for each item.
        """

        self.reset()

        if discoverCallback is None:
            discoverCallback = self.__discoverBySource

        for item in self._rootItems:
            self.__visitItem(item, itemCallback, discoverCallback)


    def __visitItem(self, item, itemCallback, discoverCallback):

        if self._visited.get(item.getId(), False):
            return False

        if discoverCallback:
            discoveredItems = discoverCallback(item)
            for discoveredItem in discoveredItems:
                self.__visitItem(discoveredItem, itemCallback, discoverCallback)

        if not itemCallback is None:
            itemCallback(item = item, traverser = self)

        self._visited[item.getId()] = True
        self._items.append(item)

        return True


    def __discoverBySource(self, item):
        result = []

        if not item.getSource() is None:
            result.append(item.getSource())

        if not item.getParent() is None and not item.getParent() == item.getSource():
            result.append(item.getParent())

        if isinstance(item, Constraint):
            for constrainer in item.getConstrainers():
                result.append(constrainer)

        if isinstance(item, Operator):
            for inputName in item.getInputNames():
                operatorInput = item.getInput(inputName)
                if not isinstance(operatorInput, list):
                    operatorInput = [operatorInput]
                for inputItem in operatorInput:
                    if isinstance(inputItem, SceneItem):
                        result.append(inputItem)
                
        return result
