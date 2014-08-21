"""Kraken - objects.component module.

Classes:
Component -- Component representation.

"""

from kraken.core.maths import *
from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.components.component_input import ComponentInput
from kraken.core.objects.components.component_output import ComponentOutput
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.attributes.base_attribute import BaseAttribute


class BaseComponent(SceneItem):
    """Kraken Base Component object."""

    __kType__ = "Component"

    def __init__(self, name, parent=None, side='M'):
        super(BaseComponent, self).__init__(name, parent)
        self.side = side
        self.inputs = []
        self.outputs = []
        self.operators = []

        self.setShapeVisibility(False)

        inputHrc = HierarchyGroup('inputs')
        inputAttrGrp = AttributeGroup('inputAttrs')
        inputHrc.addAttributeGroup(inputAttrGrp)
        self.addChild(inputHrc)

        outputHrc = HierarchyGroup('outputs')
        outputAttrGrp = AttributeGroup('outputAttrs')
        outputHrc.addAttributeGroup(outputAttrGrp)
        self.addChild(outputHrc)


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


    # =============
    # Name methods
    # =============
    def getComponentName(self):
        """Returns the name of the component used on self and all objects owned by the component

        Return:
        String, build name of the object.

        """

        return self.getName() + '_' + self.getSide()


    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """

        return self.getComponentName() + '_cmp'


    # ==============
    # Child Methods
    # ==============
    def addChild(self, child):
        super(BaseComponent, self).addChild(child)

        # Assign the child self as the component.
        child.setComponent(self)

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


    def addInput(self, inputObject):
        """Add inputObject to this object.

        Arguments:
        inputObject -- Object, input object to add.

        Return:
        True if successful.

        """

        inputHrc = self.getChildByName('inputs')
        inputAttrsGrp = inputHrc.getAttributeGroupByName('inputAttrs')

        if not isinstance(inputObject, (Locator, BaseAttribute)):
            raise Exception("'inputObject' argument is not a valid object. "
                + inputObject.getName() + " is of type:" + str(inputObject)
                + ". Must be an instance of 'Locator' or 'BaseAttribute'.")

        if inputObject in self.inputs:
            raise Exception("'inputObject' argument is already an input! Invalid object: '"
                + inputObject.getName() + "'")

        if isinstance(inputObject, Locator):
            inputHrc.addChild(inputObject)
            inputObject.setShapeVisibility(False)

        elif isinstance(inputObject, BaseAttribute):
            inputAttrsGrp.attributes.append(inputObject)
            inputObject.setParent(inputAttrsGrp)

        componentInput = ComponentInput(inputObject.getName(), inputObject)
        self.inputs.append(componentInput)

        # Assign the componentInput self as the component.
        componentInput.setComponent(self)

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
            if eachInput.getName() == name:
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
            if eachInput.getName() == name:
                return eachInput

        return None


    # ===============
    # Output Methods
    # ===============
    def checkOutputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, output index to check.

        """

        if index > len(self.outputs):
            raise IndexError("'" + str(index) + "' is out of the range of 'outputs' array.")

        return True


    def addOutput(self, outputObject):
        """Add outputObject to this object.

        Arguments:
        outputObject -- Object, input object to add.

        Return:
        True if successful.

        """

        outputHrc = self.getChildByName('outputs')
        outputAttrsGrp = outputHrc.getAttributeGroupByName('outputAttrs')

        if not isinstance(outputObject, (SceneItem, BaseAttribute)):
            raise Exception("'outputObject' argument is not a valid object. "
                + outputObject.getName() + " is of type:" + str(outputObject)
                + ". Must be an instance of 'SceneItem' or 'BaseAttribute'.")

        if outputObject in self.outputs:
            raise Exception("'outputObject' argument is already an output! Invalid object: '"
                + outputObject.getName() + "'")

        if isinstance(outputObject, SceneItem):
            outputHrc.addChild(outputObject)
            outputObject.setShapeVisibility(False)

        elif isinstance(outputObject, BaseAttribute):
            outputAttrsGrp.attributes.append(outputObject)
            outputObject.setParent(outputAttrsGrp)

        componentOutput = ComponentOutput(outputObject.getName(), outputObject)
        self.outputs.append(componentOutput)

        # Assign the componentOutput self as the component.
        componentOutput.setComponent(self)

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
            if eachOutput.getName() == name:
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
            if eachOutput.getName() == name:
                return eachOutput

        return None


    # =================
    # Operator Methods
    # =================
    def checkOperatorIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, operator index to check.

        """

        if index > len(self.operators):
            raise IndexError("'" + str(index) + "' is out of the range of the 'children' array.")

        return True


    def addOperator(self, operator):
        """Adds a operator to this object.

        Arguments:
        operator -- Object, object that will be a operator of this object.

        Return:
        True if successful.

        """

        if operator.name in [x.name for x in self.operators]:
            raise IndexError("Operator with " + operator.name + " already exists as a operator.")

        self.operators.append(operator)
        operator.setParent(self)

        return True


    def removeOperatorByIndex(self, index):
        """Removes a operator from this object by index.

        Arguments:
        index -- Integer, index of operator to remove.

        Return:
        True if successful.

        """

        if self.checkOperatorIndex(index) is not True:
            return False

        del self.operators[index]

        return True


    def removeOperatorByName(self, name):
        """Removes a operator from this object by name.

        Arguments:
        name -- String, name of operator to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachOperator in enumerate(self.operators):
            if eachOperator.getName() == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid operator of this object.")

        self.removeOperatorByIndex(removeIndex)

        return True


    def getNumOperators(self):
        """Returns the number of operators this object has.

        Return:
        Integer, number of operators of this object.

        """

        return len(self.operators)


    def getOperatorByIndex(self, index):
        """Returns the operator object at specified index.

        Return:
        Operator object at specified index.

        """

        if self.checkOperatorIndex(index) is not True:
            return False

        return self.operators[index]


    def getOperatorByName(self, name):
        """Returns the operator object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachOperator in self.operators:
            if eachOperator.getName() == name:
                return eachOperator

        return None


    def getOperatorByType(self, childType):
        """Returns all children that are of the specified type.

        Arguments:
        childType -- Type, the object type to search for.

        Return:
        Array of operator objects of the specified type.
        None if no objects of specified type are found.

        """

        childrenOfType = []
        for eachOperator in self.operators:
            if isinstance(eachOperator, childType):
                childrenOfType.append(eachOperator)

        return childrenOfType


    def getOperatorIndex(self, operator):
        """Return the index of the specified operator.

        Arguments:
        operator -- Object, operator to find the index of.

        Return:
        True if successful.
        None if operator not found on component.

        """

        for index, eachOp in xrange(self.getNumOperators()):
            if eachOp is operator:
                return index

        return None


    def moveOperatorToIndex(self, operator, index):
        """Moves an operator to the specified index.

        Arguments:
        operator -- Object, operator to move.
        index -- Integer, index position to move the operator to.

        Return:
        True if successful.

        """

        oldIndex = self.getOperatorIndex(operator)
        self.operators.insert(index, self.operators.pop(oldindex))

        return True