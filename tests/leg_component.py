from kraken.core.maths.vec import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.pin_control import PinControl
from kraken.core.objects.controls.triangle_control import TriangleControl

from kraken.core.objects.operators.splice_operator import SpliceOperator


class LegComponent(BaseComponent):
    """Leg Component"""

    def __init__(self, name, parent=None, side='M'):
        super(LegComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        if self.getSide() == "R":
            ctrlColor = "red"
            femurPosition = Vec3(-0.9811, 9.769, -0.4572)
            kneePosition = Vec3(-1.4488, 5.4418, -0.5348)
            anklePosition = Vec3(-1.841, 1.1516, -1.237)
        else:
            ctrlColor = "greenBright"
            femurPosition = Vec3(0.9811, 9.769, -0.4572)
            kneePosition = Vec3(1.4488, 5.4418, -0.5348)
            anklePosition = Vec3(1.841, 1.1516, -1.237)

        # Calculate Femur Xfo
        rootToAnkle = anklePosition.subtract(femurPosition).unit()
        rootToKnee = kneePosition.subtract(femurPosition).unit()
        bone1Normal = rootToAnkle.cross(rootToKnee).unit()
        bone1ZAxis = rootToKnee.cross(bone1Normal).unit()
        femurXfo = Xfo()
        femurXfo.setFromVectors(rootToKnee, bone1Normal, bone1ZAxis, femurPosition)

        # Calculate Shin Xfo
        kneeToAnkle = anklePosition.subtract(kneePosition).unit()
        kneeToRoot = femurPosition.subtract(kneePosition).unit()
        bone2Normal = kneeToRoot.cross(kneeToAnkle).unit()
        bone2ZAxis = kneeToAnkle.cross(bone2Normal).unit()
        shinXfo = Xfo()
        shinXfo.setFromVectors(kneeToAnkle, bone2Normal, bone2ZAxis, kneePosition)


        # Femur
        femurFKCtrl = CubeControl('femurFK')
        femurFKCtrl.alignOnXAxis()
        femurLen = femurPosition.subtract(kneePosition).length()
        femurFKCtrl.scalePoints(Vec3(femurLen, 1.0, 1.0))
        femurFKCtrl.setColor(ctrlColor)
        femurFKCtrl.xfo.copy(femurXfo)

        femurFKCtrlSrtBuffer = SrtBuffer('femurFK')
        self.addChild(femurFKCtrlSrtBuffer)
        femurFKCtrlSrtBuffer.xfo.copy(femurFKCtrl.xfo)
        femurFKCtrlSrtBuffer.addChild(femurFKCtrl)

        # Shin
        shinFKCtrl = CubeControl('shinFK')
        shinFKCtrl.alignOnXAxis()
        shinLen = kneePosition.subtract(anklePosition).length()
        shinFKCtrl.scalePoints(Vec3(shinLen, 1.0, 1.0))
        shinFKCtrl.setColor(ctrlColor)
        shinFKCtrl.xfo.copy(shinXfo)

        shinFKCtrlSrtBuffer = SrtBuffer('shinFK')
        shinFKCtrlSrtBuffer.xfo.copy(shinFKCtrl.xfo)
        shinFKCtrlSrtBuffer.addChild(shinFKCtrl)
        femurFKCtrl.addChild(shinFKCtrlSrtBuffer)

        # Ankle
        legIKCtrl = PinControl('IK')
        legIKCtrl.xfo.tr.copy(anklePosition)

        if self.getSide() == "R":
            legIKCtrl.rotatePoints(0, 90, 0)
        else:
            legIKCtrl.rotatePoints(0, -90, 0)

        legIKCtrl.setColor(ctrlColor)
        legIKCtrlSrtBuffer = SrtBuffer('IK')
        legIKCtrlSrtBuffer.xfo.copy(legIKCtrl.xfo)
        legIKCtrlSrtBuffer.addChild(legIKCtrl)
        self.addChild(legIKCtrlSrtBuffer)

        # UpV
        upVXfo = xfoFromDirAndUpV(femurPosition, anklePosition, kneePosition)
        upVXfo.tr.copy(kneePosition)
        upVOffset = Vec3(0, 0, 5)
        upVOffset = upVXfo.transformVector(upVOffset)

        legUpVCtrl = TriangleControl('UpV')
        legUpVCtrl.xfo.tr.copy(upVOffset)
        legUpVCtrl.alignOnZAxis()
        legUpVCtrl.rotatePoints(0, 0, 0)
        legUpVCtrl.setColor(ctrlColor)

        legUpVCtrlSrtBuffer = SrtBuffer('UpV')
        legUpVCtrlSrtBuffer.xfo.tr.copy(upVOffset)
        legUpVCtrlSrtBuffer.addChild(legUpVCtrl)
        self.addChild(legUpVCtrlSrtBuffer)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        legPelvisInput = Locator('pelvisInput')
        legPelvisInput.xfo.copy(femurXfo)
        femurOutput = Locator('femur')
        femurOutput.xfo.copy(femurXfo)
        shinOutput = Locator('shin')
        shinOutput.xfo.copy(shinXfo)
        legEndOutput = Locator('legEnd')
        legEndOutput.xfo.tr.copy(anklePosition)

        # Setup componnent Attribute I/O's
        bone1LenInputAttr = FloatAttribute('bone1Len', femurLen, 0.0, 100.0)
        bone2LenInputAttr = FloatAttribute('bone2Len', shinLen, 0.0, 100.0)
        fkikInputAttr = FloatAttribute('fkik', 0.0, 0.0, 1.0)
        softIKInputAttr = BoolAttribute('softIK', True)
        softDistInputAttr = FloatAttribute('softDist', 0.5, 0.0, 1.0)
        stretchInputAttr = BoolAttribute('stretch', True)
        stretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0, 0.0, 1.0)
        rightSideInputAttr = BoolAttribute('rightSide', False)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([legIKCtrl.getName(), 'To', legPelvisInput.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(legPelvisInput)
        femurFKCtrlSrtBuffer.addConstraint(legRootInputConstraint)

        # Constraint outputs


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(legPelvisInput)
        self.addOutput(femurOutput)
        self.addOutput(shinOutput)
        self.addOutput(legEndOutput)

        # Add Attribute I/O's
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
        # Add Splice Op
        spliceOp = SpliceOperator("legSpliceOp", "LimbSolver", "KrakenLimbSolver")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("bone1Len", bone1LenInputAttr)
        spliceOp.setInput("bone2Len", bone2LenInputAttr)
        spliceOp.setInput("fkik", fkikInputAttr)
        spliceOp.setInput("softIK", softIKInputAttr)
        spliceOp.setInput("softDist", softDistInputAttr)
        spliceOp.setInput("stretch", stretchInputAttr)
        spliceOp.setInput("stretchBlend", stretchBlendInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("root", legPelvisInput)
        spliceOp.setInput("bone1FK", femurFKCtrl)
        spliceOp.setInput("bone2FK", shinFKCtrl)
        spliceOp.setInput("ikHandle", legIKCtrl)
        spliceOp.setInput("upV", legUpVCtrl)

        # Add Xfo Outputs
        spliceOp.setOutput("bone01Out", femurOutput)
        spliceOp.setOutput("bone02Out", shinOutput)
        spliceOp.setOutput("bone03Out", legEndOutput)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    legLeft = LegComponent("myArm", side='L')
    print legLeft.getNumChildren()