"""Kraken - Softimage - objects.elements module.

Classes:
Scene -- Scene root representation.
Group -- Object used to group objects together.
Null -- Basic 3d transform with basic graphical representation.
Asset -- Namespace object.

"""

import json

from kraken.kraken_si.utils import *
from kraken.kraken_si.maths import *
from kraken.kraken_si.maths import mathUtils
from kraken.core.objects import elements


class Scene(elements.Scene):
    """Softimage Scene Root."""

    def __init__(self, app="si"):
        super(Scene, self).__init__()
        self.app = app
        self.object3D = si.ActiveProject3.ActiveScene.Root


    def __str__(self):
        return str("Kraken Scene: " + self.object3D.Name)


class SIObject(object):
    """Base SIObject."""

    def _checkParent(self):
        """Check if parent is set, if not set to scene root."""

        if self.parent is None:
            self.parent = Scene()

        return


    # =====================
    # Transform Operations
    # =====================
    def _initTransform(self):
        """Set the transform in Softimage.

        Return:
        True if successful.
        """

        xfo = XSIMath.CreateTransform()
        scl = XSIMath.CreateVector3(self.xfo.scl.x, self.xfo.scl.y, self.xfo.scl.z)
        quat = XSIMath.CreateQuaternion(self.xfo.rot.w, self.xfo.rot.v.x, self.xfo.rot.v.y, self.xfo.rot.v.z)
        tr = XSIMath.CreateVector3(self.xfo.tr.x, self.xfo.tr.y, self.xfo.tr.z)

        xfo.SetScaling(scl)
        xfo.SetRotationFromQuaternion(quat)
        xfo.SetTranslation(tr)

        self.object3D.Kinematics.Global.PutTransform2(None, xfo)

        return True

    def getTranslation(self):
        """Get the translation in Softimage.

        Return:
        vec3 position.
        """

        obj = self.object3D
        position = Vec3(obj.Kinematics.Global.Transform.Translation.X,
                        obj.Kinematics.Global.Transform.Translation.Y,
                        obj.Kinematics.Global.Transform.Translation.Z)
        return position



    # ====================
    # Name operations
    # ====================
    def _setObjName(self):
        """Sets object3D name.

        Return:
        True if successful.

        """

        self.object3D.Name = self.buildName()

        return True


    # =====================
    # Visibility operations
    # =====================
    def _setVisibility(self):
        """Sets object3D visibility.

        Return:
        True if successful.

        """

        self.object3D.Properties("Visibility").Parameters("viewvis").Value = self.visibility
        self.object3D.Properties("Visibility").Parameters("rendvis").Value = self.visibility

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
                    "red":[1.0,0.0,0.0],
                    "green":[0.0,1.0,0.0],
                    "blue":[0.0,1.0,0.0],
                    "yellow":[1.0,1.0,0.0],
                    "orange":[1.0,0.5,0.0],
                    "purple":[0.5,0.0,1.0],
                    "magenta":[1.0,0.0,1.0]
                 }

        if self.color is not None and type(self.color) is str and self.color in colors.keys():
            displayProp = self.object3D.AddProperty("Display Property")

            displayProp.Parameters("wirecolorr").Value = colors[self.color][0]
            displayProp.Parameters("wirecolorg").Value = colors[self.color][1]
            displayProp.Parameters("wirecolorb").Value = colors[self.color][2]

        return True


    # =====================
    # Attribute Operations
    # =====================
    def _buildAttributes(self):
        """Builds the attributes on the object3D. Implement in sub-classes."""

        attrTypeMap = {
                        "bool": constants.siBool,
                        "string": constants.siString,
                        "integer": constants.siInt4,
                        "float": constants.siFloat,
                      }

        for eachGroup in self.attributes.keys():

            if len(self.attributes[eachGroup].keys()) < 1:
                continue

            if eachGroup == "default":
                propGroup = self.object3D.AddProperty("CustomParameterSet", False, self.name + "_setttings")
            else:
                propGroup = self.object3D.AddProperty("CustomParameterSet", False, eachGroup)

            attributes = self.attributes[eachGroup]
            for eachAttribute in attributes.keys():
                attribute = attributes[eachAttribute]

                minValue = ""
                maxValue = ""

                if hasattr(attribute, "min"):
                    minValue = attribute.min

                if hasattr(attribute, "max"):
                    maxValue = attribute.max

                attribute = attributes[eachAttribute]
                newAttribute = propGroup.AddParameter3(attribute.name, attrTypeMap[attribute.attrType], attribute.value, minValue, maxValue, True, False)
                newAttribute.Keyable = True

        return


    # =====================
    # Constraint Operations
    # =====================
    def _buildConstraints(self):
        """Builds the constraints on the object3D. Implement in sub-classes."""

        constraintTypeMap = {
                        "scale": "Scaling",
                        "orientation": "Orientation",
                        "position": "Position",
                        "pose": "Pose",
                      }

        for eachConstraint in self.constraints.keys():

            constraint = self.constraints[eachConstraint]
            constrainers = getCollection()
            for eachItem in constraint.constrainers:
                constrainers.Add(eachItem.object3D)

            newConstraint = self.object3D.Kinematics.AddConstraint(constraintTypeMap[constraint.constraintType], constrainers, constraint.maintainOffset)


