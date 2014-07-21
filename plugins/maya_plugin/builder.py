"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

from kraken.core.objects.curve import Curve
from kraken.core.objects.layer import Layer
from kraken.core.objects.components.base_component import BaseComponent
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


    # ========================
    # SceneItem Build Methods
    # ========================
    def buildContainer(self, kSceneItem, objectName):
        """Builds a container / namespace object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created..

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, objectName)

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

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, objectName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildHierarchyGroup(self, kSceneItem, objectName):
        """Builds a hierarchy group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        DCC Scene Item that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, objectName)

        lockObjXfo(dccSceneItem)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildGroup(self, kSceneItem, objectName):
        """Builds a group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, objectName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildJoint(self, kSceneItem, objectName):
        """Builds a joint object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a joint to be built.
        objectName -- String, name of the object being created.

        Return:
        DCC Scene Item that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.joint(name="joint")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, objectName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLocator(self, kSceneItem, objectName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, locator / null object to be built.
        objectName -- String, name of the object being created.

        Return:
        Node that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.spaceLocator(name="locator")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, objectName)

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

        # Format points for Maya
        points = kSceneItem.getControlPoints()

        # Scale, rotate, translation shape
        curvePoints = []
        for eachSubCurve in points:
            formattedPoints = [x.toArray() for x in eachSubCurve]
            curvePoints.append(formattedPoints)

        mainCurve = None
        for i, eachSubCurve in enumerate(curvePoints):
            currentSubCurve = pm.curve(per=False, point=curvePoints[i], degree=1) #, knot=[x for x in xrange(len(curvePoints[i]))])

            if kSceneItem.getCurveSectionClosed(i):
                pm.closeCurve(currentSubCurve, preserveShape=True, replaceOriginal=True)

            if mainCurve is None:
                mainCurve = currentSubCurve

            if i > 0:
                pm.parent(currentSubCurve.getShape(), mainCurve, relative=True, shape=True)
                pm.delete(currentSubCurve)

        dccSceneItem = mainCurve
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, objectName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kAttribute):
        """Builds a Bool attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a boolean attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="bool", defaultValue=kAttribute.getValue(), keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildFloatAttribute(self, kAttribute):
        """Builds a Float attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a float attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="float", defaultValue=kAttribute.getValue(), minValue=kAttribute.min, maxValue=kAttribute.max, keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        # dccSceneItem = parentDCCSceneItem + "." + kAttribute.getName()

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a integer attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="long", defaultValue=kAttribute.getValue(), minValue=kAttribute.min, maxValue=kAttribute.max, keyable=True)
        parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a string attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), dataType="string")
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem.set(kAttribute.getValue())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Arguments:
        kAttributeGroup -- SceneItem, kraken object to build the attribute group on.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttributeGroup.getParent())

        groupName = kAttributeGroup.getName()
        if groupName == "":
            groupName = "Settings"

        parentDCCSceneItem.addAttr(groupName, niceName=groupName, attributeType="enum", enumName="-----", keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(groupName)
        pm.setAttr(parentDCCSceneItem + "." + groupName, lock=True)

        self._registerSceneItemPair(kAttributeGroup, dccSceneItem)

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
        dccSceneItem = pm.orientConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], parentDCCSceneItem, name=kConstraint.getName() + "_ori_cns", maintainOffset=kConstraint.getMaintainOffset())
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

        dccSceneItem = pm.parentConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], parentDCCSceneItem, name=kConstraint.getName() + "_par_cns", maintainOffset=kConstraint.getMaintainOffset())
        pm.scaleConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], parentDCCSceneItem, name=kConstraint.getName() + "_scl_cns", maintainOffset=kConstraint.getMaintainOffset())

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
        dccSceneItem = pm.pointConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], parentDCCSceneItem, name=kConstraint.getName() + "_pos_cns", maintainOffset=kConstraint.getMaintainOffset())
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
        dccSceneItem = pm.scaleConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], parentDCCSceneItem, name=kConstraint.getName() + "_scl_cns", maintainOffset=kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


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

            # Get shape node, if it exists, hide it.
            shape = dccSceneItem.getShape()
            if shape is not None:
                shape.visibility.set(False)

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

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        objectColor = kSceneItem.getColor()
        if objectColor not in self.VALID_COLORS.keys():
            return False

        dccSceneItem.overrideEnabled.set(True)
        dccSceneItem.overrideColor.set(self.VALID_COLORS[objectColor][0])

        return True


    # ==================
    # Transform Methods
    # ==================
    def setTransform(self, kSceneItem):
        """Translates the transform to Maya transform.

        Arguments:
        kSceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

        """

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        quat = dt.Quaternion(kSceneItem.xfo.rot.v.x, kSceneItem.xfo.rot.v.y, kSceneItem.xfo.rot.v.z, kSceneItem.xfo.rot.w)
        dccSceneItem.setScale(dt.Vector(kSceneItem.xfo.scl.x, kSceneItem.xfo.scl.y, kSceneItem.xfo.scl.z))
        dccSceneItem.setTranslation(dt.Vector(kSceneItem.xfo.tr.x, kSceneItem.xfo.tr.y, kSceneItem.xfo.tr.z), "world")
        dccSceneItem.setRotation(quat, "world")

        pm.select(clear=True)

        return True


    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Pre-Build commands.

        Arguments:
        kSceneItem -- Object, kraken kSceneItem object to build.

        Return:
        True if successful.

        """

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
        True if successful.

        """

        return True