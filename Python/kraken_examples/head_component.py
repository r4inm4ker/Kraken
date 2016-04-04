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

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class HeadComponent(BaseExampleComponent):
    """Head Component Base"""

    def __init__(self, name='headBase', parent=None):
        super(HeadComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.headBaseInputTgt = self.createInput('headBase', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.headOutputTgt = self.createOutput('head', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.jawOutputTgt = self.createOutput('jaw', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.eyeLOutputTgt = self.createOutput('eyeL', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.eyeROutputTgt = self.createOutput('eyeR', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class HeadComponentGuide(HeadComponent):
    """Head Component Guide"""

    def __init__(self, name='head', parent=None):

        Profiler.getInstance().push("Construct Head Guide Component:" + name)
        super(HeadComponentGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.headCtrl = Control('head', parent=self.ctrlCmpGrp, shape="cube")
        self.headEndCtrl = Control('headEnd', parent=self.ctrlCmpGrp, shape="sphere")
        self.eyeLeftCtrl = Control('eyeLeft', parent=self.ctrlCmpGrp, shape="sphere")
        self.eyeRightCtrl = Control('eyeRight', parent=self.ctrlCmpGrp, shape="sphere")
        self.jawCtrl = Control('jaw', parent=self.ctrlCmpGrp, shape="cube")

        data = {
                "name": name,
                "location": "M",
                "headPosition": Vec3(0.0, 17.4756, -0.421),
                "headEndPosition": Vec3(0.0, 19.5, -0.421),
                "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
                "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
                "jawPosition": Vec3(0.0, 17.613, -0.2731)
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

        data = super(HeadComponentGuide, self).saveData()

        data['headPosition'] = self.headCtrl.xfo.tr
        data['headEndPosition'] = self.headEndCtrl.xfo.tr
        data['eyeLeftPosition'] = self.eyeLeftCtrl.xfo.tr
        data['eyeRightPosition'] = self.eyeRightCtrl.xfo.tr
        data['jawPosition'] = self.jawCtrl.xfo.tr

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(HeadComponentGuide, self).loadData( data )

        self.headCtrl.xfo.tr = data['headPosition']
        self.headEndCtrl.xfo.tr = data['headEndPosition']
        self.eyeLeftCtrl.xfo.tr = data['eyeLeftPosition']
        self.eyeRightCtrl.xfo.tr = data['eyeRightPosition']
        self.jawCtrl.xfo.tr = data['jawPosition']

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(HeadComponentGuide, self).getRigBuildData()

        data['headPosition'] = self.headCtrl.xfo.tr
        data['headEndPosition'] = self.headEndCtrl.xfo.tr
        data['eyeLeftPosition'] = self.eyeLeftCtrl.xfo.tr
        data['eyeRightPosition'] = self.eyeRightCtrl.xfo.tr
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

        return HeadComponentRig


class HeadComponentRig(HeadComponent):
    """Head Component Rig"""

    def __init__(self, name='head', parent=None):

        Profiler.getInstance().push("Construct Head Rig Component:" + name)
        super(HeadComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Head
        self.headCtrlSpace = CtrlSpace('head', parent=self.ctrlCmpGrp)
        self.headCtrl = Control('head', parent=self.headCtrlSpace, shape="circle")
        self.headCtrl.rotatePoints(0, 0, 90)
        self.headCtrl.scalePoints(Vec3(3, 3, 3))
        self.headCtrl.translatePoints(Vec3(0, 1, 0.25))

        # Eye Left
        self.eyeLeftCtrlSpace = CtrlSpace('eyeLeft', parent=self.headCtrl)
        self.eyeLeftCtrl = Control('eyeLeft', parent=self.eyeLeftCtrlSpace, shape="sphere")
        self.eyeLeftCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.eyeLeftCtrl.setColor("blueMedium")

        # Eye Right
        self.eyeRightCtrlSpace = CtrlSpace('eyeRight', parent=self.headCtrl)
        self.eyeRightCtrl = Control('eyeRight', parent=self.eyeRightCtrlSpace, shape="sphere")
        self.eyeRightCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.eyeRightCtrl.setColor("blueMedium")

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
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        headDef = Joint('head', parent=self.defCmpGrp)
        headDef.setComponent(self)

        jawDef = Joint('jaw', parent=self.defCmpGrp)
        jawDef.setComponent(self)

        eyeLeftDef = Joint('eyeLeft', parent=self.defCmpGrp)
        eyeLeftDef.setComponent(self)

        eyeRightDef = Joint('eyeRight', parent=self.defCmpGrp)
        eyeRightDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        headInputConstraint = PoseConstraint('_'.join([self.headCtrlSpace.getName(), 'To', self.headBaseInputTgt.getName()]))
        headInputConstraint.setMaintainOffset(True)
        headInputConstraint.addConstrainer(self.headBaseInputTgt)
        self.headCtrlSpace.addConstraint(headInputConstraint)

        # # Constraint outputs
        headOutputConstraint = PoseConstraint('_'.join([self.headOutputTgt.getName(), 'To', self.headCtrl.getName()]))
        headOutputConstraint.addConstrainer(self.headCtrl)
        self.headOutputTgt.addConstraint(headOutputConstraint)

        jawOutputConstraint = PoseConstraint('_'.join([self.jawOutputTgt.getName(), 'To', self.jawCtrl.getName()]))
        jawOutputConstraint.addConstrainer(self.jawCtrl)
        self.jawOutputTgt.addConstraint(jawOutputConstraint)

        eyeLOutputConstraint = PoseConstraint('_'.join([self.eyeLOutputTgt.getName(), 'To', self.eyeLeftCtrl.getName()]))
        eyeLOutputConstraint.addConstrainer(self.eyeLeftCtrl)
        self.eyeLOutputTgt.addConstraint(eyeLOutputConstraint)

        eyeROutputConstraint = PoseConstraint('_'.join([self.eyeROutputTgt.getName(), 'To', self.eyeRightCtrl.getName()]))
        eyeROutputConstraint.addConstrainer(self.eyeRightCtrl)
        self.eyeROutputTgt.addConstraint(eyeROutputConstraint)


        # Add Deformer Joints Splice Op
        self.outputsToDeformersKLOp = KLOperator('headDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)
        # Add Att Inputs
        self.outputsToDeformersKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersKLOp.setInput('rigScale', self.rigScaleInputAttr)
        # Add Xfo Inputs
        self.outputsToDeformersKLOp.setInput('constrainers', [self.headOutputTgt, self.jawOutputTgt, self.eyeROutputTgt, self.eyeLOutputTgt])
        # Add Xfo Outputs
        self.outputsToDeformersKLOp.setOutput('constrainees', [headDef, jawDef, eyeLeftDef, eyeRightDef])

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(HeadComponentRig, self).loadData( data )

        self.headCtrlSpace.xfo.tr = data['headPosition']
        self.headCtrl.xfo.tr = data['headPosition']
        self.eyeLeftCtrlSpace.xfo.tr = data['eyeLeftPosition']
        self.eyeLeftCtrl.xfo.tr = data['eyeLeftPosition']
        self.eyeRightCtrlSpace.xfo.tr = data['eyeRightPosition']
        self.eyeRightCtrl.xfo.tr = data['eyeRightPosition']
        self.jawCtrlSpace.xfo.tr = data['jawPosition']
        self.jawCtrl.xfo.tr = data['jawPosition']

        # ============
        # Set IO Xfos
        # ============
        self.headBaseInputTgt.xfo.tr = data['headPosition']
        self.headOutputTgt.xfo.tr = data['headPosition']
        self.jawOutputTgt.xfo.tr = data['jawPosition']
        self.eyeLOutputTgt.xfo.tr = data['eyeLeftPosition']
        self.eyeROutputTgt.xfo.tr = data['eyeRightPosition']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(HeadComponentGuide)
ks.registerComponent(HeadComponentRig)
