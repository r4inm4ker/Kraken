"""Kraken SI - SI Builder module.

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

from kraken.plugins.si_plugin.utils import *


class Builder(BaseBuilder):
    """Builder object for building Kraken objects in Softimage."""

    def __init__(self):
        super(Builder, self).__init__()


    # ===================
    # Node Build Methods
    # ===================
    def buildContainer(self, kSceneItem, objectName):
        """Builds a container / namespace object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        if parentNode is None:
            parentNode = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentNode.AddModel(None, objectName)
        dccSceneItem.Name = objectName

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLayer(self, kSceneItem, objectName):
        """Builds a layer object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a layer to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = parentNode.AddModel(None, objectName)
        dccSceneItem.Name = objectName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildGroup(self, kSceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = parentNode.AddNull()
        dccSceneItem.Name = objectName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLocator(self, kSceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a locator / null to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """
        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = parentNode.AddNull()
        dccSceneItem.Name = objectName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildCurve(self, kSceneItem, objectName):
        """Builds a Curve object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a curve to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """
        parentNode = self._getDCCSceneItem(kSceneItem.getParent())
        dccSceneItem = None

        # Format points for Softimage
        points = kSceneItem.getControlPoints()

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
            if kSceneItem.getCurveSectionClosed(i) is True:
                knots = list(xrange(len(eachCurveSection[i]) + 1))
            else:
                knots = list(xrange(len(eachCurveSection[i])))

            if i == 0:
                dccSceneItem = parentNode.AddNurbsCurve(list(eachCurveSection), knots, kSceneItem.getCurveSectionClosed(i), 1, constants.siNonUniformParameterization, constants.siSINurbs)
                self._registerSceneItemPair(kSceneItem, dccSceneItem)
            else:
                dccSceneItem.ActivePrimitive.Geometry.AddCurve(eachCurveSection, knots, kSceneItem.getCurveSectionClosed(i), 1, constants.siNonUniformParameterization)

        dccSceneItem.Name = objectName
        return dccSceneItem


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kSceneItem):
        """Builds a Bool attribute.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a boolean attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())
        dccSceneItem = parentDCCSceneItem.AddParameter2(kSceneItem.getName(), constants.siBool, kSceneItem.getValue(), "", "", "", "", constants.siClassifUnknown, 2053, kSceneItem.getName())

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return True


    def buildColorAttribute(self, kSceneItem):
        """Builds a Color attribute.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a color attribute to be built.

        Return:
        True if successful.

        """

        return True


    def buildFloatAttribute(self, kSceneItem):
        """Builds a Float attribute.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a float attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())
        dccSceneItem = parentDCCSceneItem.AddParameter2(kSceneItem.getName(), constants.siDouble, kSceneItem.getValue(), kSceneItem.min, kSceneItem.max, kSceneItem.min, kSceneItem.max, constants.siClassifUnknown, 2053, kSceneItem.getName())

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return True


    def buildIntegerAttribute(self, kSceneItem):
        """Builds a Integer attribute.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a integer attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())
        dccSceneItem = parentDCCSceneItem.AddParameter2(kSceneItem.getName(), constants.siInt4, kSceneItem.getValue(), kSceneItem.min, kSceneItem.max, kSceneItem.min, kSceneItem.max, constants.siClassifUnknown, 2053, kSceneItem.getName())

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return True


    def buildStringAttribute(self, kSceneItem):
        """Builds a String attribute.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a string attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())
        dccSceneItem = parentDCCSceneItem.AddParameter2(kSceneItem.getName(), constants.siString, kSceneItem.getValue(), "", "", "", "", constants.siClassifUnknown, 2053, kSceneItem.getName())

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return True


    def buildAttributeGroup(self, kSceneItem):
        """Builds attribute groups on the DCC object.

        Arguments:
        kSceneItem -- SceneItem, kraken object to build the attribute group on.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

        groupName = kSceneItem.getName()
        if groupName == "":
            groupName = "Settings"

        dccSceneItem = parentDCCSceneItem.AddProperty("CustomParameterSet", False, groupName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return True


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

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        if kSceneItem.getShapeVisibility() is False:
            dccSceneItem.Properties("Visibility").Parameters("viewvis").Value = False

        return True


    # ==============
    # Build Methods
    # ==============
    def setTransform(self, kSceneItem):
        """Translates the transform to Softimage transform.

        Arguments:
        kSceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

        """

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        xfo = XSIMath.CreateTransform()
        scl = XSIMath.CreateVector3(kSceneItem.xfo.scl.x, kSceneItem.xfo.scl.y, kSceneItem.xfo.scl.z)
        quat = XSIMath.CreateQuaternion(kSceneItem.xfo.rot.w, kSceneItem.xfo.rot.v.x, kSceneItem.xfo.rot.v.y, kSceneItem.xfo.rot.v.z)
        tr = XSIMath.CreateVector3(kSceneItem.xfo.tr.x, kSceneItem.xfo.tr.y, kSceneItem.xfo.tr.z)

        xfo.SetScaling(scl)
        xfo.SetRotationFromQuaternion(quat)
        xfo.SetTranslation(tr)

        dccSceneItem.Kinematics.Global.PutTransform2(None, xfo)

        return True


    def buildConstraints(self, kSceneItem):
        """Builds constraints for the supplied kSceneItem.

        Arguments:
        kSceneItem -- Object, scene item to create constraints for.

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

        self.buildHierarchy(container, component=None)

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
        True if successful.

        """

        si.EndUndo()

        return True