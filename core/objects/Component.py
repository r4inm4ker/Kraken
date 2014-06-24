"""Kraken - objects.compoent module.

Classes:
Component -- Component representation.

"""

from collections import OrderedDict
from kraken.core.maths import *
from SceneItem import SceneItem


class BaseComponent(SceneItem):
    """Kraken Base Component object."""

    def __init__(self, name, parent=None, side='M'):
        super(Component, self).__init__(name, parent)
        self.side = side
        self.componentXfos = []
        self.inputs = []
        self.outputs = []


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
            return False

        self.side = side

        return True


    # ======================
    # Component Xfo Methods
    # ======================
    def checkComponentXfoIndex(self, index):
        """Checks if the supplied index is valid.

        Arguments:
        index -- Integer, index of the component to return.

        Return:
        True if valid.
        """

        if index > len(self.componentXfos):
            raise IndexError("'" + str(index) + "' is out of the range of 'componentXfos'.")
            return False

        return True


    def addComponentXfo(self, xfo=None):
        """Adds an Xfo to the component xfo array.

        Arguments:
        xfo -- Xfo, transform to add to the componentXfos array.
               Default Xfo if not supplied.

        Return:
        Transform that was added.
        """

        if xfo is None:
            xfo = Xfo()

        self.componentXfos.append(xfo)

        return self.componentXfos[-1]


    def removeComponentXfo(self, index):
        """Removes a componentXfo from this object at the specified index.

        Arguments:
        index -- Integer, index of the componentXfo to remove.

        Return:
        True if successful.
        """

        if self.checkComponentXfoIndex(index) is not True:
            return False

        del self.componentXfos[index]

        return True


    def getNumComponentXfos(self):
        """Returns the number of componentXfos for this object."""

        return len(self.componentXfos)


    def getComponentXfos(self):
        """Returns the componentXfos array.

        Return:
        Array of componentXfos for this object.
        """
        return self.componentXfos


    def getComponentXfoByIndex(self, index):
        """Returns a componentXfo by the specified index.

        Arguments:
        index -- Integer, index of the componentXfo you wish to be returned.

        Return:
        componentXfo as specified index.
        """

        if self.checkComponentXfoIndex(index) is not True:
            return False

        return self.componentXfos[index]


    def setComponentXfo(self, index, xfo):
        """Set the componenXfo at the specified index.

        Arguments:
        index -- Integer, index of the componentXfo to set.
        xfo -- Xfo, transform to set at the specified index.

        Return:
        True if successful.
        """

        if self.checkComponentXfoIndex(index) is not True:
            return False

        self.componentXfos[index] = xfo

        return True


    # ==================
    # Component Methods
    # ==================
    def getComponent(self, index):
        """Returns the component at the specified index.

        Arguments:
        index -- Integer, index of the component to return.

        Return:
        Component at specified index.
        """

        return self.getChildrenByType(Component)[index]


    def getNumComponents(self):
        """Return the number of components in this object as an Integer."""

        return len(self.getChildrenByType(Component))


    def addComponent(self, component):
        """Adds the specified component to this object.

        Arguments:
        component -- Object, component object to add to this object.

        Return:
        True if successful.
        """

        # check for existance

        return True


    def removeComponentByIndex(self, index):
        """Remove the component with the specified name from this object.

        Arguments:
        index -- Integer, index of the component to remove.

        Return:
        True if successful.
        """

        # Check if index is valid, then remove.

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
    def addInput(self, input):
        """Add ComponentInput to this object.

        Arguments:
        input -- ComponentInput, input object to add.

        Return:
        True if successful.
        """

        # Check if input already part of object.

        return True


    def removeInputByIndex(self, index):
        """Remove ComponentInput at specified index.

        Arguments:
        index -- Integer, index of the ComponentInput to remove.

        Return:
        True if successful.
        """

        # Check if index is valid, then remove.

        return True


    # ==============
    # Output Methods
    # ==============
    def addOutput(self, output):
        """Add ComponentOutput to this object.

        Arguments:
        output -- ComponentOutput, output object to add.

        Return:
        True if successful.
        """

        # Check if output already part of object.

        return True


    def removeOutputByIndex(self, index):
        """Remove ComponentOutput at specified index.

        Arguments:
        index -- Integer, index of the ComponentOutput to remove.

        Return:
        True if successful.
        """

        # Check if index is valid, then remove.

        return True