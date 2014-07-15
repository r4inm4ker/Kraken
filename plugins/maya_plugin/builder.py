"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

from kraken.core.objects.curve import Curve
from kraken.core.objects.layer import Layer
from kraken.core.objects.component import BaseComponent
from kraken.core.objects.controls.base_control import BaseControl
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute
from kraken.core.builders.base_builder import BaseBuilder

from kraken.plugins.maya_plugin.utils import *


class Builder(BaseBuilder):
    """Builder object for building Kraken objects in Maya."""

    def __init__(self):
        super(Builder, self).__init__()


    # ===================
    # Node Build Methods
    # ===================
    def buildContainerNode(self, parentNode, sceneItem, objectName):
        """Builds a container / namespace object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a container to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        node = pm.group(name="group", em=True)
        pm.parent(node, parentNode)
        pm.rename(node, objectName)
        sceneItem.setNode(node)

        return sceneItem.node


    def buildLayerNode(self, parentNode, sceneItem, objectName):
        """Builds a layer object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a layer to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        node = pm.group(name="group", em=True)
        pm.parent(node, parentNode)
        pm.rename(node, objectName)
        sceneItem.setNode(node)

        return sceneItem.node


    def buildGroupNode(self, parentNode, sceneItem, objectName):
        """Builds a group object.

        Arguments:
        parentNode -- Node, parent node of this object.
        sceneItem -- Object, sceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        node = pm.group(name="group", em=True)
        pm.parent(node, parentNode)
        pm.rename(node, objectName)
        sceneItem.setNode(node)

        return sceneItem.node


    def buildLocatorNode(self, parentNode, sceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        parentNode -- Node, parent node of this object.
        sceneItem -- Object, locator / null object to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        node = pm.spaceLocator(name="locator")
        pm.parent(node, parentNode)
        pm.rename(node, objectName)
        sceneItem.setNode(node)

        return sceneItem.node


    def buildCurveNode(self, parentNode, sceneItem, objectName):
        """Builds a Curve object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        # Format points for Maya
        points = sceneItem.getControlPoints()

        # Scale, rotate, translation shape
        curvePoints = []
        for eachSubCurve in points:
            formattedPoints = [x.toArray() for x in eachSubCurve]
            curvePoints.append(formattedPoints)

        mainCurve = None
        for i, eachSubCurve in enumerate(curvePoints):
            currentSubCurve = pm.curve(per=False, point=curvePoints[i], degree=1) #, knot=[x for x in xrange(len(curvePoints[i]))])

            if sceneItem.getCurveSectionClosed(i):
                pm.closeCurve(currentSubCurve, preserveShape=True, replaceOriginal=True)

            if mainCurve is None:
                mainCurve = currentSubCurve

            if i > 0:
                pm.parent(currentSubCurve.getShape(), mainCurve, relative=True, shape=True)
                pm.delete(currentSubCurve)

        node = mainCurve
        pm.parent(node, parentNode)
        pm.rename(node, objectName)
        sceneItem.setNode(node)

        return sceneItem.node


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


    # ===================
    # Visibility Methods
    # ===================
    def buildVisibility(self, sceneItem):
        """Sets the visibility of the object after its been created.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        if sceneItem.getShapeVisibility() is False:

            # Get shape node, if it exists, hide it.
            shape = sceneItem.node.getShape()
            if shape is not None:
                shape.visibility.set(False)

        return True


    # ==============
    # Build Methods
    # ==============
    def buildTransform(self, sceneItem):
        """Translates the transform to Maya transform.

        Arguments:
        sceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

        """

        quat = dt.Quaternion(sceneItem.xfo.rot.v.x, sceneItem.xfo.rot.v.y, sceneItem.xfo.rot.v.z, sceneItem.xfo.rot.w)
        sceneItem.node.setScale(dt.Vector(sceneItem.xfo.scl.x, sceneItem.xfo.scl.y, sceneItem.xfo.scl.z))
        sceneItem.node.setTranslation(dt.Vector(sceneItem.xfo.tr.x, sceneItem.xfo.tr.y, sceneItem.xfo.tr.z), "world")
        sceneItem.node.setRotation(quat, "world")

        pm.select(clear=True)

        return True


    def buildConstraints(self, sceneItem):
        """Builds constraints for the supplied sceneItem.

        Arguments:
        sceneItem -- Object, scene item to create constraints for.

        Return:
        True if successful.

        """

        return True


    def _preBuild(self, container):
        """Pre-Build commands.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        return True


    def _build(self, container):
        """Builds the supplied container into a DCC representation.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        self.buildHierarchy(container, None, component=None)

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
        True if successful.

        """

        return True