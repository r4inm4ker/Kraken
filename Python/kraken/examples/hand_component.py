from kraken.core.maths import Vec3, Vec3, Euler, Quat, Xfo

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler

class HandComponent(Component):
    """Hand Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Hand Component:" + name + " location:" + location)
        super(HandComponent, self).__init__(name, parent, location)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        handQuat = data['handQuat']
        handPos = data['handPos']

        # Calculate Clavicle Xfo
        handXfo = Xfo()
        handXfo.ori = handQuat
        handXfo.tr = handPos

        # Add Controls
        handCtrlSrtBuffer = SrtBuffer('hand', parent=self)
        handCtrlSrtBuffer.xfo = handXfo

        handCtrl = Control('hand', parent=handCtrlSrtBuffer, shape="cube")
        handCtrl.alignOnXAxis()
        handCtrl.scalePoints(Vec3(2.0, 0.75, 1.25))
        handCtrl.xfo = handCtrlSrtBuffer.xfo

        # Rig Ref objects
        handRefSrt = Locator('handRef', parent=self)
        handRefSrt.xfo = handCtrlSrtBuffer.xfo


        # Add Component Params to IK control
        handDebugInputAttr = BoolAttribute('debug', True)
        handLinkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0)

        handSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings")
        handCtrl.addAttributeGroup(handSettingsAttrGrp)
        handSettingsAttrGrp.addAttribute(handDebugInputAttr)
        handSettingsAttrGrp.addAttribute(handLinkToWorldInputAttr)


        # ==========
        # Deformers
        # ==========
        handDef = Joint('hand')
        handDef.setComponent(self)

        deformersLayer = self.getLayer('deformers')
        deformersLayer.addChild(handDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        armEndXfoInput = Locator('armEndXfo')
        armEndXfoInput.xfo = handCtrlSrtBuffer.xfo
        armEndPosInput = Locator('armEndPos')
        armEndPosInput.xfo = handCtrlSrtBuffer.xfo

        handEndOutput = Locator('handEnd')
        handEndOutput.xfo = handCtrlSrtBuffer.xfo
        handOutput = Locator('hand')
        handOutput.xfo = handCtrlSrtBuffer.xfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')
        linkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0)

        # Connect attrs to control attrs
        debugInputAttr.connect(handDebugInputAttr)
        linkToWorldInputAttr.connect(handLinkToWorldInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        handConstraint = PoseConstraint('_'.join([handOutput.getName(), 'To', handCtrl.getName()]))
        handConstraint.addConstrainer(handCtrl)
        handOutput.addConstraint(handConstraint)

        handEndConstraint = PoseConstraint('_'.join([handEndOutput.getName(), 'To', handCtrl.getName()]))
        handEndConstraint.addConstrainer(handCtrl)
        handEndOutput.addConstraint(handEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(armEndXfoInput)
        self.addInput(armEndPosInput)
        self.addOutput(handOutput)
        self.addOutput(handEndOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)
        self.addInput(linkToWorldInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Hand Solver Splice Op
        # spliceOp = SpliceOperator("handSolverSpliceOp", "HandSolver", "KrakenHandSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)
        # spliceOp.setInput("linkToWorld", linkToWorldInputAttr)

        # # Add Xfo Inputs)
        # spliceOp.setInput("armEndXfo", armEndXfoInput)
        # spliceOp.setInput("armEndPos", armEndPosInput)
        # spliceOp.setInput("handRef", handRefSrt)

        # # Add Xfo Outputs
        # spliceOp.setOutput("handCtrlSrtBuffer", handCtrlSrtBuffer)


        # Add Deformer Splice Op
        spliceOp = SpliceOperator("handDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputs)
        spliceOp.setInput("constrainer", handOutput)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", handDef)

        Profiler.getInstance().pop()

    def buildRig(self, parent):
        pass


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(HandComponent)

