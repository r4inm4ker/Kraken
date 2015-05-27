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


class PelvisComponent(Component):
    """Pelvis Component Base"""

    def __init__(self, name='pelvisBase', parent=None, data=None):
        super(PelvisComponent, self).__init__(name, parent)

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
        self.cogInputTgt = self.createInput('cog', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.pelvisOutputTgt = self.createOutput('pelvis', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class PelvisComponentGuide(PelvisComponent):
    """Pelvis Component Guide"""

    def __init__(self, name='pelvisGuide', parent=None, data=None):

        Profiler.getInstance().push("Construct Pelvis Guide Component:" + name)
        super(PelvisComponentGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Guide Controls
        self.pelvisCtrl = Control('pelvis', parent=self.ctrlCmpGrp, shape="cube")

        if data is None:
            data = {
                    "location": "M",
                    "pelvisXfo": Xfo(tr=Vec3(0.0, 11.1351, -0.1382))
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
            "name": self.getName(),
            "location": self.getLocation(),
            "pelvisXfo": self.pelvisCtrl.xfo
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
        self.pelvisCtrl.xfo = data['pelvisXfo']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        # values
        pelvisXfo = self.pelvisCtrl.xfo

        data = {
                "class":"kraken.examples.pelvis_component.PelvisComponentRig",
                "name": self.getName(),
                "location": self.getLocation(),
                "pelvisXfo": pelvisXfo
               }

        return data


class PelvisComponentRig(PelvisComponent):
    """Pelvis Component Rig"""

    def __init__(self, name='pelvis', parent=None):

        Profiler.getInstance().push("Construct Pelvis Rig Component:" + name)
        super(PelvisComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Add Controls
        self.pelvisCtrlSpace = CtrlSpace('pelvis', parent=self.ctrlCmpGrp)

        self.pelvisCtrl = Control('pelvis', parent=self.pelvisCtrlSpace, shape="cube")
        self.pelvisCtrl.alignOnYAxis(negative=True)
        self.pelvisCtrl.scalePoints(Vec3(2.0, 1.5, 1.5))

        # Add Component Params to IK control
        pelvisSettingsAttrGrp = AttributeGroup('DisplayInfo_PelvisSettings', parent=self.pelvisCtrl)


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        pelvisDef = Joint('pelvis', parent=defCmpGrp)
        pelvisDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        pelvisConstraint = PoseConstraint('_'.join([self.pelvisOutputTgt.getName(), 'To', self.pelvisCtrl.getName()]))
        pelvisConstraint.addConstrainer(self.pelvisCtrl)
        self.pelvisOutputTgt.addConstraint(pelvisConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Pelvis Solver Splice Op
        pelvisCtrlSpaceSpliceOp = SpliceOperator('pelvisCtrlSpaceSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(pelvisCtrlSpaceSpliceOp)

        # Add Att Inputs
        pelvisCtrlSpaceSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        pelvisCtrlSpaceSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        pelvisCtrlSpaceSpliceOp.setInput('constrainer', self.cogInputTgt)

        # Add Xfo Outputs
        pelvisCtrlSpaceSpliceOp.setOutput('constrainee', self.pelvisCtrlSpace)


        # Add Deformer Splice Op
        pelvisDefSpliceOp = SpliceOperator('pelvisDeformerSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(pelvisDefSpliceOp)

        # Add Att Inputs
        pelvisDefSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        pelvisDefSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs)
        pelvisDefSpliceOp.setInput('constrainer', self.pelvisOutputTgt)

        # Add Xfo Outputs
        pelvisDefSpliceOp.setOutput('constrainee', pelvisDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'pelvis'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.pelvisCtrlSpace.xfo = data['pelvisXfo']
        self.pelvisCtrl.xfo = data['pelvisXfo']

        # ============
        # Set IO Xfos
        # ============
        self.cogInputTgt.xfo = data['pelvisXfo']
        self.pelvisOutputTgt.xfo = data['pelvisXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(PelvisComponentGuide)
ks.registerComponent(PelvisComponentRig)
