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
        self.xfos = {}
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

        self.side = side

        return True


    # ======================
    # Component Xfo Methods
    # ======================
    def hasXfo(self, name):
        """Checks if the supplied name is valid.

        Arguments:
        name -- String, name of the component to return.

        Return:
        True if valid.
        """

        if name not in self.xfos.keys():
            return False

        return True


    def addXfo(self, name, xfo=None):
        """Adds an Xfo to the component xfo array.

        Arguments:
        name -- String, name of the xfo.
        xfo -- Xfo, transform to add to the xfos array.
               Default Xfo if not supplied.

        Return:
        Transform that was added.
        """

        if xfo is None:
            xfo = Xfo()

        self.xfos[name] = xfo

        return self.xfos[name]


    def removeXfo(self, name):
        """Removes a componentXfo from this object at the specified name.

        Arguments:
        name -- String, name of the componentXfo to remove.

        Return:
        True if successful.
        """

        if self.hasXfo(name) is not True:
            raise KeyError("'" + name + "' is not a valid xfo.")

        del self.xfos[name]

        return True


    def getNumXfos(self):
        """Returns the number of xfos for this object."""

        return len(self.xfos.items())


    def getXfo(self, name):
        """Returns a componentXfo by the specified name.

        Arguments:
        name -- String, name of the componentXfo you wish to be returned.

        Return:
        componentXfo as specified name.
        """

        if self.hasXfo(name) is not True:
            raise KeyError("'" + name + "' is not a valid xfo.")

        return self.xfos[name]


    def setXfo(self, name, xfo):
        """Set the componenXfo at the specified name.

        Arguments:
        name -- String, name of the componentXfo to set.
        xfo -- Xfo, transform to set at the specified name.

        Return:
        True if successful.
        """

        if self.hasXfo(name) is not True:
            raise KeyError("'" + name + "' is not a valid xfo.")

        self.xfos[name] = xfo

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