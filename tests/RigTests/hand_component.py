from kraken.core.maths.vec import Vec3
from kraken.core.maths.rotation import Euler
from kraken.core.maths.rotation import Quat
from kraken.core.maths.xfo import Xfo

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


class HandComponent(BaseComponent):
    """Hand Component"""

    def __init__(self, name, parent=None, side='M'):
        super(HandComponent, self).__init__(name, parent, side)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        if side == 'R':
            ctrlColor = "red"
            handPosition = Vec3(-7.1886, 12.2819, 0.4906)
            handUpV = Vec3(-7.7463, 13.1746, 0.4477)
            handEndPosition = Vec3(-7.945, 11.8321, 0.9655)
        else:
            ctrlColor = "greenBright"
            handPosition = Vec3(7.1886, 12.2819, 0.4906)
            handUpV = Vec3(7.7463, 13.1746, 0.4477)
            handEndPosition = Vec3(7.945, 11.8321, 0.9655)

        # Calculate Clavicle Xfo
        rootToEnd = handEndPosition.subtract(handPosition).unit()
        rootToUpV = handUpV.subtract(handPosition).unit()
        bone1ZAxis = rootToEnd.cross(rootToUpV).unit()
        bone1Normal = rootToEnd.cross(bone1ZAxis).unit()
        handXfo = Xfo()

        if side == "R":
            handQuat = Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623)
            handPos = Vec3(-7.1886, 12.2819, 0.4906)
        else:
            handQuat = Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)
            handPos = Vec3(7.1886, 12.2819, 0.4906)

        handXfo.rot = handQuat.clone()
        handXfo.tr.copy(handPos)

        # Add Controls
        handCtrlSrtBuffer = SrtBuffer('hand', parent=self)
        handCtrlSrtBuffer.xfo.copy(handXfo)

        handCtrl = CubeControl('hand', parent=handCtrlSrtBuffer)
        handCtrl.alignOnXAxis()
        handCtrl.scalePoints(Vec3(2.0, 0.75, 1.25))
        handCtrl.xfo.copy(handCtrlSrtBuffer.xfo)
        handCtrl.setColor(ctrlColor)

        # Rig Ref objects
        handRefSrt = Locator('handRef', parent=self)
        handRefSrt.xfo.copy(handCtrlSrtBuffer.xfo)


        # Add Component Params to IK control
        handDebugInputAttr = BoolAttribute('debug', True)
        handLinkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0, 0.0, 1.0)

        handSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings")
        handCtrl.addAttributeGroup(handSettingsAttrGrp)
        handSettingsAttrGrp.addAttribute(handDebugInputAttr)
        handSettingsAttrGrp.addAttribute(handLinkToWorldInputAttr)


        # ==========
        # Deformers
        # ==========
        container = self.getParent().getParent()
        deformersLayer = container.getChildByName('deformers')

        handDef = Joint('hand')
        handDef.setComponent(self)

        deformersLayer.addChild(handDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        armEndXfoInput = Locator('armEndXfo')
        armEndXfoInput.xfo.copy(handCtrlSrtBuffer.xfo)
        armEndPosInput = Locator('armEndPos')
        armEndPosInput.xfo.copy(handCtrlSrtBuffer.xfo)

        handEndOutput = Locator('handEnd')
        handEndOutput.xfo.copy(handCtrlSrtBuffer.xfo)
        handOutput = Locator('hand')
        handOutput.xfo.copy(handCtrlSrtBuffer.xfo)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', side is 'R')
        linkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0, 0.0, 1.0)

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


        # # Add Deformer Splice Op
        # spliceOp = SpliceOperator("handDeformerSpliceOp", "PoseConstraintSolver", "KrakenPoseConstraintSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # # Add Xfo Inputs)
        # spliceOp.setInput("constrainer", handOutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("constrainee", handDef)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    handLeft = HandComponent("myHand", side='L')
    print handLeft.getNumChildren()