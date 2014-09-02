from kraken.core.maths.vec import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.pin_control import PinControl
from kraken.core.objects.controls.triangle_control import TriangleControl

from kraken.core.objects.operators.splice_operator import SpliceOperator


class ArmComponent(BaseComponent):
    """Arm Component"""

    def __init__(self, name, parent=None, side='M'):
        super(ArmComponent, self).__init__(name, parent, side)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        if self.getSide() == "R":
            ctrlColor = "red"
            bicepPosition = Vec3(-2.27, 15.295, -0.753)
            forearmPosition = Vec3(-5.039, 13.56, -0.859)
            wristPosition = Vec3(-7.1886, 12.2819, 0.4906)
        else:
            ctrlColor = "greenBright"
            bicepPosition = Vec3(2.27, 15.295, -0.753)
            forearmPosition = Vec3(5.039, 13.56, -0.859)
            wristPosition = Vec3(7.1886, 12.2819, 0.4906)

        # Calculate Bicep Xfo
        rootToWrist = wristPosition.subtract(bicepPosition).unit()
        rootToElbow = forearmPosition.subtract(bicepPosition).unit()
        bone1Normal = rootToWrist.cross(rootToElbow).unit()
        bone1ZAxis = rootToElbow.cross(bone1Normal).unit()
        bicepXfo = Xfo()
        bicepXfo.setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, bicepPosition)

        # Calculate Forearm Xfo
        elbowToWrist = wristPosition.subtract(forearmPosition).unit()
        elbowToRoot = bicepPosition.subtract(forearmPosition).unit()
        bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
        bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()
        forearmXfo = Xfo()
        forearmXfo.setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, forearmPosition)

        # Bicep
        bicepFKCtrl = CubeControl('bicepFK')
        bicepFKCtrl.alignOnXAxis()
        bicepLen = bicepPosition.subtract(forearmPosition).length()
        bicepFKCtrl.scalePoints(Vec3(bicepLen, 1.75, 1.75))
        bicepFKCtrl.setColor(ctrlColor)
        bicepFKCtrl.xfo.copy(bicepXfo)

        bicepFKCtrlSrtBuffer = SrtBuffer('bicepFK')
        self.addChild(bicepFKCtrlSrtBuffer)
        bicepFKCtrlSrtBuffer.xfo.copy(bicepFKCtrl.xfo)
        bicepFKCtrlSrtBuffer.addChild(bicepFKCtrl)

        # Forearm
        forearmFKCtrl = CubeControl('forearmFK')
        forearmFKCtrl.alignOnXAxis()
        forearmLen = forearmPosition.subtract(wristPosition).length()
        forearmFKCtrl.scalePoints(Vec3(forearmLen, 1.5, 1.5))
        forearmFKCtrl.setColor(ctrlColor)
        forearmFKCtrl.xfo.copy(forearmXfo)

        forearmFKCtrlSrtBuffer = SrtBuffer('forearmFK')
        bicepFKCtrl.addChild(forearmFKCtrlSrtBuffer)
        forearmFKCtrlSrtBuffer.xfo.copy(forearmFKCtrl.xfo)
        forearmFKCtrlSrtBuffer.addChild(forearmFKCtrl)

        # Arm IK
        armIKCtrlSrtBuffer = SrtBuffer('IK', parent=self)
        armIKCtrlSrtBuffer.xfo.tr.copy(wristPosition)

        armIKCtrl = PinControl('IK', parent=armIKCtrlSrtBuffer)
        armIKCtrl.xfo.copy(armIKCtrlSrtBuffer.xfo)
        armIKCtrl.setColor(ctrlColor)

        if self.getSide() == "R":
            armIKCtrl.rotatePoints(0, 90, 0)
        else:
            armIKCtrl.rotatePoints(0, -90, 0)


        # Add Component Params to IK control
        armDebugInputAttr = BoolAttribute('debug', True)
        armBone1LenInputAttr = FloatAttribute('bone1Len', bicepLen, 0.0, 100.0)
        armBone2LenInputAttr = FloatAttribute('bone2Len', forearmLen, 0.0, 100.0)
        armFkikInputAttr = FloatAttribute('fkik', 0.0, 0.0, 1.0)
        armSoftIKInputAttr = BoolAttribute('softIK', True)
        armSoftDistInputAttr = FloatAttribute('softDist', 0.0, 0.0, 1.0)
        armStretchInputAttr = BoolAttribute('stretch', True)
        armStretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0, 0.0, 1.0)

        armSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings")
        armIKCtrl.addAttributeGroup(armSettingsAttrGrp)
        armSettingsAttrGrp.addAttribute(armDebugInputAttr)
        armSettingsAttrGrp.addAttribute(armBone1LenInputAttr)
        armSettingsAttrGrp.addAttribute(armBone2LenInputAttr)
        armSettingsAttrGrp.addAttribute(armFkikInputAttr)
        armSettingsAttrGrp.addAttribute(armSoftIKInputAttr)
        armSettingsAttrGrp.addAttribute(armSoftDistInputAttr)
        armSettingsAttrGrp.addAttribute(armStretchInputAttr)
        armSettingsAttrGrp.addAttribute(armStretchBlendInputAttr)

        # UpV
        upVXfo = xfoFromDirAndUpV(bicepPosition, wristPosition, forearmPosition)
        upVXfo.tr.copy(forearmPosition)
        upVOffset = Vec3(0, 0, 5)
        upVOffset = upVXfo.transformVector(upVOffset)

        armUpVCtrl = TriangleControl('UpV')
        armUpVCtrl.xfo.tr.copy(upVOffset)
        armUpVCtrl.alignOnZAxis()
        armUpVCtrl.rotatePoints(180, 0, 0)
        armUpVCtrl.setColor(ctrlColor)

        armUpVCtrlSrtBuffer = SrtBuffer('UpV')
        self.addChild(armUpVCtrlSrtBuffer)
        armUpVCtrlSrtBuffer.xfo.tr.copy(upVOffset)
        armUpVCtrlSrtBuffer.addChild(armUpVCtrl)


        # ==========
        # Deformers
        # ==========
        container = self.getParent().getParent()
        deformersLayer = container.getChildByName('deformers')

        bicepDef = Joint('bicep')
        bicepDef.setComponent(self)

        forearmDef = Joint('forearm')
        forearmDef.setComponent(self)

        wristDef = Joint('wrist')
        wristDef.setComponent(self)

        deformersLayer.addChild(bicepDef)
        deformersLayer.addChild(forearmDef)
        deformersLayer.addChild(wristDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        clavicleEndInput = Locator('clavicleEnd')
        clavicleEndInput.xfo.copy(bicepXfo)

        bicepOutput = Locator('bicep')
        bicepOutput.xfo.copy(bicepXfo)
        forearmOutput = Locator('forearm')
        forearmOutput.xfo.copy(forearmXfo)

        armEndXfo = Xfo()
        armEndXfo.rot = forearmXfo.rot.clone()
        armEndXfo.tr.copy(wristPosition)
        armEndXfoOutput = Locator('armEndXfo')
        armEndXfoOutput.xfo.copy(armEndXfo)

        armEndPosOutput = Locator('armEndPos')
        armEndPosOutput.xfo.copy(armEndXfo)


        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        bone1LenInputAttr = FloatAttribute('bone1Len', bicepLen, 0.0, 100.0)
        bone2LenInputAttr = FloatAttribute('bone2Len', forearmLen, 0.0, 100.0)
        fkikInputAttr = FloatAttribute('fkik', 0.0, 0.0, 1.0)
        softIKInputAttr = BoolAttribute('softIK', True)
        softDistInputAttr = FloatAttribute('softDist', 0.5, 0.0, 1.0)
        stretchInputAttr = BoolAttribute('stretch', True)
        stretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0, 0.0, 1.0)
        rightSideInputAttr = BoolAttribute('rightSide', side is 'R')

        # Connect attrs to control attrs
        debugInputAttr.connect(armDebugInputAttr)
        bone1LenInputAttr.connect(armBone1LenInputAttr)
        bone2LenInputAttr.connect(armBone2LenInputAttr)
        fkikInputAttr.connect(armFkikInputAttr)
        softIKInputAttr.connect(armSoftIKInputAttr)
        softDistInputAttr.connect(armSoftDistInputAttr)
        stretchInputAttr.connect(armStretchInputAttr)
        stretchBlendInputAttr.connect(armStretchBlendInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        armRootInputConstraint = PoseConstraint('_'.join([armIKCtrl.getName(), 'To', clavicleEndInput.getName()]))
        armRootInputConstraint.setMaintainOffset(True)
        armRootInputConstraint.addConstrainer(clavicleEndInput)
        bicepFKCtrlSrtBuffer.addConstraint(armRootInputConstraint)

        # Constraint outputs


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(clavicleEndInput)
        self.addOutput(bicepOutput)
        self.addOutput(forearmOutput)
        self.addOutput(armEndXfoOutput)
        self.addOutput(armEndPosOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(bone1LenInputAttr)
        self.addInput(bone2LenInputAttr)
        self.addInput(fkikInputAttr)
        self.addInput(softIKInputAttr)
        self.addInput(softDistInputAttr)
        self.addInput(stretchInputAttr)
        self.addInput(stretchBlendInputAttr)
        self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Solver Splice Op
        spliceOp = SpliceOperator("armSpliceOp", "LimbSolver", "KrakenLimbSolver")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("bone1Len", bone1LenInputAttr)
        spliceOp.setInput("bone2Len", bone2LenInputAttr)
        spliceOp.setInput("fkik", fkikInputAttr)
        spliceOp.setInput("softIK", softIKInputAttr)
        spliceOp.setInput("softDist", softDistInputAttr)
        spliceOp.setInput("stretch", stretchInputAttr)
        spliceOp.setInput("stretchBlend", stretchBlendInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("root", clavicleEndInput)
        spliceOp.setInput("bone1FK", bicepFKCtrl)
        spliceOp.setInput("bone2FK", forearmFKCtrl)
        spliceOp.setInput("ikHandle", armIKCtrl)
        spliceOp.setInput("upV", armUpVCtrl)

        # Add Xfo Outputs
        spliceOp.setOutput("bone01Out", bicepOutput)
        spliceOp.setOutput("bone02Out", forearmOutput)
        spliceOp.setOutput("bone03Out", armEndXfoOutput)
        spliceOp.setOutput("bone03PosOut", armEndPosOutput)


        # Add Deformer Splice Op
        spliceOp = SpliceOperator("armDeformerSpliceOp", "LimbConstraintSolver", "KrakenLimbSolver")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("bone01Constrainer", bicepOutput)
        spliceOp.setInput("bone02Constrainer", forearmOutput)
        spliceOp.setInput("bone03Constrainer", armEndXfoOutput)

        # Add Xfo Outputs
        spliceOp.setOutput("bone01Deformer", bicepDef)
        spliceOp.setOutput("bone02Deformer", forearmDef)
        spliceOp.setOutput("bone03Deformer", wristDef)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    print armLeft.getNumChildren()

    def traverseHierarchy(kObject):
        print kObject.getBuildName()
        # Build children
        for i in xrange(kObject.getNumChildren()):
            child = kObject.getChildByIndex(i)
            traverseHierarchy(child)
    traverseHierarchy(armLeft)
