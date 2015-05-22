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
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class HandComponentGuide(Component):
    """Hand Component Guide"""

    def __init__(self, name='handGuide', parent=None, data=None):
        super(HandComponentGuide, self).__init__(name, parent)

        # ================
        # Setup Hierarchy
        # ================
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs', parent=inputHrcGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs', parent=outputHrcGrp)


        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.armEndXfoInputTgt = self.createInput('armEndXfo', dataType='Xfo', parent=inputHrcGrp)
        self.armEndPosInputTgt = self.createInput('armEndPos', dataType='Xfo', parent=inputHrcGrp)

        # Declare Output Xfos
        self.handOutputTgt = self.createOutput('hand', dataType='Xfo', parent=outputHrcGrp)
        self.handEndOutputTgt = self.createOutput('handEnd', dataType='Xfo', parent=outputHrcGrp)

        # Declare Input Attrs
        self.debugInputAttr = self.createInput('debug', dataType='Boolean', parent=cmpInputAttrGrp)
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=cmpInputAttrGrp)

        # Declare Output Attrs

        # =========
        # Controls
        # =========
        # Guide Controls
        self.handCtrl = Control('hand', parent=ctrlCmpGrp, shape="cube")

        if data is None:
            data = {
                    "location": "L",
                    "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906),
                                   ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623))
                   }

        self.loadData(data)


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
            "handXfo": self.handCtrl.xfo
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
        self.handCtrl.xfo = data['handXfo']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        # values
        handXfo = self.handCtrl.xfo

        data = {
                "class":"kraken.examples.hand_component.HandComponent",
                "name": self.getName(),
                "location": self.getLocation(),
                "handXfo": handXfo
               }

        return data


class HandComponent(Component):
    """Hand Component"""

    def __init__(self, name='hand', parent=None):

        Profiler.getInstance().push("Construct Hand Component:" + name)
        super(HandComponent, self).__init__(name, parent)

        # ================
        # Setup Hierarchy
        # ================
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs', parent=inputHrcGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs', parent=outputHrcGrp)


        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.armEndXfoInputTgt = self.createInput('armEndXfo', dataType='Xfo', parent=inputHrcGrp)
        self.armEndPosInputTgt = self.createInput('armEndPos', dataType='Xfo', parent=inputHrcGrp)

        # Declare Output Xfos
        self.handOutputTgt = self.createOutput('hand', dataType='Xfo', parent=outputHrcGrp)
        self.handEndOutputTgt = self.createOutput('handEnd', dataType='Xfo', parent=outputHrcGrp)

        # Declare Input Attrs
        self.debugInputAttr = self.createInput('debug', dataType='Boolean', parent=cmpInputAttrGrp)
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=cmpInputAttrGrp)

        # Declare Output Attrs


        # =========
        # Controls
        # =========
        # Add Controls
        self.handCtrlSpace = CtrlSpace('hand', parent=ctrlCmpGrp)

        self.handCtrl = Control('hand', parent=self.handCtrlSpace, shape="cube")
        self.handCtrl.alignOnXAxis()
        self.handCtrl.scalePoints(Vec3(2.0, 0.75, 1.25))

        # Rig Ref objects
        self.handRefSrt = Locator('handRef', parent=ctrlCmpGrp)

        # Add Component Params to IK control
        handSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings",
            parent=self.handCtrl)
        handLinkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0,
            maxValue=1.0, parent=handSettingsAttrGrp)


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        handDef = Joint('hand', parent=defCmpGrp)
        handDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        handConstraint = PoseConstraint('_'.join([self.handOutputTgt.getName(), 'To', self.handCtrl.getName()]))
        handConstraint.addConstrainer(self.handCtrl)
        self.handOutputTgt.addConstraint(handConstraint)

        handEndConstraint = PoseConstraint('_'.join([self.handEndOutputTgt.getName(), 'To', self.handCtrl.getName()]))
        handEndConstraint.addConstrainer(self.handCtrl)
        self.handEndOutputTgt.addConstraint(handEndConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Hand Solver Splice Op
        # spliceOp = SpliceOperator("handSolverSpliceOp", "HandSolver", "KrakenHandSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", self.debugInputAttr)
        # spliceOp.setInput("rightSide", self.rightSideInputAttr)
        # spliceOp.setInput("linkToWorld", handLinkToWorldInputAttr)

        # # Add Xfo Inputs)
        # spliceOp.setInput("armEndXfo", self.armEndXfoInputTgt)
        # spliceOp.setInput("armEndPos", self.armEndPosInputTgt)
        # spliceOp.setInput("handRef", self.handRefSrt)

        # # Add Xfo Outputs
        # spliceOp.setOutput("handCtrlSpace", self.handCtrlSpace)


        # Add Deformer Splice Op
        spliceOp = SpliceOperator("handDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", self.debugInputAttr)
        spliceOp.setInput("rightSide", self.rightSideInputAttr)

        # Add Xfo Inputs)
        spliceOp.setInput("constrainer", self.handOutputTgt)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", handDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'hand'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.handCtrlSpace.xfo = data['handXfo']
        self.handCtrl.xfo = data['handXfo']
        self.handRefSrt.xfo = data['handXfo']

        # ============
        # Set IO Xfos
        # ============
        self.armEndXfoInputTgt.xfo = data['handXfo']
        self.armEndPosInputTgt.xfo = data['handXfo']
        self.handEndOutputTgt.xfo = data['handXfo']
        self.handOutputTgt.xfo = data['handXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(HandComponent)
ks.registerComponent(HandComponentGuide)
