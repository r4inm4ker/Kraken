"""Kraken - objects.components.component_inputXfo input module.

Classes:
ComponentInputXfo -- Component input representation.

"""

from kraken.core.objects.scene_item import SceneItem


class ComponentInputXfo(SceneItem):
    """Component Input Object."""

    __kType__ = "ComponentInputXfo"

    def __init__(self, name, dataType='Xfo'):
        super(ComponentInputXfo, self).__init__(name, None)
        self.name = name
        self.dataType = dataType
        self.connection = None


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
    def setConnection(self, componentOutput):
        """Sets the connection attribute to the supplied output.

        Arguments:
        componentOutput -- Object, component output object to connect.

        Return:
        True if successful.

        """

        if componentOutput.getKType() not in ["ComponentOutputXfo", "ComponentOutputAttr"]:
            raise Exception("Output components can only be connected to input components. connection type:'" + componentOutput.getKType() + "'")

        if self.dataType != componentOutput.dataType:
            raise Exception("Connected component output data type:'" + componentOutput.dataType + "' does not match this component data type:'" + self.dataType)

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