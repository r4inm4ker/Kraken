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
        self.ioPorts = []
        self.klOperators = []


    # ===================
    # Input Port Methods
    # ===================
    def checkInputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, intput port index to check.

        """

        if index > len(self.inputPorts):
            raise IndexError("'" + str(index) + "' is out of the range of the 'inputPorts' array.")

        return True


    def addInputPort(self, portName, dataType, targets=None, arrayType="Single Value", autoInitObjects=True, extension=""):
        """Adds a port to the splice operator.

        Arguments:
        portName -- String, name of the port.
        dataType -- String, data type of the port.
        targets -- Object / list of objects, target objects for the port.
        arrayType -- String, Single Value or Multi Value (Maya Specific)
        autoInitObjects -- Boolean, whether or not to initialize the object when added.
        extension -- String, name of the KL Extension to load.

        Return:
        True if successful.

        """

        portData = {
                     "portType": "input",
                     "portName": portName,
                     "dataType": dataType,
                     "targets": targets,
                     "arrayType": arrayType,
                     "autoInitObjects": autoInitObjects,
                     "extension": extension
                   }

        self.ports.append(portData)

        return True


    def addParameter(self, portName, dataType):
        """Adds a parameter to the splice operator.

        Arguments:
        portName -- String, name of the parameter.
        dataType -- String, data type of the parameter.

        Return:
        True if successful.

        """

        parameterData = {
                          "portType": "parameter",
                          "portName": portName,
                          "dataType": dataType
                        }

        self.inputPorts.append(portData)

        return parameterData


    def getNumInputPorts(self):
        """Returns the number of input ports.

        Return:
        Integer, number of input ports on the operator.

        """

        return len(self.inputPorts)


    def removeInputPortByIndex(self, index):
        """Removes an input port by it's index.

        Arguments:
        index -- Integer, index of the output port to remove.

        Return:
        True if successful.

        """

        if self.checkInputIndex(index) is not True:
            return False

        del self.inputPorts[index]


    # ====================
    # Output Port Methods
    # ====================
    def checkOutputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, output port index to check.

        """

        if index > len(self.outputPorts):
            raise IndexError("'" + str(index) + "' is out of the range of the 'outputPorts' array.")

        return True


    def addOutputPort(self, portName, dataType, targets=None, arrayType="Single Value", autoInitObjects=True, extension=""):
        """Adds a port to the splice operator.

        Arguments:
        portName -- String, name of the port.
        dataType -- String, data type of the port.
        target -- Object / list of objects, target objects for the port.

        Return:
        True if successful.

        """

        portData = {
                     "portType": "output",
                     "portName": portName,
                     "dataType": dataType,
                     "targets": targets,
                     "arrayType": arrayType,
                     "autoInitObjects": autoInitObjects,
                     "extension": extension
                   }

        self.ports.append(portData)

        return True


    def getNumOutputPorts(self):
        """Returns the number of output ports.

        Return:
        Integer, number of output ports on the operator.

        """

        return len(self.outputPorts)


    def removeOutputPortByIndex(self, index):
        """Removes an output port by it's index.

        Arguments:
        index -- Integer, index of the output port to remove.

        Return:
        True if successful.

        """

        if self.checkOutputIndex(index) is not True:
            return False

        del self.outputPorts[index]


    # ================
    # IO Port Methods
    # ================
    def addIOPort(self, portName, dataType, targets=None, arrayType="Single Value", autoInitObjects=True, extension=""):
        """Adds a port to the splice operator.

        Arguments:
        portName -- String, name of the port.
        dataType -- String, data type of the port.
        target -- Object / list of objects, target objects for the port.

        Return:
        True if successful.

        """

        portData = {
                     "portType": "io",
                     "portName": portName,
                     "dataType": dataType,
                     "targets": targets,
                     "arrayType": arrayType,
                     "autoInitObjects": autoInitObjects,
                     "extension": extension
                   }

        self.ioPorts.append(portData)

        return True


    # =================
    # Operator Methods
    # =================
    def checkKLOperatorIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, KL Operator index to check.

        """

        if index > len(self.klOperators):
            raise IndexError("'" + str(index) + "' is out of the range of the 'klOperators' array.")

        return True


    def addKLOperator(self, opName, entry="", portMap=""):
        """Adds a KL Operator to the Splice Operator.

        Arguments:
        opName -- String, name of the operator to add.
        entry -- String, name of the entry function to use, defaults to opName.
        opName -- String, string to string dictionary which defines the portmapping.

        Return:
        True if successful.

        """

        operatorData = {
                    "opName": opName,
                    "entry": entry,
                    "portMap": portMap,
                    "sourceCode": ""
                 }

        self.klOperators.append(operatorData)

        return True


    def getKLOperatorByIndex(self, index):
        """Returns the operator at specified index.

        Return:
        KLOperator at specified index.

        """

        if self.checkKLOperatorIndex(index) is not True:
            return False

        return self.klOperators[index]


    def getKLOperatorByName(self, opName):
        """Returns the KL Operator with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for i in xrange(self.getNumKLOperators()):
            if self.klOperators[i]['opName'] == name:
                return self.klOperators[i]

        return None


    def setKLOperatorCode(self, opName, entry="", sourceCode=""):
        """Sets the source code for the specified operator.

        Arguments:
        opName -- String, name of the operator to set the code on.
        entry -- String, name of the entry function.

        Return:
        True if successful.

        """

        klOperator = self.getKLOperatorByName(opName)
        if klOperator is None:
            raise Exception("KL Operator with name '" + opName + "' does not exist!")

        klOperator['sourceCode'] = sourceCode

        return True


    def getKLOperatorCode(self, opName):
        """Gets the source code for the specified operator.

        Arguments:
        opName -- String, name of the operator to get the code from.

        Return:
        String, source code of the operator.

        """

        klOperator = self.getKLOperatorByName(opName)
        if klOperator is None:
            raise Exception("KL Operator with name '" + opName + "' does not exist!")

        return klOperator['sourceCode']


    def getNumKLOperators(self):
        """Returns the number of KL operators on the Splice Operator.

        Return:
        Integer, number of KL Operators on the Splice Operator.

        """

        return len(self.klOperators)