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
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class FabriceHead(BaseExampleComponent):
    """Fabrice Head Component Base"""

    def __init__(self, name='fabriceHeadBase', parent=None, data=None):
        super(FabriceHead, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.headBaseInputTgt = self.createInput('headBase', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.headOutputTgt = self.createOutput('head', dataType='Xfo', parent=self.outputHrcGrp)
        self.jawOutputTgt = self.createOutput('jaw', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class FabriceHeadGuide(FabriceHead):
    """Fabrice Head Component Guide"""

    def __init__(self, name='head', parent=None, data=None):

        Profiler.getInstance().push("Construct Head Guide Component:" + name)
        super(FabriceHeadGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.headCtrl = Control('head', parent=self.ctrlCmpGrp, shape="cube")
        self.headCtrl.alignOnZAxis()
        self.headCtrl.scalePoints(Vec3(0.75, 0.75, 1.5))
        self.headCtrl.translatePoints(Vec3(0.0, -0.25, 0.0))

        self.jawCtrl = Control('jaw', parent=self.ctrlCmpGrp, shape="cube")
        self.jawCtrl.alignOnZAxis()
        self.jawCtrl.scalePoints(Vec3(2.0, 0.5, 2.0))
        self.jawCtrl.alignOnYAxis(negative=True)
        self.jawCtrl.setColor('orange')

        if data is None:
            data = {
                    "name": name,
                    "location": "M",
                    "headCtrlCrvData": self.headCtrl.getCurveData(),
                    "headXfo": Xfo(Vec3(0.0, 1.67, 1.75)),
                    "jawPosition": Vec3(0.0, 1.2787, 2.0078)
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

        data = super(FabriceHeadGuide, self).saveData()

        data['headCtrlCrvData'] = self.headCtrl.getCurveData()
        data['headXfo'] = self.headCtrl.xfo
        data['jawPosition'] = self.jawCtrl.xfo.tr

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceHeadGuide, self).loadData( data )

        self.headCtrl.setCurveData(data['headCtrlCrvData'])
        self.headCtrl.xfo = data['headXfo']
        self.jawCtrl.xfo.tr = data['jawPosition']

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(FabriceHeadGuide, self).getRigBuildData()

        data['headCtrlCrvData'] = self.headCtrl.getCurveData()
        data['headXfo'] = self.headCtrl.xfo
        data['jawPosition'] = self.jawCtrl.xfo.tr

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

        return FabriceHeadRig


class FabriceHeadRig(FabriceHead):
    """Fabrice Head Component Rig"""

    def __init__(self, name='h  ead', parent=None):

        Profiler.getInstance().push("Construct Head Rig Component:" + name)
        super(FabriceHeadRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Head
        self.headCtrlSpace = CtrlSpace('head', parent=self.ctrlCmpGrp)
        self.headCtrl = Control('head', parent=self.headCtrlSpace, shape="circle")
        self.headCtrl.rotatePoints(90.0, 0.0, 0.0)
        self.headCtrl.scalePoints(Vec3(3, 3, 3))
        self.headCtrl.translatePoints(Vec3(0.0, 0.0, 0.25))

        # Jaw
        self.jawCtrlSpace = CtrlSpace('jawCtrlSpace', parent=self.headCtrl)
        self.jawCtrl = Control('jaw', parent=self.jawCtrlSpace, shape="cube")
        self.jawCtrl.alignOnYAxis(negative=True)
        self.jawCtrl.alignOnZAxis()
        self.jawCtrl.scalePoints(Vec3(1.45, 0.65, 1.25))
        self.jawCtrl.translatePoints(Vec3(0, -0.25, 0))
        self.jawCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        headDef = Joint('head', parent=defCmpGrp)
        headDef.setComponent(self)

        jawDef = Joint('jaw', parent=defCmpGrp)
        jawDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.headInputConstraint = PoseConstraint('_'.join([self.headCtrlSpace.getName(), 'To', self.headBaseInputTgt.getName()]))
        self.headInputConstraint.setMaintainOffset(True)
        self.headInputConstraint.addConstrainer(self.headBaseInputTgt)
        self.headCtrlSpace.addConstraint(self.headInputConstraint)

        # # Constraint outputs
        self.headOutputConstraint = PoseConstraint('_'.join([self.headOutputTgt.getName(), 'To', self.headCtrl.getName()]))
        self.headOutputConstraint.addConstrainer(self.headCtrl)
        self.headOutputTgt.addConstraint(self.headOutputConstraint)

        self.jawOutputConstraint = PoseConstraint('_'.join([self.jawOutputTgt.getName(), 'To', self.jawCtrl.getName()]))
        self.jawOutputConstraint.addConstrainer(self.jawCtrl)
        self.jawOutputTgt.addConstraint(self.jawOutputConstraint)

        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        self.deformersToOutputsSpliceOp = SpliceOperator('headDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.deformersToOutputsSpliceOp)

        # Add Att Inputs
        self.deformersToOutputsSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.deformersToOutputsSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Outputs
        for output in [self.headOutputTgt, self.jawOutputTgt]:
            self.deformersToOutputsSpliceOp.setInput('constrainers', output)

        # Add Xfo Outputs
        for joint in [headDef, jawDef]:
            self.deformersToOutputsSpliceOp.setOutput('constrainees', joint)

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceHeadRig, self).loadData( data )

        headCtrlCrvData = data['headCtrlCrvData']
        headXfo = data['headXfo']
        jawPosition = data['jawPosition']

        self.headCtrlSpace.xfo = headXfo
        self.headCtrl.xfo = headXfo
        self.headCtrl.setCurveData(headCtrlCrvData)
        self.jawCtrlSpace.xfo.tr = jawPosition
        self.jawCtrl.xfo.tr = jawPosition

        # ============
        # Set IO Xfos
        # ============
        self.headBaseInputTgt.xfo = headXfo
        self.headOutputTgt.xfo = headXfo
        self.jawOutputTgt.xfo.tr = jawPosition

        # ====================
        # Evaluate Splice Ops
        # ====================
        # evaluate the constraint op so that all the joint transforms are updated.
        self.deformersToOutputsSpliceOp.evaluate()

        # evaluate the constraints to ensure the outputs are now in the correct location.
        self.headInputConstraint.evaluate()
        self.headOutputConstraint.evaluate()
        self.jawOutputConstraint.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FabriceHeadGuide)
ks.registerComponent(FabriceHeadRig)
