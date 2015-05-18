"""Kraken - builders module.

Classes:
Builder -- Base builder object to build objects in DCC.

"""


from kraken.core.kraken_system import KrakenSystem
from kraken.core.configs.config import Config
from kraken.core.profiler import Profiler

from kraken.core.objects.components.component import Component
from kraken.core.objects.constraints.pose_constraint import PoseConstraint


class Builder(object):
    """Builder object for building objects in DCC's. Sub-class per DCC in a
    plugin."""


    def __init__(self):
        super(Builder, self).__init__()
        self._buildElements = []

        self.config = Config.getInstance()


    # ====================
    # Object registration
    # ====================
    def _registerSceneItemPair(self, kSceneItem, dccSceneItem):
        """Registers a pairing between the kraken scene item and the dcc scene item
        for querying later.

        Arguments:
        kSceneItem -- Object, kraken scene item that you want to pair.
        dccSceneItem -- Object, dcc scene item that you want to pair.

        Return:
        True if successful.

        """

        pairing = {
                   'src': kSceneItem,
                   'tgt': dccSceneItem
                  }

        self._buildElements.append(pairing)

        return True


    def getDCCSceneItem(self, kSceneItem):
        """Given a kSceneItem, returns the built dcc scene item.

        Arguments:
        kSceneItem -- Object, kSceneItem to base the search.

        Return:
        Object, the DCC Scene Item that corresponds to the given scene item

        """

        for builtElement in self._buildElements:
            if builtElement['src'] == kSceneItem:
                return builtElement['tgt']

        return None


    # ========================
    # SceneItem Build Methods
    # ========================
    def buildContainer(self, kSceneItem, buildName):
        """Builds a container / namespace object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a layer to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildGroup(self, kSceneItem, buildName):
        """Builds a group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a joint to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a locator / null to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a curve to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a control to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        return None


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kAttribute):
        """Builds a Bool attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a string attribute to be built.

        Return:
        True if successful.

        """

        return True


    def buildFloatAttribute(self, kAttribute):
        """Builds a Float attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a string attribute to be built.

        Return:
        True if successful.

        """

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a string attribute to be built.

        Return:
        True if successful.

        """

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a string attribute to be built.

        Return:
        True if successful.

        """

        return True


    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Arguments:
        kAttributeGroup -- SceneItem, kraken object to build the attribute group on.

        Return:
        True if successful.

        """

        return True


    def connectAttribute(self, kAttribute):
        """Connects the driver attribute to this one.

        Arguments:
        kAttribute -- Object, attribute to connect.

        Return:
        True if successful.

        """

        return True


    # =========================
    # Constraint Build Methods
    # =========================
    def buildOrientationConstraint(self, kConstraint):
        """Builds an orientation constraint represented by the kConstraint.

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        dccSceneItem that was created.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPoseConstraint(self, kConstraint):
        """Builds an pose constraint represented by the kConstraint.

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildScaleConstraint(self, kConstraint):
        """Builds an scale constraint represented by the kConstraint.

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    # ========================
    # Component Build Methods
    # ========================
    def buildXfoConnection(self, componentInput):
        """Builds the constraint between the target and connection target.

        Arguments:
        componentInput -- Object, kraken component input to build connections for.

        Return:
        True if successful.

        """

        connection = componentInput.getConnection()
        connectionTarget = connection.getTarget()
        inputTarget = componentInput.getTarget()

        if connection.getDataType().endswith('[]'):
            connectionTarget = connection.getTarget()[componentInput.getIndex()]
        else:
            connectionTarget = connection.getTarget()

        constraint = PoseConstraint('_'.join([inputTarget.getName(), 'To', connectionTarget.getName()]))
        constraint.setMaintainOffset(True)
        constraint.setConstrainee(inputTarget)
        constraint.addConstrainer(connectionTarget)

        dccSceneItem = self.buildPoseConstraint(constraint)
        self._registerSceneItemPair(componentInput, dccSceneItem)

        return True


    def buildAttributeConnection(self, componentInput):
        """Builds the link between the target and connection target.

        Arguments:
        componentInput -- Object, kraken connection to build.

        Return:
        True if successful.

        """

        # Implemented in DCC Plugins.

        return True


    # =========================
    # Operator Builder Methods
    # =========================
    def buildSpliceOperators(self, kOperator):
        """Builds Splice Operators on the components.

        Arguments:
        kOperator -- Object, kraken operator that represents a Splice operator.

        Return:
        True if successful.

        """

        return True


    # =====================
    # Build Object Methods
    # =====================
    def buildAttributes(self, kObject):
        """Builds attributes on the DCC object.

        Arguments:
        kObject -- SceneItem, kraken object to build attributes for.

        Return:
        True if successful.

        """

        for i in xrange(kObject.getNumAttributeGroups()):
            attributeGroup = kObject.getAttributeGroupByIndex(i)

            attributeCount = attributeGroup.getNumAttributes()
            self.buildAttributeGroup(attributeGroup)

        return True


    def getBuildName(self, kObject):
        """Returns the build name for the object.

        Arguments:
        kObject -- Kraken Object, object to get the build name for.

        Return:
        String, name to be used in the DCC.

        """

        typeNameHierarchy = kObject.getTypeHierarchyNames()

        config = self.getConfig()

        # If flag is set on object to use explicit name, return it.
        if config.getExplicitNaming() is True or kObject.testFlag('EXPLICIT_NAME'):
            return kObject.getName()

        nameTemplate = config.getNameTemplate()

        # Get the token list for this type of object
        format = None
        for typeName in nameTemplate['formats'].keys():
            if typeName in typeNameHierarchy:
                format = nameTemplate['formats'][typeName]
                break

        if format is None:
            format = nameTemplate['formats']['default']

        objectType = None
        for eachType in typeNameHierarchy:
            if eachType in nameTemplate['types'].keys():
                objectType = eachType
                break

        if objectType is None:
            objectType = "default"

        # Generate a name by concatenating the resolved tokens together.
        builtName = ""
        skipSep = False
        for token in format:

            if token is 'sep':
                if not skipSep:
                    builtName += nameTemplate['separator']

            elif token is 'location':
                if isinstance(kObject, Component):
                    location = kObject.getLocation()
                else:
                    location = kObject.getComponent().getLocation()

                if location not in nameTemplate['locations']:
                    raise ValueError("Invalid location on: " + kObject.getFullName())

                builtName += location

            elif token is 'type':

                if objectType == "Locator" and kObject.testFlag("inputObject"):
                    objectType = "ComponentInput"
                elif objectType == "Locator" and kObject.testFlag("outputObject"):
                    objectType = "ComponentOutput"

                builtName += nameTemplate['types'][objectType]

            elif token is 'name':
                builtName += kObject.getName()

            elif token is 'component':
                if kObject.getComponent() is None:
                    skipSep = True
                    continue
                builtName += kObject.getComponent().getName()

            elif token is 'container':
                if kObject.getContainer() is None:
                    skipSep = True
                    continue
                builtName += kObject.getContainer().getName()

            else:
                raise ValueError("Unresolvabled token '" + token + "' used on: " + kObject.getFullName())

        return builtName


    def buildHierarchy(self, kObject, component=None):
        """Builds the hierarchy for the supplied kObject.

        Arguments:
        kObject -- Object, kraken object to build.
        component -- Component, component that this object belongs to.

        Return:
        DCC object that was created.

        """

        dccSceneItem = None

        buildName = self.getBuildName(kObject)

        # Build Object
        if kObject.isTypeOf("Container"):
            dccSceneItem = self.buildContainer(kObject, buildName)

        elif kObject.isTypeOf("Layer"):
            dccSceneItem = self.buildLayer(kObject, buildName)

        elif kObject.isTypeOf("Component"):
            pass

        elif kObject.isTypeOf("ComponentGroup"):
            dccSceneItem = self.buildGroup(kObject, buildName)
            component = kObject

        elif kObject.isTypeOf("HierarchyGroup"):
            dccSceneItem = self.buildHierarchyGroup(kObject, buildName)

        elif kObject.isTypeOf("CtrlSpace"):
            dccSceneItem = self.buildGroup(kObject, buildName)

        elif kObject.isTypeOf("Locator"):
            dccSceneItem = self.buildLocator(kObject, buildName)

        elif kObject.isTypeOf("Joint"):
            dccSceneItem = self.buildJoint(kObject, buildName)

        elif kObject.isTypeOf("Control"):
            dccSceneItem = self.buildControl(kObject, buildName)

        elif kObject.isTypeOf("Curve"):
            dccSceneItem = self.buildCurve(kObject, buildName)

        # Important Note: The order of these tests is important.
        # New classes should be added above the classes they are derrived from.
        # No new types should be added below SceneItem here.
        elif kObject.isTypeOf("SceneItem"):
            dccSceneItem = self.buildLocator(kObject, buildName)

        else:
            raise NotImplementedError(kObject.getName() + ' has an unsupported type: ' + str(type(kObject)))

        if dccSceneItem is not None:
            self.buildAttributes(kObject)
            self.setTransform(kObject)
            self.lockParameters(kObject)
            self.setVisibility(kObject)
            self.setObjectColor(kObject)

        # Build children
        for i in xrange(kObject.getNumChildren()):
            child = kObject.getChildByIndex(i)
            self.buildHierarchy(child, component)

        return dccSceneItem


    def buildConstraints(self, kObject):
        """Builds constraints for the supplied kObject.

        Arguments:
        kObject -- Object, kraken object to create constraints for.

        Return:
        True if successful.

        """

        dccSceneItem = None
        for i in xrange(kObject.getNumConstraints()):

            constraint = kObject.getConstraintByIndex(i)

            # Build Object
            if constraint.isTypeOf("OrientationConstraint"):
                dccSceneItem = self.buildOrientationConstraint(constraint)

            elif constraint.isTypeOf("PoseConstraint"):
                dccSceneItem = self.buildPoseConstraint(constraint)

            elif constraint.isTypeOf("PositionConstraint"):
                dccSceneItem = self.buildPositionConstraint(constraint)

            elif constraint.isTypeOf("ScaleConstraint"):
                dccSceneItem = self.buildScaleConstraint(constraint)

            else:
                raise NotImplementedError(constraint.getName() + ' has an unsupported type: ' + str(type(constraint)))

        # Build children
        for i in xrange(kObject.getNumChildren()):
            child = kObject.getChildByIndex(i)
            self.buildConstraints(child)

        return True


    def buildIOConnections(self, kObject):
        """Builds the connections between the component inputs and outputs of each
        component.

        Only input connections are built otherwise duplicate constraints / expressions
        would be created.

        Arguments:
        kObject -- Object, kraken object to create connections for.

        Return:
        True if successful.

        """

        if kObject.isTypeOf('Component'):

            # Build input connections
            for i in xrange(kObject.getNumInputs()):
                componentInput = kObject.getInputByIndex(i)
                if componentInput.getTarget() is None or componentInput.getConnection() is None:
                    continue

                if componentInput.getDataType().startswith('Xfo'):
                    self.buildXfoConnection(componentInput)

                elif componentInput.getDataType().startswith(('Boolean', 'Float', 'Integer', 'String')):
                    self.buildAttributeConnection(componentInput)

            # Build output connections
            # for i in xrange(kObject.getNumOutputs()):
            #     componentOutput = kObject.getOutputByIndex(i)
            #     if componentOutput.getTarget() is None or componentOutput.getConnection() is None:
            #         continue

            #     if componentOutput.getDataType().startswith('Xfo'):
            #         self.buildXfoConnection(componentOutput)

            #     elif componentOutput.getDataType() == 'Attribute':
            #         self.buildAttributeConnection(componentOutput)

        # Build connections for children.
        for i in xrange(kObject.getNumChildren()):
            child = kObject.getChildByIndex(i)
            self.buildIOConnections(child)

        return True


    def buildAttrConnections(self, kObject):
        """Builds the connections between the component inputs and outputs of each
        component.

        Arguments:
        kObject -- Object, kraken object to create connections for.

        Return:
        True if successful.

        """

        # Build input connections
        for i in xrange(kObject.getNumAttributeGroups()):
            attributeGroup = kObject.getAttributeGroupByIndex(i)

            for y in xrange(attributeGroup.getNumAttributes()):
                attribute = attributeGroup.getAttributeByIndex(y)
                self.connectAttribute(attribute)

        # Build connections for children.
        for i in xrange(kObject.getNumChildren()):
            child = kObject.getChildByIndex(i)
            self.buildAttrConnections(child)

        return True


    def buildOperators(self, kObject):
        """Build operators in the hierarchy.

        Arguments:
        kObject -- Object, kraken object to create operators for.

        Return:
        True if successful.

        """
        if kObject.isTypeOf('Component'):

            # Build operators
            for i in xrange(kObject.getNumOperators()):
                operator = kObject.getOperatorByIndex(i)

                if operator.isTypeOf('SpliceOperator'):
                    self.buildSpliceOperators(operator)

                else:
                    raise NotImplementedError(operator.getName() + ' has an unsupported type: ' + str(type(kObject)))

        # Build connections for children.
        for i in xrange(kObject.getNumChildren()):
            child = kObject.getChildByIndex(i)
            self.buildOperators(child)

        return True


    # ==================
    # Parameter Methods
    # ==================
    def lockParameters(self, kSceneItem):
        """Locks flagged SRT parameters.

        Arguments:
        kSceneItem -- Object, kraken object to lock the SRT parameters on.

        Return:
        True if successful.

        """

        return True


    # ===================
    # Visibility Methods
    # ===================
    def setVisibility(self, kSceneItem):
        """Sets the visibility of the object after its been created.

        Arguments:
        kSceneItem -- Object, kraken object to set the visibility on.

        Return:
        True if successful.

        """

        if hasattr(kSceneItem, 'getShapeVisibility') is False:
            return False

        if kSceneItem.getShapeVisibility() is False:
            pass

            # Re-implement in DCC builders.

        return True


    # ================
    # Display Methods
    # ================
    def getBuildColor(self, kSceneItem):
        """Gets the build color for the object.

        Arguments:
        kSceneItem -- Object, kraken object to get the color for.

        Return:
        String, color to set on the object.

        """

        config = self.getConfig()
        colors = config.getColors()
        colorMap = config.getColorMap()
        typeNames = kSceneItem.getTypeHierarchyNames()
        component = kSceneItem.getComponent()
        objectColor = kSceneItem.getColor()

        buildColor = None
        if objectColor is not None:

            if objectColor not in colors.keys():
                raise ValueError("Invalid color '" + objectColor + "' set on: " + kSceneItem.getFullName())

            buildColor = objectColor

        else:
            # Find the first color mapping that matches a type in the object hierarchy.
            for typeName in typeNames:
                if typeName in colorMap.keys():
                    if component is None:
                        buildColor = colorMap[typeName]['default']
                    else:
                        componentLocation = component.getLocation()
                        buildColor = colorMap[typeName][componentLocation]
                    break;

        return buildColor


    def setObjectColor(self, kSceneItem):
        """Sets the color on the dccSceneItem.

        Arguments:
        kSceneItem -- Object, kraken object to set the color on.

        Return:
        True if successful.

        """

        return True


    # ==================
    # Transform Methods
    # ==================
    def setTransform(self, kSceneItem):
        """Translates the transform to Softimage transform.

        Arguments:
        kSceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        # Re-implement in DCC builders.

        return True


    # ===============
    # Config Methods
    # ===============
    def getConfig(self):
        """Gets the current config for the builder.

        Return:
        Object, config.

        """

        return self.config


    def setConfig(self, config):
        """Sets the builder's config.

        Arguments:
        config -- Config, the config to use for this builder.

        Return:
        True if successful.

        """

        self.config = config

        return True


    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Protected Pre-Build method.

        Arguments:
        kSceneItem -- Object, kraken kSceneItem object to build.

        Return:
        True if successful.

        """

        return True


    def _build(self, kSceneItem):
        """Protected build method.

        Arguments:
        kSceneItem -- Object, kraken kSceneItem object to build.

        Return:
        True if successful.

        """

        self.buildHierarchy(kSceneItem, component=None)
        self.buildAttrConnections(kSceneItem)
        self.buildIOConnections(kSceneItem)
        self.buildOperators(kSceneItem)
        self.buildConstraints(kSceneItem)

        return True


    def build(self, kSceneItem):
        """Builds the supplied kSceneItem into a DCC representation.

        Arguments:
        kSceneItem -- Object, kraken kSceneItem object to build.

        Return:
        The DCC scene item of the kSceneItem that was passed to the builder.

        """

        Profiler.getInstance().push("build:" + kSceneItem.getName())

        try:
            self._preBuild(kSceneItem)
            self._build(kSceneItem)

        finally:
            self._postBuild()

            # Clear Config when finished.
            self.config.clearInstance()

        Profiler.getInstance().pop()

        return self.getDCCSceneItem(kSceneItem)


    def _postBuild(self):
        """Protected Post-Build method.

        Return:
        True if successful.

        """

        return True

