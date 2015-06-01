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


class HandComponent(Component):
    """Hand Component Base"""

    def __init__(self, name='handBase', parent=None, data=None):
        super(HandComponent, self).__init__(name, parent)

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
        self.armEndXfoInputTgt = self.createInput('armEndXfo', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.handOutputTgt = self.createOutput('hand', dataType='Xfo', parent=self.outputHrcGrp)
        self.handEndOutputTgt = self.createOutput('handEnd', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', parent=self.cmpInputAttrGrp)
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class HandComponentGuide(HandComponent):
    """Hand Component Guide"""

    def __init__(self, name='handGuide', parent=None, data=None):

        Profiler.getInstance().push("Construct Hand Guide Component:" + name)
        super(HandComponentGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Guide Controls
        self.handCtrl = Control('hand', parent=self.ctrlCmpGrp, shape="cube")

        if data is None:
            data = {
                    "location": "L",
                    "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906),
                                   ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623))
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
            'class':"kraken.examples.hand_component.HandComponentGuide",
            'name': self.getName(),
            'location': self.getLocation(),
            'handXfo': self.handCtrl.xfo
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


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        # values
        handXfo = self.handCtrl.xfo

        data = {
            "class":"kraken.examples.hand_component.HandComponentRig",
            "name": self.getName(),
            "location": self.getLocation(),
            "handXfo": handXfo
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

class HandComponentRig(HandComponent):
    """Hand Component Rig"""

    def __init__(self, name='hand', parent=None):

        Profiler.getInstance().push("Construct Hand Rig Component:" + name)
        super(HandComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Add Controls
        self.handCtrlSpace = CtrlSpace('hand', parent=self.ctrlCmpGrp)

        self.handCtrl = Control('hand', parent=self.handCtrlSpace, shape="cube")
        self.handCtrl.alignOnXAxis()
        self.handCtrl.scalePoints(Vec3(2.0, 0.75, 1.25))

        # Rig Ref objects
        self.handRefSrt = Locator('handRef', parent=self.ctrlCmpGrp)

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
        handCtrlSpaceSpliceOp = SpliceOperator('handCtrlSpaceSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(handCtrlSpaceSpliceOp)

        # Add Att Inputs
        handCtrlSpaceSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        handCtrlSpaceSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs)
        handCtrlSpaceSpliceOp.setInput('constrainer', self.armEndXfoInputTgt)

        # Add Xfo Outputs
        handCtrlSpaceSpliceOp.setOutput('constrainee', self.handCtrlSpace)


        # Add Deformer Splice Op
        handDefSpliceOp = SpliceOperator('handDeformerSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(handDefSpliceOp)

        # Add Att Inputs
        handDefSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        handDefSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs)
        handDefSpliceOp.setInput('constrainer', self.handOutputTgt)

        # Add Xfo Outputs
        handDefSpliceOp.setOutput('constrainee', handDef)

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
        self.handEndOutputTgt.xfo = data['handXfo']
        self.handOutputTgt.xfo = data['handXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(HandComponentGuide)
ks.registerComponent(HandComponentRig)
