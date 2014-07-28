from kraken.core.maths.vec import Vec3
from kraken.core.maths.rotation import Quat
from kraken.core.maths.rotation import Euler
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.pin_control import PinControl

from kraken.core.objects.operators.splice_operator import SpliceOperator


class ArmComponent(BaseComponent):
    """Arm Component"""

    def __init__(self, name, parent=None, side='M'):
        super(ArmComponent, self).__init__(name, parent, side)

        container = self.getParent()
        armatureLayer = container.getChildByName('armature')

        # =========
        # Armature
        # =========
        # armatureParent = armatureLayer
        # if armatureParent is None:
        #     armatureParent = self

        # bicepDef = Joint('bicep')
        # armatureParent.addChild(bicepDef)


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
        bicepFKCtrl.scalePoints(Vec3(bicepLen, 1.0, 1.0))
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
        forearmFKCtrl.scalePoints(Vec3(forearmLen, 1.0, 1.0))
        forearmFKCtrl.setColor(ctrlColor)
        forearmFKCtrl.xfo.copy(forearmXfo)

        forearmFKCtrlSrtBuffer = SrtBuffer('forearmFK')
        forearmFKCtrlSrtBuffer.xfo.copy(forearmFKCtrl.xfo)
        forearmFKCtrlSrtBuffer.addChild(forearmFKCtrl)
        bicepFKCtrl.addChild(forearmFKCtrlSrtBuffer)

        # Arm IK
        armIKCtrl = PinControl('IK')
        armIKCtrl.xfo.tr.copy(wristPosition)
        armIKCtrl.rotatePoints(90, 0, 0)
        armIKCtrl.setColor(ctrlColor)

        armIKCtrlSrtBuffer = SrtBuffer('IK')
        armIKCtrlSrtBuffer.xfo.copy(armIKCtrl.xfo)
        armIKCtrlSrtBuffer.addChild(armIKCtrl)
        self.addChild(armIKCtrlSrtBuffer)

        # Setup component Xfo I/O's
        clavicleEndInput = Locator('clavicleEnd')
        clavicleEndInput.xfo.copy(bicepXfo)

        bicepOutput = Locator('bicep')
        bicepOutput.xfo.copy(bicepXfo)
        forearmOutput = Locator('forearm')
        forearmOutput.xfo.copy(forearmXfo)
        armEndOutput = Locator('armEnd')
        armEndOutput.xfo.tr.copy(wristPosition)

        # Setup componnent Attribute I/O's
        armFollowBodyInputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint inputs
        armRootInputConstraint = PoseConstraint('_'.join([armIKCtrl.getName(), 'To', clavicleEndInput.getName()]))
        armRootInputConstraint.setMaintainOffset(True)
        armRootInputConstraint.addConstrainer(clavicleEndInput)
        bicepFKCtrlSrtBuffer.addConstraint(armRootInputConstraint)

        # Constraint outputs
        # armEndOutputConstraint = PoseConstraint('_'.join([armEndOutput.getName(), 'To', armIKCtrl.getName()]))
        # armEndOutputConstraint.addConstrainer(armIKCtrl)
        # armEndOutput.addConstraint(armEndOutputConstraint)

        # Add Xfo I/O's
        self.addInput(clavicleEndInput)
        self.addOutput(bicepOutput)
        self.addOutput(forearmOutput)
        self.addOutput(armEndOutput)

        # Add Attribute I/O's
        self.addInput(armFollowBodyInputAttr)


        # Add Splice Op
        spliceOp = SpliceOperator("armSpliceOp", "ArmSolver", "KrakenArmSolver")
        spliceOp.setInput("clav", clavicleEndInput)
        spliceOp.setInput("blend", armFollowBodyInputAttr)
        spliceOp.setOutput("wrist", armEndOutput)
        self.addOperator(spliceOp)

        # Think about how to add multiple operators to the SpliceOp
        # armSolveKLOp = spliceOp.AddKLOp("armSolve")
        # armDebugKLOp = spliceOp.AddKLOp("armDebug")
        # klOp.appendInput


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    print armLeft.getNumChildren()