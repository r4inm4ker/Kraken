from kraken.core.maths import Vec3

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.layer import Layer
from kraken.core.objects.controls.circle_control  import  CircleControl

from kraken.core.objects.operators.splice_operator import SpliceOperator


from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler

class SpineComponent(BaseComponent):
    """Spine Component"""

    def __init__(self, name, parent=None, location='M'):
        Profiler.getInstance().push("Construct Spine Component:" + name + " location:" + location)
        super(SpineComponent, self).__init__(name, parent, location)

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
        cogCtrlSrtBuffer = SrtBuffer('cog', parent=self)
        cogCtrlSrtBuffer.xfo.tr = cogPosition

        cogCtrl = CircleControl('cog', parent=cogCtrlSrtBuffer)
        cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        cogCtrl.xfo.tr = cogPosition
        cogCtrl.setColor("orange")

        # Spine01
        spine01CtrlSrtBuffer = SrtBuffer('spine01', parent=cogCtrl)
        spine01CtrlSrtBuffer.xfo.tr = spine01Position

        spine01Ctrl = CircleControl('spine01', parent=spine01CtrlSrtBuffer)
        spine01Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine01Ctrl.xfo.tr = spine01Position

        # Spine02
        spine02CtrlSrtBuffer = SrtBuffer('spine02', parent=spine01Ctrl)
        spine02CtrlSrtBuffer.xfo.tr = spine02Position

        spine02Ctrl = CircleControl('spine02', parent=spine02CtrlSrtBuffer)
        spine02Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        spine02Ctrl.xfo.tr = spine02Position
        spine02Ctrl.setColor("blue")

        # Spine03
        spine03CtrlSrtBuffer = SrtBuffer('spine03', parent=spine02Ctrl)
        spine03CtrlSrtBuffer.xfo.tr = spine03Position

        spine03Ctrl = CircleControl('spine03', parent=spine03CtrlSrtBuffer)
        spine03Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        spine03Ctrl.xfo.tr = spine03Position
        spine03Ctrl.setColor("blue")

        # Spine04
        spine04CtrlSrtBuffer = SrtBuffer('spine04', parent=cogCtrl)
        spine04CtrlSrtBuffer.xfo.tr = spine04Position

        spine04Ctrl = CircleControl('spine04', parent=spine04CtrlSrtBuffer)
        spine04Ctrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        spine04Ctrl.xfo.tr = spine04Position

        # ==========
        # Deformers
        # ==========

        spine01Def = Joint('spine01')
        spine01Def.setComponent(self)

        spine02Def = Joint('spine02')
        spine02Def.setComponent(self)

        spine03Def = Joint('spine03')
        spine03Def.setComponent(self)

        spine04Def = Joint('spine04')
        spine04Def.setComponent(self)

        container = self.getContainer()
        if container is not None:
            deformersLayer = container.getChildByName('deformers')
        else:
            # When building the spine in a testing scene, generate a 'deformers' layer.
            deformersLayer = Layer('deformers', parent=self)

        deformersLayer.addChild(spine01Def)
        deformersLayer.addChild(spine02Def)
        deformersLayer.addChild(spine03Def)
        deformersLayer.addChild(spine04Def)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        spine01Output = Locator('spine01')
        spine01Output.xfo.tr = spine01Ctrl.xfo.tr
        spine02Output = Locator('spine02')
        spine02Output.xfo.tr = spine01Ctrl.xfo.tr
        spine03Output = Locator('spine03')
        spine03Output.xfo.tr = spine01Ctrl.xfo.tr
        spine04Output = Locator('spine04')
        spine04Output.xfo.tr = spine01Ctrl.xfo.tr

        spineBaseOutput = Locator('spineBase')
        spineBaseOutput.xfo.tr = spine01Ctrl.xfo.tr

        spineEndOutput = Locator('spineEnd')
        spineEndOutput.xfo.tr = spine03Ctrl.xfo.tr

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        spineBaseOutputConstraint = PoseConstraint('_'.join([spineBaseOutput.getName(), 'To', 'spineBase']))
        spineBaseOutputConstraint.addConstrainer(spine01Ctrl)
        spineBaseOutput.addConstraint(spineBaseOutputConstraint)

        spineEndOutputConstraint = PoseConstraint('_'.join([spineEndOutput.getName(), 'To', 'spineEnd']))
        spineEndOutputConstraint.addConstrainer(spine04Ctrl)
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


        # Add Deformer Splice Op
        outputsToDeformersSpliceOp = SpliceOperator("spineDeformerSpliceOp", "MultiPoseConstraintSolver", "Kraken")
        self.addOperator(outputsToDeformersSpliceOp)

        # Add Att Inputs
        outputsToDeformersSpliceOp.setInput("debug", debugInputAttr)

        # Add Xfo Inputstrl)
        outputsToDeformersSpliceOp.setInput("constrainers", spine01Output)
        outputsToDeformersSpliceOp.setInput("constrainers", spine02Output)
        outputsToDeformersSpliceOp.setInput("constrainers", spine03Output)
        outputsToDeformersSpliceOp.setInput("constrainers", spine04Output)

        # Add Xfo Outputs
        outputsToDeformersSpliceOp.setOutput("constraineess", spine01Def)
        outputsToDeformersSpliceOp.setOutput("constraineess", spine02Def)
        outputsToDeformersSpliceOp.setOutput("constraineess", spine03Def)
        outputsToDeformersSpliceOp.setOutput("constraineess", spine04Def)

        Profiler.getInstance().pop()


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    spine = SpineComponent("mySpine")
    logHierarchy(spine)