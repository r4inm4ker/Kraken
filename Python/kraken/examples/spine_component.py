from kraken.core.maths import Vec3

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.layer import Layer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class SpineComponent(Component):
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
        cogCtrlSpace = CtrlSpace('cog', parent=self)
        cogCtrlSpace.xfo.tr = cogPosition

        cogCtrl = Control('cog', parent=cogCtrlSpace, shape="circle")
        cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        cogCtrl.xfo.tr = cogPosition
        cogCtrl.setColor("orange")

        # Spine01
        spine01CtrlSpace = CtrlSpace('spine01', parent=cogCtrl)
        spine01CtrlSpace.xfo.tr = spine01Position

        spine01Ctrl = Control('spine01', parent=spine01CtrlSpace, shape="circle")
        spine01Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine01Ctrl.xfo.tr = spine01Position

        # Spine02
        spine02CtrlSpace = CtrlSpace('spine02', parent=spine01Ctrl)
        spine02CtrlSpace.xfo.tr = spine02Position

        spine02Ctrl = Control('spine02', parent=spine02CtrlSpace, shape="circle")
        spine02Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        spine02Ctrl.xfo.tr = spine02Position


        # Spine03
        spine03CtrlSpace = CtrlSpace('spine03', parent=spine02Ctrl)
        spine03CtrlSpace.xfo.tr = spine03Position

        spine03Ctrl = Control('spine03', parent=spine03CtrlSpace, shape="circle")
        spine03Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        spine03Ctrl.xfo.tr = spine03Position
        spine03Ctrl.setColor("blue")

        # Spine04
        spine04CtrlSpace = CtrlSpace('spine04', parent=cogCtrl)
        spine04CtrlSpace.xfo.tr = spine04Position

        spine04Ctrl = Control('spine04', parent=spine04CtrlSpace, shape="circle")
        spine04Ctrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        spine04Ctrl.xfo.tr = spine04Position


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

        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's


        spineOutputs = []
        for i in range(numDeformers):
            if i < 10:
                name = 'spine0'+str(i)
            else:
                name = 'spine'+str(i)

            spineOutput = Locator(name)
            spineOutputs.append(spineOutput)

        spineBaseOutput = Locator('spineBase')
        spineEndOutput = Locator('spineEnd')

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)

        length = spine01Position.distanceTo(spine02Position) + spine02Position.distanceTo(spine03Position) + spine03Position.distanceTo(spine04Position)
        lengthInputAttr = FloatAttribute('length', value=length, maxValue=length * 3.0)



        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        spineBaseOutputConstraint = PoseConstraint('_'.join([spineBaseOutput.getName(), 'To', 'spineBase']))
        spineBaseOutputConstraint.addConstrainer(spineOutputs[0])
        spineBaseOutput.addConstraint(spineBaseOutputConstraint)

        spineEndOutputConstraint = PoseConstraint('_'.join([spineEndOutput.getName(), 'To', 'spineEnd']))
        spineEndOutputConstraint.addConstrainer(spineOutputs[len(spineOutputs)-1])
        spineEndOutput.addConstraint(spineEndOutputConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's

        for spineOutput in spineOutputs:
            self.addOutput(spineOutput)
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
        for spineOutput in spineOutputs:
            bezierSpineSpliceOp.setOutput("outputs", spineOutput)

        # evaluate the spine op so that all the output transforms are updated.
        bezierSpineSpliceOp.evaluate()

        # Add Deformer Splice Op
        outputsToDeformersSpliceOp = SpliceOperator("spineDeformerSpliceOp", "MultiPoseConstraintSolver", "Kraken")
        self.addOperator(outputsToDeformersSpliceOp)

        # Add Att Inputs
        outputsToDeformersSpliceOp.setInput("debug", debugInputAttr)

        # Add Xfo Inputstrl)
        for spineOutput in spineOutputs:
            outputsToDeformersSpliceOp.setInput("constrainers", spineOutput)

        # Add Xfo Outputs
        for joint in deformerJoints:
            outputsToDeformersSpliceOp.setOutput("constrainees", joint)

        # evaluate the constraint op so that all the joint transforms are updated.
        outputsToDeformersSpliceOp.evaluate()

        Profiler.getInstance().pop()


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(SpineComponent)
