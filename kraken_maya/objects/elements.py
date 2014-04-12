"""Kraken - Maya - objects.elements module.

Classes:
Scene -- Scene root representation.
Group -- Object used to group objects together.
Null -- Basic 3d transform with basic graphical representation.
Asset -- Namespace object.

"""

import json

from kraken.kraken_maya.utils import *
from kraken.core.objects import elements


class Scene(elements.Scene):
    """Maya Scene Root."""

    def __init__(self):
        super(Scene, self).__init__()
        self.app = "maya"
        self.object3D = None


    def __str__(self):
        return str("Kraken Scene: " + self.name)


class MayaObject(object):
    """Base MayaObject."""

    def _checkParent(self):
        """Check if parent is set, if not set to scene root."""

        if self.parent is None:
            self.parent = Scene()

        return


    # ================
    # Build Operations
    # ================
    def _preBuild(self):
        """Pre-build operations.

        Return:
        True if successful.

        """

        super(MayaObject, self)._preBuild()

        pm.select(clear=True)

        return True


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(MayaObject, self)._postBuild()

        if self.parent.object3D is not None:
            pm.parent(self.object3D, self.parent.object3D)

        pm.select(clear=True)

        return True


    # =====================
    # Transform Operations
    # =====================
    def _initTransform(self):
        """Set the transform in Maya.

        Return:
        True if successful.
        """

        quat = dt.Quaternion(self.xfo.rot.v.x, self.xfo.rot.v.y, self.xfo.rot.v.z, self.xfo.rot.w)
        self.object3D.setScale(dt.Vector(self.xfo.scl.x, self.xfo.scl.y, self.xfo.scl.z))
        self.object3D.setTranslation(dt.Vector(self.xfo.tr.x, self.xfo.tr.y, self.xfo.tr.z), "world")
        self.object3D.setRotation(quat, "world")

        pm.select(clear=True)

        return True


    # ====================
    # Name operations
    # ====================
    def _setObjName(self):
        """Sets object3D name.

        Return:
        True if successful.

        """

        pm.rename(self.object3D, self.buildName())

        return True


    # =====================
    # Visibility operations
    # =====================
    def _setVisibility(self):
        """Sets object3D visibility.

        Return:
        True if successful.

        """

        self.object3D.attr("visibility").set(self.visibility)

        return True


    # ===================
    # Display operations
    # ===================
    def _setDisplay(self):
        """Sets object3D display properties.

        Return:
        True if successful.

        """

        colors = {
                    "red":13,
                    "green":14,
                    "blue":6,
                    "yellow":16,
                    "orange":12,
                    "purple":8,
                    "magenta":9
                 }

        if self.color is not None and type(self.color) is str and self.color in colors.keys():
            self.object3D.overrideEnabled.set(True)
            self.object3D.overrideColor.set(colors[self.color])

        return True


    # =====================
    # Attribute Operations
    # =====================
    def _buildAttributes(self):
        """Builds the attributes on the object3D. Implement in sub-classes."""

        attrTypeMap = {
                        "bool": "bool",
                        "string": "string",
                        "integer": "long",
                        "float": "float",
                      }

        for eachGroup in self.attributes.keys():

            if len(self.attributes[eachGroup].keys()) < 1:
                continue

            if eachGroup == "default":
                continue
            else:
                propGroup = self.object3D.addAttr(eachGroup, niceName=eachGroup, attributeType="enum", enumName="None:", keyable=True)
                pm.setAttr(self.object3D + "." + eachGroup, lock=True)

            attributes = self.attributes[eachGroup]
            for eachAttribute in attributes.keys():
                attribute = attributes[eachAttribute]

                minValue = 0
                maxValue = 0

                if hasattr(attribute, "min"):
                    minValue = attribute.min

                if hasattr(attribute, "max"):
                    maxValue = attribute.max

                if attribute.attrType in ("bool", "integer", "float"):
                    attrType = attrTypeMap[attribute.attrType]

                    if attrType == "bool":
                        newAttribute = self.object3D.addAttr(attribute.name, niceName=attribute.name, attributeType=attrType, defaultValue=attribute.value, keyable=True)
                    else:
                        newAttribute = self.object3D.addAttr(attribute.name, niceName=attribute.name, attributeType=attrType, defaultValue=attribute.value, minValue=minValue, maxValue=maxValue, keyable=True)

                elif attribute.attrType == "string":
                    newAttribute = self.object3D.addAttr(attribute.name, niceName=attribute.name, attributeType=attrType, defaultValue=attribute.value, keyable=True)
                else:
                    return

        return


    # =====================
    # Constraint Operations
    # =====================
    def _buildConstraints(self):
        """Builds the constraints on the object3D. Implement in sub-classes."""

        for eachConstraint in self.constraints.keys():
            constraint = self.constraints[eachConstraint]
            constraintType = constraint.constraintType

            if constraintType == "scale":
                pm.scaleConstraint(constraint.constrainers[0].object3D, self.object3D, name=constraint.name + "_scl_cns", maintainOffset=constraint.maintainOffset)
            elif constraintType == "orientation":
                pm.orientConstraint(constraint.constrainers[0].object3D, self.object3D, name=constraint.name + "_ori_cns", maintainOffset=constraint.maintainOffset)
            elif constraintType == "position":
                pm.pointConstraint(constraint.constrainers[0].object3D, self.object3D, name=constraint.name + "_pos_cns", maintainOffset=constraint.maintainOffset)
            elif constraintType == "pose":
                pm.parentConstraint(constraint.constrainers[0].object3D, self.object3D, name=constraint.name + "_par_cns", maintainOffset=constraint.maintainOffset)
                pm.scaleConstraint(constraint.constrainers[0].object3D, self.object3D, name=constraint.name + "_scl_cns", maintainOffset=constraint.maintainOffset)


