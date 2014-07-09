"""Kraken - objects.component output module.

Classes:
ComponentOutput -- Component output representation.

"""

class ComponentOutput(object):
    """Component Output object."""

    __kType__ = "ComponentOutput"

    def __init__(self, name, dataType):
        super(ComponentOutput, self).__init__()
        self.name = name
        self.dataType = dataType
        self.connections = []


    # ===================
    # Connection Methods
    # ===================
    def addConnection(self, componentOutput):
        """Adds a connection to this object.

        Arguments:
        componentOutput -- Object, component output object to add.

        Return:
        True if successful.

        """

        self.connections.append(componentOutput)

        return True


    def removeConnection(self, instance):
        """Removes the connection to the output that is set.

        Arguments:
        instance -- Object, connection to remove.

        Return:
        True if successful.

        """

        index = self.connections.index(instance)
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