"""Kraken - objects.components.component_input input module.

Classes:
ComponentOutput -- Component input representation.

"""

from kraken.core.objects.scene_item import SceneItem


class ComponentOutput(SceneItem):
    """Component Output Object."""

    def __init__(self, name, parent, dataType):
        super(ComponentOutput, self).__init__(name, parent=parent)
        self._dataType = None
        self._connections = []
        self._target = None

        self.setDataType(dataType)


    # =================
    # DataType Methods
    # =================
    def setDataType(self, dataType):
        """Sets the data type for this input.

        Arguments:
        dataType -- String, type of input source.

        Return:
        True if successful.

        """

        self._dataType = dataType

        return True


    def getDataType(self):
        """Returns the data type for this input.

        Return:
        String, data type of this input.

        """

        return self._dataType


    # ====================
    # Connections Methods
    # ====================
    def isConnected(self):
        """Checks if there is a connection.

        Return:
        Boolean, whether there are any output connections.

        """

        return len(self._connections) > 0


    def getConnection(self, index):
        """Gets the connection of this input.

        Return:
        Connection object or None if not set.

        """

        return self._connections[index]


    def _addConnection(self, connectionObj):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        if connectionObj.getDataType() != self.getDataType() and connectionObj.getDataType() != self.getDataType()[:-2]:
            raise Exception("Data Type mismatch! Cannot connect '" +
                connectionObj.getDataType() + "' to '" + self.getDataType())

        if connectionObj in self._connections:
            raise Exception("'connectionObj' is already in the connections.")

        self._connections.append(connectionObj)

        return True


    # ===============
    # Target Methods
    # ===============
    def setTarget(self, target):
        """Sets the taret for this input.

        Arguments:
        target -- Object, kraken object that is the target of this input.

        Return:
        True if successful.

        """

        self._target = target


    def getTarget(self):
        """Returns the target of the input.

        Return:
        Object, the target of the input.

        """

        return self._target
