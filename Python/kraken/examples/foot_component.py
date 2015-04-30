from kraken.core.maths import Vec3, Vec3, Euler, Quat, Xfo

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control  import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler


class FootComponent(Component):
    """Foot Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Foot Component:" + name + " location:" + location)
        super(FootComponent, self).__init__(name, parent, location)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Input values
        footQuat = data['footQuat']
        footPos = data['footPos']

        footXfo = Xfo()
        footXfo.ori = footQuat
        footXfo.tr = footPos

        # Add Controls
        footCtrlSpace = CtrlSpace('foot', parent=self)
        footCtrlSpace.xfo = footXfo

        footCtrl = Control('foot', parent=footCtrlSpace, shape="cube")
        footCtrl.alignOnXAxis()
        footCtrl.scalePoints(Vec3(2.5, 1.5, 0.75))
        footCtrl.xfo = footCtrlSpace.xfo

        # Rig Ref objects
        footRefSrt = Locator('footRef', parent=self)
        footRefSrt.xfo = footCtrlSpace.xfo

        # Add Component Params to IK control
        footDebugInputAttr = BoolAttribute('debug', True)
        footLinkToWorldInputAttr = FloatAttribute('linkToWorld', 1.0)
        footLinkToWorldInputAttr.setMax(1.0)

        footSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings")
        footCtrl.addAttributeGroup(footSettingsAttrGrp)
        footSettingsAttrGrp.addAttribute(footDebugInputAttr)
        footSettingsAttrGrp.addAttribute(footLinkToWorldInputAttr)


        # ==========
        # Deformers
        # ==========

        footDef = Joint('foot')
        footDef.setComponent(self)

        deformersLayer = self.getLayer('deformers')
        deformersLayer.addChild(footDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        legEndXfoInput = Locator('legEndXfo')
        legEndXfoInput.xfo = footCtrlSpace.xfo
        legEndPosInput = Locator('legEndPos')
        legEndPosInput.xfo = footCtrlSpace.xfo

        footEndOutput = Locator('handEnd')
        footEndOutput.xfo = footCtrlSpace.xfo
        footOutput = Locator('hand')
        footOutput.xfo = footCtrlSpace.xfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')
        linkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0)
        linkToWorldInputAttr.setMax(1.0)

        # Connect attrs to control attrs
        debugInputAttr.connect(footDebugInputAttr)
        linkToWorldInputAttr.connect(footLinkToWorldInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        handConstraint = PoseConstraint('_'.join([footOutput.getName(), 'To', footCtrl.getName()]))
        handConstraint.addConstrainer(footCtrl)
        footOutput.addConstraint(handConstraint)

        handEndConstraint = PoseConstraint('_'.join([footEndOutput.getName(), 'To', footCtrl.getName()]))
        handEndConstraint.addConstrainer(footCtrl)
        footEndOutput.addConstraint(handEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(legEndXfoInput)
        self.addInput(legEndPosInput)
        self.addOutput(footOutput)
        self.addOutput(footEndOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)
        self.addInput(linkToWorldInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Hand Solver Splice Op
        # spliceOp = SpliceOperator("footSolverSpliceOp", "HandSolver", "KrakenHandSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)
        # spliceOp.setInput("linkToWorld", linkToWorldInputAttr)

        # # Add Xfo Inputs)
        # spliceOp.setInput("armEndXfo", legEndXfoInput)
        # spliceOp.setInput("armEndPos", legEndPosInput)
        # spliceOp.setInput("handRef", footRefSrt)

        # # Add Xfo Outputs
        # spliceOp.setOutput("handCtrlSpace", footCtrlSpace)


        # Add Deformer Splice Op
        spliceOp = SpliceOperator("footDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputs)
        spliceOp.setInput("constrainer", footOutput)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", footDef)

        Profiler.getInstance().pop()

    def buildRig(self, parent):
        pass

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(FootComponent)
