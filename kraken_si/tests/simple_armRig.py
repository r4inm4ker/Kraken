from kraken.core.maths import Vec3
from kraken.core.maths import Euler
from kraken.core.maths import mathUtils

from kraken.core.objects import elements
from kraken.kraken_si.objects import elements

# ================
# Setup Asset
# ================
armRig = elements.Asset("armRig")


# ===============
# Setup Armature
# ===============
armatureLayer = elements.Asset("armRig_armature", parent=armRig)

bicepSrt = elements.Null("arm_L_bicep_srt", parent=armatureLayer)
bicepSrt.setLocalTranslation(Vec3(0,0,0))
bicepSrt.setGlobalRotation(Euler(mathUtils.degToRad(-90),mathUtils.degToRad(36.8699),0))

forearmSrt = elements.Null("arm_L_forearm_srt", parent=armatureLayer)
forearmSrt.setLocalTranslation(Vec3(4,0,-3))
forearmSrt.setGlobalRotation(Euler(mathUtils.degToRad(-90),mathUtils.degToRad(-36.8699),0))

wristSrt = elements.Null("arm_L_wrist_srt", parent=armatureLayer)
wristSrt.setLocalTranslation(Vec3(8,0,0))
wristSrt.setGlobalRotation(Euler(mathUtils.degToRad(-90),mathUtils.degToRad(-36.8699),0))

# ============
# Setup Ctrls
# ============
ctrlLayer = elements.Asset("armRig_controls", parent=armRig)

# Setup Hierarchy
armHrc = elements.Group("arm_L_hrc", parent=ctrlLayer)
armCtrlHrc = elements.Group("arm_L_ctrl_hrc", parent=armHrc)

armIOHrc = elements.Group("arm_L_io_hrc", parent=armHrc)
armIOHrc.addAttributeGroup("DisplayInfo_Arm_Settings")
armIOHrc.addAttribute("float", "bone1Len", 5.0, minValue=0.0, maxValue=100.0, group="DisplayInfo_Arm_Settings")
armIOHrc.addAttribute("float", "bone2Len", 5.0, minValue=0.0, maxValue=100.0, group="DisplayInfo_Arm_Settings")
armIOHrc.addAttribute("bool", "softIK", True, group="DisplayInfo_Arm_Settings")
armIOHrc.addAttribute("float", "softDist", 0.5, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")
armIOHrc.addAttribute("bool", "stretch", True, group="DisplayInfo_Arm_Settings")
armIOHrc.addAttribute("float", "stretchBlend", 1.0, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")


# Creat Inputs
clavicleKineIn = elements.Null("arm_L_clavicle_kineIn", parent=armIOHrc)

# Create Controls
ikHandleZero = elements.Group("arm_L_ikHandle_ctrl_zero", parent=armCtrlHrc)
ikHandleZero.setLocalTranslation(Vec3(8,0,0))

ikHandleCtrl = elements.Control("arm_L_ikHandle_ctrl", "pin", parent=ikHandleZero)
ikHandleCtrl.setLocalTranslation(Vec3(0,0,0))
ikHandleCtrl.color = "green"
ikHandleCtrl.rotOffset = [-90,0,0]
ikHandleCtrl.sclOffset = [1.5,1.5,1.5]

upVZero = elements.Group("arm_L_upV_ctrl_zero", parent=armCtrlHrc)
upVZero.setLocalTranslation(Vec3(4,0,-6))

upVCtrl = elements.Control("arm_L_upV_ctrl", "triangle", parent=upVZero)
upVCtrl.setLocalTranslation(Vec3(0,0,0))
upVCtrl.color = "green"
upVCtrl.rotOffset = [0,-90,0]
upVCtrl.posOffset = [0,0,-1]

bicepFKZero = elements.Group("arm_L_bicepFK_ctrl_zero", parent=armCtrlHrc)
bicepFKZero.setLocalTranslation(Vec3(0,0,0))
bicepFKZero.setGlobalRotation(Euler(mathUtils.degToRad(-90),mathUtils.degToRad(36.8699),0))

bicepFKCtrl = elements.Control("arm_L_bicepFK_ctrl", "cubeXAligned", parent=bicepFKZero)
bicepFKCtrl.setLocalTranslation(Vec3(0,0,0))
bicepFKCtrl.color = "green"
bicepFKCtrl.sclOffset = [5,1,1]

forearmFKZero = elements.Group("arm_L_forearmFK_ctrl_zero", parent=bicepFKCtrl)
forearmFKZero.setLocalTranslation(Vec3(4,0,-3))
forearmFKZero.setGlobalRotation(Euler(mathUtils.degToRad(-90),mathUtils.degToRad(-36.8699),0))

forearmFKCtrl = elements.Control("arm_L_forearmFK_ctrl", "cubeXAligned", parent=forearmFKZero)
forearmFKCtrl.setLocalTranslation(Vec3(0,0,0))
forearmFKCtrl.color = "green"
forearmFKCtrl.sclOffset = [5,1,1]

armRig.build()