from kraken.core.maths import Vec3, Vec3, Euler, Quat, Xfo

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control  import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class FootComponentGuide(Component):
    """Foot Component Guide"""

    def __init__(self, name='Foot', parent=None):
        super(FootComponentGuide, self).__init__(name, parent)

        self.foot = Control('foot', parent=self, shape="sphere")

        self.loadData({
            "name": name,
            "location": "L",
            "footXfo": Xfo(tr=Vec3(1.841, 1.1516, -1.237), ori=Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190))
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
            'name': self.getName(),
            'location': self.getLocation(),
            'footXfo': self.foot.xfo
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
        self.foot.xfo = data['footXfo']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        # values
        footXfo = self.foot.xfo

        return {
                "class":"kraken.examples.foot_component.FootComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "footXfo": footXfo
                }


class FootComponent(Component):
    """Foot Component"""

    def __init__(self, name='Foot', parent=None):

        Profiler.getInstance().push("Construct Foot Component:" + name)
        super(FootComponent, self).__init__(name, parent)

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

        # Foot
        self.footCtrlSpace = CtrlSpace('foot', parent=ctrlCmpGrp)

        self.footCtrl = Control('foot', parent=self.footCtrlSpace, shape="cube")
        self.footCtrl.alignOnXAxis()
        self.footCtrl.scalePoints(Vec3(2.5, 1.5, 0.75))

        # Rig Ref objects
        self.footRefSrt = Locator('footRef', parent=ctrlCmpGrp)


        # Add Component Params to IK control
        footDebugInputAttr = BoolAttribute('debug', True)
        footLinkToWorldInputAttr = FloatAttribute('linkToWorld', 1.0, maxValue=1.0)

        footSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings")
        self.footCtrl.addAttributeGroup(footSettingsAttrGrp)
        footSettingsAttrGrp.addAttribute(footDebugInputAttr)
        footSettingsAttrGrp.addAttribute(footLinkToWorldInputAttr)


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), parent=deformersLayer)

        footDef = Joint('foot', parent=defCmpGrp)
        footDef.setComponent(self)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        self.legEndXfoInput = Locator('legEndXfo', parent=inputHrcGrp)
        self.legEndPosInput = Locator('legEndPos', parent=inputHrcGrp)

        self.footEndOutput = Locator('handEnd', parent=outputHrcGrp)
        self.footOutput = Locator('hand', parent=outputHrcGrp)


        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', self.getLocation() is 'R')
        linkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0, maxValue=1.0)

        # Connect attrs to control attrs
        debugInputAttr.connect(footDebugInputAttr)
        linkToWorldInputAttr.connect(footLinkToWorldInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        handConstraint = PoseConstraint('_'.join([self.footOutput.getName(), 'To', self.footCtrl.getName()]))
        handConstraint.addConstrainer(self.footCtrl)
        self.footOutput.addConstraint(handConstraint)

        handEndConstraint = PoseConstraint('_'.join([self.footEndOutput.getName(), 'To', self.footCtrl.getName()]))
        handEndConstraint.addConstrainer(self.footCtrl)
        self.footEndOutput.addConstraint(handEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(self.legEndXfoInput)
        self.addInput(self.legEndPosInput)
        self.addOutput(self.footOutput)
        self.addOutput(self.footEndOutput)

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
        spliceOp.setInput("constrainer", self.footOutput)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", footDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'Arm'))
        location = data.get('location', 'M')

        self.footCtrlSpace.xfo = data['footXfo']
        self.footCtrl.xfo = data['footXfo']
        self.footRefSrt.xfo = data['footXfo']

        # ============
        # Set IO Xfos
        # ============
        self.legEndXfoInput.xfo = data['footXfo']
        self.legEndPosInput.xfo = data['footXfo']
        self.footEndOutput.xfo = data['footXfo']
        self.footOutput.xfo = data['footXfo']


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(FootComponent)
