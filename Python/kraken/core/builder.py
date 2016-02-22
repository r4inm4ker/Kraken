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


    def __init__(self, debugMode = False):
        super(Builder, self).__init__()
        self._buildElements = []

        self.config = Config.getInstance()

        self._debugMode = debugMode


    # ====================
    # Object registration
    # ====================
    def _registerSceneItemPair(self, kSceneItem, dccSceneItem):
        """Registers a pairing between the kraken scene item and the dcc scene item
        for querying later.

        Args:
            kSceneItem (object): kraken scene item that you want to pair.
            dccSceneItem (object): dcc scene item that you want to pair.

        Returns:
            bool: True if successful.

        """

        pairing = {
                   'src': kSceneItem,
                   'tgt': dccSceneItem
                  }

        self._buildElements.append(pairing)

        return True

    def deleteBuildElements(self):
        """Clear out all dcc built elements from the scene if exist."""

        return None


    def getDCCSceneItem(self, kSceneItem):
        """Given a kSceneItem, returns the built dcc scene item.

        Args:
            kSceneItem (object): kSceneItem to base the search.

        Returns:
            object: The DCC Scene Item that corresponds to the given scene item

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

        Args:
            kSceneItem (object): kSceneItem that represents a container to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Args:
            kSceneItem (object): kSceneItem that represents a layer to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Args:
            kSceneItem (object): kSceneItem that represents a group to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    def buildGroup(self, kSceneItem, buildName):
        """Builds a group object.

        Args:
            kSceneItem (object): kSceneItem that represents a group to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Args:
            kSceneItem (object): kSceneItem that represents a joint to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Args:
            kSceneItem (object): kSceneItem that represents a locator / null to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Args:
            kSceneItem (object): kSceneItem that represents a curve to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Args:
            kSceneItem (object): kSceneItem that represents a control to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        return None


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kAttribute):
        """Builds a Bool attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            object: True if successful.

        """

        return True


    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            bool: True if successful.

        """

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            bool: True if successful.

        """

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            bool: True if successful.

        """

        return True


    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Args:
            kAttributeGroup (SceneObject): kraken object to build the attribute group on.

        Returns:
            bool: True if successful.

        """

        return True


    def connectAttribute(self, kAttribute):
        """Connects the driver attribute to this one.

        Args:
            kAttribute (object): attribute to connect.

        Returns:
            bool: True if successful.

        """

        return True


    # =========================
    # Constraint Build Methods
    # =========================
    def buildOrientationConstraint(self, kConstraint):
        """Builds an orientation constraint represented by the kConstraint.

        Args:
            kConstraint (object): kraken constraint object to build.

        Returns:
            object: DCC Scene Item that was created.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPoseConstraint(self, kConstraint):
        """Builds an pose constraint represented by the kConstraint.

        Args:
            kConstraint (object): kraken constraint object to build.

        Returns:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Args:
            kConstraint (object): kraken constraint object to build.

        Returns:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildScaleConstraint(self, kConstraint):
        """Builds an scale constraint represented by the kConstraint.

        Args:
            kConstraint (object): kraken constraint object to build.

        Returns:
            bool: True if successful.

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

        Args:
            componentInput (object): kraken component input to build connections for.

        Returns:
            bool: True if successful.

        """

        if componentInput.isConnected() is False:
            return False

        connection = componentInput.getConnection()
        connectionTarget = connection.getTarget()
        inputTarget = componentInput.getTarget()

        if connection.getDataType().endswith('[]'):
            if componentInput.getIndex() > len(connection.getTarget()) - 1:

                inputParent = componentInput.getParent()
                inputParentDecoration = inputParent.getNameDecoration()
                fullInputName = inputParent.getName() + inputParentDecoration + "." + componentInput.getName()

                raise Exception(fullInputName + " index ("
                                + str(componentInput.getIndex()) + ") is out of range ("
                                + str(len(connection.getTarget()) - 1) + ")!")

            connectionTarget = connection.getTarget()[componentInput.getIndex()]
        else:
            connectionTarget = connection.getTarget()

        # There should be no offset between an output xfo from one component and the connected input of another
        # If connected, they should be exactly the same.
        constraint = inputTarget.constrainTo(connectionTarget, maintainOffset=False)

        dccSceneItem = self.buildPoseConstraint(constraint)
        self._registerSceneItemPair(componentInput, dccSceneItem)

        return True


    def buildAttributeConnection(self, componentInput):
        """Builds the link between the target and connection target.

        Args:
            componentInput (object): kraken connection to build.

        Returns:
            bool: True if successful.

        """

        # Implemented in DCC Plugins.

        return True


    # =========================
    # Operator Builder Methods
    # =========================
    def buildKLOperator(self, kKLOperator):
        """Builds Splice Operators on the components.

        Args:
            kOperator (object): kraken operator that represents a KL operator.

        Returns:
            bool: True if successful.

        """

        return True

    def buildCanvasOperator(self, kOperator):
        """Builds Splice Operators on the components.

        Args:
            kOperator (object): kraken operator that represents a Canvas operator.

        Returns:
            bool: True if successful.

        """

        return True


    # =====================
    # Build Object Methods
    # =====================
    def buildAttributes(self, kObject):
        """Builds attributes on the DCC object.

        Args:
            kObject (SceneObject): kraken object to build attributes for.

        Returns:
            bool: True if successful.

        """

        for i in xrange(kObject.getNumAttributeGroups()):
            attributeGroup = kObject.getAttributeGroupByIndex(i)
            self.buildAttributeGroup(attributeGroup)

        return True


    def buildHierarchy(self, kObject, component=None):
        """Builds the hierarchy for the supplied kObject.

        Args:
            kObject (object): kraken object to build.
            component (Component): component that this object belongs to.

        Returns:
            object: DCC object that was created.

        """


        dccSceneItem = None

        buildName = kObject.getBuildName()

        if self._debugMode:
            print "building:" + kObject.getPath() + " as:" + buildName

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

        elif kObject.isTypeOf("Transform"):
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

        Args:
            kObject (object): kraken object to create constraints for.

        Returns:
            bool: True if successful.

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


    def buildInputConnections(self, kObject):
        """Builds the connections between the component inputs of each
        component.

        Only input connections are built otherwise duplicate constraints / expressions
        would be created.

        Args:
            kObject (object): kraken object to create connections for.

        Returns:
            bool: True if successful.

        """

        if kObject.isTypeOf('Component'):

            # Build input connections
            for i in xrange(kObject.getNumInputs()):

                componentInput = kObject.getInputByIndex(i)
                if componentInput.getTarget() is None or componentInput.getConnection() is None:
                    continue

                if self._debugMode:
                    print "buildConnection:" + componentInput.getName()

                if componentInput.getDataType().startswith('Xfo'):
                    self.buildXfoConnection(componentInput)

                elif componentInput.getDataType().startswith(('Boolean', 'Float', 'Integer', 'String')):
                    self.buildAttributeConnection(componentInput)

        # Build connections for children.
        for i in xrange(kObject.getNumChildren()):
            child = kObject.getChildByIndex(i)
            self.buildInputConnections(child)

        return True


    def buildAttrConnections(self, kObject):
        """Builds the connections between the component inputs and outputs of each
        component.

        Args:
            kObject (object): kraken object to create connections for.

        Returns:
            bool: True if successful.

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

        Args:
            kObject (object): kraken object to create operators for.

        Returns:
            bool: True if successful.

        """

        if kObject.isTypeOf('Component'):

            # Build operators
            for i in xrange(kObject.getNumOperators()):
                operator = kObject.getOperatorByIndex(i)

                if operator.isTypeOf('KLOperator'):
                    self.buildKLOperator(operator)
                elif operator.isTypeOf('CanvasOperator'):
                    self.buildCanvasOperator(operator)
                else:
                    raise NotImplementedError(operator.getName() + ' has an unsupported type: ' + str(type(operator)))

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

        Args:
            kSceneItem (object): kraken object to lock the SRT parameters on.

        Returns:
            bool: True if successful.

        """

        return True


    # ===================
    # Visibility Methods
    # ===================
    def setVisibility(self, kSceneItem):
        """Sets the visibility of the object after its been created.

        Args:
            kSceneItem (object): kraken object to set the visibility on.

        Returns:
            bool: True if successful.

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

        Args:
            kSceneItem (object): kraken object to get the color for.

        Returns:
            str: color to set on the object.

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
                raise ValueError("Invalid color '" + objectColor + "' set on: " + kSceneItem.getPath())

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
                    break

        return buildColor


    def setObjectColor(self, kSceneItem):
        """Sets the color on the dccSceneItem.

        Args:
            kSceneItem (object): kraken object to set the color on.

        Returns:
            bool: True if successful.

        """

        return True


    # ==================
    # Transform Methods
    # ==================
    def setTransform(self, kSceneItem):
        """Translates the transform to Softimage transform.

        Args:
            kSceneItem (object): object to set the transform on.

        Returns:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        # Re-implement in DCC builders.

        return True


    # ===============
    # Config Methods
    # ===============
    def getConfig(self):
        """Gets the current config for the builder.

        Returns:
            object: config.

        """

        return self.config


    def setConfig(self, config):
        """Sets the builder's config.

        Args:
            config (Config): the config to use for this builder.

        Returns:
            bool: True if successful.

        """

        self.config = config

        return True


    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Protected Pre-Build method.

        Args:
            kSceneItem (object): kraken kSceneItem object to build.

        Returns:
            bool: True if successful.

        """

        return True


    def _build(self, kSceneItem):
        """Protected build method.

        Args:
            kSceneItem (object): kraken kSceneItem object to build.

        Returns:
            bool: True if successful.

        """

        self.buildHierarchy(kSceneItem, component=None)
        self.buildAttrConnections(kSceneItem)
        self.buildInputConnections(kSceneItem)
        self.buildOperators(kSceneItem)
        self.buildConstraints(kSceneItem)

        return True


    def build(self, kSceneItem):
        """Builds the supplied kSceneItem into a DCC representation.

        Args:
            kSceneItem (object): kraken kSceneItem object to build.

        Returns:
            object: The DCC scene item of the kSceneItem that was passed to the builder.

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

        Returns:
            bool: True if successful.

        """

        return True

