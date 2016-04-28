"""Kraken - builders module.

Classes:
Builder -- Base builder object to build objects in DCC.

"""

from collections import deque

from kraken.core.kraken_system import KrakenSystem
from kraken.core.configs.config import Config
from kraken.core.profiler import Profiler

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.components.component import Component
from kraken.core.objects.constraints.pose_constraint import Constraint
from kraken.core.objects.operators.operator import Operator
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.traverser.traverser import Traverser


class Builder(object):
    """Builder object for building objects in DCC's. Sub-class per DCC in a
    plugin."""

    _buildPhase_3DObjectsAttributes = 0
    _buildPhase_AttributeConnections = 1
    _buildPhase_ConstraintsOperators = 2

    def __init__(self, debugMode = False):
        super(Builder, self).__init__()
        self._buildElements = []
        self._sceneItemsById = {}

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

        if isinstance(kSceneItem, SceneItem):
            for builtElement in self._buildElements:
                if builtElement['src'] == kSceneItem:
                    return builtElement['tgt']

        return None


    def getDCCSceneItemPairs(self):
        """Returns all of the built dcc scene item pairs.

        Returns:
            array: An array of dicts with 'src' and 'tgt' key value pairs

        """
        return self._buildElements


    # ========================
    # SceneItem Build Methods
    # ========================
    def buildContainer(self, kContainer, buildName):
        """Builds a container / namespace object.

        Args:
            kContainer (object): kContainer that represents a container to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        if self._debugMode:
            print "buildContainer: " + kContainer.getPath() + " as: " + buildName

        return self.buildLocator(kContainer, buildName)


    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Args:
            kSceneItem (object): kSceneItem that represents a layer to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        if self._debugMode:
            print "buildLayer: " + kSceneItem.getPath() + " as: " + buildName

        return None


    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Args:
            kSceneItem (object): kSceneItem that represents a group to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """


        if self._debugMode:
            print "buildHierarchyGroup: " + kSceneItem.getPath() + " as: " + buildName

        return None


    def buildGroup(self, kSceneItem, buildName):
        """Builds a group object.

        Args:
            kSceneItem (object): kSceneItem that represents a group to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        if self._debugMode:
            print "buildGroup: " + kSceneItem.getPath() + " as: " + buildName

        return None


    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Args:
            kSceneItem (object): kSceneItem that represents a joint to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        if self._debugMode:
            print "buildJoint: " + kSceneItem.getPath() + " as: " + buildName

        return None


    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Args:
            kSceneItem (object): kSceneItem that represents a locator / null to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """


        if self._debugMode:
            print "buildLocator: " + kSceneItem.getPath() + " as: " + buildName

        return None


    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Args:
            kSceneItem (object): kSceneItem that represents a curve to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        if self._debugMode:
            print "buildCurve: " + kSceneItem.getPath() + " as: " + buildName


        return None


    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Args:
            kSceneItem (object): kSceneItem that represents a control to be built.
            buildName (string): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        if self._debugMode:
            print "buildControl:" + kSceneItem.getPath() + " as: " + buildName

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

        if self._debugMode:
            print "buildBoolAttribute: " + kAttribute.getPath()

        return True


    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            bool: True if successful.

        """


        if self._debugMode:
            print "buildScalarAttribute: " + kAttribute.getPath()

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            bool: True if successful.

        """


        if self._debugMode:
            print "buildIntegerAttribute: " + kAttribute.getPath()

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            bool: True if successful.

        """

        if self._debugMode:
            print "buildStringAttribute: " + kAttribute.getPath()

        return True


    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Args:
            kAttributeGroup (SceneObject): kraken object to build the attribute group on.

        Returns:
            bool: True if successful.

        """

        if self._debugMode:
            print "buildAttributeGroup: " + kAttributeGroup.getPath()

        return True


    def connectAttribute(self, kAttribute):
        """Connects the driver attribute to this one.

        Args:
            kAttribute (object): attribute to connect.

        Returns:
            bool: True if successful.

        """


        if self._debugMode:
            print "connectAttribute: " + kAttribute.getPath()

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

        if self._debugMode:
            print "buildOrientationConstraint: " + kConstraint.getPath() + " to: " + kConstraint.getConstrainee().getPath()

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
        if self._debugMode:
            print "buildPoseConstraint: " + kConstraint.getPath() + " to: " + kConstraint.getConstrainee().getPath()

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
        if self._debugMode:
            print "buildPositionConstraint:" + kConstraint.getPath() + " to: " + kConstraint.getConstrainee().getPath()

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
        if self._debugMode:
            print "buildScaleConstraint: " + kConstraint.getPath() + " to: " + kConstraint.getConstrainee().getPath()

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    # ========================
    # Component Build Methods
    # ========================

    def buildAttributeConnection(self, componentInput):
        """Builds the link between the target and connection target.

        Args:
            componentInput (object): kraken connection to build.

        Returns:
            bool: True if successful.

        """
        if self._debugMode:
            print "buildAttributeConnection: " + componentInput.getPath()


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
        if self._debugMode:
            print "buildKLOperator:" + kKLOperator.getPath()

        return True

    def buildCanvasOperator(self, kOperator):
        """Builds Splice Operators on the components.

        Args:
            kOperator (object): kraken operator that represents a Canvas operator.

        Returns:
            bool: True if successful.

        """
        if self._debugMode:
            print "buildCanvasOperator: " + kOperator.getPath()

        return True


    # =====================
    # Build Object Methods
    # =====================

    def __buildSceneItem(self, kObject, phase):
        """Builds the DCC sceneitem for the supplied kObject.

        Args:
            kObject (object): kraken object to build.

        Returns:
            object: DCC object that was created.

        """

        dccSceneItem = None

        buildName = kObject.getName()
        if hasattr(kObject, 'getBuildName'):
            buildName = kObject.getBuildName()

        if self._debugMode:
            print "building(" + str(phase) + "): " + kObject.getPath() + " as: " + buildName + " type: " + kObject.getTypeName()

        # Build Object
        if kObject.isTypeOf("Rig"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildContainer(kObject, buildName)

        elif kObject.isTypeOf("Layer"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildLayer(kObject, buildName)

        elif kObject.isTypeOf("Component"):
            return None

        elif kObject.isTypeOf("ComponentGroup"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildGroup(kObject, buildName)

        elif kObject.isTypeOf("HierarchyGroup"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildHierarchyGroup(kObject, buildName)

        elif kObject.isTypeOf("CtrlSpace"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildGroup(kObject, buildName)

        elif kObject.isTypeOf("Transform"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildGroup(kObject, buildName)

        elif kObject.isTypeOf("Locator"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildLocator(kObject, buildName)

        elif kObject.isTypeOf("Joint"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildJoint(kObject, buildName)

        elif kObject.isTypeOf("Control"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildControl(kObject, buildName)

        elif kObject.isTypeOf("Curve"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildCurve(kObject, buildName)

        elif kObject.isTypeOf('AttributeGroup'):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildAttributeGroup(kObject)

        elif kObject.isTypeOf("BoolAttribute"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildBoolAttribute(kObject)
            elif phase == self._buildPhase_AttributeConnections:
                self.connectAttribute(kObject)

        elif kObject.isTypeOf("ScalarAttribute"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildScalarAttribute(kObject)
            elif phase == self._buildPhase_AttributeConnections:
                self.connectAttribute(kObject)

        elif kObject.isTypeOf("IntegerAttribute"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem= self.buildIntegerAttribute(kObject)
            elif phase == self._buildPhase_AttributeConnections:
                self.connectAttribute(kObject)

        elif kObject.isTypeOf("StringAttribute"):
            if phase == self._buildPhase_3DObjectsAttributes:
                dccSceneItem = self.buildStringAttribute(kObject)
            elif phase == self._buildPhase_AttributeConnections:
                self.connectAttribute(kObject)

        elif kObject.isTypeOf("OrientationConstraint"):
            if phase == self._buildPhase_ConstraintsOperators:
                dccSceneItem = self.buildOrientationConstraint(kObject)

        elif kObject.isTypeOf("PoseConstraint"):
            if phase == self._buildPhase_ConstraintsOperators:
                dccSceneItem = self.buildPoseConstraint(kObject)

        elif kObject.isTypeOf("PositionConstraint"):
            if phase == self._buildPhase_ConstraintsOperators:
                dccSceneItem = self.buildPositionConstraint(kObject)

        elif kObject.isTypeOf("ScaleConstraint"):
            if phase == self._buildPhase_ConstraintsOperators:
                dccSceneItem = self.buildScaleConstraint(kObject)

        elif kObject.isTypeOf("KLOperator"):
            if phase == self._buildPhase_ConstraintsOperators:
                dccSceneItem = self.buildKLOperator(kObject)

        elif kObject.isTypeOf("CanvasOperator"):
            if phase == self._buildPhase_ConstraintsOperators:
                dccSceneItem = self.buildCanvasOperator(kObject)

        # Important Note: The order of these tests is important.
        # New classes should be added above the classes they are derrived from.
        # No new types should be added below SceneItem here.
        elif kObject.isTypeOf("SceneItem"):
            if phase == 0:
                dccSceneItem = self.buildLocator(kObject, buildName)

        else:
            raise NotImplementedError(kObject.getName() + ' has an unsupported type: ' + str(type(kObject)))

        if dccSceneItem is not None:
            self._sceneItemsById[kObject.getId()] = dccSceneItem
        else:
            dccSceneItem = self._sceneItemsById.get(kObject.getId(), None)

        if dccSceneItem is not None and isinstance(kObject, Object3D) and phase == self._buildPhase_ConstraintsOperators:
            self.setTransform(kObject)
            self.lockParameters(kObject)
            self.setVisibility(kObject)
            self.setObjectColor(kObject)

        return dccSceneItem


    def __buildSceneItemList(self, kObjects, phase):

        for kObject in kObjects:
            self.__buildSceneItem(kObject, phase)


    def build(self, kSceneItem):
        """Builds a rig object.

        We have to re-order component children by walking the graph to ensure
        that inputs objects are in place for the dependent components.

        Args:
            kSceneItem (sceneitem): The item to be built.

        Returns:
            object: DCC Scene Item that is created.

        """

        Profiler.getInstance().push("build:" + kSceneItem.getName())

        traverser = Traverser('Children')
        traverser.addRootItem(kSceneItem)
        
        rootItems = traverser.traverse(discoverCallback=traverser.discoverChildren, discoveredItemsFirst=False)

        traverser = Traverser('Build')
        for rootItem in rootItems:
            traverser.addRootItem(rootItem)
        traverser.traverse()

        try:
            self._preBuild(kSceneItem)

            buildName = kSceneItem.getBuildName()

            objects3d = traverser.getItemsOfType('Object3D')
            attributes = traverser.getItemsOfType(['AttributeGroup', 'Attribute'])

            # build all 3D objects and attributes
            self.__buildSceneItemList(objects3d, self._buildPhase_3DObjectsAttributes)
            self.__buildSceneItemList(attributes, self._buildPhase_3DObjectsAttributes)

            # connect all attributes
            self.__buildSceneItemList(attributes, self._buildPhase_AttributeConnections)

            # build all additional connections
            self.__buildSceneItemList(traverser.items, self._buildPhase_ConstraintsOperators)

        finally:
            self._postBuild()

            # Clear Config when finished.
            self.config.clearInstance()

        Profiler.getInstance().pop()

        return self.getDCCSceneItem(kSceneItem)

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

    def _postBuild(self):
        """Protected Post-Build method.

        Returns:
            bool: True if successful.

        """

        return True

