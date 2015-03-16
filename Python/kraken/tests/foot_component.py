from kraken.core.maths import Vec3, Vec3, Euler, Quat, Xfo

from kraken.core.objects.components.base_component import BaseComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.cube_control  import CubeControl

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler

class FootComponent(BaseComponent):
    """Foot Component"""

    def __init__(self, name, parent=None, location='M'):
        Profiler.getInstance().push("Construct Foot Component:" + name + " location:" + location)
        super(FootComponent, self).__init__(name, parent, location)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        if location == 'R':
            footPosition = Vec3(-7.1886, 12.2819, 0.4906)
            footUpV = Vec3(-1.7454, 0.1922, -1.7397)
            footEndPosition = Vec3(-2.0939, 0.4288, 0.0944)
        else:
            footPosition = Vec3(7.1886, 12.2819, 0.4906)
            footUpV = Vec3(1.7454, 0.1922, -1.7397)
            footEndPosition = Vec3(2.0939, 0.4288, 0.0944)

        # Calculate Clavicle Xfo
        rootToEnd = footEndPosition.subtract(footPosition).unit()
        rootToUpV = footUpV.subtract(footPosition).unit()
        bone1ZAxis = rootToEnd.cross(rootToUpV).unit()
        bone1Normal = rootToEnd.cross(bone1ZAxis).unit()
        footXfo = Xfo()

        if location == "R":
            footQuat = Quat(Vec3(0.5695, -0.6377, 0.4190), 0.3053)
            footPos = Vec3(-1.841, 1.1516, -1.237)
        else:
            footQuat = Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190)
            footPos = Vec3(1.841, 1.1516, -1.237)

        footXfo.ori = footQuat
        footXfo.tr = footPos

        # Add Controls
        footCtrlSrtBuffer = SrtBuffer('foot', parent=self)
        footCtrlSrtBuffer.xfo = footXfo

        footCtrl = CubeControl('foot', parent=footCtrlSrtBuffer)
        footCtrl.alignOnXAxis()
        footCtrl.scalePoints(Vec3(2.5, 1.5, 0.75))
        footCtrl.xfo = footCtrlSrtBuffer.xfo

        # Rig Ref objects
        footRefSrt = Locator('footRef', parent=self)
        footRefSrt.xfo = footCtrlSrtBuffer.xfo


        # Add Component Params to IK control
        footDebugInputAttr = BoolAttribute('debug', True)
        footLinkToWorldInputAttr = FloatAttribute('linkToWorld', 1.0, 0.0, 1.0)

        footSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings")
        footCtrl.addAttributeGroup(footSettingsAttrGrp)
        footSettingsAttrGrp.addAttribute(footDebugInputAttr)
        footSettingsAttrGrp.addAttribute(footLinkToWorldInputAttr)


        # ==========
        # Deformers
        # ==========

        footDef = Joint('foot')
        footDef.setComponent(self)

        container = self.getContainer()
        if container is not None:
            deformersLayer = container.getChildByName('deformers')
            deformersLayer.addChild(footDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        legEndXfoInput = Locator('legEndXfo')
        legEndXfoInput.xfo = footCtrlSrtBuffer.xfo
        legEndPosInput = Locator('legEndPos')
        legEndPosInput.xfo = footCtrlSrtBuffer.xfo

        footEndOutput = Locator('handEnd')
        footEndOutput.xfo = footCtrlSrtBuffer.xfo
        footOutput = Locator('hand')
        footOutput.xfo = footCtrlSrtBuffer.xfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')
        linkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0, 0.0, 1.0)

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
        # spliceOp.setOutput("handCtrlSrtBuffer", footCtrlSrtBuffer)


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


if __name__ == "__main__":
    handLeft = FootComponent("myFoot", location='L')
    logHierarchy(handLeft)
