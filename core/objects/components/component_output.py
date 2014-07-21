"""Kraken - objects.components.component_output output module.

Classes:
ComponentOutput -- Component output representation.

"""

from kraken.core.objects.locator import Locator
from kraken.core.objects.attributes.base_attribute import BaseAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint


class ComponentOutput(object):
    """Component Output object."""

    __kType__ = "ComponentOutput"

    def __init__(self, name, connectionObj):
        super(ComponentOutput, self).__init__()
        self.name = name
        self.dataType = None
        self.source = None
        self.target = connectionObj

        if isinstance(connectionObj, Locator):
            self.setDataType('Xfo')
        elif isinstance(connectionObj, BaseAttribute):
            self.setDataType('Attribute')


    # =============
    # Name methods
    # =============
    def getName(self):
        """Returns the name of the object as a string.

        Return:
        String of the object's name.

        """

        return self.name


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

        self.dataType = dataType

        return True


    def getDataType(self):
        """Returns the data type for this input.

        Return:
        String, data type of this input.

        """

        return self.dataType


    # ===============
    # Target Methods
    # ===============
    def getTarget(self):
        """Returns the target of the input.

        Return:
        Object, the target of the input.

        """

        return self.target


    # ===============
    # Source Methods
    # ===============
    def setSource(self, sourceObj):
        """Sets the source attribute to the supplied output.

        Arguments:
        sourceObj -- Object, object to connect.

        Return:
        True if successful.

        """


        if self.getDataType() == 'Xfo' and not isinstance(sourceObj, Locator):
            raise Exception("'Xfo' inputs can only be connected to 'Locator' objects. Object '"
                + sourceObj.getName() + "' has type:'" + sourceObj.getKType() + "'")

        if self.getDataType() == 'Attribute' and not isinstance(sourceObj, BaseAttribute):
            raise Exception("'Attribute' inputs can only be connected to 'Attribute' objects. Object '"
                + sourceObj.getName() + "' has type:'" + sourceObj.getKType() + "'")

        self.source = sourceObj

        return True


    def removeSource(self):
        """Removes the source to the output that is set.

        Return:
        True if successful.

        """

        if self.source is None:
            return True

        self.source = None
        self.setDataType(None)
        self.setSource(None)

        return True


    def getSource(self):
        """Gets the output source object for this input object.

        Return:
        Connection of this object.

        """

        return self.source