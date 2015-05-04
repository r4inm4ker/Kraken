from kraken.core.maths import Vec3

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class HeadComponentGuide(Component):
    """Head Component Guide"""

    def __init__(self, name='Head', parent=None):
        super(HeadComponentGuide, self).__init__(name, parent)

        self.head = Control('head', parent=self, shape="cube")
        self.headEnd = Control('headEnd', parent=self, shape="sphere")
        self.eyeLeft = Control('eyeLeft', parent=self, shape="sphere")
        self.eyeRight = Control('eyeRight', parent=self, shape="sphere")
        self.jaw = Control('jaw', parent=self, shape="cube")

        self.loadData({
            "name": name,
            "location": "L",
            "headPosition": Vec3(0.0, 17.4756, -0.421),
            "headEndPosition": Vec3(0.0, 19.5, -0.421),
            "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
            "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
            "jawPosition": Vec3(0.0, 17.613, -0.2731)
        })


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = {
            "name": self.getName(),
            "location": self.getLocation(),
            "headPosition": self.head.xfo.tr,
            "headEndPosition": self.headEnd.xfo.tr,
            "eyeLeftPosition": self.eyeLeft.xfo.tr,
            "eyeRightPosition": self.eyeRight.xfo.tr,
            "jawPosition": self.jaw.xfo.tr
            }

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        self.setName(data['name'])
        self.setLocation(data['location'])
        self.head.xfo.tr = data['headPosition']
        self.headEnd.xfo.tr = data['headEndPosition']
        self.eyeLeft.xfo.tr = data['eyeLeftPosition']
        self.eyeRight.xfo.tr = data['eyeRightPosition']
        self.jaw.xfo.tr = data['jawPosition']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        # values
        self.head
        self.headEnd
        self.eyeLeft
        self.eyeRight
        self.jaw

        return {
                "class":"kraken.examples.head_component.HeadComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "headPosition": self.head.xfo.tr,
                "headEndPosition": self.headEnd.xfo.tr,
                "eyeLeftPosition": self.eyeLeft.xfo.tr,
                "eyeRightPosition": self.eyeRight.xfo.tr,
                "jawPosition": self.jaw.xfo.tr
                }