class SceneObj(MayaObject, elements.SceneObj):
    """Base scene object representation."""

    def __init__(self, name, parent=None):
        """Initializes base scene object.

        Arguments:
        name -- String, Name of scene object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.SceneObj.__init__(self, name, parent=parent)
        self.app = "maya"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations.

        Return:
        True if successful.

        """

        super(SceneObj, self)._preBuild()

        return True


    def _build(self):
        """Builds element in Maya.

        Return:
        3D Object in Maya.

        """

        self.object3D = pm.group(name="group", em=True)

        return self.object3D


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(SceneObj, self)._postBuild()

        return True


class Group(MayaObject, elements.Group):
    """Group / locator object."""

    def __init__(self, name, parent=None):
        """Initializes Group object.

        Arguments:
        name -- String, Name of Group object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Group.__init__(self, name, parent=parent)
        self.app = "maya"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # =================
    # Build operations
    # =================
    def _build(self):
        """Builds element in Maya.

        Return:
        3D Object in Maya.

        """

        self.object3D = pm.group(name="group", em=True)

        return self.object3D


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(Group, self)._postBuild()

        return True


class Null(MayaObject, elements.Null):
    """Null / locator object."""

    def __init__(self, name, parent=None):
        """Initializes Null object.

        Arguments:
        name -- String, Name of Null object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Null.__init__(self, name, parent=parent)
        self.app = "maya"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # =================
    # Build operations
    # =================
    def _build(self):
        """Builds element in Maya.

        Return:
        3D Object in Maya.

        """

        self.object3D = pm.spaceLocator(name="locator")

        return self.object3D


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(Null, self)._postBuild()

        return True


class Control(MayaObject, elements.Control):
    """Control object."""


    def __init__(self, name, shape, parent=None):
        """Initializes Control object.

        Arguments:
        name -- String, Name of Control object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Control.__init__(self, name, shape, parent=parent)
        self.app = "maya"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # =================
    # Build operations
    # =================
    def _build(self):
        """Builds element in Softimage.

        Return:
        3D Object in Softimage.

        """

        # Scale, rotate, translation shape
        ctrlPnts = []
        for eachVec in self.shapes[self.shape]:
            pointVec = dt.Vector(eachVec)
            pointXfo = dt.TransformationMatrix()
            pointXfo.addRotation((pmUtil.radians(self.rotOffset[0]),pmUtil.radians(self.rotOffset[1]),pmUtil.radians(self.rotOffset[2])), 'XYZ', 'transform')
            pointVec = pointVec.rotateBy(pointXfo)
            pointVec.x = (pointVec.x*self.sclOffset[0]) + self.posOffset[0]
            pointVec.y = (pointVec.y*self.sclOffset[1]) + self.posOffset[1]
            pointVec.z = (pointVec.z*self.sclOffset[2]) + self.posOffset[2]

            ctrlPnts.append(pointVec)

        self.object3D = pm.curve(per=False, point=ctrlPnts, degree=1)

        return self.object3D


class Chain(MayaObject, elements.Chain):
    """Chain object."""

    def __init__(self, name, positions, parent=None):
        """Initializes Chain object.

        Arguments:
        name -- String, Name of Chain object.
        positions -- List, List of [x,y,z] values of joint positions.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Chain.__init__(self, name, positions, parent=parent)
        self.app = "maya"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # ===============
    # Xfo operations
    # ===============
    def _initTransform(self):
        """Set the transform.

        Return:
        True if successful.
        """

        return True


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Chain, self)._preBuild()

        if len(self.positions) < 2:
            raise ValueError("There are not enough chain positions. There must be more than 1!")

        return True


    def _build(self):
        """Builds element in Softimage.

        Return:
        3D Object in Softimage.

        """

        newJoints = []
        for eachPos in self.positions:
            newJoint = pm.joint(absolute=True, radius=0.3, position=eachPos)
            newJoints.append(newJoint)

        for eachJoint in newJoints:
            pm.joint(eachJoint.name(), edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="ydown")

        self.object3D = newJoints[0]

        return self.object3D


class Joint(MayaObject, elements.Joint):
    """Joint object."""

    def __init__(self, name, parent=None):
        """Initializes Joint object.

        Arguments:
        name -- String, Name of Joint object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Joint.__init__(self, name, parent=parent)
        self.app = "maya"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Joint, self)._preBuild()

        return True


    def _build(self):
        """Builds element in Softimage.

        Return:
        3D Object in Softimage.

        """

        self.object3D = pm.joint(absolute=True, radius=0.5, position=[0,0,0])
        pm.joint(self.object3D.name(), edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="ydown")

        return self.object3D


class Asset(MayaObject, elements.Asset):
    """Asset object."""

    def __init__(self, name, parent=None):
        """Initializes Asset / namespace object.

        Arguments:
        name -- String, Name of Asset object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Asset.__init__(self, name, parent=parent)
        self.app = "maya"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # =================
    # Build operations
    # =================
    def _build(self):
        """Builds element in Maya.

        Return:
        3D Object in Maya.

        """

        self.object3D = pm.group(name="asset")

        return self.object3D


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(Asset, self)._postBuild()

        return True


    def addGroup(self, groupName, members=None):
        """Adds a group to asset.

        Arguments:
        groupName -- String, Name of the group.
        members -- List, Objects to be in the group.

        Return:
        New group object.

        """

        if groupName in self.groups.keys():
            print groupName + " is already a group!"
            return False

        self.groups[groupName] = Group(groupName, self, members=members)

        if members:
            for eachItem in members:
                self.groups[groupName] = members

        return self.groups[groupName]