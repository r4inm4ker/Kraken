from kraken.core.maths.vec import Vec3

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.circle_control  import  CircleControl

from kraken.core.objects.operators.splice_operator import SpliceOperator


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
        spine02Position = Vec3(0.0, 11.8013, -0.1995)
        spine03Position = Vec3(0.0, 12.4496, -0.3649)
        spine04Position = Vec3(0.0, 13.1051, -0.4821)

        # COG
        cogCtrl = CircleControl('cog')
        cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        cogCtrl.xfo.tr.copy(cogPosition)
        cogCtrl.setColor("orange")

        cogCtrlSrtBuffer = SrtBuffer('cog')
        cogCtrlSrtBuffer.xfo.tr.copy(cogPosition)
        cogCtrlSrtBuffer.addChild(cogCtrl)
        self.addChild(cogCtrl)

        # Spine01
        spine01Ctrl = CircleControl('spine01')
        spine01Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine01Ctrl.xfo.tr.copy(spine01Position)
        spine01Ctrl.setColor("yellow")

        spine01CtrlSrtBuffer = SrtBuffer('spine01')
        spine01CtrlSrtBuffer.xfo.copy(spine01Ctrl.xfo)
        spine01CtrlSrtBuffer.addChild(spine01Ctrl)
        cogCtrl.addChild(spine01CtrlSrtBuffer)

        # Spine02
        spine02Ctrl = CircleControl('spine02')
        spine02Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine02Ctrl.xfo.tr.copy(spine02Position)
        spine02Ctrl.setColor("yellow")

        spine02CtrlSrtBuffer = SrtBuffer('spine02')
        spine02CtrlSrtBuffer.xfo.copy(spine02Ctrl.xfo)
        spine02CtrlSrtBuffer.addChild(spine02Ctrl)
        spine01Ctrl.addChild(spine02CtrlSrtBuffer)

        # Spine03
        spine03Ctrl = CircleControl('spine03')
        spine03Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine03Ctrl.xfo.tr.copy(spine03Position)
        spine03Ctrl.setColor("yellow")

        spine03CtrlSrtBuffer = SrtBuffer('spine03')
        spine03CtrlSrtBuffer.xfo.copy(spine03Ctrl.xfo)
        spine03CtrlSrtBuffer.addChild(spine03Ctrl)

        # Spine04
        spine04Ctrl = CircleControl('spine04')
        spine04Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine04Ctrl.xfo.tr.copy(spine04Position)
        spine04Ctrl.setColor("yellow")
        spine04Ctrl.addChild(spine03CtrlSrtBuffer)

        spine04CtrlSrtBuffer = SrtBuffer('spine04')
        spine04CtrlSrtBuffer.xfo.copy(spine04Ctrl.xfo)
        spine04CtrlSrtBuffer.addChild(spine04Ctrl)
        cogCtrl.addChild(spine04CtrlSrtBuffer)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        spine01Output = Joint('spine01')
        spine01Output.xfo.tr.copy(spine01Ctrl.xfo.tr)
        spine02Output = Joint('spine02')
        spine02Output.xfo.tr.copy(spine01Ctrl.xfo.tr)
        spine03Output = Joint('spine03')
        spine03Output.xfo.tr.copy(spine01Ctrl.xfo.tr)
        spine04Output = Joint('spine04')
        spine04Output.xfo.tr.copy(spine01Ctrl.xfo.tr)

        spineBaseOutput = Locator('spineBase')
        spineBaseOutput.xfo.tr.copy(spine01Ctrl.xfo.tr)

        spineEndOutput = Locator('spineEnd')
        spineEndOutput.xfo.tr.copy(spine03Ctrl.xfo.tr)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', False)

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
        self.addInput(debugInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        # spliceOp = SpliceOperator("spineSpliceOp", "SpineSolver", "KrakenSpineSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)

        # # Add Xfo Inputs
        # spliceOp.setInput("spine01Ctrl", spine01Ctrl)
        # spliceOp.setInput("spine02Ctrl", spine02Ctrl)
        # spliceOp.setInput("spine03Ctrl", spine03Ctrl)
        # spliceOp.setInput("spine04Ctrl", spine04Ctrl)

        # # Add Xfo Outputs
        # spliceOp.setOutput("spine01Out", spine01Output)
        # spliceOp.setOutput("spine02Out", spine02Output)
        # spliceOp.setOutput("spine03Out", spine03Output)
        # spliceOp.setOutput("spine04Out", spine04Output)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    spine = SpineComponent("mySpine")
    print spine.getNumChildren()