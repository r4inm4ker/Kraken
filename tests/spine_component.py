from kraken.core.maths.vec import Vec3

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.circle_control  import  CircleControl


class SpineComponent(BaseComponent):
    """Spine Component"""

    def __init__(self, name, parent=None, side='M'):
        super(SpineComponent, self).__init__(name, parent, side)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        cogPosition = Vec3(0.0, 11.1351, -0.1382)
        spine01Position = Vec3(0.0, 11.1351, -0.1382)
        spine02Position = Vec3(0.0, 12.3085, -0.265)
        spine03Position = Vec3(0.0, 13.1051, -0.4821)

        # COG
        cogCtrl = CircleControl('cog')
        cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        cogCtrl.xfo.tr.copy(cogPosition)
        cogCtrl.setColor("orange")
        self.addChild(cogCtrl)

        # Spine01
        spine01Ctrl = CircleControl('spine01')
        spine01Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine01Ctrl.xfo.tr.copy(spine01Position)
        spine01Ctrl.setColor("yellow")

        spine01CtrlSrtBuffer = SrtBuffer('spine01SrtBuffer')
        spine01CtrlSrtBuffer.xfo.copy(spine01Ctrl.xfo)
        spine01CtrlSrtBuffer.addChild(spine01Ctrl)
        cogCtrl.addChild(spine01CtrlSrtBuffer)

        # Spine02
        spine02Ctrl = CircleControl('spine02')
        spine02Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine02Ctrl.xfo.tr.copy(spine02Position)
        spine02Ctrl.setColor("yellow")

        spine02CtrlSrtBuffer = SrtBuffer('spine02SrtBuffer')
        spine02CtrlSrtBuffer.xfo.copy(spine02Ctrl.xfo)
        spine02CtrlSrtBuffer.addChild(spine02Ctrl)
        cogCtrl.addChild(spine02CtrlSrtBuffer)

        # Spine03
        spine03Ctrl = CircleControl('spine03')
        spine03Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine03Ctrl.xfo.tr.copy(spine03Position)
        spine03Ctrl.setColor("yellow")

        spine03CtrlSrtBuffer = SrtBuffer('spine03SrtBuffer')
        spine03CtrlSrtBuffer.xfo.copy(spine03Ctrl.xfo)
        spine03CtrlSrtBuffer.addChild(spine03Ctrl)
        spine02Ctrl.addChild(spine03CtrlSrtBuffer)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        spine01Output = Joint('spine01')
        spine01Output.xfo.tr.copy(spine01Ctrl.xfo.tr)
        spine02Output = Joint('spine02')
        spine02Output.xfo.tr.copy(spine02Ctrl.xfo.tr)
        spine03Output = Joint('spine03')
        spine03Output.xfo.tr.copy(spine03Ctrl.xfo.tr)
        spine04Output = Joint('spine04')
        spine04Output.xfo.tr.copy(spine04Ctrl.xfo.tr)

        spineBaseOutput = Locator('spineBase')
        spineBaseOutput.xfo.tr.copy(spine01Ctrl.xfo.tr)

        spineEndOutput = Locator('spineEnd')
        spineEndOutput.xfo.tr.copy(spine03Ctrl.xfo.tr)

        # Setup componnent Attribute I/O's
        maxLengthInputAttr = FloatAttribute('maxLength', 3.0, 0.0, 10.0)
        tangentLengthInputAttr = FloatAttribute('tangentLength', 1.0, 0.0, 5.0)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        spineBaseOutputConstraint = PoseConstraint('_'.join([spineBaseOutput.getName(), 'To', 'spineBase']))
        spineBaseOutputConstraint.addConstrainer(spine01Ctrl)
        spineBaseOutput.addConstraint(spineBaseOutputConstraint)

        spineEndOutputConstraint = PoseConstraint('_'.join([spineEndOutput.getName(), 'To', 'spineEnd']))
        spineEndOutputConstraint.addConstrainer(spine03Ctrl)
        spineEndOutput.addConstraint(spineEndOutputConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addOutput(spine01Output)
        self.addOutput(spine02Output)
        self.addOutput(spine03Output)
        self.addOutput(spine04Output)
        self.addOutput(spineBaseOutput)
        self.addOutput(spineEndOutput)

        # Add Attribute I/O's


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        spliceOp = SpliceOperator("spineSpliceOp", "SpineSolver", "KrakenSpineSolver")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("maxLength", maxLengthInputAttr)
        spliceOp.setInput("tangentLength", tangentLengthInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("spine01Ctrl", spine01Ctrl)
        spliceOp.setInput("spine02Ctrl", spine02Ctrl)
        spliceOp.setInput("spine03Ctrl", spine03Ctrl)

        # Add Xfo Outputs
        spliceOp.setOutput("spine01Out", spine01Output)
        spliceOp.setOutput("spine02Out", spine02Output)
        spliceOp.setOutput("spine03Out", spine03Output)
        spliceOp.setOutput("spine04Out", spine04Output)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    spine = SpineComponent("mySpine")
    print spine.getNumChildren()