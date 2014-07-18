"""Kraken - builders module.

Classes:
BaseBuilder -- Base builder object to build objects in DCC.

"""

from kraken.core import logger as pyLogger
logger = pyLogger.getLogger("pyLogger")


class BaseBuilder(object):
    """BaseBuilder object for building objects in DCC's. Sub-class per DCC in a
    plugin.

    """

    # Note: These were taken from Maya and is the least common denominator since
    # you can't set colors by scalar values. :\
    VALID_COLORS = {
                    "black": [1, [0.00, 0.00, 0.0]],
                    "lightGrey": [2, [0.75, 0.75, 0.75]],
                    "darkGrey": [3, [0.50, 0.50, 0.50]],
                    "fusia": [4, [0.80, 0.00, 0.20]],
                    "blueDark": [5, [0.00, 0.00, 0.40]],
                    "blue": [6, [0.00, 0.00, 1.00]],
                    "green": [7, [0.00, 0.30, 0.00]],
                    "purpleDark": [8, [0.20, 0.00, 0.30]],
                    "magenta": [9, [0.80, 0.00, 0.80]],
                    "brownLight": [10, [0.60, 0.30, 0.20]],
                    "brownDark": [11, [0.25, 0.13, 0.13]],
                    "orange": [12, [0.70, 0.20, 0.00]],
                    "red": [13, [1.00, 0.00, 0.00]],
                    "greenBright": [14, [0.00, 1.00, 0.00]],
                    "blueMedium": [15, [0.00, 0.30, 0.60]],
                    "white": [16, [1.00, 1.00, 1.00]],
                    "yellow": [17, [1.00, 1.00, 0.00]],
                    "greenBlue": [18, [0.00, 1.00, 1.00]],
                    "turqoise": [19, [0.00, 1.00, 0.80]],
                    "pink": [20, [1.00, 0.70, 0.70]],
                    "peach": [21, [0.90, 0.70, 0.50]],
                    "yellowLight": [22, [1.00, 1.00, 0.40]],
                    "turqoiseDark": [23, [0.00, 0.70, 0.40]],
                    "brownMuted": [24, [0.60, 0.40, 0.20]],
                    "yellowMuted": [25, [0.63, 0.63, 0.17]],
                    "greenMuted": [26, [0.40, 0.60, 0.20]],
                    "turqoiseMuted": [27, [0.20, 0.63, 0.35]],
                    "blueLightMuted": [28, [0.18, 0.63, 0.63]],
                    "blueDarkMuted": [29, [0.18, 0.40, 0.63]],
                    "purpleLight": [30, [0.43, 0.18, 0.63]],
                    "mutedMagenta": [31, [0.63, 0.18, 0.40]]
                   }


    def __init__(self):
        super(BaseBuilder, self).__init__()
        self._buildElements = []


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


    # ===================
    # Node Build Methods
    # ===================
    def buildContainer(self, kSceneItem, objectName):
        """Builds a container / namespace object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        objectName -- String, name of the object being created.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildLayer(self, kSceneItem, objectName):
        """Builds a layer object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a layer to be built.
        objectName -- String, name of the object being created.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildHierarchyGroup(self, kSceneItem, objectName):
        """Builds a hierarchy group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildGroup(self, kSceneItem, objectName):
        """Builds a group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildLocator(self, kSceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a locator / null to be built.
        objectName -- String, name of the object being created.

        Return:
        DCC Scene Item that is created.

        """

        return None


    def buildCurve(self, kSceneItem, objectName):
        """Builds a Curve object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

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


    def buildColorAttribute(self, kAttribute):
        """Builds a Color attribute.

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

        parentDCCSceneItem = self._getDCCSceneItem(kConstraint.getParent())
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

        parentDCCSceneItem = self._getDCCSceneItem(kConstraint.getParent())
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

        parentDCCSceneItem = self._getDCCSceneItem(kConstraint.getParent())
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

        parentDCCSceneItem = self._getDCCSceneItem(kConstraint.getParent())
        dccSceneItem = None # Add constraint object here.
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    # =====================
    # Build Object Methods
    # =====================
    def buildAttributes(self, kSceneItem):
        """Builds attributes on the DCC object.

        Arguments:
        kSceneItem -- SceneItem, kraken object to build attributes for.

        Return:
        True if successful.

        """

        for i in xrange(kSceneItem.getNumAttributeGroups()):
            attributeGroup = kSceneItem.getAttributeGroupByIndex(i)

            attributeCount = attributeGroup.getNumAttributes()
            if attributeCount < 1:
                continue

            self.buildAttributeGroup(attributeGroup)

            for j in xrange(attributeCount):
                attribute = attributeGroup.getAttributeByIndex(j)
                kType = attribute.getKType()

                if kType == "FloatAttribute":
                    self.buildFloatAttribute(attribute)

                elif kType == "BoolAttribute":
                    self.buildBoolAttribute(attribute)

                elif kType == "IntegerAttribute":
                    self.buildIntegerAttribute(attribute)

                elif kType == "StringAttribute":
                    self.buildStringAttribute(attribute)

        return True


    def buildHierarchy(self, kSceneItem, component=None):
        """Builds the hierarchy for the supplied kSceneItem.

        Arguments:
        kSceneItem -- SceneItem, kraken object to build.
        component -- Component, component that this object belongs to.

        Return:
        DCC object that was created.

        """

        dccSceneItem = None
        objectName = self.buildName(kSceneItem, component=component)
        kType = kSceneItem.getKType()

        # Build Object
        if kType == "Container":
            dccSceneItem = self.buildContainer(kSceneItem, objectName)

        elif kType == "Layer":
            dccSceneItem = self.buildLayer(kSceneItem, objectName)

        elif kType == "Component":
            dccSceneItem = self.buildGroup(kSceneItem, objectName)
            component = kSceneItem

        elif kType == "HierarchyGroup":
            dccSceneItem = self.buildHierarchyGroup(kSceneItem, objectName)

        elif kType == "SceneItem":
            dccSceneItem = self.buildLocator(kSceneItem, objectName)

        elif kType == "Curve":
            dccSceneItem = self.buildCurve(kSceneItem, objectName)

        elif kType == "Control":
            dccSceneItem = self.buildCurve(kSceneItem, objectName)

        else:
            raise NotImplementedError(kSceneItem.getName() + ' has an unsupported type: ' + str(type(kSceneItem)))

        self.buildAttributes(kSceneItem)
        self.setTransform(kSceneItem)
        self.setVisibility(kSceneItem)
        self.setObjectColor(kSceneItem)

        # Build children
        for i in xrange(kSceneItem.getNumChildren()):
            child = kSceneItem.getChildByIndex(i)
            self.buildHierarchy(child, component)

        return dccSceneItem


    def buildConstraints(self, kSceneItem):
        """Builds constraints for the supplied kSceneItem.

        Arguments:
        kSceneItem -- Object, kraken scene item to create constraints for.

        Return:
        True if successful.

        """

        dccSceneItem = None
        for i in xrange(kSceneItem.getNumConstraints()):

            constraint = kSceneItem.getConstraintByIndex(i)
            kType = constraint.getKType()

            # Build Object
            if kType == "OrientationConstraint":
                dccSceneItem = self.buildOrientationConstraint(constraint)

            elif kType == "PoseConstraint":
                dccSceneItem = self.buildPoseConstraint(constraint)

            elif kType == "PositionConstraint":
                dccSceneItem = self.buildPositionConstraint(constraint)

            elif kType == "ScaleConstraint":
                dccSceneItem = self.buildScaleConstraint(constraint)

            else:
                raise NotImplementedError(constraint.getName() + ' has an unsupported type: ' + str(type(constraint)))

        # Build children
        for i in xrange(kSceneItem.getNumChildren()):
            child = kSceneItem.getChildByIndex(i)
            self.buildConstraints(child)

        return dccSceneItem


    def buildName(self, kSceneItem, component=None):
        """Builds the name for the kSceneItem that is passed.

        Arguments:
        kSceneItem -- SceneItem, kraken object to build the name for.
        component -- Component, component that this object belongs to.

        Return:
        Built name as a string.
        None if it fails.

        """

        componentName = ""
        side = ""
        kType = kSceneItem.getKType()

        if component is not None:
            componentName = component.getName()
            side = component.getSide()

        if kType == "Container":
            return '_'.join([kSceneItem.getName()])

        elif kType == "Layer":
            return '_'.join([kSceneItem.parent.getName(), kSceneItem.getName()])

        elif kType == "Component":
            return '_'.join([kSceneItem.getName(), kSceneItem.getSide(), 'hrc'])

        elif kType == "HierarchyGroup":
            return '_'.join([componentName, side, kSceneItem.getName(), 'hrc'])

        elif kType == "Locator":
            return '_'.join([componentName, kSceneItem.getName(), side, 'null'])

        elif kType == "SceneItem":
            return '_'.join([componentName, kSceneItem.getName(), side, 'null'])

        elif kType == "Curve":
            return '_'.join([componentName, kSceneItem.getName(), side, 'crv'])

        elif kType == "Control":
            nameParts = [componentName, kSceneItem.getName(), side, 'ctrl']
            nameParts = [x for x in nameParts if x != ""]
            return '_'.join(nameParts)

        else:
            raise NotImplementedError('buildName() not implemented for ' + str(type(kSceneItem)))

        return None


    # ===================
    # Visibility Methods
    # ===================
    def setVisibility(self, kSceneItem):
        """Sets the visibility of the object after its been created.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        if kSceneItem.getShapeVisibility() is False:
            pass

            # Re-implement in DCC builders.

        return True


    # ================
    # Display Methods
    # ================
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
        self.buildConstraints(kSceneItem)

        return True


    def build(self, kSceneItem):
        """Builds the supplied kSceneItem into a DCC representation.

        Arguments:
        kSceneItem -- Object, kraken kSceneItem object to build.

        Return:
        True if successful.

        """

        try:
            self._preBuild(kSceneItem)
            self._build(kSceneItem)

        finally:
            self._postBuild()

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

            kType = kSceneItem.getKType()

            # Build Object
            if kType == "Container":
                self.synchronizeContainerNode(kSceneItem, dccSceneItem)

            elif kType == "Layer":
                self.synchronizeLayerNode(kSceneItem, dccSceneItem)

            elif kType == "Component":
                self.synchronizeGroupNode(kSceneItem, dccSceneItem)

            elif kType == "SceneItem":
                self.synchronizeLocatorNode(kSceneItem, dccSceneItem)

            elif kType == "Curve":
                self.synchronizeCurveNode(kSceneItem, dccSceneItem)

            elif kType == "Control":
                self.synchronizeCurveNode(kSceneItem, dccSceneItem)

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
            kType = attribute.getKType()

            if kType == "FloatAttribute":
                print kSceneItem.attributes[i].name

            elif kType == "BoolAttribute":
                print kSceneItem.attributes[i].name

            elif kType == "IntegerAttribute":
                print kSceneItem.attributes[i].name

            elif kType == "StringAttribute":
                print kSceneItem.attributes[i].name

        return True