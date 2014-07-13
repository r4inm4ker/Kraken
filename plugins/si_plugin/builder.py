"""Kraken SI - SI Builder module.

Classes:
SIBuilder -- Component representation.

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

from kraken.plugins.si_plugin.utils import *


class Builder(BaseBuilder):
    """Builder object for building Kraken objects in Softimage."""

    def __init__(self):
        super(SIBuilder, self).__init__()


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

        node = parentNode.AddModel(None, objectName)
        node.Name = objectName
        sceneItem.setNode(node)

        return node


    def buildLayerNode(self, parentNode, sceneItem, objectName):
        """Builds a layer object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a layer to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        node = parentNode.AddModel(None, objectName)
        node.Name = objectName
        sceneItem.setNode(node)

        return node


    def buildGroupNode(self, parentNode, sceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        parentNode -- Node, parent node of this object.
        sceneItem -- Object, sceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        node = parentNode.AddNull()
        node.Name = objectName
        sceneItem.setNode(node)

        return node


    def buildLocatorNode(self, parentNode, sceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        parentNode -- Node, parent node of this object.
        sceneItem -- Object, sceneItem that represents a locator / null to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        node = parentNode.AddNull()
        node.Name = objectName
        sceneItem.setNode(node)

        return node


    def buildCurveNode(self, parentNode, sceneItem, objectName):
        """Builds a Curve object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        # Format points for Softimage
        points = sceneItem.getControlPoints()

        curvePoints = []
        for eachSubCurve in points:
            subCurvePoints = [x.toArray() for x in eachSubCurve]

            formattedPoints = []
            for i in xrange(3):
                axisPositions = []
                for p, eachPnt in enumerate(subCurvePoints):
                    if p < len(subCurvePoints):
                        axisPositions.append(eachPnt[i])

                formattedPoints.append(axisPositions)

            formattedPoints.append([1.0] * len(subCurvePoints))
            curvePoints.append(formattedPoints)

        # Build the curve
        for i, eachCurveSection in enumerate(curvePoints):

            # Create knots
            if sceneItem.getCurveSectionClosed(i) is True:
                knots = list(xrange(len(eachCurveSection) + 1))
            else:
                knots = list(xrange(len(eachCurveSection) + 2))

            if i == 0:
                node = parentNode.AddNurbsCurve(list(eachCurveSection), list(xrange(len(eachCurveSection[0]) + 1)), sceneItem.getCurveSectionClosed(i), 1, constants.siNonUniformParameterization, constants.siSINurbs)
                sceneItem.setNode(node)
            else:
                sceneItem.getNode().ActivePrimitive.Geometry.AddCurve(eachCurveSection, list(xrange(len(eachCurveSection[0]))), sceneItem.getCurveSectionClosed(i), 1, constants.siNonUniformParameterization)

        node.Name = objectName

        return node


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
    def buildTransform(self, sceneItem):
        """Translates the transform to Softimage transform.

        Arguments:
        sceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

        """

        xfo = XSIMath.CreateTransform()
        scl = XSIMath.CreateVector3(sceneItem.xfo.scl.x, sceneItem.xfo.scl.y, sceneItem.xfo.scl.z)
        quat = XSIMath.CreateQuaternion(sceneItem.xfo.rot.w, sceneItem.xfo.rot.v.x, sceneItem.xfo.rot.v.y, sceneItem.xfo.rot.v.z)
        tr = XSIMath.CreateVector3(sceneItem.xfo.tr.x, sceneItem.xfo.tr.y, sceneItem.xfo.tr.z)

        xfo.SetScaling(scl)
        xfo.SetRotationFromQuaternion(quat)
        xfo.SetTranslation(tr)

        sceneItem.node.Kinematics.Global.PutTransform2(None, xfo)

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

        si.BeginUndo("Kraken SI Build: " + container.name)

        return True


    def _build(self, container):
        """Builds the supplied container into a DCC representation.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        scnRoot = si.ActiveProject3.ActiveScene.Root
        self.buildHierarchy(container, scnRoot, component=None)

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
        True if successful.

        """

        si.EndUndo()

        return True