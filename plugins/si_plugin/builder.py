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

from utils import *


class SIBuilder(BaseBuilder):
    """Builder object for building Kraken objects in Softimage."""

    def __init__(self):
        super(SIBuilder, self).__init__()


    # ===================
    # Node Build Methods
    # ===================
    def buildCurveNode(self, parentNode, sceneItem, name):
        """Builds a Curve object.

        Arguments:
        parentNode -- Object, sceneItem that represents the parent of this object.
        sceneItem -- Object, sceneItem that represents a curve to be built.
        name -- String, name of the object being created.

        Return:
        node that is created.

        """

        for e, eachCurveSection in enumerate(sceneItem.getControlPoints()):

            points = sceneItem.getControlPoints()[e]

            formattedPoints = []
            for i in xrange(3):

                axisPositions = []
                for p, eachPnt in enumerate(points):
                    if p < len(points):
                        axisPositions.append(eachPnt.toArray()[i])

                formattedPoints.append(axisPositions)

            formattedPoints.append([1.0] * len(points))

            # Scale, rotate, translation shape
            ctrlPnts = []
            ctrlPnts.append([x for x in formattedPoints[0]])
            ctrlPnts.append([x for x in formattedPoints[1]])
            ctrlPnts.append([x for x in formattedPoints[2]])
            ctrlPnts.append(formattedPoints[3])

            if sceneItem.getCurveSectionClosed(e) is True:
                knots = list(xrange(len(ctrlPnts) + 1))
            else:
                knots = list(xrange(len(ctrlPnts)))

            if e == 0:
                node = parentNode.AddNurbsCurve(ctrlPnts, knots, sceneItem.getCurveSectionClosed(e), 1, 1, constants.siSINurbs)
                sceneItem.setNode(node)
            else:
                sceneItem.getNode().ActivePrimitive.Geometry.AddCurve(ctrlPnts, knots, sceneItem.getCurveSectionClosed(e), 1, 1)

        node.Name = name

        return node


    # ======================
    # Generic Build Methods
    # ======================
    def buildAttributes(self, sceneItem, node):
        """Builds attributes on the DCC object.

        Arguments:
        sceneItem -- SceneItem, kraken object to build attributes for.
        node -- DCC Object, DCC object to build attributes on.

        Return:
        True if successful.

        """

        for i in xrange(sceneItem.getNumAttributes()):
            attribute = sceneItem.getAttributeByIndex(i)

            if isinstance(attribute, FloatAttribute):
                pass
                # log(attribute.name)

            elif isinstance(attribute, BoolAttribute):
                pass
                # log(attribute.name)

            elif isinstance(attribute, IntegerAttribute):
                pass
                # log(attribute.name)

            elif isinstance(attribute, StringAttribute):
                pass
                # log(attribute.name)

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
        if kType == "Layer":
            node = parentNode.AddModel(None, objectName)
            sceneItem.setNode(node)

        elif kType == "Component":
            node = parentNode.AddNull(objectName)
            component = sceneItem
            sceneItem.setNode(node)

        elif kType == "Curve":
            node = self.buildCurveNode(parentNode, sceneItem, objectName)
            # node = parentNode.AddNull(objectName)
            # TODO: Actually create curve objects.

        elif kType == "Control":
            node = self.buildCurveNode(parentNode, sceneItem, objectName)
            # node = parentNode.AddNull(objectName)

        else:
            raise NotImplementedError(sceneItem.getName() + ' has an unsupported type: ' + str(type(sceneItem)))


        self.buildAttributes(sceneItem, node)
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

        if isinstance(sceneItem, BaseComponent):
            return '_'.join([sceneItem.getName(), sceneItem.getSide(), 'hrc'])

        componentName = ""
        side = ""

        if component is not None:
            componentName = component.getName()
            side = component.getSide()

        if isinstance(sceneItem, Layer):
            return '_'.join([sceneItem.parent.getName(), sceneItem.getName()])

        elif isinstance(sceneItem, BaseControl):
            return '_'.join([componentName, sceneItem.getName(), side, 'ctrl'])

        elif isinstance(sceneItem, Curve):
            return '_'.join([componentName, sceneItem.getName(), side, 'crv'])

        else:
            raise NotImplementedError('buildName() not implemented for ' + str(type(sceneItem)))

        return None


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



    def build(self, container):
        """Builds the supplied container into a DCC representation.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.

        """

        try:
            si.BeginUndo("Kraken SI Build: " + container.name)

            scnRoot = si.ActiveProject3.ActiveScene.Root

            containerNull = scnRoot.AddModel(None, container.name)
            container.setNode(containerNull)

            # Create Each Component
            for eachLayer in container.getChildrenByType(Layer):
                self.buildHierarchy(eachLayer, containerNull, component=None)

        finally:
            si.EndUndo()

        return True