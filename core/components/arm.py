from kraken.core.maths import *
from kraken.core.maths import mathUtils
from kraken.core.components.base import BaseComponent
from kraken.core.objects import elements


class ArmComponent(BaseComponent):
    """Arm Rig Component"""

    def __init__(self, name, side="M", parent=None):
        super(ArmComponent, self).__init__(name, side=side, parent=parent)

        self.positions = [Vec3(5.0, 20.0, 0.0), Vec3(8.535533905932736, 16.46446609406726, -2.5), Vec3(12.071067811865474, 12.92893218813452, 0.0)]
        self.componentXfo = Xfo()
        self.upVXfo = Xfo()
        self.boneData = {
                          "bicep":
                                  {
                                    "xfo": Xfo(),
                                    "length": None,
                                  },

                          "forearm":
                                    {
                                      "xfo": Xfo(),
                                      "length": None,
                                    },
                          "wrist":
                                  {
                                    "xfo": Xfo(),
                                    "length": None,
                                  },
                          }

        self.addAttribute("float", "bone1Len", 1.0, minValue=0.0, maxValue=100.0)
        self.addAttribute("float", "bone2Len", 1.0, minValue=0.0, maxValue=100.0)
        self.addAttribute("float", "fkik", 1.0, minValue=0.0, maxValue=1.0)
        self.addAttribute("float", "softDist", 0.5, minValue=0.0, maxValue=1.0)
        self.addAttribute("bool", "softIK", True)
        self.addAttribute("bool", "stretch", True)
        self.addAttribute("float", "stretchBlend", 1.0, minValue=0.0, maxValue=1.0)
        self.addAttribute("string", "Side", self.side)
        self.addAttribute("bool", "toggleDebugging", True)


    # ===============
    # Init Functions
    # ===============
    def initDataFromGuide(self, inputGuide):
        """Initilizes component data from the input guide.

        Arguments:
        inputGuide -- Object, Scene object that is the parent of the guide.

        Return:
        True if successful.

        """
        guides = ["bicep", "forearm", "wrist"]

        for i,obj in enumerate(guides):
            guide = inputGuide.findChild("_".join([obj, self.side , "gdSrt"]))

            if guide is None:
                raise ValueError("Could not locate all guide srt's!")

            self.positions[i] = guide.getTranslation()

        return True


    # ======================
    # Guide Build Functions
    # ======================
    def _preBuildGuide(self):
        """Pre-build Guide operations.

        Return:
        True if successful.

        """

        super(ArmComponent, self)._preBuildGuide()

        return


    def _buildGuide(self):
        """Builds the component guide in the DCC.

        Return:
        True if successful.

        """

        self.guide = elements.Group("_".join([self.name.split("_")[0], self.side, "guide_hrc"]), parent=None)

        bicepGdSrt = elements.Null("_".join(["bicep", self.side , "gdSrt"]), parent=self.guide)

        if self.side == "L":
            bicepGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508984), 0.9238795325112867)
            bicepGdSrt.xfo.tr.set(5.0, 20.0, 0.0)
        elif self.side == "R":
            bicepGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, 0.0), 0.0)
            bicepGdSrt.xfo.tr.set(-5.0, 20.0, 0.0)

        forearmGdSrt = elements.Null("_".join(["forearm", self.side, "gdSrt"]), parent=bicepGdSrt)

        if self.side == "L":
            forearmGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508995), 0.9238795325112866)
            forearmGdSrt.xfo.tr.set(8.535533905932736, 16.46446609406726, -2.5)
        elif self.side == "R":
            forearmGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, 0.0), 0.0)
            forearmGdSrt.xfo.tr.set(-8.535533905932736, 16.46446609406726, -2.5)

        wristGdSrt = elements.Null("_".join(["wrist", self.side, "gdSrt"]), parent=forearmGdSrt)

        if self.side == "L":
            wristGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508995), 0.9238795325112866)
            wristGdSrt.xfo.tr.set(12.071067811865474, 12.92893218813452, 0.0)
        elif self.side == "R":
            wristGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, 0.0), 0.0)
            wristGdSrt.xfo.tr.set(-12.071067811865474, 12.92893218813452, 0.0)

        self.guide.build()

        return True


    def _postBuildGuide(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(ArmComponent, self)._postBuildGuide()

        return


    # ==========================
    # Component Build Functions
    # ==========================
    def getComponentXfo(self):
        """Calculates the base component transform space.

        Return:
        self.componentXfo

        """

        if self.side == "L":
            rootToWrist = self.positions[2].subtract(self.positions[0]).unit()
            rootToElbow = self.positions[1].subtract(self.positions[0]).unit()
            chainNormal = rootToWrist.cross(rootToElbow).unit()
            zAxis = rootToWrist.cross(chainNormal).unit()

            # Set from dir upV
            mat = Matrix33(rootToWrist, chainNormal, zAxis).transpose()
            self.componentXfo.rot.setFromMatrix33(mat)
            self.componentXfo.tr = self.positions[0]

        elif self.side == "R":
            rootToWrist = self.positions[0].subtract(self.positions[2]).unit()
            rootToElbow = self.positions[0].subtract(self.positions[1]).unit()
            chainNormal = rootToWrist.cross(rootToElbow).unit()
            zAxis = rootToWrist.cross(chainNormal).unit()

            # Set from dir upV
            self.componentXfo.setFromVectors(rootToWrist, chainNormal, zAxis, self.positions[0])

        return self.componentXfo


    def getUpVXfo(self):
        """Calcualtes the position for the up vector control based on the input
        positions.

        Return:
        upVXfo

        """

        self.upVXfo.copy(self.componentXfo)
        offset = self.positions[0].distanceBetween(self.positions[2]) / 2
        self.upVXfo.tr = self.positions[1].add(Vec3(0.0,0.0,-offset))

        return self.upVXfo


    def getBoneData(self):
        """Calculates the transforms for bone1, bone2, and wrist and stores bone lengths.

        Return:
        bone1Xfo, bone2Xfo, wristOutXfo

        """

        self.boneData["bicep"]["length"] = self.positions[0].distanceBetween(self.positions[1])
        self.boneData["forearm"]["length"] = self.positions[1].distanceBetween(self.positions[2])
        self.boneData["wrist"]["length"] = 1.0

        if self.side == "L":

            # ===========
            # Bone 1 Xfo
            # ===========
            rootToWrist = self.positions[2].subtract(self.positions[0]).unit()
            rootToElbow = self.positions[1].subtract(self.positions[0]).unit()
            bone1Normal = rootToWrist.cross(rootToElbow).unit()
            bone1ZAxis = rootToElbow.cross(bone1Normal).unit()

            # Set Orientation from dir upV
            self.boneData["bicep"]["xfo"].setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, self.positions[0])

            # ===========
            # Bone 2 Xfo
            # ===========
            elbowToWrist = self.positions[2].subtract(self.positions[1]).unit()
            elbowToRoot = self.positions[0].subtract(self.positions[1]).unit()
            bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
            bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()

            # Set Orientation from dir upV
            self.boneData["forearm"]["xfo"].setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, self.positions[1])

            # ===========
            # Bone 3 Xfo
            # ===========
            self.boneData["wrist"]["xfo"].setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, self.positions[2])


        elif self.side == "R":

            # ===========
            # Bone 1 Xfo
            # ===========
            rootToWrist = self.positions[0].subtract(self.positions[2]).unit()
            rootToElbow = self.positions[0].subtract(self.positions[1]).unit()
            bone1Normal = rootToWrist.cross(rootToElbow).unit()
            bone1ZAxis = rootToElbow.cross(bone1Normal).unit()

            # Set Orientation from dir upV
            self.boneData["bicep"]["xfo"].setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, self.positions[0])

            # ===========
            # Bone 2 Xfo
            # ===========
            elbowToWrist = self.positions[1].subtract(self.positions[2]).unit()
            elbowToRoot = self.positions[1].subtract(self.positions[0]).unit()
            bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
            bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()

            # Set Orientation from dir upV
            self.boneData["forearm"]["xfo"].setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, self.positions[1])

            # ===========
            # Bone 3 Xfo
            # ===========
            self.boneData["wrist"]["xfo"].setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, self.positions[2])

        return


    def _build(self):
        """Internal build function for building the component in Softimage."""

        super(ArmComponent, self)._build()

        # ====================
        # Calculate positions
        # ====================
        self.getComponentXfo()
        self.getUpVXfo()
        self.getBoneData()


        # ===================
        # Create Hierarchies
        # ===================
        armatureLayer = self.addLayer("armature")
        ctrlLayer = self.addLayer("controls")
        ioLayer = self.addLayer("io")


        # ============
        # Setup Ctrls
        # ============

        # Setup Attributes
        ioLayer.addAttributeGroup("DisplayInfo_Arm_Settings")
        ioLayer.attributes["DisplayInfo_Arm_Settings"] = self.attributes["default"]

        # Creat Inputs
        clavicleKineIn = elements.Null("_".join(["arm", self.side, "clavicle_kineIn"]), parent=ioLayer)
        clavicleKineIn.setGlobalTranslation(self.positions[0])

        # Create Controls
        ikHandleZero = elements.Group("_".join(["arm", self.side, "ikHandle_ctrl_zero"]), parent=ctrlLayer)
        ikHandleZero.setLocalTranslation(self.boneData["wrist"]["xfo"].tr)

        ikHandleCtrl = elements.Control("_".join(["arm", self.side, "ikHandle_ctrl"]), "pin", parent=ikHandleZero)
        ikHandleCtrl.setLocalTranslation(Vec3(0,0,0))
        ikHandleCtrl.color = self.ctrlColor
        ikHandleCtrl.rotOffset = [-90,0,0]
        ikHandleCtrl.sclOffset = [1.5,1.5,1.5]

        upVZero = elements.Group("_".join(["arm", self.side, "upV_ctrl_zero"]), parent=ctrlLayer)
        upVZero.setLocalTranslation(self.upVXfo.tr)

        upVCtrl = elements.Control("_".join(["arm", self.side, "upV_ctrl"]), "triangle", parent=upVZero)
        upVCtrl.setLocalTranslation(Vec3(0,0,0))
        upVCtrl.color = self.ctrlColor
        upVCtrl.rotOffset = [0,-90,0]
        upVCtrl.posOffset = [0,0,-1]

        bicepFKZero = elements.Group("_".join(["arm", self.side, "bicepFK_ctrl_zero"]), parent=ctrlLayer)
        bicepFKZero.setLocalTranslation(self.boneData["bicep"]["xfo"].tr)
        bicepFKZero.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)

        bicepFKCtrl = elements.Control("_".join(["arm", self.side, "bicepFK_ctrl"]), "cubeXAligned", parent=bicepFKZero)
        bicepFKCtrl.setLocalTranslation(Vec3(0,0,0))
        bicepFKCtrl.color = self.ctrlColor
        bicepFKCtrl.sclOffset = [self.boneData["bicep"]["length"] * self.sideScale,1,1]

        forearmFKZero = elements.Group("_".join(["arm", self.side, "forearmFK_ctrl_zero"]), parent=bicepFKCtrl)
        forearmFKZero.setGlobalTranslation(self.boneData["forearm"]["xfo"].tr)
        forearmFKZero.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)

        forearmFKCtrl = elements.Control("_".join(["arm", self.side, "forearmFK_ctrl"]), "cubeXAligned", parent=forearmFKZero)
        forearmFKCtrl.setLocalTranslation(Vec3(0,0,0))
        forearmFKCtrl.color = self.ctrlColor
        forearmFKCtrl.sclOffset = [self.boneData["forearm"]["length"] * self.sideScale,1,1]

        # Setup SRTs
        bicepKineOut = elements.Null("_".join(["arm", self.side, "bicep_kineOut"]), parent=ioLayer)
        bicepKineOut.setLocalTranslation(self.boneData["bicep"]["xfo"].tr)
        bicepKineOut.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)

        forearmKineOut = elements.Null("_".join(["arm", self.side, "forearm_kineOut"]), parent=ioLayer)
        forearmKineOut.setLocalTranslation(self.boneData["forearm"]["xfo"].tr)
        forearmKineOut.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)

        wristKineOut = elements.Null("_".join(["arm", self.side, "wrist_kineOut"]), parent=ioLayer)
        wristKineOut.setLocalTranslation(self.boneData["wrist"]["xfo"].tr)
        wristKineOut.setGlobalRotation(self.boneData["wrist"]["xfo"].rot)

        # ===============
        # Setup Armature
        # ===============

        # Setup Joints
        bicepJnt = elements.Joint("_".join(["arm", self.side, "bicep_jnt"]), parent=armatureLayer)
        bicepJnt.setLocalTranslation(Vec3(0,0,0))
        bicepJnt.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)
        bicepJnt.addConstraint("bicepJntToKineOut", "pose", [bicepKineOut])

        forearmJnt = elements.Joint("_".join(["arm", self.side, "forearm_jnt"]), parent=armatureLayer)
        forearmJnt.setLocalTranslation(Vec3(4,0,-3))
        forearmJnt.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)
        forearmJnt.addConstraint("forearmJntToKineOut", "pose", [forearmKineOut])

        wristJnt = elements.Joint("_".join(["arm", self.side, "wrist_jnt"]), parent=armatureLayer)
        wristJnt.setLocalTranslation(Vec3(8,0,0))
        wristJnt.setGlobalRotation(self.boneData["wrist"]["xfo"].rot)
        wristJnt.addConstraint("wristJntToKineOut", "pose", [wristKineOut])

        return


    def _postBuild(self):

        super(ArmComponent, self)._postBuild()