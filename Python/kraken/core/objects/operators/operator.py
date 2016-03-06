"""Kraken - objects.operators.operator module.

Classes:
Operator - Base operator object.

"""

from kraken.core.objects.scene_item import SceneItem


class Operator(SceneItem):
    """Operator representation."""

    def __init__(self, name, parent=None):
        super(Operator, self).__init__(name, parent)

        self.inputs = {}
        self.outputs = {}


    # ==============
    # Input Methods
    # ==============


    def resizeInput(self, name, count):
        """Resizes and array output to a given size.

        Args:
            name (str): Name of the output.
            count (Object): Output object.

        Returns:
            bool: True if successful.

        """

        if name not in self.inputs:
            raise Exception("Input with name '" + name + "' was not found in operator: " + self.getName() + ".")

        if isinstance(self.inputs[name], list):
            self.inputs.resize(count)
        else:
            raise Exception("Output is not an array output: " + name + ".")

        return True


    def setInput(self, name, operatorInput, index=0):
        """Sets the input by the given name.

        Args:
            name (str): Name of the input.
            operatorInput (Object): Input object.

        Returns:
            bool: True if successful.

        """

        if name not in self.inputs:
            raise Exception("Input with name '" + name + "' was not found in operator: " + self.getName() + ".\nValid inputs are:\n" + "\n".join(self.inputs.keys()))

        if isinstance(self.inputs[name], list):
            # Set the entire output array
            if isinstance(operatorInput, list):
                self.inputs[name] = operatorInput
            else:
                if index >= len(self.inputs[name]):
                    raise Exception("Out of range index for array output index: " + str(index) + " size: " + str(len(self.inputs[name])) + ".")
                self.inputs[name][index] = operatorInput
        else:
            self.inputs[name] = operatorInput

        return True


    def getInput(self, name):
        """Returns the input with the specified name.

        Args:
            name (str): Name of the input to get.

        Returns:
            object: Input object.

        """

        if name not in self.inputs:
            raise Exception("Input with name '" + name + "' was not found in operator: " + self.getName() + ".")

        return self.inputs[name]


    def getInputNames(self):
        """Returns the names of all inputs.

        Returns:
            list: Names of all inputs.

        """

        return self.inputs.keys()


    # ==============
    # Output Methods
    # ==============

    def resizeOutput(self, name, count):
        """Resizes and array output to a given size.

        Args:
            name (str): Name of the output.
            count (Object): Output object.

        Returns:
            bool: True if successful.

        """

        if name not in self.outputs:
            raise Exception("Output with name '" + name + "' was not found in operator: " + self.getName() + ".")

        if isinstance(self.outputs[name], list):
            self.outputs.resize(count)
        else:
            raise Exception("Output is not an array output: " + name + ".")

        return True


    def setOutput(self, name, operatorOutput, index=0):
        """Sets the output by the given name.

        Args:
            name (str): Name of the output.
            operatorOutput (Object): Output object.

        Returns:
            bool: True if successful.

        """

        if name not in self.outputs:
            raise Exception("Output with name '" + name + "' was not found in operator: " + self.getName() + ".")

        if isinstance(self.outputs[name], list):
            # Set the entire output array
            if isinstance(operatorOutput, list):
                self.outputs[name] = operatorOutput
            else:
                if index >= len(self.outputs[name]):
                    raise Exception("Out of range index for array output index: " + str(index) + " size: " + str(len(self.outputs[name])) + ".")
                self.outputs[name][index] = operatorOutput
        else:
            self.outputs[name] = operatorOutput

        return True


    def getOutput(self, name):
        """Returns the output with the specified name.

        Args:
            name (str): Name of the output to get.

        Returns:
            Object: Output object.

        """

        if name not in self.outputs.keys():
            raise Exception("Output with name '" + name + "' was not found in operator: " + self.getName() + ".")

        return self.outputs[name]


    def getOutputNames(self):
        """Returns the names of all outputs.

        Returns:
            list: Names of all outputs.

        """

        return self.outputs.keys()

