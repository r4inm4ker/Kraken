"""Kraken - objects.components.component_inputAttribute input module.

Classes:
ComponentInputAttr -- Component input representation.

"""

from kraken.core.objects.attributes.base_attribute import BaseAttribute


class ComponentInputAttr(BaseAttribute):
    """Component Input Object."""

    __kType__ = "ComponentInputAttr"

    def __init__(self, name, dataType='Attribute'):
        super(ComponentInputAttr, self).__init__()
        self.name = name
        self.dataType = dataType
        self.connection = None


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
    def setConnection(self, componentOutput):
        """Sets the connection attribute to the supplied output.

        Arguments:
        componentOutput -- Object, component output object to connect.

        Return:
        True if successful.

        """

        if componentOutput.getKType() != "ComponentOutput":
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


    # ==============
    # kType Methods
    # ==============
    def getKType(self):
        """Returns the kType of this object.

        Return:
        True if successful.

        """

        return self.__kType__