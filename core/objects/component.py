"""Kraken - objects.component module.

Classes:
Component -- Component representation.

"""

from kraken.core.maths import *
from kraken.core.objects.scene_item import SceneItem


class BaseComponent(SceneItem):
    """Kraken Base Component object."""

    __kType__ = "Component"

    def __init__(self, name, parent=None, side='M'):
        super(BaseComponent, self).__init__(name, parent)
        self.side = side
        self.inputs = []
        self.outputs = []

        self.setShapeVisibility(False)


    # =============
    # Side Methods
    # =============
    def getSide(self):
        """Returns the side of the component as a string.

        Return:
        String, the side of the component.

        """

        return self.side


    def setSide(self, side):
        """Sets the side of the component.

        Arguments:
        side -- String, side that the component is on. Valid values: L, M, R.

        Return:
        True if successful.

        """

        if side not in ['L', 'M', 'R']:
            raise ValueError("'" + side + "' is not a valid side.")

        self.side = side

        return True


    # ==============
    # Input Methods
    # ==============
    def addInput(self, componentInput):
        """Add ComponentInput to this object.

        Arguments:
        componentInput -- ComponentInput, input object to add.

        Return:
        True if successful.

        """

        # TODO: Check if input already part of object.
        self.inputs.append(componentInput)

        return True


    def removeInputByIndex(self, index):
        """Remove ComponentInput at specified index.

        Arguments:
        index -- Integer, index of the ComponentInput to remove.

        Return:
        True if successful.

        """

        # TODO: Check if index is valid, then remove.

        return True


    # ==============
    # Output Methods
    # ==============
    def addOutput(self, componentOutput):
        """Add ComponentOutput to this object.

        Arguments:
        output -- ComponentOutput, output object to add.

        Return:
        True if successful.

        """

        # TODO: Check if output already part of object.
        self.outputs.append(componentOutput)

        return True


    def removeOutputByIndex(self, index):
        """Remove ComponentOutput at specified index.

        Arguments:
        index -- Integer, index of the ComponentOutput to remove.

        Return:
        True if successful.

        """

        # TODO: Check if index is valid, then remove.

        return True


    def addOperatorBinding(self, operatorBinding):
        """Adds an operator binding to the component.

        Arguments:
        operatorBinding -- Object, the operator binding object to add to the component.

        Return:
        True if successful.

        """

        return True