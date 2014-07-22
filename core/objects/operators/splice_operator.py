"""Kraken - objects.operators.base_operator module.

Classes:
BaseOperator - Base operator object.

"""

from kraken.core.objects.operators.base_operator import BaseOperator


class SpliceOperator(BaseOperator):
    """Base Operator representation."""

    __kType__ = "SpliceOperator"

    def __init__(self, name):
        super(BaseOperator, self).__init__(name)
        self.inputPorts = []
        self.outputPorts = []


    def addInputPort(self, name, dataType, targets, extension=""):
        """Adds a port to the splice operator.

        Arguments:
        name -- String, name of the port.
        dataType -- String, data type of the port.
        target -- Object / list of objects, target objects for the port.

        Return:
        True if successful.

        """

        portData = {
                     "portType": "input",
                     "name": name,
                     "dataType": dataType,
                     "targets": targets,
                     "extension": extension
                   }

        self.ports.append()

        return True


    def addParameter(self, name, dataType):
        """Adds a parameter to the splice operator.

        Arguments:
        name -- String, name of the parameter.
        dataType -- String, data type of the parameter.

        Return:
        True if successful.

        """

        parameterData = {
                          "portName": name,
                          "dataType": dataType
                        }

        return parameterData


    def buildJSON(self):
        """Builds JSON string to feed into the Splice commands to build the operator
        in the DCC.

        Return:
        String, JSON data to pass to the splice command.

        """

        spliceJSON = ""

        return spliceJSON