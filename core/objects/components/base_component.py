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
    def checkInputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, input index to check.

        """

        if index > len(self.inputs):
            raise IndexError("'" + str(index) + "' is out of the range of 'inputs' array.")

        return True


    def addInput(self, componentInput):
        """Add ComponentInput to this object.

        Arguments:
        componentInput -- ComponentInput, input object to add.

        Return:
        True if successful.

        """

        if componentInput.getKType() != "ComponentInput":
            raise Exception("'componentInput' argument is not a 'ComponentInput' object. Invalid type:'" + componentInput.getKType() + "'")

        if componentInput in self.inputs:
            raise Exception("'componentInput' argument is already an input! Invalid object: '" + componentInput.getName() + "'")

        self.inputs.append(componentInput)

        return True


    def removeInputByIndex(self, index):
        """Remove ComponentInput at specified index.

        Arguments:
        index -- Integer, index of the ComponentInput to remove.

        Return:
        True if successful.

        """

        if self.checkInputIndex(index) is not True:
            return False

        del self.inputs[index]

        return True


    def removeInputByName(self, name):
        """Removes a input from this object by name.

        Arguments:
        name -- String, name of input to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachInput in enumerate(self.inputs):
            if eachInput.name == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid input of this object.")

        self.removeInputByIndex(removeIndex)

        return True


    def getNumInputs(self):
        """Returns the number of inputs this component has.

        Return:
        Integer, number of inputs of this object.

        """

        return len(self.inputs)


    def getInputByIndex(self, index):
        """Returns the input object at specified index.

        Return:
        Input object at specified index.

        """

        if self.checkInputIndex(index) is not True:
            return False

        return self.inputs[index]


    def getInputByName(self, name):
        """Returns the input object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachInput in self.inputs:
            if eachInput.name == name:
                return eachInput

        return None


    # ==============
    # Output Methods
    # ==============
    def checkOutputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, output index to check.

        """

        if index > len(self.outputs):
            raise IndexError("'" + str(index) + "' is out of the range of 'outputs' array.")

        return True


    def addOutput(self, componentOutput):
        """Add ComponentOutput to this object.

        Arguments:
        output -- ComponentOutput, output object to add.

        Return:
        True if successful.

        """

        if componentOutput.getKType() != "ComponentOutput":
            raise Exception("'componentOutput' argument is not a 'ComponentOutput' object. Invalid type:'" + componentOutput.getKType() + "'")

        if componentOutput in self.outputs:
            raise Exception("'componentOutput' argument is already an input! Invalid object: '" + componentOutput.getName() + "'")

        self.outputs.append(componentOutput)

        return True


    def removeOutputByIndex(self, index):
        """Remove ComponentInput at specified index.

        Arguments:
        index -- Integer, index of the ComponentInput to remove.

        Return:
        True if successful.

        """

        if self.checkInputIndex(index) is not True:
            return False

        del self.outputs[index]

        return True


    def removeOutputByName(self, name):
        """Removes a output from this object by name.

        Arguments:
        name -- String, name of output to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachOutput in enumerate(self.outputs):
            if eachOutput.name == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid output of this object.")

        self.removeInputByIndex(removeIndex)

        return True


    def getNumOutputs(self):
        """Returns the number of outputs this component has.

        Return:
        Integer, number of outputs of this object.

        """

        return len(self.outputs)


    def getOutputByIndex(self, index):
        """Returns the output object at specified index.

        Return:
        Output object at specified index.

        """

        if self.checkOutputIndex(index) is not True:
            return False

        return self.outputs[index]


    def getOutputByName(self, name):
        """Returns the output object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachOutput in self.outputs:
            if eachOutput.name == name:
                return eachOutput

        return None


    # =========================
    # Operator Binding Methods
    # =========================
    def addOperatorBinding(self, operatorBinding):
        """Adds an operator binding to the component.

        Arguments:
        operatorBinding -- Object, the operator binding object to add to the component.

        Return:
        True if successful.

        """

        return True