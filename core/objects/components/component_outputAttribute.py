"""Kraken - objects.components.component_outputAttribute output module.

Classes:
ComponentOutputAttr -- Component output representation.

"""

from kraken.core.objects.attributes.base_attribute import BaseAttribute


class ComponentOutputAttr(BaseAttribute):
    """Component Output object."""

    __kType__ = "ComponentOutputAttr"

    def __init__(self, name, dataType='Attribute'):
        super(ComponentOutputAttr, self).__init__()
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


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the paret of this attribute.

        Return:
        Parent object of this attribute.

        """

        return self.parent


    def setParent(self, parent):
        """Sets the paret of this attribute.

        Arguments:
        parent -- Object, parent object of this attribute.

        Return:
        True if successful.

        """

        self.parent = parent

        return True


    # =================
    # DataType Methods
    # =================
    def getDataType(self):
        """Returns the data type for this input.

        Return:
        String, data type of this input.

        """

        return self.dataType


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