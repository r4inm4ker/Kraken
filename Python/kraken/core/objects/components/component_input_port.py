"""Kraken - objects.components.component_input port module.

Classes:
ComponentInputPort -- Component input port representation.

"""

from kraken.core.objects.scene_item import SceneItem


class ComponentInputPort(SceneItem):
    """Component Input Object."""

    def __init__(self, name, parent, dataType):
        super(ComponentInputPort, self).__init__(name, parent=parent)
        self._dataType = None
        self._connection = None
        self._target = None
        self._index = 0

        self.setDataType(dataType)


    # =================
    # DataType Methods
    # =================
    def setDataType(self, dataType):
        """Sets the data type for this input.

        Args:
            dataType (str): Type of input source.

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
            bool: Whether it is connected or not.

        """

        return self._connection is not None


    def getConnection(self):
        """Gets the connection of this input.

        Returns:
            Connection object or None if not set.

        """

        return self._connection


    def setConnection(self, connectionObj):
        """Sets the connection to the component output.

        Args:
            connectionObj (ComponentOutput): Output object to connect to.

        Returns:
            bool: True if successful.

        """

        if connectionObj.getDataType() != self.getDataType() and connectionObj.getDataType()[:-2] != self.getDataType():
            raise Exception("Data Type mismatch! Cannot connect '" +
                connectionObj.getDataType() + "' to '" + self.getDataType())

        if connectionObj is self.getConnection():
            raise Exception("'connectionObj' is already set as the connection.")

        self._connection = connectionObj

        connectionObj._addConnection(self)

        return True



    def removeConnection(self):
        """Removes the connection to the component output.

        Returns:
            bool: True if successful.

        """

        self._connection._removeConnection(self)
        self._connection = None

        return True


    # ===============
    # Target Methods
    # ===============
    def setTarget(self, target):
        """Sets the taret for this input.

        Args:
            target (Object): Kraken object that is the target of this input.

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


    # ==============
    # Index Methods
    # ==============
    def getIndex(self):
        """Gets the index of the connection.

        Returns:
            Integer, the index of the connection.

        """

        return self._index


    def setIndex(self, index):
        """Sets the index of the connection.

        Args:
            index (int): The index to set this to.

        Returns:
            bool: True if successful.

        """

        self._index = index

        return True