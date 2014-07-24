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
        self.inputs = {}
        self.outputs = {}


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
    def setInput(self, name, operatorInput):
        """Sets the input by the given name.

        Arguments:
        name -- String, name of the input.
        operatorInput -- Object, input object.

        Return:
        True if successful.

        """

        self.inputs[name] = operatorInput

        return True


    def getInput(self, name):
        """Returns the input with the specified name.

        Arguments:
        name -- String, name of the input to get.

        Return:
        Object, input object.

        """

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

        self.outputs[name] = operatorOutput

        return True


    def getOutput(self, name):
        """Returns the output with the specified name.

        Arguments:
        name -- String, name of the output to get.

        Return:
        Object, output object.

        """

        return self.outputs[name]