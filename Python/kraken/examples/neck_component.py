from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.control  import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler


class NeckComponent(Component):
    """Neck Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Neck Component:" + name + " location:" + location)
        super(NeckComponent, self).__init__(name, parent, location)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Input data values
        neckPosition = data['neckPosition']
        neckUpV = neckPosition.add(data['neckUpVOffset']).unit()
        neckEndPosition = data['neckEndPosition']

        # Calculate Clavicle Xfo
        rootToEnd = neckEndPosition.subtract(neckPosition).unit()
        rootToUpV = neckUpV.subtract(neckPosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()
        neckXfo = Xfo()
        neckXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, neckPosition)

        # Add Guide Controls
        neckCtrlSrtBuffer = SrtBuffer('neck', parent=self)
        neckCtrlSrtBuffer.xfo = neckXfo

        neckCtrl = Control('neck', parent=neckCtrlSrtBuffer, shape="pin")
        neckCtrl.scalePoints(Vec3(1.25, 1.25, 1.25))
        neckCtrl.translatePoints(Vec3(0, 0, -0.5))
        neckCtrl.rotatePoints(90, 0, 90)
        neckCtrl.xfo = neckXfo
        neckCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========

        neckDef = Joint('neck')
        neckDef.setComponent(self)

        deformersLayer = self.getLayer('deformers')
        deformersLayer.addChild(neckDef)

        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        neckEndInput = Locator('neckBase')
        neckEndInput.xfo = neckXfo
        neckEndOutput = Locator('neckEnd')
        neckEndOutput.xfo = neckXfo
        neckOutput = Locator('neck')
        neckOutput.xfo = neckXfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([neckCtrl.getName(), 'To', neckEndInput.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(neckEndInput)
        neckCtrlSrtBuffer.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        neckEndConstraint = PoseConstraint('_'.join([neckEndOutput.getName(), 'To', neckCtrl.getName()]))
        neckEndConstraint.addConstrainer(neckCtrl)
        neckEndOutput.addConstraint(neckEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(neckEndInput)
        self.addOutput(neckEndOutput)
        self.addOutput(neckOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        #Add Deformer Splice Op
        spliceOp = SpliceOperator("neckDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputstrl)
        spliceOp.setInput("constrainer", neckEndOutput)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", neckDef)

        Profiler.getInstance().pop()

    def buildRig(self, parent):
        pass

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(NeckComponent)


