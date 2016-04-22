from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

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


class LegComponent(BaseExampleComponent):
    """Leg Component"""

    def __init__(self, name='legBase', parent=None):

        super(LegComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.legPelvisInputTgt = self.createInput('pelvisInput', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.legIKTargetInputTgt = self.createInput('ikTarget', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.femurOutputTgt = self.createOutput('femur', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.shinOutputTgt = self.createOutput('shin', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.ikHandleOutputTgt = self.createOutput('ikHandle', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.legEndOutputTgt = self.createOutput('legEnd', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.legEndFKOutputTgt = self.createOutput('legEndFK', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', value=1.0, dataType='Float', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs
        self.drawDebugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', value=False, parent=self.cmpOutputAttrGrp).getTarget()
        self.ikBlendOutputAttr = self.createOutput('ikBlend', dataType='Float', value=0.0, parent=self.cmpOutputAttrGrp).getTarget()


class LegComponentGuide(LegComponent):
    """Leg Component Guide"""

    def __init__(self, name='leg', parent=None):

        Profiler.getInstance().push("Construct Leg Guide Component:" + name)
        super(LegComponentGuide, self).__init__(name, parent)


        # =========
        # Controls
        # ========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        # Guide Controls
        self.femurCtrl = Control('femur', parent=self.ctrlCmpGrp, shape="sphere")
        self.kneeCtrl = Control('knee', parent=self.ctrlCmpGrp, shape="sphere")
        self.ankleCtrl = Control('ankle', parent=self.ctrlCmpGrp, shape="sphere")

        self.default_data = {
                "name": name,
                "location": "L",
                "createIKHandle": False,
                "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
                "kneeXfo": Xfo(Vec3(1.408, 5.4371, -0.5043)),
                "ankleXfo": Xfo(Vec3(1.75, 1.15, -1.25))
               }

        self.loadData(self.default_data)

        Profiler.getInstance().pop()


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.


        Return:
        The JSON data object

        """

        data = super(LegComponentGuide, self).saveData()

        data['femurXfo'] = self.femurCtrl.xfo
        data['kneeXfo'] = self.kneeCtrl.xfo
        data['ankleXfo'] = self.ankleCtrl.xfo

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(LegComponentGuide, self).loadData( data )

        self.femurCtrl.xfo = data.get('femurXfo')
        self.kneeCtrl.xfo = data.get('kneeXfo')
        self.ankleCtrl.xfo = data.get('ankleXfo')

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(LegComponentGuide, self).getRigBuildData()

        # Values
        femurPosition = self.femurCtrl.xfo.tr
        kneePosition = self.kneeCtrl.xfo.tr
        anklePosition = self.ankleCtrl.xfo.tr

        # Calculate Bicep Xfo
        rootToWrist = anklePosition.subtract(femurPosition).unit()
        rootToKnee = kneePosition.subtract(femurPosition).unit()

        bone1Normal = rootToWrist.cross(rootToKnee).unit()
        bone1ZAxis = rootToKnee.cross(bone1Normal).unit()

        femurXfo = Xfo()
        femurXfo.setFromVectors(rootToKnee, bone1Normal, bone1ZAxis, femurPosition)

        # Calculate Forearm Xfo
        elbowToWrist = anklePosition.subtract(kneePosition).unit()
        elbowToRoot = femurPosition.subtract(kneePosition).unit()
        bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
        bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()

        kneeXfo = Xfo()
        kneeXfo.setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, kneePosition)

        femurLen = femurPosition.subtract(kneePosition).length()
        shinLen = kneePosition.subtract(anklePosition).length()

        handleXfo = Xfo()
        handleXfo.tr = anklePosition

        upVXfo = xfoFromDirAndUpV(femurPosition, anklePosition, kneePosition)
        upVXfo.tr = kneePosition
        upVXfo.tr = upVXfo.transformVector(Vec3(0, 0, 5))

        data['femurXfo'] = femurXfo
        data['kneeXfo'] = kneeXfo
        data['handleXfo'] = handleXfo
        data['upVXfo'] = upVXfo
        data['femurLen'] = femurLen
        data['shinLen'] = shinLen

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

        return LegComponentRig


class LegComponentRig(LegComponent):
    """Leg Component"""

    def __init__(self, name='leg', parent=None):

        Profiler.getInstance().push("Construct Leg Rig Component:" + name)
        super(LegComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Femur
        self.femurFKCtrlSpace = CtrlSpace('femurFK', parent=self.ctrlCmpGrp)
        self.femurFKCtrl = Control('femurFK', parent=self.femurFKCtrlSpace, shape="cube")
        self.femurFKCtrl.alignOnXAxis()

        # Shin
        self.shinFKCtrlSpace = CtrlSpace('shinFK', parent=self.femurFKCtrl)
        self.shinFKCtrl = Control('shinFK', parent=self.shinFKCtrlSpace, shape="cube")
        self.shinFKCtrl.alignOnXAxis()

        # IK Handle
        self.legIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.legIKCtrl = Control('IK', parent=self.legIKCtrlSpace, shape="pin")

        # Add Component Params to IK control
        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings", parent=self.legIKCtrl)
        legDrawDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=legSettingsAttrGrp)
        self.legRightSideInputAttr = BoolAttribute('rightSide', value=False, parent=legSettingsAttrGrp)
        self.legBone0LenInputAttr = ScalarAttribute('bone0Len', value=1.0, parent=legSettingsAttrGrp)
        self.legBone1LenInputAttr = ScalarAttribute('bone1Len', value=1.0, parent=legSettingsAttrGrp)
        legIKBlendInputAttr = ScalarAttribute('ikblend', value=1.0, minValue=0.0, maxValue=1.0, parent=legSettingsAttrGrp)
        legSoftIKInputAttr = BoolAttribute('softIK', value=True, parent=legSettingsAttrGrp)
        legSoftDistInputAttr = ScalarAttribute('softDist', value=0.0, minValue=0.0, parent=legSettingsAttrGrp)
        legStretchInputAttr = BoolAttribute('stretch', value=True, parent=legSettingsAttrGrp)
        legStretchBlendInputAttr = ScalarAttribute('stretchBlend', value=0.0, minValue=0.0, maxValue=1.0, parent=legSettingsAttrGrp)

        # Util Objects
        self.ikRootPosition = Locator("ikRootPosition", parent=self.ctrlCmpGrp)

        # Connect Input Attrs
        self.drawDebugInputAttr.connect(legDrawDebugInputAttr)

        # Connect Output Attrs
        self.drawDebugOutputAttr.connect(legDrawDebugInputAttr)
        self.ikBlendOutputAttr.connect(legIKBlendInputAttr)

        # UpV
        self.legUpVCtrlSpace = CtrlSpace('UpV', parent=self.ctrlCmpGrp)
        self.legUpVCtrl = Control('UpV', parent=self.legUpVCtrlSpace, shape="triangle")
        self.legUpVCtrl.alignOnZAxis()


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        femurDef = Joint('femur', parent=self.defCmpGrp)
        femurDef.setComponent(self)

        shinDef = Joint('shin', parent=self.defCmpGrp)
        shinDef.setComponent(self)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.legIKCtrlSpaceInputConstraint = PoseConstraint('_'.join([self.legIKCtrlSpace.getName(), 'To', self.globalSRTInputTgt.getName()]))
        self.legIKCtrlSpaceInputConstraint.setMaintainOffset(True)
        self.legIKCtrlSpaceInputConstraint.addConstrainer(self.globalSRTInputTgt)
        self.legIKCtrlSpace.addConstraint(self.legIKCtrlSpaceInputConstraint)

        self.legUpVCtrlSpaceInputConstraint = PoseConstraint('_'.join([self.legUpVCtrlSpace.getName(), 'To', self.globalSRTInputTgt.getName()]))
        self.legUpVCtrlSpaceInputConstraint.setMaintainOffset(True)
        self.legUpVCtrlSpaceInputConstraint.addConstrainer(self.globalSRTInputTgt)
        self.legUpVCtrlSpace.addConstraint(self.legUpVCtrlSpaceInputConstraint)

        self.legRootInputConstraint = PoseConstraint('_'.join([self.femurFKCtrlSpace.getName(), 'To', self.legPelvisInputTgt.getName()]))
        self.legRootInputConstraint.setMaintainOffset(True)
        self.legRootInputConstraint.addConstrainer(self.legPelvisInputTgt)
        self.femurFKCtrlSpace.addConstraint(self.legRootInputConstraint)

        self.ikRootPosInputConstraint = PoseConstraint('_'.join([self.ikRootPosition.getName(), 'To', self.legPelvisInputTgt.getName()]))
        self.ikRootPosInputConstraint.setMaintainOffset(True)
        self.ikRootPosInputConstraint.addConstrainer(self.legPelvisInputTgt)
        self.ikRootPosition.addConstraint(self.ikRootPosInputConstraint)

        # Constraint outputs
        self.legEndFKOutputConstraint = PoseConstraint('_'.join([self.legEndFKOutputTgt.getName(), 'To', self.shinFKCtrl.getName()]))
        self.legEndFKOutputConstraint.setMaintainOffset(True)
        self.legEndFKOutputConstraint.addConstrainer(self.shinFKCtrl)
        self.legEndFKOutputTgt.addConstraint(self.legEndFKOutputConstraint)

        self.ikHandleOutputConstraint = PoseConstraint('_'.join([self.ikHandleOutputTgt.getName(), 'To', self.legIKCtrl.getName()]))
        self.ikHandleOutputConstraint.setMaintainOffset(True)
        self.ikHandleOutputConstraint.addConstrainer(self.legIKCtrl)
        self.ikHandleOutputTgt.addConstraint(self.ikHandleOutputConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Leg Splice Op
        self.legIKKLOp = KLOperator('legKLOp', 'TwoBoneIKSolver', 'Kraken')
        self.addOperator(self.legIKKLOp)

        # Add Att Inputs
        self.legIKKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.legIKKLOp.setInput('rigScale', self.rigScaleInputAttr)

        self.legIKKLOp.setInput('bone0Len', self.legBone0LenInputAttr)
        self.legIKKLOp.setInput('bone1Len', self.legBone1LenInputAttr)
        self.legIKKLOp.setInput('ikblend', legIKBlendInputAttr)
        self.legIKKLOp.setInput('softIK', legSoftIKInputAttr)
        self.legIKKLOp.setInput('softDist', legSoftDistInputAttr)
        self.legIKKLOp.setInput('stretch', legStretchInputAttr)
        self.legIKKLOp.setInput('stretchBlend', legStretchBlendInputAttr)
        self.legIKKLOp.setInput('rightSide', self.legRightSideInputAttr)

        # Add Xfo Inputs
        self.legIKKLOp.setInput('root', self.ikRootPosition)
        self.legIKKLOp.setInput('bone0FK', self.femurFKCtrl)
        self.legIKKLOp.setInput('bone1FK', self.shinFKCtrl)
        self.legIKKLOp.setInput('ikHandle', self.legIKTargetInputTgt)
        self.legIKKLOp.setInput('upV', self.legUpVCtrl)

        # Add Xfo Outputs
        self.legIKKLOp.setOutput('bone0Out', self.femurOutputTgt)
        self.legIKKLOp.setOutput('bone1Out', self.shinOutputTgt)
        self.legIKKLOp.setOutput('bone2Out', self.legEndOutputTgt)


        # Add Leg Deformer Splice Op
        self.outputsToDeformersKLOp = KLOperator('legDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)

        # Add Att Inputs
        self.outputsToDeformersKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersKLOp.setInput('constrainers', [self.femurOutputTgt, self.shinOutputTgt])

        # Add Xfo Outputs
        self.outputsToDeformersKLOp.setOutput('constrainees', [femurDef, shinDef])

        Profiler.getInstance().pop()

    # =============
    # Data Methods
    # =============
    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(LegComponentRig, self).loadData( data )

        createIKHandle = data.get('createIKHandle')
        femurXfo = data.get('femurXfo')
        kneeXfo = data.get('kneeXfo')
        handleXfo = data.get('handleXfo')
        upVXfo = data.get('upVXfo')
        femurLen = data.get('femurLen')
        shinLen = data.get('shinLen')


        self.femurFKCtrlSpace.xfo = femurXfo
        self.femurFKCtrl.xfo = femurXfo
        self.femurFKCtrl.scalePoints(Vec3(femurLen, 1.75, 1.75))

        self.femurOutputTgt.xfo = femurXfo
        self.shinOutputTgt.xfo = kneeXfo

        self.shinFKCtrlSpace.xfo = kneeXfo
        self.shinFKCtrl.xfo = kneeXfo
        self.shinFKCtrl.scalePoints(Vec3(shinLen, 1.5, 1.5))

        self.legEndFKOutputTgt.xfo.tr = handleXfo.tr
        self.legEndFKOutputTgt.xfo.ori = kneeXfo.ori

        self.ikHandleOutputTgt.xfo = handleXfo

        self.ikRootPosition.xfo = femurXfo

        self.legIKCtrlSpace.xfo = handleXfo
        self.legIKCtrl.xfo = handleXfo

        if self.getLocation() == 'R':
            self.legIKCtrl.rotatePoints(0, 90, 0)
            self.legIKCtrl.translatePoints(Vec3(-1.0, 0.0, 0.0))
        else:
            self.legIKCtrl.rotatePoints(0, -90, 0)
            self.legIKCtrl.translatePoints(Vec3(1.0, 0.0, 0.0))

        self.legUpVCtrlSpace.xfo = upVXfo
        self.legUpVCtrl.xfo = upVXfo

        self.legRightSideInputAttr.setValue(self.getLocation() is 'R')
        self.legBone0LenInputAttr.setMin(0.0)
        self.legBone0LenInputAttr.setMax(femurLen * 3.0)
        self.legBone0LenInputAttr.setValue(femurLen)
        self.legBone1LenInputAttr.setMin(0.0)
        self.legBone1LenInputAttr.setMax(shinLen * 3.0)
        self.legBone1LenInputAttr.setValue(shinLen)

        self.legPelvisInputTgt.xfo = femurXfo
        self.legIKTargetInputTgt.xfo = handleXfo

        # TODO: We need the Rig class to be modified to handle the ability to
        # query if the ports are connected during loadData. Currently just a
        # place holder until that happens.

        # If IK Target input is not connected, switch to legIKCtrl
        # ikTargetInput = self.getInputByName('ikTarget')
        # if not ikTargetInput.isConnected():
            # self.legIKKLOp.setInput('ikHandle', self.legIKCtrl)

        # Eval Input Constraints
        self.ikRootPosInputConstraint.evaluate()
        self.legIKCtrlSpaceInputConstraint.evaluate()
        self.legUpVCtrlSpaceInputConstraint.evaluate()
        self.legRootInputConstraint.evaluate()

        # Eval Operators
        self.legIKKLOp.evaluate()
        self.outputsToDeformersKLOp.evaluate()

        # Eval Output Constraints
        self.legEndFKOutputConstraint.evaluate()
        self.ikHandleOutputConstraint.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(LegComponentGuide)
ks.registerComponent(LegComponentRig)
