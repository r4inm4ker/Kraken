"""Kraken - objects.component module.

Classes:
Component -- Component representation.

"""

from kraken.core.maths import *
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.layer import Layer
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.components.component_input import ComponentInput
from kraken.core.objects.components.component_output import ComponentOutput
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.attribute import Attribute


class Component(Object3D):
    """Kraken Component object."""

    def __init__(self, name, parent=None, location='M'):
        super(Component, self).__init__(name, parent)
        self.location = location
        self.inputs = []
        self.outputs = []
        self.operators = []

        self.setShapeVisibility(False)

        self.lockRotation(x=True, y=True, z=True)
        self.lockScale(x=True, y=True, z=True)
        self.lockTranslation(x=True, y=True, z=True)


    # =============
    # Side Methods
    # =============
    def getLocation(self):
        """Returns the location of the component as a string.

        Return:
        String, the location of the component.

        """

        return self.location


    def setLocation(self, location):
        """Sets the location of the component.

        Arguments:
        location -- String, location that the component is on. Valid values: L,
                            M, R.

        Return:
        True if successful.

        """

        self.location = location

        return True


    # =============
    # Name methods
    # =============
    def getComponentName(self):
        """Returns the name of the component used on self and all objects owned
        by the component

        Return:
        String, build name of the object.

        """

        return self.getName() + '_' + self.getLocation()


    # =============
    # Layer methods
    # =============
    def getLayer(self, name):
        """Retrieves a layer from the owning container, or generates a layer
        (and warning message)

        Return:
        Layer, the layer from the container, or generated layer.

        """

        container = self.getContainer()
        if container is None:
            container = self

        layer = container.getChildByName(name)
        if layer is None or not layer.isTypeOf('Layer'):
            raise KeyError("Layer '" + + "' was not found!")

        return layer


    def getOrCreateLayer(self, name):
        """Retrieves a layer from the owning container, or generates a layer (and warning message)

        Return:
        Layer, the layer from the container, or generated layer.

        """

        container = self.getContainer()
        if container is None:
            container = self

        layer = container.getChildByName(name)
        if layer is None or not layer.isTypeOf('Layer'):
            layer = Layer(name, parent=container)

        return layer


    # ==============
    # Child Methods
    # ==============
    def addChild(self, child):
        """Adds a child to the component and sets the object's component
        attribute.

        Arguments:
        child -- Object, object to add as a child.

        Return:
        True if successful.

        """

        super(Component, self).addChild(child)

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


    def addInput(self, name, dataType):
        """Add inputObject to this object.

        Arguments:
        name -- String, name of the input to create.
        dataType -- String, data type of the input.

        Return:
        New input object.

        """

        if inputObject.getTypeName() == "ComponentInput":
            raise Exception("'inputObject' argument is not a ComponentInput.")

        if inputObject in self.inputs:
            raise Exception("'inputObject' argument is already an input! Invalid object: '"
                + inputObject.getName() + "'")

        componentInput = ComponentInput(name, parent=self, dataType=dataType)

        self.inputs.append(componentInput)

        return componentInput


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


    def addOutput(self, name, dataType):
        """Add outputObject to this object.

        Arguments:
        name -- String, name of the output to create.
        dataType -- String, data type of the output.

        Return:
        New output object.

        """

        if self.getOutputByName(name) is not None:
            raise Exception("'outputObject' argument is already an output!")

        componentOutput = ComponentOutput(name, parent=self, dataType=dataType)

        self.outputs.append(outputObject)

        return componentOutput


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
