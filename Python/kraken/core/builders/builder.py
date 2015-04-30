"""Kraken - builders module.

Classes:
Builder -- Base builder object to build objects in DCC.

"""

from kraken.core import logger as pyLogger
logger = pyLogger.getLogger("pyLogger")

from kraken.core.configs.config import Config

from kraken.core.objects.components.component import Component
from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.profiler import Profiler


class Builder(object):
    """Builder object for building objects in DCC's. Sub-class per DCC in a
    plugin.

    """


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


    def _getDCCSceneItem(self, kSceneItem):
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

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())
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

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())
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

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())
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

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    # ========================
    # Component Build Methods
    # ========================
    def buildXfoConnection(self, kConnection):
        """Builds the connection between the xfo and the connection.

        Arguments:
        kConnection -- Object, kraken connection to build.

        Return:
        True if successful.

        """

        source = kConnection.getSource()
        target = kConnection.getTarget()

        if source is None or target is None:
            raise Exception("Component connection '" + kConnection.getName() + "'is invalid! Missing Source or Target!")

        constraint = PoseConstraint('_'.join([target.getName(), 'To', source.getName()]))
        constraint.setMaintainOffset(True)
        constraint.setConstrainee(target)
        constraint.addConstrainer(source)
        dccSceneItem = self.buildPoseConstraint(constraint)
        self._registerSceneItemPair(kConnection, dccSceneItem)

        return None


    def buildAttributeConnection(self, kConnection):
        """Builds the connection between the attribute and the connection.

        Arguments:
        kConnection -- Object, kraken connection to build.

        Return:
        True if successful.

        """

        return None


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
            if attributeCount < 1:
                continue

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

        Arguments:
        kObject -- Object, kraken object to create connections for.

        Return:
        True if successful.

        """

        if kObject.isTypeOf('Component'):

            # Build input connections
            for i in xrange(kObject.getNumInputs()):
                componentInput = kObject.getInputByIndex(i)

                if componentInput.getDataType() == 'Xfo':
                    if componentInput.getSource() is None:
                        continue

                    self.buildXfoConnection(componentInput)

                elif componentInput.getDataType() == 'Attribute':
                    if componentInput.getSource() is None:
                        continue

                    self.buildAttributeConnection(componentInput)

            # Build output connections
            for i in xrange(kObject.getNumOutputs()):
                componentOutput = kObject.getOutputByIndex(i)

                if componentOutput.getDataType() == 'Xfo':
                    if componentOutput.getSource() is None:
                        continue

                    self.buildXfoConnection(componentOutput)

                elif componentOutput.getDataType() == 'Attribute':
                    if componentOutput.getSource() is None:
                        continue

                    self.buildAttributeConnection(componentOutput)

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

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

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
        True if successful.

        """

        Profiler.getInstance().push("build:" + kSceneItem.getName())

        try:
            self._preBuild(kSceneItem)
            self._build(kSceneItem)

        finally:
            self._postBuild()

            # Clear config instance when finished.
            self.config.clearInstance()

        Profiler.getInstance().pop()

        return True


    def _postBuild(self):
        """Protected Post-Build method.

        Return:
        True if successful.

        """

        return True


    # ==============================
    # Synchrnization Object Methods
    # ==============================
    def synchronizeName(self, kSceneItem, dccSceneItem):
        """Synchronizes the name between the dcc scene item and the corresponding kraken scene item.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        dccSceneItem -- Object, the element in the host DCC application

        Return:
        True if the synchronization was successful.

        """

        return False


    def synchronizeContainerNode(self, kSceneItem, dccSceneItem):
        """Synchronizes a container / namespace with the corresponding kraken scene item.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        dccSceneItem -- Object, the element in the host DCC application

        Return:
        True if the synchronization was successful.

        """

        return False


    def synchronizeLayerNode(self, kSceneItem, dccSceneItem):
        """Synchronizes a layer object with the corresponding kraken scene item.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a layer to be built.
        dccSceneItem -- Object, the element in the host DCC application

        Return:
        True if the synchronization was successful.

        """

        return False


    def synchronizeGroupNode(self, kSceneItem, dccSceneItem):
        """Synchronizes a group object with the corresponding kraken scene item.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        dccSceneItem -- Object, the element in the host DCC application

        Return:
        True if the synchronization was successful.

        """

        return False


    def synchronizeLocatorNode(self, kSceneItem, dccSceneItem):
        """Synchronizes a locator / null object with the corresponding kraken scene item.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a locator / null to be built.
        dccSceneItem -- Object, the element in the host DCC application

        Return:
        True if the synchronization was successful.

        """

        return False


    def synchronizeCurveNode(self, kSceneItem, dccSceneItem):
        """Synchronizes a Curve object with the corresponding kraken scene item.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a curve to be built.
        dccSceneItem -- Object, the element in the host DCC application

        Return:
        True if the synchronization was successful.

        """

        return False


    def synchronize(self):
        """Synchronizes the Kraken hierarchy with the DCC data

        Return:
        True if the synchronization was successful.

        """

        for builtElement in self._buildElements:
            dccSceneItem = builtElement['tgt']
            kSceneItem = builtElement['src']

            # Build Object
            if kSceneItem.isTypeOf("Container"):
                self.synchronizeContainerNode(kSceneItem, dccSceneItem)

            elif kSceneItem.isTypeOf("Layer"):
                self.synchronizeLayerNode(kSceneItem, dccSceneItem)

            elif kSceneItem.isTypeOf("Component"):
                self.synchronizeGroupNode(kSceneItem, dccSceneItem)

            elif kSceneItem.isTypeOf("Control"):
                self.synchronizeCurveNode(kSceneItem, dccSceneItem)

            elif kSceneItem.isTypeOf("Curve"):
                self.synchronizeCurveNode(kSceneItem, dccSceneItem)

            elif kSceneItem.isTypeOf("SceneItem"):
                self.synchronizeLocatorNode(kSceneItem, dccSceneItem)

            else:
                raise NotImplementedError(kSceneItem.getName() + ' has an unsupported type: ' + str(type(kSceneItem)))


    # ==============================
    # Synchronize Attribute Methods
    # ==============================
    def synchronizeBoolAttributeNode(self):
        """Synchronizes a Bool attribute with the corresponding kraken scene item.

        Return:
        True if the synchronization was successful.

        """

        return True


    def synchronizeColorAttributeNode(self):
        """Synchronizes a Color attribute with the corresponding kraken scene item.

        Return:
        True if the synchronization was successful.

        """

        return True


    def synchronizeFloatAttributeNode(self):
        """Synchronizes a Float attribute with the corresponding kraken scene item.

        Return:
        True if the synchronization was successful.

        """

        return True


    def synchronizeIntegerAttributeNode(self):
        """Synchronizes a Integer attribute with the corresponding kraken scene item.

        Return:
        True if the synchronization was successful.

        """

        return True


    def synchronizeStringAttributeNode(self):
        """Synchronizes a String attribute with the corresponding kraken scene item.

        Return:
        True if the synchronization was successful.

        """

        return True


    def synchronizeAttributes(self, kSceneItem, dccSceneItem):
        """Synchronizes attributes on the DCC object.

        Arguments:
        kSceneItem -- SceneItem, kraken object to build attributes for.

        Return:
        True if the synchronization was successful.

        """

        for i in xrange(kSceneItem.getNumAttributeGroups()):
            attribute = kSceneItem.getAttributeByIndex(i)

            if attribute.isTypeOf("FloatAttribute"):
                print kSceneItem.attributes[i].name

            elif attribute.isTypeOf("BoolAttribute"):
                print kSceneItem.attributes[i].name

            elif attribute.isTypeOf("IntegerAttribute"):
                print kSceneItem.attributes[i].name

            elif attribute.isTypeOf("StringAttribute"):
                print kSceneItem.attributes[i].name

        return True