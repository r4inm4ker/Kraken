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

from kraken.core.objects.operators.kl_operator import KLOperator
from kraken.core.objects.operators.canvas_operator import CanvasOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class FabriceHead(BaseExampleComponent):
    """Fabrice Head Component Base"""

    def __init__(self, name='fabriceHeadBase', parent=None):
        super(FabriceHead, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.headBaseInputTgt = self.createInput('headBase', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.headOutputTgt = self.createOutput('head', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.jawOutputTgt = self.createOutput('jaw', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class FabriceHeadGuide(FabriceHead):
    """Fabrice Head Component Guide"""

    def __init__(self, name='head', parent=None):

        Profiler.getInstance().push("Construct Head Guide Component:" + name)
        super(FabriceHeadGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.headCtrl = Control('head', parent=self.ctrlCmpGrp, shape="circle")
        self.headCtrl.rotatePoints(90.0, 0.0, 0.0)
        self.headCtrl.scalePoints(Vec3(3.5, 3.5, 3.5))

        self.jawCtrl = Control('jaw', parent=self.ctrlCmpGrp, shape="cube")
        self.jawCtrl.alignOnZAxis()
        self.jawCtrl.scalePoints(Vec3(2.0, 0.5, 2.0))
        self.jawCtrl.alignOnYAxis(negative=True)
        self.jawCtrl.setColor('orange')

        data = {
                "name": name,
                "location": "M",
                "headXfo": Xfo(Vec3(0.0, 1.67, 1.75)),
                "headCtrlCrvData": self.headCtrl.getCurveData(),
                "jawPosition": Vec3(0.0, 1.2787, 2.0078),
                "jawCtrlCrvData": self.jawCtrl.getCurveData(),
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

        data['headXfo'] = self.headCtrl.xfo
        data['headCtrlCrvData'] = self.headCtrl.getCurveData()
        data['jawPosition'] = self.jawCtrl.xfo.tr
        data['jawCtrlCrvData'] = self.jawCtrl.getCurveData()

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceHeadGuide, self).loadData( data )

        self.headCtrl.xfo = data['headXfo']
        self.headCtrl.setCurveData(data['headCtrlCrvData'])
        self.jawCtrl.xfo.tr = data['jawPosition']
        self.jawCtrl.setCurveData(data['jawCtrlCrvData'])

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(FabriceHeadGuide, self).getRigBuildData()

        data['headXfo'] = self.headCtrl.xfo
        data['headCtrlCrvData'] = self.headCtrl.getCurveData()
        data['jawPosition'] = self.jawCtrl.xfo.tr
        data['jawCtrlCrvData'] = self.jawCtrl.getCurveData()

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

    def __init__(self, name='head', parent=None):

        Profiler.getInstance().push("Construct Head Rig Component:" + name)
        super(FabriceHeadRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Head Aim
        self.headAimCtrlSpace = CtrlSpace('headAim', parent=self.ctrlCmpGrp)
        self.headAimCtrl = Control('headAim', parent=self.headAimCtrlSpace, shape="sphere")
        self.headAimCtrl.scalePoints(Vec3(0.35, 0.35, 0.35))
        self.headAimCtrl.lockScale(x=True, y=True, z=True)

        self.headAimUpV = Locator('headAimUpV', parent=self.headAimCtrl)
        self.headAimUpV.setShapeVisibility(False)

        # Head
        self.headAim = Locator('headAim', parent=self.ctrlCmpGrp)
        self.headAim.setShapeVisibility(False)

        self.headCtrlSpace = CtrlSpace('head', parent=self.ctrlCmpGrp)
        self.headCtrl = Control('head', parent=self.headCtrlSpace, shape="circle")
        self.headCtrl.lockTranslation(x=True, y=True, z=True)
        self.headCtrl.lockScale(x=True, y=True, z=True)

        # Jaw
        self.jawCtrlSpace = CtrlSpace('jawCtrlSpace', parent=self.headCtrl)
        self.jawCtrl = Control('jaw', parent=self.jawCtrlSpace, shape="cube")
        self.jawCtrl.lockTranslation(x=True, y=True, z=True)
        self.jawCtrl.lockScale(x=True, y=True, z=True)
        self.jawCtrl.setColor("orange")

        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        headDef = Joint('head', parent=defCmpGrp)
        headDef.setComponent(self)

        jawDef = Joint('jaw', parent=defCmpGrp)
        jawDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        self.headToAimConstraint = PoseConstraint('_'.join([self.headCtrlSpace.getName(), 'To', self.headAim.getName()]))
        self.headToAimConstraint.setMaintainOffset(True)
        self.headToAimConstraint.addConstrainer(self.headAim)
        self.headCtrlSpace.addConstraint(self.headToAimConstraint)

        # Constraint inputs
        self.headAimInputConstraint = PoseConstraint('_'.join([self.headAimCtrlSpace.getName(), 'To', self.headBaseInputTgt.getName()]))
        self.headAimInputConstraint.setMaintainOffset(True)
        self.headAimInputConstraint.addConstrainer(self.headBaseInputTgt)
        self.headAimCtrlSpace.addConstraint(self.headAimInputConstraint)

        # # Constraint outputs
        self.headOutputConstraint = PoseConstraint('_'.join([self.headOutputTgt.getName(), 'To', self.headCtrl.getName()]))
        self.headOutputConstraint.addConstrainer(self.headCtrl)
        self.headOutputTgt.addConstraint(self.headOutputConstraint)

        self.jawOutputConstraint = PoseConstraint('_'.join([self.jawOutputTgt.getName(), 'To', self.jawCtrl.getName()]))
        self.jawOutputConstraint.addConstrainer(self.jawCtrl)
        self.jawOutputTgt.addConstraint(self.jawOutputConstraint)

        # ==============
        # Add Operators
        # ==============

        # Add Aim Canvas Op
        # =================
        self.headAimCanvasOp = CanvasOperator('headAimCanvasOp', 'Kraken.Solvers.DirectionConstraintSolver')
        self.addOperator(self.headAimCanvasOp)

        # Add Att Inputs
        self.headAimCanvasOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.headAimCanvasOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.headAimCanvasOp.setInput('position', self.headBaseInputTgt)
        self.headAimCanvasOp.setInput('upVector', self.headAimUpV)
        self.headAimCanvasOp.setInput('atVector', self.headAimCtrl)

        # Add Xfo Outputs
        self.headAimCanvasOp.setOutput('constrainee', self.headAim)

        # Add Deformer KL Op
        # ==================
        self.deformersToOutputsKLOp = KLOperator('headDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.deformersToOutputsKLOp)

        # Add Att Inputs
        self.deformersToOutputsKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.deformersToOutputsKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Outputs
        self.deformersToOutputsKLOp.setInput('constrainers', [self.headOutputTgt, self.jawOutputTgt])

        # Add Xfo Outputs
        self.deformersToOutputsKLOp.setOutput('constrainees', [headDef, jawDef])

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceHeadRig, self).loadData( data )

        headXfo = data['headXfo']
        headCtrlCrvData = data['headCtrlCrvData']
        jawPosition = data['jawPosition']
        jawCtrlCrvData = data['jawCtrlCrvData']

        self.headAimCtrlSpace.xfo.ori = headXfo.ori
        self.headAimCtrlSpace.xfo.tr = headXfo.tr.add(Vec3(0, 0, 4))
        self.headAimCtrl.xfo = self.headAimCtrlSpace.xfo

        self.headAimUpV.xfo.ori = self.headAimCtrl.xfo.ori
        self.headAimUpV.xfo.tr = self.headAimCtrl.xfo.tr.add(Vec3(0, 3, 0))

        self.headAim.xfo = headXfo
        self.headCtrlSpace.xfo = headXfo
        self.headCtrl.xfo = headXfo
        self.headCtrl.setCurveData(headCtrlCrvData)

        self.jawCtrlSpace.xfo.tr = jawPosition
        self.jawCtrl.xfo.tr = jawPosition
        self.jawCtrl.setCurveData(jawCtrlCrvData)

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
        self.headAimCanvasOp.evaluate()
        self.deformersToOutputsKLOp.evaluate()

        # evaluate the constraints to ensure the outputs are now in the correct location.
        self.headToAimConstraint.evaluate()
        self.headAimInputConstraint.evaluate()
        self.headOutputConstraint.evaluate()
        self.jawOutputConstraint.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FabriceHeadGuide)
ks.registerComponent(FabriceHeadRig)
