"""Kraken - objects.component module.

Classes:
Component -- Component representation.

"""

from kraken.core.configs.config import Config
from kraken.helpers.utility_methods import mirrorData
from kraken.core.maths import *
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.layer import Layer
from kraken.core.objects.locator import Locator
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.components.component_input import ComponentInput
from kraken.core.objects.components.component_output import ComponentOutput


class Component(Object3D):
    """Kraken Component object."""

    def __init__(self, name, parent=None, location='M'):
        self._location = location
        super(Component, self).__init__(name, parent)
        self._inputs = []
        self._outputs = []
        self._operators = []

        self.setShapeVisibility(False)

        self.lockRotation(x=True, y=True, z=True)
        self.lockScale(x=True, y=True, z=True)
        self.lockTranslation(x=True, y=True, z=True)

        self._graphPos = Vec2()



    # =============
    # Name Methods
    # =============

    def getNameDecoration(self):
        """Gets the decorated name of the object.

        Return:
        String, decorated name of the object.

        """

        # We decorate the name of the component with the location. This
        # enables multiple components to have the same name as long as they
        # have different locations. e.g. Leg:R, and Leg:L
        return ":" + self.getLocation()


    # =============
    # Side Methods
    # =============
    def getLocation(self):
        """Returns the location of the component as a string.

        Return:
        String, the location of the component.

        """

        return self._location


    def setLocation(self, location):
        """Sets the location of the component.

        Arguments:
        location -- String, location that the component is on. Valid values: L, M, R.

        Return:
        True if successful.

        """

        # TODO: check that the given location is a valid value found in the config

        self._location = location

        # The new location might cause a name colision.
        # forcing a name refresh will generate a new name if a collision exists
        self.setName(self.getName())

        return True


    # =============
    # Graph UI
    # =============
    def getGraphPos(self):
        """Returns the graphPos of the component as a string.

        Return:
        String, the graphPos of the component.

        """

        return self._graphPos


    def setGraphPos(self, graphPos):
        """Sets the graphPos of the component.

        Arguments:
        graphPos -- Vec2, The position in the graph where this node is placed.

        Return:
        True if successful.

        """

        self._graphPos = graphPos

        return True


    # =============
    # Layer methods
    # =============
    def getLayer(self, name):
        """Retrieves a layer from the owning container, or generates a layer
        (and warning message)

        Return:
        Layer, the layer from the container, or generated layer.

        """

        container = self.getContainer()
        if container is None:
            container = self

        layer = container.getChildByName(name)
        if layer is None or not layer.isTypeOf('Layer'):
            raise KeyError("Layer '" + + "' was not found!")

        return layer


    def getOrCreateLayer(self, name):
        """Retrieves a layer from the owning container, or generates a layer (and warning message)

        Return:
        Layer, the layer from the container, or generated layer.

        """

        container = self.getContainer()
        if container is None:
            container = self

        layer = container.getChildByName(name)
        if layer is None or not layer.isTypeOf('Layer'):
            layer = Layer(name, parent=container)

        return layer


    # ==============
    # Child Methods
    # ==============
    def addChild(self, child):
        """Adds a child to the component and sets the object's component attribute.

        Arguments:
        child -- Object, object to add as a child.

        Return:
        True if successful.

        """

        super(Component, self).addChild(child)

        # Assign the child self as the component.
        child.setComponent(self)

        return True


    # ==============
    # Input Methods
    # ==============
    def checkInputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, input index to check.

        """

        if index > len(self._inputs):
            raise IndexError("'" + str(index) + "' is out of the range of 'inputs' array.")

        return True


    def createInput(self, name, dataType, **kwargs):
        """Creates an input object and also a connected target object that matches
        the data type that is passed.

        Arguments:
        name -- String, name of the input to create.
        dataType -- String, data type of the input.

        Return:
        Object, the connected target object for the input.

        """

        componentInput = self.addInput(name, dataType)

        # Create object
        if dataType.startswith('Xfo'):
            newInputTgt = Locator(name)

        elif dataType.startswith('Boolean'):
            newInputTgt = BoolAttribute(name)

        elif dataType.startswith('Float'):
            newInputTgt = ScalarAttribute(name)

        elif dataType.startswith('Integer'):
            newInputTgt = IntegerAttribute(name)

        elif dataType.startswith('String'):
            newInputTgt = StringAttribute(name)

        # Handle keyword arguments
        for k, v in kwargs.iteritems():
            if k == 'value':
                newInputTgt.setValue(v)
            elif k == 'minValue':
                newInputTgt.setMin(v)
                newInputTgt.setUIMin(v)
            elif k == 'maxValue':
                newInputTgt.setMax(v)
                newInputTgt.setUIMax(v)
            elif k == 'parent':
                if dataType.startswith('Xfo'):
                    v.addChild(newInputTgt)
                else:
                    v.addAttribute(newInputTgt)
            else:
                print "Keyword '" + k + "' is not supported with createInput method!"

        componentInput.setTarget(newInputTgt)

        return newInputTgt


    def addInput(self, name, dataType):
        """Add inputObject to this object.

        Arguments:
        name -- String, name of the input to create.
        dataType -- String, data type of the input.

        Return:
        New input object.

        """

        if self.getInputByName(name) is not None:
            raise Exception("'" + name + "' argument is already an output!")

        componentInput = ComponentInput(name, parent=self, dataType=dataType)

        self._inputs.append(componentInput)

        return componentInput


    def removeInputByIndex(self, index):
        """Remove ComponentInput at specified index.

        Arguments:
        index -- Integer, index of the ComponentInput to remove.

        Return:
        True if successful.

        """

        if self.checkInputIndex(index) is not True:
            return False

        del self._inputs[index]

        return True


    def removeInputByName(self, name):
        """Removes a input from this object by name.

        Arguments:
        name -- String, name of input to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachInput in enumerate(self._inputs):
            if eachInput.getName() == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid input of this object.")

        self.removeInputByIndex(removeIndex)

        return True


    def getNumInputs(self):
        """Returns the number of inputs this component has.

        Return:
        Integer, number of inputs of this object.

        """

        return len(self._inputs)


    def getInputByIndex(self, index):
        """Returns the input object at specified index.

        Return:
        Input object at specified index.

        """

        if self.checkInputIndex(index) is not True:
            return False

        return self._inputs[index]


    def getInputByName(self, name):
        """Returns the input object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachInput in self._inputs:
            if eachInput.getName() == name:
                return eachInput

        return None


    # ===============
    # Output Methods
    # ===============
    def checkOutputIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, output index to check.

        """

        if index > len(self._outputs):
            raise IndexError("'" + str(index) + "' is out of the range of 'outputs' array.")

        return True


    def createOutput(self, name, dataType, **kwargs):
        """Creates an output object and also a connected target object that matches
        the data type that is passed.

        Arguments:
        name -- String, name of the output to create.
        dataType -- String, data type of the output.

        Return:
        Object, the connected target object for the output.

        """

        componentOutput = self.addOutput(name, dataType)

        # Create object
        if dataType.startswith('Xfo'):
            newOutputTgt = Locator(name)

        elif dataType.startswith('Boolean'):
            newOutputTgt = BoolAttribute(name)

        elif dataType.startswith('Float'):
            newOutputTgt = ScalarAttribute(name)

        elif dataType.startswith('Integer'):
            newOutputTgt = IntegerAttribute(name)

        elif dataType.startswith('String'):
            newOutputTgt = StringAttribute(name)

        # Handle keyword arguments
        for k, v in kwargs.iteritems():
            if k == 'value':
                newOutputTgt.setValue(v)
            elif k == 'minValue':
                newOutputTgt.setMin(v)
            elif k == 'maxValue':
                newOutputTgt.setMax(v)
            elif k == 'parent':
                if dataType.startswith('Xfo'):
                    v.addChild(newOutputTgt)
                else:
                    v.addAttribute(newOutputTgt)
            else:
                print "Keyword '" + k + "' is not supported with createOutput method!"

        componentOutput.setTarget(newOutputTgt)

        return newOutputTgt


    def addOutput(self, name, dataType):
        """Add outputObject to this object.

        Arguments:
        name -- String, name of the output to create.
        dataType -- String, data type of the output.

        Return:
        New output object.

        """

        if self.getOutputByName(name) is not None:
            raise Exception("'outputObject' argument is already an output!")

        componentOutput = ComponentOutput(name, parent=self, dataType=dataType)

        self._outputs.append(componentOutput)

        return componentOutput


    def getNumOutputs(self):
        """Returns the number of outputs this component has.

        Return:
        Integer, number of outputs of this object.

        """

        return len(self._outputs)


    def getOutputByIndex(self, index):
        """Returns the output object at specified index.

        Return:
        Output object at specified index.

        """

        if self.checkOutputIndex(index) is not True:
            return False

        return self._outputs[index]


    def getOutputByName(self, name):
        """Returns the output object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachOutput in self._outputs:
            if eachOutput.getName() == name:
                return eachOutput

        return None


    # =================
    # Operator Methods
    # =================
    def checkOperatorIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, operator index to check.

        """

        if index > len(self._operators):
            raise IndexError("'" + str(index) + "' is out of the range of the 'children' array.")

        return True


    def addOperator(self, operator):
        """Adds a operator to this object.

        Arguments:
        operator -- Object, object that will be a operator of this object.

        Return:
        True if successful.

        """

        if operator.getName() in [x.getName() for x in self._operators]:
            raise IndexError("Operator with " + operator.getName() + " already exists as a operator.")

        self._operators.append(operator)
        operator.setParent(self)

        return True


    def removeOperatorByIndex(self, index):
        """Removes a operator from this object by index.

        Arguments:
        index -- Integer, index of operator to remove.

        Return:
        True if successful.

        """

        if self.checkOperatorIndex(index) is not True:
            return False

        del self._operators[index]

        return True


    def removeOperatorByName(self, name):
        """Removes a operator from this object by name.

        Arguments:
        name -- String, name of operator to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachOperator in enumerate(self._operators):
            if eachOperator.getName() == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid operator of this object.")

        self.removeOperatorByIndex(removeIndex)

        return True


    def getNumOperators(self):
        """Returns the number of operators this object has.

        Return:
        Integer, number of operators of this object.

        """

        return len(self._operators)


    def getOperatorByIndex(self, index):
        """Returns the operator object at specified index.

        Return:
        Operator object at specified index.

        """

        if self.checkOperatorIndex(index) is not True:
            return False

        return self._operators[index]


    def getOperatorByName(self, name):
        """Returns the operator object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachOperator in self._operators:
            if eachOperator.getName() == name:
                return eachOperator

        return None


    def getOperatorByType(self, childType):
        """Returns all children that are of the specified type.

        Arguments:
        childType -- Type, the object type to search for.

        Return:
        Array of operator objects of the specified type.
        None if no objects of specified type are found.

        """

        childrenOfType = []
        for eachOperator in self._operators:
            if isinstance(eachOperator, childType):
                childrenOfType.append(eachOperator)

        return childrenOfType


    def getOperatorIndex(self, operator):
        """Return the index of the specified operator.

        Arguments:
        operator -- Object, operator to find the index of.

        Return:
        True if successful.
        None if operator not found on component.

        """

        for index, eachOp in xrange(self.getNumOperators()):
            if eachOp is operator:
                return index

        return None


    def moveOperatorToIndex(self, operator, index):
        """Moves an operator to the specified index.

        Arguments:
        operator -- Object, operator to move.
        index -- Integer, index position to move the operator to.

        Return:
        True if successful.

        """

        oldIndex = self.getOperatorIndex(operator)
        self._operators.insert(index, self._operators.pop(oldindex))

        return True



    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.


        Return:
        The JSON data object

        """

        data = {
            'class': self.__class__.__module__ + "." + self.__class__.__name__,
            'name': self.getName(),
            'location': self.getLocation(),
            'graphPos': self._graphPos
           }


        # TODO: AttributeGroup needs to become a hierachy object like all the others.
        # so it can be traversed usign the regular traversial methods.
        # attributeGroups = self.getChildrenByType('AttributeGroup')
        # attributeGroups = getNumAttributeGroups()
        # for grp in attributeGroups:
        for i in range(self.getNumAttributeGroups()):
            grp = self.getAttributeGroupByIndex(i)
            for j in range(grp.getNumAttributes()):
                attr = grp.getAttributeByIndex(j)
                data[attr.getName()] = attr.getValue()

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        if 'name' in data:
            self.setName(data['name'])

        if 'location' in data:
            self.setLocation(data['location'])

        if 'graphPos' in data:
            self.setGraphPos(data['graphPos'])

        attributeGroups = self.getChildrenByType('AttributeGroup')
        for grp in attributeGroups:
            for i in range(grp.getNumAttributes()):
                attr = grp.getAttributeByIndex(i)
                if attr.getName() in data:
                    attr.setValue(data[attr.getName()])

        return True

    # ==================
    # Copy/Paste Methods
    # ==================

    def copyData(self):
        """Copy the data for the component to our clipboard.

        Return:
        The JSON data object

        """

        return self.saveData()


    def pasteData(self, data):
        """Paste a copied guide representation.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        if data['location'] != self.getLocation():
            config = Config.getInstance()
            mirrorMap = config.getNameTemplate()['mirrorMap']
            if mirrorMap[data['location']] != data['location']:
                data = mirrorData(data, 0)
                del data['location']

        self.loadData( data )
        return True

    # ==================
    # Rig Build Methods
    # =================

    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        rigComponentClass = self.getRigComponentClass()

        data = {
            'class': rigComponentClass.__module__ + '.' + rigComponentClass.__name__,
            'name': self.getName(),
            'location': self.getLocation()
        }

        # automatically save all attributes.
        for i in range(self.getNumAttributeGroups()):
            grp = self.getAttributeGroupByIndex(i)
            for j in range(grp.getNumAttributes()):
                attr = grp.getAttributeByIndex(j)
                data[attr.getName()] = attr.getValue()

        return data


    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):
        """Enables introspection of the class prior to construction to determine if it is a guide component.

        Return:
        The true if this component is a guide component.

        """

        return 'Base'
