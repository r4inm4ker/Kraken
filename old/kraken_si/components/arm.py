from kraken.kraken_si.utils import *
from kraken.kraken_si.maths import *
from kraken.kraken_si.maths import mathUtils
from kraken.kraken_si.components.base import BaseComponent
from kraken.kraken_si.objects import elements

from kraken.core.components import arm


class ArmComponent(arm.ArmComponent, BaseComponent):
    """Arm Rig Component"""

    def __init__(self, name, side="M", parent=None, layer=None):
        super(ArmComponent, self).__init__(name, side=side, parent=parent, layer=layer)


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

        self.guide = elements.Group(self.name.split("_")[0] + "_" + self.side + "_guide_hrc", parent=None)

        bicepGdSrt = elements.Null("_".join(["bicep", self.side , "gdSrt"]), parent=self.guide)

        if self.side == "L":
            bicepGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508984), 0.9238795325112867)
            bicepGdSrt.xfo.tr.set(5.0, 20.0, 0.0)
        elif self.side == "R":
            bicepGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, -3.313870358775352e-17), 8.000390764101651e-17)
            bicepGdSrt.xfo.tr.set(-5.0, 20.0, 0.0)

        forearmGdSrt = elements.Null("_".join(["forearm", self.side, "gdSrt"]), parent=bicepGdSrt)

        if self.side == "L":
            forearmGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508995), 0.9238795325112866)
            forearmGdSrt.xfo.tr.set(8.535533905932736, 16.46446609406726, -2.5)
        elif self.side == "R":
            forearmGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, 8.00039076410165e-17), 3.3138703587753523e-17)
            forearmGdSrt.xfo.tr.set(-8.535533905932736, 16.46446609406726, -2.5)

        wristGdSrt = elements.Null("_".join(["wrist", self.side, "gdSrt"]), parent=forearmGdSrt)

        if self.side == "L":
            wristGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508995), 0.9238795325112866)
            wristGdSrt.xfo.tr.set(12.071067811865474, 12.92893218813452, 0.0)
        elif self.side == "R":
            wristGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, 8.000390764101648e-17), 3.313870358775353e-17)
            wristGdSrt.xfo.tr.set(-12.071067811865474, 12.92893218813452, 0.0)

        self.guide.build()

        return


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
    def _build(self):
        """Internal build function for building the component in Softimage."""

        super(ArmComponent, self)._build()

        # ====================
        # Calculate positions
        # ====================
        self.getComponentXfo()
        self.getUpVXfo()
        self.getBoneData()

        # =================
        # Find Hierarchies
        # =================
        ioHrc = self.findChild("arm_io_hrc")
        ctrlHrc = self.findChild("arm_ctrl_hrc")
        armatureHrc = self.findChild("arm_armature_hrc")

        # ============
        # Setup Ctrls
        # ============

        # Setup Hierarchy
        ioHrc.addAttributeGroup("DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "bone1Len", self.boneData["bicep"]["length"], minValue=0.0, maxValue=100.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "bone2Len", self.boneData["forearm"]["length"], minValue=0.0, maxValue=100.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "fkik", 1.0, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "softDist", 0.5, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "softIK", True, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "stretch", True, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "stretchBlend", 1.0, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "rightSide", self.side == "R", group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "toggleDebugging", True, group="DisplayInfo_Arm_Settings")

        # Creat Inputs
        clavicleKineIn = elements.Null("_".join(["arm", self.side, "clavicle_kineIn"]), parent=ioHrc)
        clavicleKineIn.setGlobalTranslation(self.positions[0])

        # Create Controls
        ikHandleZero = elements.Group("_".join(["arm", self.side, "ikHandle_ctrl_zero"]), parent=ctrlHrc)
        ikHandleZero.setLocalTranslation(self.boneData["wrist"]["xfo"].tr)

        ikHandleCtrl = elements.Control("_".join(["arm", self.side, "ikHandle_ctrl"]), "pin", parent=ikHandleZero)
        ikHandleCtrl.setLocalTranslation(Vec3(0,0,0))
        ikHandleCtrl.color = self.ctrlColor
        ikHandleCtrl.rotOffset = [-90,0,0]
        ikHandleCtrl.sclOffset = [1.5,1.5,1.5]

        upVZero = elements.Group("_".join(["arm", self.side, "upV_ctrl_zero"]), parent=ctrlHrc)
        upVZero.setLocalTranslation(self.upVXfo.tr)

        upVCtrl = elements.Control("_".join(["arm", self.side, "upV_ctrl"]), "triangle", parent=upVZero)
        upVCtrl.setLocalTranslation(Vec3(0,0,0))
        upVCtrl.color = self.ctrlColor
        upVCtrl.rotOffset = [0,-90,0]
        upVCtrl.posOffset = [0,0,-1]

        bicepFKZero = elements.Group("_".join(["arm", self.side, "bicepFK_ctrl_zero"]), parent=ctrlHrc)
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
        bicepKineOut = elements.Null("_".join(["arm", self.side, "bicep_kineOut"]), parent=ioHrc)
        bicepKineOut.setLocalTranslation(self.boneData["bicep"]["xfo"].tr)
        bicepKineOut.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)

        forearmKineOut = elements.Null("_".join(["arm", self.side, "forearm_kineOut"]), parent=ioHrc)
        forearmKineOut.setLocalTranslation(self.boneData["forearm"]["xfo"].tr)
        forearmKineOut.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)

        wristKineOut = elements.Null("_".join(["arm", self.side, "wrist_kineOut"]), parent=ioHrc)
        wristKineOut.setLocalTranslation(self.boneData["wrist"]["xfo"].tr)
        wristKineOut.setGlobalRotation(self.boneData["wrist"]["xfo"].rot)

        # ===============
        # Setup Armature
        # ===============
        self.layer="armature"

        # Setup Joints
        bicepJnt = elements.Joint("_".join(["arm", self.side, "bicep_jnt"]), parent=armatureHrc)
        bicepJnt.setLocalTranslation(Vec3(0,0,0))
        bicepJnt.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)
        bicepJnt.addConstraint("bicepJntToKineOut", "pose", [bicepKineOut])

        forearmJnt = elements.Joint("_".join(["arm", self.side, "forearm_jnt"]), parent=armatureHrc)
        forearmJnt.setLocalTranslation(Vec3(4,0,-3))
        forearmJnt.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)
        forearmJnt.addConstraint("forearmJntToKineOut", "pose", [forearmKineOut])

        wristJnt = elements.Joint("_".join(["arm", self.side, "wrist_jnt"]), parent=armatureHrc)
        wristJnt.setLocalTranslation(Vec3(8,0,0))
        wristJnt.setGlobalRotation(self.boneData["wrist"]["xfo"].rot)
        wristJnt.addConstraint("wristJntToKineOut", "pose", [wristKineOut])

        return


    def _postBuild(self):

        super(ArmComponent, self)._postBuild()