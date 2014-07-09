"""Kraken - objects.component input module.

Classes:
ComponentInput -- Component input representation.

"""

class ComponentInput(object):
    """Component Input Object."""

    __kType__ = "ComponentInput"

    def __init__(self, name, dataType):
        super(ComponentInput, self).__init__()
        self.name = name
        self.dataType = dataType
        self.connection = None


    # ===================
    # Connection Methods
    # ===================
    def setConnection(self, componentOutput):
        """Sets the connection attribute to the supplied output.

        Arguments:
        componentOutput -- Object, component output object to connect.

        Return:
        True if successful.

        """

        self.connection = componentOutput
        componentOutput.addConnection(self)

        return True


    def removeConnection(self):
        """Removes the connection to the output that is set.

        Return:
        True if successful.

        """

        if self.connection is None:
            return True

        self.connection.removeConnection(self)
        self.setConnection(None)

        return True


    def getConnection(self):
        """Gets the output connection object for this input object.

        Return:
        Connection of this object.

        """

        return self.connection