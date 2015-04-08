from kraken.core.maths import Vec3

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.layer import Layer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator


from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler

class SpineComponent(BaseComponent):
    """Spine Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')
        
        Profiler.getInstance().push("Construct Spine Component:" + name + " location:" + location)
        super(SpineComponent, self).__init__(name, parent, location)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        cogPosition = data['cogPosition']
        spine01Position = data['spine01Position']
        spine02Position = data['spine02Position']
        spine03Position = data['spine03Position']
        spine04Position = data['spine04Position']
        numDeformers = data['numDeformers']

        # COG
        cogCtrlSrtBuffer = SrtBuffer('cog', parent=self)
        cogCtrlSrtBuffer.xfo.tr = cogPosition

        cogCtrl = Control('cog', parent=cogCtrlSrtBuffer, shape="circle")
        cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        cogCtrl.xfo.tr = cogPosition
        cogCtrl.setColor("orange")

        # Spine01
        spine01CtrlSrtBuffer = SrtBuffer('spine01', parent=cogCtrl)
        spine01CtrlSrtBuffer.xfo.tr = spine01Position

        spine01Ctrl = Control('spine01', parent=spine01CtrlSrtBuffer, shape="circle")
        spine01Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine01Ctrl.xfo.tr = spine01Position

        # Spine02
        spine02CtrlSrtBuffer = SrtBuffer('spine02', parent=spine01Ctrl)
        spine02CtrlSrtBuffer.xfo.tr = spine02Position

        spine02Ctrl = Control('spine02', parent=spine02CtrlSrtBuffer, shape="circle")
        spine02Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        spine02Ctrl.xfo.tr = spine02Position


        # Spine03
        spine03CtrlSrtBuffer = SrtBuffer('spine03', parent=spine02Ctrl)
        spine03CtrlSrtBuffer.xfo.tr = spine03Position

        spine03Ctrl = Control('spine03', parent=spine03CtrlSrtBuffer, shape="circle")
        spine03Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        spine03Ctrl.xfo.tr = spine03Position
        spine03Ctrl.setColor("blue")

        # Spine04
        spine04CtrlSrtBuffer = SrtBuffer('spine04', parent=cogCtrl)
        spine04CtrlSrtBuffer.xfo.tr = spine04Position

        spine04Ctrl = Control('spine04', parent=spine04CtrlSrtBuffer, shape="circle")
        spine04Ctrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        spine04Ctrl.xfo.tr = spine04Position

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

        length = spine01Position.distanceTo(spine02Position) + spine02Position.distanceTo(spine03Position) + spine03Position.distanceTo(spine04Position)
        lengthInputAttr = FloatAttribute('length', length)

        # ==========
        # Deformers
        # ==========

        deformersLayer = self.getLayer('deformers')
        deformerJoints = []
        for i in range(numDeformers):
            if i < 10:
                name = 'spine0'+str(i+1)
            else:
                name = 'spine'+str(i+1)
            spineDef = Joint(name)
            spineDef.setComponent(self)
            deformersLayer.addChild(spineDef)
            deformerJoints.append(spineDef)


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
        self.addInput(lengthInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        bezierSpineSpliceOp = SpliceOperator("spineSpliceOp", "BezierSpineSolver", "Kraken")
        self.addOperator(bezierSpineSpliceOp)

        # Add Att Inputs
        bezierSpineSpliceOp.setInput("debug", debugInputAttr)
        bezierSpineSpliceOp.setInput("length", lengthInputAttr)

        # Add Xfo Inputs
        bezierSpineSpliceOp.setInput("base", spine01Ctrl)
        bezierSpineSpliceOp.setInput("baseHandle", spine02Ctrl)
        bezierSpineSpliceOp.setInput("tipHandle", spine03Ctrl)
        bezierSpineSpliceOp.setInput("tip", spine04Ctrl)

        # Add Xfo Outputs
        bezierSpineSpliceOp.setOutput("outputs", spine01Output)
        bezierSpineSpliceOp.setOutput("outputs", spine02Output)
        bezierSpineSpliceOp.setOutput("outputs", spine03Output)
        bezierSpineSpliceOp.setOutput("outputs", spine04Output)


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
        for joint in deformerJoints:
            outputsToDeformersSpliceOp.setOutput("constrainees", joint)

        Profiler.getInstance().pop()


    def buildRig(self, parent):
        pass

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(SpineComponent)
