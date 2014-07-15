"""Kraken - builders module.

Classes:
BaseBuilder -- Base builder object to build objects in DCC.

"""

from kraken.core import logger as pyLogger
logger = pyLogger.getLogger("pyLogger")


class BaseBuilder(object):
    """BaseBuilder object for building objects in DCC's. Sub-class per DCC in
    plugin.

    """

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
    def buildContainerNode(self, kSceneItem, objectName):
        """Builds a container / namespace object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        return None


    def buildLayerNode(self, kSceneItem, objectName):
        """Builds a layer object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a layer to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        return None


    def buildGroupNode(self, kSceneItem, objectName):
        """Builds a group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        return None


    def buildLocatorNode(self, kSceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a locator / null to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        return None


    def buildCurveNode(self, kSceneItem, objectName):
        """Builds a Curve object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        return None


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttributeNode(self):
        """Builds a Bool attribute.

        Return:
        True if successful.

        """

        return True


    def buildColorAttributeNode(self):
        """Builds a Color attribute.

        Return:
        True if successful.

        """

        return True


    def buildFloatAttributeNode(self):
        """Builds a Float attribute.

        Return:
        True if successful.

        """

        return True


    def buildIntegerAttributeNode(self):
        """Builds a Integer attribute.

        Return:
        True if successful.

        """

        return True


    def buildStringAttributeNode(self):
        """Builds a String attribute.

        Return:
        True if successful.

        """

        return True


    # ==============
    # Build Methods
    # ==============
    def buildAttributes(self, kSceneItem):
        """Builds attributes on the DCC object.

        Arguments:
        kSceneItem -- SceneItem, kraken object to build attributes for.

        Return:
        True if successful.

        """

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        for i in xrange(kSceneItem.getNumAttributes()):
            attribute = kSceneItem.getAttributeByIndex(i)
            kType = attribute.getKType()

            if kType == "FloatAttribute":
                self.buildFloatAttributeNode
                print kSceneItem.attributes[i].name

            elif kType == "BoolAttribute":
                print kSceneItem.attributes[i].name

            elif kType == "IntegerAttribute":
                print kSceneItem.attributes[i].name

            elif kType == "StringAttribute":
                print kSceneItem.attributes[i].name

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
            dccSceneItem = self.buildContainerNode(kSceneItem, objectName)

        elif kType == "Layer":
            dccSceneItem = self.buildLayerNode(kSceneItem, objectName)

        elif kType == "Component":
            dccSceneItem = self.buildGroupNode(kSceneItem, objectName)
            component = kSceneItem

        elif kType == "SceneItem":
            dccSceneItem = self.buildLocatorNode(kSceneItem, objectName)

        elif kType == "Curve":
            dccSceneItem = self.buildCurveNode(kSceneItem, objectName)

        elif kType == "Control":
            dccSceneItem = self.buildCurveNode(kSceneItem, objectName)

        else:
            raise NotImplementedError(kSceneItem.getName() + ' has an unsupported type: ' + str(type(kSceneItem)))

        self.buildAttributes(kSceneItem)
        self.setTransform(kSceneItem)
        self.setVisibility(kSceneItem)

        # Build children
        for i in xrange(kSceneItem.getNumChildren()):
            child = kSceneItem.getChildByIndex(i)
            self.buildHierarchy(child, component)

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

        if kType == "Component":
            return '_'.join([kSceneItem.getName(), kSceneItem.getSide(), 'hrc'])

        elif kType == "Container":
            return '_'.join([kSceneItem.getName()])

        elif kType == "Layer":
            return '_'.join([kSceneItem.parent.getName(), kSceneItem.getName()])

        elif kType == "SceneItem":
            return '_'.join([componentName, kSceneItem.getName(), side, 'null'])

        elif kType == "Curve":
            return '_'.join([componentName, kSceneItem.getName(), side, 'crv'])

        elif kType == "Control":
            return '_'.join([componentName, kSceneItem.getName(), side, 'ctrl'])

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


    # ==============
    # Build Methods
    # ==============
    def setTransform(self, sceneItem):
        """Translates the transform to Softimage transform.

        Arguments:
        sceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

        """

        dccSceneItem = self._getDCCSceneItem(sceneItem)

        # Re-implement in DCC builders.

        return True


    def buildConstraints(self, sceneItem):
        """Builds constraints for the supplied sceneItem.

        Arguments:
        sceneItem -- Object, scene item to create constraints for.

        Return:
        True if successful.

        """

        # Re-implement in DCC builders.

        return True


    def _preBuild(self, container):
        """Protected Pre-Build method.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        return True


    def _build(self, container):
        """Protected build method.

        Return:
        True if successful.

        """

        self.buildHierarchy(container, component=None)

        return True


    def build(self, container):
        """Builds the supplied container into a DCC representation.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        try:
            self._preBuild(container)
            self._build(container)

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

        for i in xrange(kSceneItem.getNumAttributes()):
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