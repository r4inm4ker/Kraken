"""Kraken - objects.operators.base_operator module.

Classes:
BaseOperator - Base operator object.

"""


class BaseOperator(object):
    """Base Operator representation."""

    __kType__ = "Operator"

    def __init__(self, name):
        super(BaseOperator, self).__init__()
        self.name = name
        self.parent = None
        self.inputs = []
        self.outputs = []


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the parent of the object as an object.

        Return:
        Parent of this object.

        """

        return self.parent


    def setParent(self, parent):
        """Sets the parent attribute of this object.

        Arguments:
        parent -- Object, object that is the parent of this one.

        Return:
        True if successful.

        """

        self.parent = parent

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
            raise IndexError("'" + str(index) + "' is out of the range of the 'inputs' array.")

        return True


    def addInput(self, operatorInput):
        """Adds an input to this operator.

        Arguments:
        operatorInput -- Object, kraken object to add as an input.

        Return:
        True if successful.

        """

        self.inputs.append(operatorInput)

        return True


    def removeInputByIndex(self, index):
        """Removes a child from this object by index.

        Arguments:
        index -- Integer, index of child to remove.

        Return:
        True if successful.

        """

        if self.checkInputIndex(index) is not True:
            return False

        del self.inputs[index]

        return True


    def removeInputByName(self, name):
        """Removes a child from this object by name.

        Arguments:
        name -- String, name of child to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachInput in enumerate(self.inputs):
            if eachInput.getName() == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid child of this object.")

        self.removeInputByIndex(removeIndex)

        return True


    def getNumInputs(self):
        """Returns the number of children this object has.

        Return:
        Integer, number of children of this object.

        """

        return len(self.inputs)


    def getInputByIndex(self, index):
        """Returns the child object at specified index.

        Return:
        Input object at specified index.

        """

        if self.checkInputIndex(index) is not True:
            return False

        return self.inputs[index]


    def getInputByName(self, name):
        """Returns the child object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachInput in self.inputs:
            if eachInput.getName() == name:
                return eachInput

        return None


    def getInputIndex(self, input):
        """Return the index of the specified input.

        Arguments:
        input -- Object, input to find the index of.

        Return:
        True if successful.
        None if input not found on component.

        """

        for index, eachOp in xrange(self.getNumInputs()):
            if eachOp is input:
                return index

        return None


    def moveInputToIndex(self, input, index):
        """Moves an input to the specified index.

        Arguments:
        input -- Object, input to move.
        index -- Integer, index position to move the input to.

        Return:
        True if successful.

        """

        oldIndex = self.getInputIndex(input)
        self.inputs.insert(index, self.inputs.pop(oldindex))

        return True


    # ==============
    # Output Methods
    # ==============
    def checkOutputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, output index to check.

        """

        if index > len(self.outputs):
            raise IndexError("'" + str(index) + "' is out of the range of the 'outputs' array.")

        return True


    def addOutput(self, operatorOutput):
        """Adds an output to this operator.

        Arguments:
        operatorOutput -- Object, kraken object to add as an output.

        Return:
        True if successful.

        """

        self.outputs.append(operatorOutput)

        return True


    def removeOutputByIndex(self, index):
        """Removes a output from this object by index.

        Arguments:
        index -- Integer, index of output to remove.

        Return:
        True if successful.

        """

        if self.checkOutputIndex(index) is not True:
            return False

        del self.outputs[index]

        return True


    def removeOutputByName(self, name):
        """Removes a child from this object by name.

        Arguments:
        name -- String, name of child to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachOutput in enumerate(self.outputs):
            if eachOutput.getName() == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid child of this object.")

        self.removeOutputByIndex(removeIndex)

        return True


    def getNumOutputs(self):
        """Returns the number of children this object has.

        Return:
        Integer, number of children of this object.

        """

        return len(self.outputs)


    def getOutputByIndex(self, index):
        """Returns the child object at specified index.

        Return:
        Output object at specified index.

        """

        if self.checkOutputIndex(index) is not True:
            return False

        return self.outputs[index]


    def getOutputByName(self, name):
        """Returns the child object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachOutput in self.outputs:
            if eachOutput.getName() == name:
                return eachOutput

        return None


    def getOutputIndex(self, output):
        """Return the index of the specified output.

        Arguments:
        output -- Object, output to find the index of.

        Return:
        True if successful.
        None if output not found on component.

        """

        for index, eachOp in xrange(self.getNumOutputs()):
            if eachOp is output:
                return index

        return None


    def moveOutputToIndex(self, output, index):
        """Moves an output to the specified index.

        Arguments:
        output -- Object, output to move.
        index -- Integer, index position to move the output to.

        Return:
        True if successful.

        """

        oldIndex = self.getOutputIndex(output)
        self.outputs.insert(index, self.outputs.pop(oldindex))

        return True