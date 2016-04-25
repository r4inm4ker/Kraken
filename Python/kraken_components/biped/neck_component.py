from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control  import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class NeckComponent(BaseExampleComponent):
    """Neck Component"""

    def __init__(self, name="neckBase", parent=None):
        super(NeckComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.neckBaseInputTgt = self.createInput('neckBase', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.neckOutputTgt = self.createOutput('neck', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.neckEndOutputTgt = self.createOutput('neckEnd', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', value=self.getLocation() is 'R', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class NeckComponentGuide(NeckComponent):
    """Neck Component Guide"""

    def __init__(self, name='neck', parent=None):

        Profiler.getInstance().push("Construct Neck Component:" + name)
        super(NeckComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # ========

        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        # Guide Controls
        self.neckCtrl = Control('neck', parent=self.ctrlCmpGrp, shape="sphere")
        self.neckEndCtrl = Control('neckEnd', parent=self.ctrlCmpGrp, shape="sphere")

        data = {
                "name": name,
                "location": "M",
                "neckPosition": Vec3(0.0, 16.5572, -0.6915),
                "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
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

        data = super(NeckComponentGuide, self).saveData()

        data['neckPosition'] = self.neckCtrl.xfo.tr
        data['neckEndPosition'] = self.neckEndCtrl.xfo.tr

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(NeckComponentGuide, self).loadData( data )

        self.neckCtrl.xfo.tr = data['neckPosition']
        self.neckEndCtrl.xfo.tr = data['neckEndPosition']

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(NeckComponentGuide, self).getRigBuildData()

        # values
        neckEndPosition = self.neckCtrl.xfo.tr
        neckPosition = self.neckEndCtrl.xfo.tr
        neckUpV = Vec3(0.0, 0.0, -1.0)

        # Calculate Neck Xfo
        rootToEnd = neckEndPosition.subtract(neckPosition).unit()
        rootToUpV = neckUpV.subtract(neckPosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()

        neckXfo = Xfo()
        neckXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, neckPosition)

        data['neckXfo'] = neckXfo

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


    @classmethod
    def getRigComponentClass(cls):
        """Returns the corresponding rig component class for this guide component class

        Return:
        The rig component class.

        """

        return NeckComponentRig


class NeckComponentRig(NeckComponent):
    """Neck Component"""

    def __init__(self, name="neck", parent=None):

        Profiler.getInstance().push("Construct Neck Rig Component:" + name)
        super(NeckComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Neck
        self.neckCtrlSpace = CtrlSpace('neck', parent=self.ctrlCmpGrp)
        self.neckCtrl = Control('neck', parent=self.neckCtrlSpace, shape="pin")
        self.neckCtrl.scalePoints(Vec3(1.25, 1.25, 1.25))
        self.neckCtrl.translatePoints(Vec3(0, 0, -0.5))
        self.neckCtrl.rotatePoints(90, 0, 90)
        self.neckCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        neckDef = Joint('neck', parent=self.defCmpGrp)
        neckDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        neckInputConstraint = PoseConstraint('_'.join([self.neckCtrlSpace.getName(), 'To', self.neckBaseInputTgt.getName()]))
        neckInputConstraint.setMaintainOffset(True)
        neckInputConstraint.addConstrainer(self.neckBaseInputTgt)
        self.neckCtrlSpace.addConstraint(neckInputConstraint)

        # Constraint outputs
        neckOutputConstraint = PoseConstraint('_'.join([self.neckOutputTgt.getName(), 'To', self.neckCtrl.getName()]))
        neckOutputConstraint.addConstrainer(self.neckCtrl)
        self.neckOutputTgt.addConstraint(neckOutputConstraint)

        neckEndConstraint = PoseConstraint('_'.join([self.neckEndOutputTgt.getName(), 'To', self.neckCtrl.getName()]))
        neckEndConstraint.addConstrainer(self.neckCtrl)
        self.neckEndOutputTgt.addConstraint(neckEndConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        #Add Deformer Splice Op
        spliceOp = KLOperator('neckDeformerKLOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        spliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputstrl)
        spliceOp.setInput('constrainer', self.neckEndOutputTgt)

        # Add Xfo Outputs
        spliceOp.setOutput('constrainee', neckDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(NeckComponentRig, self).loadData( data )

        self.neckCtrlSpace.xfo = data['neckXfo']
        self.neckCtrl.xfo = data['neckXfo']

        # ============
        # Set IO Xfos
        # ============
        self.neckBaseInputTgt.xfo = data['neckXfo']
        self.neckEndOutputTgt.xfo = data['neckXfo']
        self.neckOutputTgt.xfo = data['neckXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(NeckComponentGuide)
ks.registerComponent(NeckComponentRig)
