from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy



class FabriceClavicle(BaseExampleComponent):
    """Clavicle Component Base"""

    def __init__(self, name='clavicle', parent=None):
        super(FabriceClavicle, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.spineEndInputTgt = self.createInput('spineEnd', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.clavicleOutputTgt = self.createOutput('clavicle', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs



class FabriceClavicleGuide(FabriceClavicle):
    """Clavicle Component Guide"""

    def __init__(self, name='clavicle', parent=None):

        Profiler.getInstance().push("Construct Clavicle Guide Component:" + name)
        super(FabriceClavicleGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Guide Controls
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.clavicleCtrl = Control('clavicle', parent=self.ctrlCmpGrp, shape="cube")
        self.clavicleCtrl.alignOnXAxis()
        self.clavicleCtrl.scalePoints(Vec3(1.0, 0.25, 0.25))

        data = {
                "name": name,
                "location": "L",
                "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
                'clavicleCtrlCrvData': self.clavicleCtrl.getCurveData()
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

        data = super(FabriceClavicleGuide, self).saveData()

        data['clavicleXfo'] = self.clavicleCtrl.xfo
        data['clavicleCtrlCrvData'] = self.clavicleCtrl.getCurveData()

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceClavicleGuide, self).loadData( data )

        self.clavicleCtrl.xfo = data['clavicleXfo']
        self.clavicleCtrl.setCurveData(data['clavicleCtrlCrvData'])

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(FabriceClavicleGuide, self).getRigBuildData()


        data['clavicleXfo'] = self.clavicleCtrl.xfo
        data['clavicleCtrlCrvData'] = self.clavicleCtrl.getCurveData()

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

        return FabriceClavicleRig


class FabriceClavicleRig(FabriceClavicle):
    """Clavicle Component"""

    def __init__(self, name='Clavicle', parent=None):

        Profiler.getInstance().push("Construct Clavicle Rig Component:" + name)
        super(FabriceClavicleRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Clavicle
        self.clavicleCtrlSpace = CtrlSpace('clavicle', parent=self.ctrlCmpGrp)
        self.clavicleCtrl = Control('clavicle', parent=self.clavicleCtrlSpace, shape="cube")
        self.clavicleCtrl.alignOnXAxis()


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        self.ctrlCmpGrp.setComponent(self)

        self.clavicleDef = Joint('clavicle', parent=defCmpGrp)
        self.clavicleDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([self.clavicleCtrl.getName(), 'To', self.spineEndInputTgt.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(self.spineEndInputTgt)
        self.clavicleCtrlSpace.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        clavicleConstraint = PoseConstraint('_'.join([self.clavicleOutputTgt.getName(), 'To', self.clavicleCtrl.getName()]))
        clavicleConstraint.addConstrainer(self.clavicleCtrl)
        self.clavicleOutputTgt.addConstraint(clavicleConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        spliceOp = KLOperator('clavicleDeformerKLOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        spliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput('constrainer', self.clavicleOutputTgt)

        # Add Xfo Outputs
        spliceOp.setOutput('constrainee', self.clavicleDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceClavicleRig, self).loadData( data )

        self.clavicleCtrlSpace.xfo = data['clavicleXfo']
        self.clavicleCtrl.xfo = data['clavicleXfo']
        self.clavicleCtrl.setCurveData(data['clavicleCtrlCrvData'])

        # ============
        # Set IO Xfos
        # ============
        self.spineEndInputTgt.xfo = data['clavicleXfo']
        self.clavicleOutputTgt.xfo = data['clavicleXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FabriceClavicleGuide)
ks.registerComponent(FabriceClavicleRig)
