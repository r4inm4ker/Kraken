from kraken.core.maths.vec import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_component import BaseComponent
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

        handXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, handPosition)

        # Add Controls
        handCtrlSrtBuffer = SrtBuffer('hand', parent=self)
        handCtrlSrtBuffer.xfo.copy(handXfo)

        handCtrl = CubeControl('hand', parent=handCtrlSrtBuffer)
        handCtrl.alignOnXAxis()
        # handLen = handPosition.subtract(handEndPosition).length()
        handCtrl.scalePoints(Vec3(2.0, 0.75, 1.25))
        handCtrl.xfo.copy(handXfo)
        handCtrl.setColor(ctrlColor)


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
        armEndInput = Locator('armEnd')
        armEndInput.xfo.copy(handXfo)

        handEndOutput = Locator('handEnd')
        handEndOutput.xfo.copy(handXfo)
        handOutput = Locator('hand')
        handOutput.xfo.copy(handXfo)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', side is 'R')


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        handInputConstraint = PoseConstraint('_'.join([handCtrl.getName(), 'To', armEndInput.getName()]))
        handInputConstraint.setMaintainOffset(True)
        handInputConstraint.addConstrainer(armEndInput)
        handCtrlSrtBuffer.addConstraint(handInputConstraint)

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
        self.addInput(armEndInput)
        self.addOutput(handEndOutput)
        self.addOutput(handOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # # Add Deformer Splice Op
        # spliceOp = SpliceOperator("handDeformerSpliceOp", "PoseConstraintSolver", "KrakenPoseConstraintSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # # Add Xfo Inputstrl)
        # spliceOp.setInput("constrainer", handOutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("constrainee", handDef)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    handLeft = HandComponent("myHand", side='L')
    print handLeft.getNumChildren()