class SceneObj(SIObject, elements.SceneObj):
    """Base scene object representation."""

    def __init__(self, name, parent=None):
        """Initializes base scene object.

        Arguments:
        name -- String, Name of scene object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.SceneObj.__init__(self, name, parent=parent)
        self.app = "si"


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
        """Builds element in Softimage.

        Return:
        3D Object in Softimage.

        """

        self.object3D = self.parent.object3D.AddNull()

        return True


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(SceneObj, self)._postBuild()

        return True


class Group(SIObject, elements.Group):
    """Group / locator object."""

    def __init__(self, name, parent=None):
        """Initializes Group object.

        Arguments:
        name -- String, Name of Group object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Group.__init__(self, name, parent=parent)
        self.app = "si"


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

        self.object3D = self.parent.object3D.AddNull()

        self.object3D.Parameters("primary_icon").Value = 0

        return self.object3D


class Null(SIObject, elements.Null):
    """Null / locator object."""

    def __init__(self, name, parent=None):
        """Initializes Null object.

        Arguments:
        name -- String, Name of Null object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Null.__init__(self, name, parent=parent)
        self.app = "si"


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

        self.object3D = self.parent.object3D.AddNull()

        return self.object3D


class Control(SIObject, elements.Control):
    """Control object."""

    def __init__(self, name, shape, parent=None):
        """Initializes Control object.

        Arguments:
        name -- String, Name of Control object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Control.__init__(self, name, shape, parent=parent)
        self.app = "si"


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

        points = self.shapes[self.shape]

        formattedPoints = []
        for i in xrange(3):

            axisPositions = []
            for p, eachPnt in enumerate(points):
                if p < len(points):
                    axisPositions.append(eachPnt[i])

            formattedPoints.append(axisPositions)

        formattedPoints.append([1.0]*len(points))

        # Scale, rotate, translation shape
        ctrlPnts = []
        ctrlPnts.append([x * self.sclOffset[0] for x in formattedPoints[0]])
        ctrlPnts.append([x * self.sclOffset[1] for x in formattedPoints[1]])
        ctrlPnts.append([x * self.sclOffset[2] for x in formattedPoints[2]])
        ctrlPnts.append(formattedPoints[3])

        for i in xrange(len(formattedPoints[0])):
            pointPos = XSIMath.CreateVector3(ctrlPnts[0][i], ctrlPnts[1][i], ctrlPnts[2][i])
            pointRotation = XSIMath.CreateRotation(XSIMath.DegreesToRadians(self.rotOffset[0]), XSIMath.DegreesToRadians(self.rotOffset[1]), XSIMath.DegreesToRadians(self.rotOffset[2]))
            pointPos.MulByRotationInPlace(pointRotation)
            posOffset = XSIMath.CreateVector3(self.posOffset[0] * self.sclOffset[0], self.posOffset[1] * self.sclOffset[1], self.posOffset[2] * self.sclOffset[2])
            pointPos.AddInPlace(posOffset)

            ctrlPnts[0][i] = pointPos.X
            ctrlPnts[1][i] = pointPos.Y
            ctrlPnts[2][i] = pointPos.Z

        self.object3D = self.parent.object3D.AddNurbsCurve(ctrlPnts, None, False, 1, constants.siNonUniformParameterization, constants.siSINurbs)

        return self.object3D


