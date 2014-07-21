"""Kraken - objects.components.component_outputXfo output module.

Classes:
ComponentOutputXfo -- Component output representation.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.constraints.pose_constraint import PoseConstraint


class ComponentOutputXfo(SceneItem):
    """Component Output object."""

    __kType__ = "ComponentOutputXfo"

    def __init__(self, name, dataType='Xfo'):
        super(ComponentOutputXfo, self).__init__(name, None)
        self.name = name
        self.dataType = dataType
        self.connections = []


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

        if componentInput.getKType() not in ["ComponentInputXfo", "ComponentInputAttr"]:
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