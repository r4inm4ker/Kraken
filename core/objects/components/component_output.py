"""Kraken - objects.component output module.

Classes:
ComponentOutput -- Component output representation.

"""

class ComponentOutput(object):
    """Component Output object."""

    __kType__ = "ComponentOutput"

    def __init__(self, name, dataType='Xfo'):
        super(ComponentOutput, self).__init__()
        self.name = name
        self.dataType = dataType
        self.connections = []


    # =============
    # Name methods
    # =============
    def getName(self):
        """Returns the name of the object as a string.

        Return:
        String of the object's name.

        """

        return self.name


    # ===================
    # Connection Methods
    # ===================
    def addConnection(self, componentInput):
        """Adds a connection to this object.

        Arguments:
        componentInput -- Object, component input object to add.

        Return:
        True if successful.

        """


        if componentInput.getKType() != "ComponentInput":
            raise Exception("Output components can only be connected to input components. connection type:'" + str(type(componentInput)) + "'")

        if self.dataType != componentInput.dataType:
            raise Exception("Connected component input data type:'" + componentInput.dataType + "' does not match this component data type:'" + self.dataType)

        self.connections.append(componentInput)

        return True


    def removeConnection(self, connection):
        """Removes the connection to the output that is set.

        Arguments:
        connection -- Object, connection to remove.

        Return:
        True if successful.

        """

        index = self.connections.index(connection)
        if index == -1:
            raise Exception("")
        del self.connections[index]

        return True


    def getNumConnections(self):
        """Gets the number of connections for this object.

        Return:
        The number of connections.

        """

        return len(self.connections)


    def getConnection(self, index):
        """Gets the connection by its index.

        Arguments:
        index -- Integer, index of the connection to return.

        Return:
        Connection at the supplied index.

        """

        return self.connections[index]


    # ==============
    # kType Methods
    # ==============
    def getKType(self):
        """Returns the kType of this object.

        Return:
        True if successful.

        """

        return self.__kType__