"""Kraken - objects.components.component_output_port module.

Classes:
ComponentOutputPort -- Component output port representation.

"""

from kraken.core.objects.scene_item import SceneItem


class ComponentOutputPort(SceneItem):
    """Component Output Object."""

    def __init__(self, name, parent, dataType):
        super(ComponentOutputPort, self).__init__(name, parent=parent)
        self._dataType = None
        self._connections = []
        self._target = None

        self.setDataType(dataType)


    # =================
    # DataType Methods
    # =================
    def setDataType(self, dataType):
        """Sets the data type for this input.

        Args:
            dataType (str): type of input source.

        Returns:
            bool: True if successful.

        """

        self._dataType = dataType

        return True


    def getDataType(self):
        """Returns the data type for this input.

        Returns:
            str: Data type of this input.

        """

        return self._dataType


    # ====================
    # Connections Methods
    # ====================
    def isConnected(self):
        """Checks if there is a connection.

        Returns:
            bool: Whether there are any output connections.

        """

        return len(self._connections) > 0


    def getConnection(self, index):
        """Gets the connection of this input.

        Args:
            index (int): Index of connection to return.

        Returns:
            object: Connection object or None if not set.

        """

        return self._connections[index]


    def _addConnection(self, connectionObj):
        """Adds a connection to the output.

        Args:
            connectionObj (object): Object to set as a connection.

        Returns:
            bool: True if successful.

        """

        if connectionObj.getDataType() != self.getDataType() and connectionObj.getDataType() != self.getDataType()[:-2]:
            raise Exception("Data Type mismatch! Cannot connect '" +
                connectionObj.getDataType() + "' to '" + self.getDataType())

        if connectionObj in self._connections:
            raise Exception("'connectionObj' is already in the connections.")

        self._connections.append(connectionObj)

        return True


    def _removeConnection(self, connectionObj):
        """Removes a connection.

        Args:
            connectionObj (object): Object to remove the connection for.

        Returns:
            bool: True if successful.

        """

        if connectionObj not in self._connections:
            raise Exception("'connectionObj' is not in the connections list.")

        self._connections.remove(connectionObj)

        return True


    # ===============
    # Target Methods
    # ===============
    def setTarget(self, target):
        """Sets the taret for this input.

        Args:
            target (object): Kraken object that is the target of this input.

        Returns:
            bool: True if successful.

        """

        self._target = target


    def getTarget(self):
        """Returns the target of the input.

        Returns:
            Object, the target of the input.

        """

        return self._target
