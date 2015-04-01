from kraken.core.maths import Vec3
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

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler

class ClavicleComponent(BaseComponent):
    """Clavicle Component"""

    def __init__(self, name, parent=None, data={}):
        
        location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Clavicle Component:" + name + " location:" + location)
        super(ClavicleComponent, self).__init__(name, parent, location)

        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Input values
        claviclePosition = data['claviclePosition']
        clavicleUpV = claviclePosition.add(data['clavicleUpVOffset']).unit()
        clavicleEndPosition = data['clavicleEndPosition']

        # Calculate Clavicle Xfo
        rootToEnd = clavicleEndPosition.subtract(claviclePosition).unit()
        rootToUpV = clavicleUpV.subtract(claviclePosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()
        clavicleXfo = Xfo()

        clavicleXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, claviclePosition)

        # Add Controls
        clavicleCtrlSrtBuffer = SrtBuffer('clavicle', parent=self)
        clavicleCtrlSrtBuffer.xfo = clavicleXfo

        clavicleCtrl = CubeControl('clavicle', parent=clavicleCtrlSrtBuffer)
        clavicleCtrl.alignOnXAxis()
        clavicleLen = claviclePosition.subtract(clavicleEndPosition).length()
        clavicleCtrl.scalePoints(Vec3(clavicleLen, 0.75, 0.75))

        if location == "R":
            clavicleCtrl.translatePoints(Vec3(0.0, 0.0, -1.0))
        else:
            clavicleCtrl.translatePoints(Vec3(0.0, 0.0, 1.0))

        clavicleCtrl.xfo = clavicleXfo


        # ==========
        # Deformers
        # ==========
        clavicleDef = Joint('clavicle')
        clavicleDef.setComponent(self)

        deformersLayer = self.getLayer('deformers')
        deformersLayer.addChild(clavicleDef)

        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        spineEndInput = Locator('spineEnd')
        spineEndInput.xfo = clavicleXfo

        clavicleEndOutput = Locator('clavicleEnd')
        clavicleEndOutput.xfo = clavicleXfo
        clavicleOutput = Locator('clavicle')
        clavicleOutput.xfo = clavicleXfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')
        armFollowBodyOutputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([clavicleCtrl.getName(), 'To', spineEndInput.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(spineEndInput)
        clavicleCtrlSrtBuffer.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        clavicleConstraint = PoseConstraint('_'.join([clavicleOutput.getName(), 'To', clavicleCtrl.getName()]))
        clavicleConstraint.addConstrainer(clavicleCtrl)
        clavicleOutput.addConstraint(clavicleConstraint)

        clavicleEndConstraint = PoseConstraint('_'.join([clavicleEndOutput.getName(), 'To', clavicleCtrl.getName()]))
        clavicleEndConstraint.addConstrainer(clavicleCtrl)
        clavicleEndOutput.addConstraint(clavicleEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(spineEndInput)
        self.addOutput(clavicleEndOutput)
        self.addOutput(clavicleOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)
        self.addOutput(armFollowBodyOutputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        spliceOp = SpliceOperator("clavicleDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("constrainer", clavicleOutput)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", clavicleDef)

        Profiler.getInstance().pop()

    def buildRig(self, parent):
        pass


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(ClavicleComponent)