class HeadComponent(Component):
    """Head Component"""

    def __init__(self, name='Head', parent=None):

        Profiler.getInstance().push("Construct Head Component:" + name)
        super(HeadComponent, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs')
        inputHrcGrp.addAttributeGroup(cmpInputAttrGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs')
        outputHrcGrp.addAttributeGroup(cmpOutputAttrGrp)

        # Head
        headCtrlSpace = CtrlSpace('head', parent=ctrlCmpGrp)

        headCtrl = Control('head', parent=headCtrlSpace, shape="circle")
        headCtrl.rotatePoints(0, 0, 90)
        headCtrl.scalePoints(Vec3(3, 3, 3))
        headCtrl.translatePoints(Vec3(0, 1, 0.25))

        # Eye Left
        eyeLeftCtrlSpace = CtrlSpace('eyeLeft', parent=headCtrl)

        eyeLeftCtrl = Control('eyeLeft', parent=eyeLeftCtrlSpace, shape="sphere")
        eyeLeftCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        eyeLeftCtrl.setColor("blueMedium")

        # Eye Right
        eyeRightCtrlSpace = CtrlSpace('eyeRight', parent=headCtrl)
        eyeRightCtrlSpace.xfo.tr = eyeRightPosition

        eyeRightCtrl = Control('eyeRight', parent=eyeRightCtrlSpace, shape="sphere")
        eyeRightCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        eyeRightCtrl.setColor("blueMedium")

        # Jaw
        jawCtrlSpace = CtrlSpace('jawCtrlSpace', parent=headCtrl)

        jawCtrl = Control('jaw', parent=jawCtrlSpace, shape="cube")
        jawCtrl.alignOnYAxis(negative=True)
        jawCtrl.alignOnZAxis()
        jawCtrl.scalePoints(Vec3(1.45, 0.65, 1.25))
        jawCtrl.translatePoints(Vec3(0, -0.25, 0))
        jawCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), parent=deformersLayer)

        headDef = Joint('head', parent=defCmpGrp)
        headDef.setComponent(self)

        jawDef = Joint('jaw', parent=defCmpGrp)
        jawDef.setComponent(self)

        eyeLeftDef = Joint('eyeLeft', parent=defCmpGrp)
        eyeLeftDef.setComponent(self)

        eyeRightDef = Joint('eyeRight', parent=defCmpGrp)
        eyeRightDef.setComponent(self)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        headBaseInput = Locator('headBase', parent=inputHrcGrp)
        headBaseInput.xfo = headCtrl.xfo

        headOutput = Locator('head', parent=outputHrcGrp)
        headOutput.xfo = headCtrl.xfo
        jawOutput = Locator('jaw', parent=outputHrcGrp)
        jawOutput.xfo = jawCtrl.xfo
        eyeLOutput = Locator('eyeL', parent=outputHrcGrp)
        eyeLOutput.xfo = eyeLeftCtrl.xfo
        eyeROutput = Locator('eyeR', parent=outputHrcGrp)
        eyeROutput.xfo = eyeRightCtrl.xfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        headInputConstraint = PoseConstraint('_'.join([headCtrlSpace.getName(), 'To', headBaseInput.getName()]))
        headInputConstraint.setMaintainOffset(True)
        headInputConstraint.addConstrainer(headBaseInput)
        headCtrlSpace.addConstraint(headInputConstraint)

        # Constraint outputs
        headOutputConstraint = PoseConstraint('_'.join([headOutput.getName(), 'To', headCtrl.getName()]))
        headOutputConstraint.setMaintainOffset(True)
        headOutputConstraint.addConstrainer(headCtrl)
        headOutput.addConstraint(headOutputConstraint)

        jawOutputConstraint = PoseConstraint('_'.join([jawOutput.getName(), 'To', jawCtrl.getName()]))
        jawOutputConstraint.setMaintainOffset(True)
        jawOutputConstraint.addConstrainer(jawCtrl)
        jawOutput.addConstraint(jawOutputConstraint)

        eyeLOutputConstraint = PoseConstraint('_'.join([eyeLOutput.getName(), 'To', eyeLeftCtrl.getName()]))
        eyeLOutputConstraint.setMaintainOffset(True)
        eyeLOutputConstraint.addConstrainer(eyeLeftCtrl)
        eyeLOutput.addConstraint(eyeLOutputConstraint)

        eyeROutputConstraint = PoseConstraint('_'.join([eyeROutput.getName(), 'To', eyeRightCtrl.getName()]))
        eyeROutputConstraint.setMaintainOffset(True)
        eyeROutputConstraint.addConstrainer(eyeRightCtrl)
        eyeROutput.addConstraint(eyeROutputConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(headBaseInput)

        self.addOutput(headOutput)
        self.addOutput(jawOutput)
        self.addOutput(eyeLOutput)
        self.addOutput(eyeROutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        # spliceOp = SpliceOperator("headDeformerSpliceOp", "HeadConstraintSolver", "KrakenHeadConstraintSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # # Add Xfo Inputstrl)
        # spliceOp.setInput("headConstrainer", headOutput)
        # spliceOp.setInput("jawConstrainer", jawOutput)
        # spliceOp.setInput("eyeLeftConstrainer", eyeLOutput)
        # spliceOp.setInput("eyeRightConstrainer", eyeROutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("headDeformer", headDef)
        # spliceOp.setOutput("jawDeformer", jawDef)
        # spliceOp.setOutput("eyeLeftDeformer", eyeLeftDef)
        # spliceOp.setOutput("eyeRightDeformer", eyeRightDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'Head'))
        location = data.get('location', 'M')
        self.setLocation(location)

        headCtrlSpace.xfo.tr = data['headPosition']
        headCtrl.xfo.tr = data['headPosition']
        eyeLeftCtrlSpace.xfo.tr = data['eyeLeftPosition']
        eyeLeftCtrl.xfo.tr = data['eyeLeftPosition']
        eyeRightCtrl.xfo.tr = data['eyeRightPosition']
        jawCtrlSpace.xfo.tr = data['jawPosition']
        jawCtrl.xfo.tr = data['jawPosition']

        # ============
        # Set IO Xfos
        # ============


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(HeadComponent)
