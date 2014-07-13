"""Kraken - builders module.

Classes:
BaseBuilder -- Base builder object to build objects in DCC.

"""


class BaseBuilder(object):
    """BaseBuilder object for building objects in DCC's. Sub-class per DCC in
    plugin.

    """

    def __init__(self):
        super(BaseBuilder, self).__init__()


    # ===================
    # Node Build Methods
    # ===================
    def buildContainerNode(self, parentNode, sceneItem, objectName):
        """Builds a container / namespace object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        return None


    def buildLayerNode(self, parentNode, sceneItem, objectName):
        """Builds a layer object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        return None


    def buildLocatorNode(self, parentNode, sceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        parentNode -- Node, parent node of this object.
        sceneItem -- Object, locator / null object to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        return None


    def buildCurveNode(self, parentNode, sceneItem, objectName):
        """Builds a Curve object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        return None


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttributeNode(self):
        pass


    def buildColorAttributeNode(self):
        pass


    def buildFloatAttributeNode(self):
        pass


    def buildIntegerAttributeNode(self):
        pass


    def buildStringAttributeNode(self):
        pass


    # ==============
    # Build Methods
    # ==============
    def buildAttributes(self, sceneItem):
        """Builds attributes on the DCC object.

        Arguments:
        sceneItem -- SceneItem, kraken object to build attributes for.

        Return:
        True if successful.

        """

        node = sceneItem.getNode()

        for i in xrange(sceneItem.getNumAttributes()):
            attribute = sceneItem.getAttributeByIndex(i)
            kType = attribute.getKType()

            if kType == "FloatAttribute":
                print kType

            elif kType == "BoolAttribute":
                print kType

            elif kType == "IntegerAttribute":
                print kType

            elif kType == "StringAttribute":
                print kType

        return True


    def buildHierarchy(self, sceneItem, parentNode, component=None):
        """Builds the hierarchy for the supplied sceneItem.

        Arguments:
        sceneItem -- SceneItem, kraken object to build.
        parentNode -- DCC Object, object that is the parent of the created object.
        component -- Component, component that this object belongs to.

        Return:
        DCC object that was created.

        """

        if sceneItem.testFlag('guide'):
            return None

        node = None
        objectName = self.buildName(sceneItem, component=component)
        kType = sceneItem.getKType()

        # Build Object
        if kType == "Container":
            node = self.buildContainerNode(parentNode, sceneItem, objectName)

        elif kType == "Layer":
            node = self.buildLayerNode(parentNode, sceneItem, objectName)

        elif kType == "Component":
            node = self.buildLocatorNode(parentNode, sceneItem, objectName)
            component = sceneItem

        elif kType == "SceneItem":
            node = self.buildLocatorNode(parentNode, sceneItem, objectName)

        elif kType == "Curve":
            node = self.buildCurveNode(parentNode, sceneItem, objectName)

        elif kType == "Control":
            node = self.buildCurveNode(parentNode, sceneItem, objectName)

        else:
            raise NotImplementedError(sceneItem.getName() + ' has an unsupported type: ' + str(type(sceneItem)))

        self.buildAttributes(sceneItem)
        self.buildTransform(sceneItem)

        # Build children
        for i in xrange(sceneItem.getNumChildren()):
            child = sceneItem.getChildByIndex(i)
            self.buildHierarchy(child, node, component)

        return node


    def buildName(self, sceneItem, component=None):
        """Builds the name for the sceneItem that is passed.

        Arguments:
        sceneItem -- SceneItem, kraken object to build the name for.
        component -- Component, component that this object belongs to.

        Return:
        Built name as a string.
        None if it fails.

        """

        componentName = ""
        side = ""
        kType = sceneItem.getKType()

        if component is not None:
            componentName = component.getName()
            side = component.getSide()

        if kType == "Component":
            return '_'.join([sceneItem.getName(), sceneItem.getSide(), 'hrc'])

        elif kType == "Container":
            return '_'.join([sceneItem.getName()])

        elif kType == "Layer":
            return '_'.join([sceneItem.parent.getName(), sceneItem.getName()])

        elif kType == "SceneItem":
            return '_'.join([componentName, sceneItem.getName(), side, 'null'])

        elif kType == "Curve":
            return '_'.join([componentName, sceneItem.getName(), side, 'crv'])

        elif kType == "Control":
            return '_'.join([componentName, sceneItem.getName(), side, 'ctrl'])

        else:
            raise NotImplementedError('buildName() not implemented for ' + str(type(sceneItem)))

        return None


    def _preBuild(self):
        """Protected Pre-Build method.

        Return:
        True if successful.

        """

        return True


    def _build(self, container):
        """Protected build method.

        Return:
        True if successful.

        """

        return True


    def build(self, container):
        """Builds the supplied container into a DCC representation.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        try:
            self._preBuild()
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