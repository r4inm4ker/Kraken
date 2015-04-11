"""Kraken - objects.operators.operator module.

Classes:
Operator - Base operator object.

"""

from kraken.core.objects.base_item import BaseItem

class Operator(BaseItem):
    """Operator representation."""

    def __init__(self, name, parent=None):
        super(Operator, self).__init__(name, parent)

        self.inputs = {}
        self.outputs = {}


    # ==============
    # Input Methods
    # ==============
    def setInput(self, name, operatorInput):
        """Sets the input by the given name.

        Arguments:
        name -- String, name of the input.
        operatorInput -- Object, input object.

        Return:
        True if successful.

        """

        if name not in self.inputs:
            raise Exception("Input with name '" + name + "' was not found in operator: " + self.getName() + ".")

        if isinstance(self.inputs[name], list):
            self.inputs[name].append(operatorInput)
        else:
            self.inputs[name] = operatorInput

        return True


    def getInput(self, name):
        """Returns the input with the specified name.

        Arguments:
        name -- String, name of the input to get.

        Return:
        Object, input object.

        """

        if name not in self.inputs:
            raise Exception("Input with name '" + name + "' was not found in operator: " + self.getName() + ".")

        return self.inputs[name]


    # ==============
    # Output Methods
    # ==============
    def setOutput(self, name, operatorOutput):
        """Sets the output by the given name.

        Arguments:
        name -- String, name of the output.
        operatorOutput -- Object, output object.

        Return:
        True if successful.

        """

        if name not in self.outputs:
            raise Exception("Output with name '" + name + "' was not found in operator: " + self.getName() + ".")

        if isinstance(self.outputs[name], list):
            self.outputs[name].append(operatorOutput)
        else:
            self.outputs[name] = operatorOutput

        return True


    def getOutput(self, name):
        """Returns the output with the specified name.

        Arguments:
        name -- String, name of the output to get.

        Return:
        Object, output object.

        """

        if name not in self.outputs.keys():
            raise Exception("Output with name '" + name + "' was not found in operator: " + self.getName() + ".")

        return self.outputs[name]