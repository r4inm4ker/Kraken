"""Kraken - objects.component module.

Classes:
Component -- Component representation.

"""

from kraken.core.maths import *
from kraken.core.objects.scene_item import SceneItem


class BaseComponent(SceneItem):
    """Kraken Base Component object."""

    __kType__ = "Component"

    def __init__(self, name, parent=None, side='M'):
        super(BaseComponent, self).__init__(name, parent)
        self.side = side
        self.inputs = []
        self.outputs = []

        self.setShapeVisibility(False)


    # =============
    # Side Methods
    # =============
    def getSide(self):
        """Returns the side of the component as a string."""

        return self.side


    def setSide(self, side):
        """Sets the side of the component.

        Arguments:
        side -- String, side that the component is on. Valid values: L, M, R.

        Return:
        True if successful.
        """

        if side not in ["L", "M", "R"]:
            raise ValueError("'" + side + "' is not a valid side.")

        self.side = side

        return True

    # ==================
    # Component Methods
    # ==================
    def getComponent(self, name):
        """Returns the component with the specified name.

        Arguments:
        name -- String, name of the component to return.

        Return:
        Component with specified name.
        """

        return self.getChildrenByType(BaseComponent)[name]


    def getNumComponents(self):
        """Return the number of components in this object as an Integer."""

        return len(self.getChildrenByType(BaseComponent))


    def addComponent(self, component):
        """Adds the specified component to this object.

        Arguments:
        component -- Object, component object to add to this object.

        Return:
        True if successful.
        """

        # check for existance

        return True


    def removeComponentByIndex(self, name):
        """Remove the component with the specified name from this object.

        Arguments:
        name -- String, name of the component to remove.

        Return:
        True if successful.
        """

        # Check if name is valid, then remove.

        return True


    def removeComponentByName(self, componentName):
        """Remove the component with the specified name from this object.

        Arguments:
        componentName, String, name of the component to remove.

        Return:
        True if successful.
        """

        # Check if component with name is part of object. Then remove.

        return True


    # ==============
    # Input Methods
    # ==============
    def addInput(self, componentInput):
        """Add ComponentInput to this object.

        Arguments:
        componentInput -- ComponentInput, input object to add.

        Return:
        True if successful.
        """

        # TODO: Check if input already part of object.
        self.inputs.append(componentInput)

        return True


    def removeInputByIndex(self, index):
        """Remove ComponentInput at specified index.

        Arguments:
        index -- Integer, index of the ComponentInput to remove.

        Return:
        True if successful.
        """

        # TODO: Check if index is valid, then remove.

        return True


    # ==============
    # Output Methods
    # ==============
    def addOutput(self, componentOutput):
        """Add ComponentOutput to this object.

        Arguments:
        output -- ComponentOutput, output object to add.

        Return:
        True if successful.
        """

        # TODO: Check if output already part of object.
        self.outputs.append(componentOutput)
        return True


    def removeOutputByIndex(self, index):
        """Remove ComponentOutput at specified index.

        Arguments:
        index -- Integer, index of the ComponentOutput to remove.

        Return:
        True if successful.
        """

        # TODO: Check if index is valid, then remove.

        return True


    def addOperatorBinding(self, operatorBinding):
        


    def buildRig(self, parent):

        component = BaseComponent()

    def save

    def load