class Chain(SIObject, elements.Chain):
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
        self.app = "si"


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

        if len(self.positions) < 1:
            raise ValueError("No bone positions specified!")

        return True


    def _build(self):
        """Builds element in Softimage.

        Return:
        3D Object in Softimage.

        """

        if len(self.positions) < 2:
            rootPos = self.positions[0]
            effPos = list(self.positions[0])
            effPos[0] = effPos[0] + 1
            chainNormal = XSIMath.CreateVector3(0,0,1)
            self.object3D = self.parent.object3D.Add2DChain(rootPos, effPos, chainNormal, constants.si2DChainNormalRadian, self.name)

        else:
            bone1Pos = XSIMath.CreateVector3(self.positions[0])
            bone2Pos = XSIMath.CreateVector3(self.positions[1])
            boneLastPos = XSIMath.CreateVector3(self.positions[-1])

            bone1ToBone2 = XSIMath.CreateVector3()
            bone1ToBone2.Sub(bone2Pos, bone1Pos)

            bone1ToBoneLast = XSIMath.CreateVector3()
            bone1ToBoneLast.Sub(boneLastPos, bone1Pos)

            if self.positions < 3 or bone2Pos.EpsilonEquals(boneLastPos, 0.001):
                chainNormal = XSIMath.CreateVector3(0,0,1)
            else:
                chainNormal = XSIMath.CreateVector3()
                chainNormal.Cross(bone1ToBone2, bone1ToBoneLast)
                chainNormal.NormalizeInPlace()

            self.object3D = self.parent.object3D.Add2DChain(self.positions[0], self.positions[1], chainNormal, constants.si2DChainNormalRadian, self.name)

            if len(self.positions) > 2:
                for eachPos in self.positions[2:]:
                    self.object3D.AddBone(eachPos, constants.siChainBonePin)

            self.object3D.Kinematics.Global.PutTransform2(None, self.object3D.Bones(0).Kinematics.Global.GetTransform2(None))
            self.object3D.Bones(0).Kinematics.Global.PutTransform2(None, self.object3D.Kinematics.Global.GetTransform2(None))

        return self.object3D


class Joint(SIObject, elements.Joint):
    """Joint object."""

    def __init__(self, name, parent=None):
        """Initializes Joint object.

        Arguments:
        name -- String, Name of Joint object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Joint.__init__(self, name, parent=parent)
        self.app = "si"


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # ===================
    # Display operations
    # ===================
    def _setDisplay(self):
        """Sets object3D display properties.

        Return:
        True if successful.

        """

        super(Joint, self)._setDisplay()

        self.object3D.Parameters("primary_icon").Value = 2
        self.object3D.Parameters("size").Value = 0.5

        return True


    # =================
    # Build operations
    # =================
    def _build(self):
        """Builds element in Softimage.

        Return:
        3D Object in Softimage.

        """

        self.object3D = self.parent.object3D.AddNull()

        return self.object3D


class Asset(SIObject, elements.Asset):
    """Asset object."""

    def __init__(self, name, parent=None):
        """Initializes Asset / namespace object.

        Arguments:
        name -- String, Name of Asset object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        elements.Asset.__init__(self, name, parent=parent)
        self.app = "si"
        self.visibility = False


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

        self.object3D = self.parent.object3D.AddModel()

        return self.object3D


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(Asset, self)._postBuild()

        return True