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


class FootComponent(Component):
    """Foot Component Base"""

    def __init__(self, name='Foot', parent=None, data=None):
        super(FootComponent, self).__init__(name, parent)

        # ================
        # Setup Hierarchy
        # ================
        self.controlsLayer = self.getOrCreateLayer('controls')
        self.ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=self.controlsLayer)

        # IO Hierarchies
        self.inputHrcGrp = HierarchyGroup('inputs', parent=self.ctrlCmpGrp)
        self.cmpInputAttrGrp = AttributeGroup('inputs', parent=self.inputHrcGrp)

        self.outputHrcGrp = HierarchyGroup('outputs', parent=self.ctrlCmpGrp)
        self.cmpOutputAttrGrp = AttributeGroup('outputs', parent=self.outputHrcGrp)


        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.legEndXfoInputTgt = self.createInput('legEndXfo', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.footEndOutputTgt = self.createOutput('footEnd', dataType='Xfo', parent=self.outputHrcGrp)
        self.footOutputTgt = self.createOutput('foot', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', parent=self.cmpInputAttrGrp)
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class FootComponentGuide(FootComponent):
    """Foot Component Guide"""

    def __init__(self, name='Foot', parent=None, data=None):

        Profiler.getInstance().push("Construct Foot Rig Component:" + name)
        super(FootComponentGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Guide Controls
        self.footCtrl = Control('foot', parent=self.ctrlCmpGrp, shape="sphere")

        if data is None:
            data = {
                    "name": name,
                    "location": "L",
                    "footXfo": Xfo(tr=Vec3(1.841, 1.1516, -1.237), ori=Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190))
                   }

        self.loadData(data)

        Profiler.getInstance().pop()


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
            'footXfo': self.footCtrl.xfo
            }

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        if 'name' in data:
            self.setName(data['name'])

        self.setLocation(data['location'])
        self.footCtrl.xfo = data['footXfo']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        # values
        footXfo = self.footCtrl.xfo

        data = {
                "class":"kraken.examples.foot_component.FootComponentRig",
                "name": self.getName(),
                "location": self.getLocation(),
                "footXfo": footXfo
               }

        return data


    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):
        """Enables introspection of the class prior to construction to determine if it is a guide component.

        Return:
        The true if this component is a guide component.

        """

        return 'Guide'

class FootComponentRig(FootComponent):
    """Foot Component"""

    def __init__(self, name='foot', parent=None):

        Profiler.getInstance().push("Construct Foot Rig Component:" + name)
        super(FootComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Foot
        self.footCtrlSpace = CtrlSpace('foot', parent=self.ctrlCmpGrp)

        self.footCtrl = Control('foot', parent=self.footCtrlSpace, shape="cube")
        self.footCtrl.alignOnXAxis()
        self.footCtrl.scalePoints(Vec3(2.5, 1.5, 0.75))

        # Rig Ref objects
        self.footRefSrt = Locator('footRef', parent=self.ctrlCmpGrp)

        # Add Component Params to IK control
        footSettingsAttrGrp = AttributeGroup("DisplayInfo_FootSettings", parent=self.footCtrl)
        footLinkToWorldInputAttr = FloatAttribute('linkToWorld', 1.0, maxValue=1.0, parent=footSettingsAttrGrp)


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        footDef = Joint('foot', parent=defCmpGrp)
        footDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        handConstraint = PoseConstraint('_'.join([self.footOutputTgt.getName(), 'To', self.footCtrl.getName()]))
        handConstraint.addConstrainer(self.footCtrl)
        self.footOutputTgt.addConstraint(handConstraint)

        handEndConstraint = PoseConstraint('_'.join([self.footEndOutputTgt.getName(), 'To', self.footCtrl.getName()]))
        handEndConstraint.addConstrainer(self.footCtrl)
        self.footEndOutputTgt.addConstraint(handEndConstraint)



        # ===============
        # Add Splice Ops
        # ===============
        # Add Hand Solver Splice Op
        # spliceOp = SpliceOperator('footSolverSpliceOp', 'HandSolver', 'KrakenHandSolver')
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        # spliceOp.setInput('rightSide', self.rightSideInputAttr)
        # spliceOp.setInput('linkToWorld', footLinkToWorldInputAttr)

        # # Add Xfo Inputs)
        # spliceOp.setInput('armEndXfo', legEndXfoInput)
        # spliceOp.setInput('handRef', footRefSrt)

        # # Add Xfo Outputs
        # spliceOp.setOutput('handCtrlSpace', footCtrlSpace)


        # Add Deformer Splice Op
        spliceOp = SpliceOperator('footDeformerSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        spliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs)
        spliceOp.setInput('constrainer', self.footOutputTgt)

        # Add Xfo Outputs
        spliceOp.setOutput('constrainee', footDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'foot'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.footCtrlSpace.xfo = data['footXfo']
        self.footCtrl.xfo = data['footXfo']
        self.footRefSrt.xfo = data['footXfo']

        # ============
        # Set IO Xfos
        # ============
        self.legEndXfoInputTgt.xfo = data['footXfo']
        self.footEndOutputTgt.xfo = data['footXfo']
        self.footOutputTgt.xfo = data['footXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FootComponentGuide)
ks.registerComponent(FootComponentRig)
