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

from kraken.core.objects.operators.splice_operator import SpliceOperator

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

        # Declare Output Xfos
        self.femurOutputTgt = self.createOutput('femur', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.shinOutputTgt = self.createOutput('shin', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.legEndXfoOutputTgt = self.createOutput('legEndXfo', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.footOutputTgt = self.createOutput('foot', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.toeOutputTgt = self.createOutput('toe', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', value=1.0, dataType='Float', parent=self.cmpInputAttrGrp).getTarget()
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs
        self.drawDebugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', value=False, parent=self.cmpOutputAttrGrp).getTarget()


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
        self.toeCtrl = Control('toe', parent=self.ctrlCmpGrp, shape="sphere")
        self.toeTipCtrl = Control('toeTip', parent=self.ctrlCmpGrp, shape="sphere")

        data = {
                "name": name,
                "location": "L",
                "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
                "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
                "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237)),
                "toeXfo": Xfo(Vec3(1.85, 0.4, 0.25)),
                "toeTipXfo": Xfo(Vec3(1.85, 0.4, 1.5))
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

        data = super(LegComponentGuide, self).saveData()

        data['femurXfo'] = self.femurCtrl.xfo
        data['kneeXfo'] = self.kneeCtrl.xfo
        data['ankleXfo'] = self.ankleCtrl.xfo
        data['toeXfo'] = self.toeCtrl.xfo
        data['toeTipXfo'] = self.toeTipCtrl.xfo

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(LegComponentGuide, self).loadData( data )

        self.femurCtrl.xfo = data['femurXfo']
        self.kneeCtrl.xfo = data['kneeXfo']
        self.ankleCtrl.xfo = data['ankleXfo']
        self.toeCtrl.xfo = data['toeXfo']
        self.toeTipCtrl.xfo = data['toeTipXfo']

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
        toePosition = self.toeCtrl.xfo.tr
        toeTipPosition = self.toeTipCtrl.xfo.tr

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

        ankleXfo = Xfo()
        ankleXfo.tr = anklePosition
        # ankleXfo.ori = kneeXfo.ori

        toeXfo = Xfo()
        toeXfo.tr = toePosition
        # toeXfo.ori = kneeXfo.ori

        upVXfo = xfoFromDirAndUpV(femurPosition, anklePosition, kneePosition)
        upVXfo.tr = kneePosition
        upVXfo.tr = upVXfo.transformVector(Vec3(0, 0, 5))

        data['femurXfo'] = femurXfo
        data['kneeXfo'] = kneeXfo
        data['handleXfo'] = handleXfo
        data['ankleXfo'] = ankleXfo
        data['toeXfo'] = toeXfo
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

        # Ankle
        self.legIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.legIKCtrl = Control('IK', parent=self.legIKCtrlSpace, shape="pin")

        # FK Foot
        self.footCtrlSpace = CtrlSpace('foot', parent=self.ctrlCmpGrp)
        self.footCtrl = Control('foot', parent=self.footCtrlSpace, shape="cube")
        self.footCtrl.alignOnXAxis()

        # FK Toe
        self.toeCtrlSpace = CtrlSpace('toe', parent=self.footCtrl)
        self.toeCtrl = Control('toe', parent=self.toeCtrlSpace, shape="cube")
        self.toeCtrl.alignOnXAxis()

        # Rig Ref objects
        self.footRefSrt = Locator('footRef', parent=self.ctrlCmpGrp)

        # Add Component Params to IK control
        footSettingsAttrGrp = AttributeGroup("DisplayInfo_FootSettings", parent=self.footCtrl)
        footLinkToWorldInputAttr = ScalarAttribute('linkToWorld', 1.0, maxValue=1.0, parent=footSettingsAttrGrp)

        # Add Component Params to IK control
        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings", parent=self.legIKCtrl)
        legDrawDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=legSettingsAttrGrp)
        self.legBone0LenInputAttr = ScalarAttribute('bone0Len', value=1.0, parent=legSettingsAttrGrp)
        self.legBone1LenInputAttr = ScalarAttribute('bone1Len', value=1.0, parent=legSettingsAttrGrp)
        legIKBlendInputAttr = ScalarAttribute('ikblend', value=1.0, minValue=0.0, maxValue=1.0, parent=legSettingsAttrGrp)
        legSoftIKInputAttr = BoolAttribute('softIK', value=True, parent=legSettingsAttrGrp)
        legSoftDistInputAttr = ScalarAttribute('softDist', value=0.0, minValue=0.0, parent=legSettingsAttrGrp)
        legStretchInputAttr = BoolAttribute('stretch', value=True, parent=legSettingsAttrGrp)
        legStretchBlendInputAttr = ScalarAttribute('stretchBlend', value=0.0, minValue=0.0, maxValue=1.0, parent=legSettingsAttrGrp)

        self.drawDebugInputAttr.connect(legDrawDebugInputAttr)

        # UpV
        self.legUpVCtrlSpace = CtrlSpace('UpV', parent=self.ctrlCmpGrp)
        self.legUpVCtrl = Control('UpV', parent=self.legUpVCtrlSpace, shape="triangle")
        self.legUpVCtrl.alignOnZAxis()


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        femurDef = Joint('femur', parent=self.defCmpGrp)
        femurDef.setComponent(self)

        shinDef = Joint('shin', parent=self.defCmpGrp)
        shinDef.setComponent(self)

        ankleDef = Joint('ankle', parent=self.defCmpGrp)
        ankleDef.setComponent(self)

        self.footDef = Joint('foot', parent=self.defCmpGrp)
        self.footDef.setComponent(self)

        self.toeDef = Joint('toe', parent=self.defCmpGrp)
        self.toeDef.setComponent(self)


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

        self.legRootInputConstraint = PoseConstraint('_'.join([self.legIKCtrl.getName(), 'To', self.legPelvisInputTgt.getName()]))
        self.legRootInputConstraint.setMaintainOffset(True)
        self.legRootInputConstraint.addConstrainer(self.legPelvisInputTgt)
        self.femurFKCtrlSpace.addConstraint(self.legRootInputConstraint)

        # Constraint outputs
        self.footOutputConstraint = PoseConstraint('_'.join([self.footOutputTgt.getName(), 'To', self.footCtrl.getName()]))
        self.footOutputConstraint.addConstrainer(self.footCtrl)
        self.footOutputTgt.addConstraint(self.footOutputConstraint)

        self.toeOutputConstraint = PoseConstraint('_'.join([self.toeOutputTgt.getName(), 'To', self.toeCtrl.getName()]))
        self.toeOutputConstraint.addConstrainer(self.toeCtrl)
        self.toeOutputTgt.addConstraint(self.toeOutputConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Leg Splice Op
        self.legIKSpliceOp = SpliceOperator('legSpliceOp', 'TwoBoneIKSolver', 'Kraken')
        self.addOperator(self.legIKSpliceOp)

        # Add Att Inputs
        self.legIKSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.legIKSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        self.legIKSpliceOp.setInput('bone0Len', self.legBone0LenInputAttr)
        self.legIKSpliceOp.setInput('bone1Len', self.legBone1LenInputAttr)
        self.legIKSpliceOp.setInput('ikblend', legIKBlendInputAttr)
        self.legIKSpliceOp.setInput('softIK', legSoftIKInputAttr)
        self.legIKSpliceOp.setInput('softDist', legSoftDistInputAttr)
        self.legIKSpliceOp.setInput('stretch', legStretchInputAttr)
        self.legIKSpliceOp.setInput('stretchBlend', legStretchBlendInputAttr)
        self.legIKSpliceOp.setInput('rightSide', self.rightSideInputAttr)

        # Add Xfo Inputs
        self.legIKSpliceOp.setInput('root', self.legPelvisInputTgt)
        self.legIKSpliceOp.setInput('bone0FK', self.femurFKCtrl)
        self.legIKSpliceOp.setInput('bone1FK', self.shinFKCtrl)
        self.legIKSpliceOp.setInput('ikHandle', self.legIKCtrl)
        self.legIKSpliceOp.setInput('upV', self.legUpVCtrl)

        # Add Xfo Outputs
        self.legIKSpliceOp.setOutput('bone0Out', self.femurOutputTgt)
        self.legIKSpliceOp.setOutput('bone1Out', self.shinOutputTgt)
        self.legIKSpliceOp.setOutput('bone2Out', self.legEndXfoOutputTgt)


        # Add Leg Deformer Splice Op
        self.outputsToDeformersSpliceOp = SpliceOperator('legDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersSpliceOp)

        # Add Att Inputs
        self.outputsToDeformersSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersSpliceOp.setInput('constrainers', [self.femurOutputTgt, self.shinOutputTgt, self.legEndXfoOutputTgt])

        # Add Xfo Outputs
        self.outputsToDeformersSpliceOp.setOutput('constrainees', [femurDef, shinDef, ankleDef])

        # Add Foot Deformer Splice Op
        self.footDefSpliceOp = SpliceOperator('footDeformerSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(self.footDefSpliceOp)

        # Add Att Inputs
        self.footDefSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.footDefSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs)
        self.footDefSpliceOp.setInput('constrainer', self.footOutputTgt)

        # Add Xfo Outputs
        self.footDefSpliceOp.setOutput('constrainee', self.footDef)

        # Add Toe Deformer Splice Op
        self.toeDefSpliceOp = SpliceOperator('toeDeformerSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(self.toeDefSpliceOp)

        # Add Att Inputs
        self.toeDefSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.toeDefSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.toeDefSpliceOp.setInput('constrainer', self.toeOutputTgt)

        # Add Xfo Outputs
        self.toeDefSpliceOp.setOutput('constrainee', self.toeDef)

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

        self.femurFKCtrlSpace.xfo = data['femurXfo']
        self.femurFKCtrl.xfo = data['femurXfo']
        self.femurFKCtrl.scalePoints(Vec3(data['femurLen'], 1.75, 1.75))

        self.femurOutputTgt.xfo = data['femurXfo']
        self.shinOutputTgt.xfo = data['kneeXfo']

        self.shinFKCtrlSpace.xfo = data['kneeXfo']
        self.shinFKCtrl.xfo = data['kneeXfo']
        self.shinFKCtrl.scalePoints(Vec3(data['shinLen'], 1.5, 1.5))

        self.footCtrlSpace.xfo.tr = data['ankleXfo'].tr
        self.footCtrl.xfo.tr = data['ankleXfo'].tr

        self.toeCtrlSpace.xfo = data['toeXfo']
        self.toeCtrl.xfo = data['toeXfo']

        self.legIKCtrlSpace.xfo.tr = data['ankleXfo'].tr
        self.legIKCtrl.xfo.tr = data['ankleXfo'].tr

        if self.getLocation() == "R":
            self.legIKCtrl.rotatePoints(0, 90, 0)
            self.legIKCtrl.translatePoints(Vec3(-1.0, 0.0, 0.0))
        else:
            self.legIKCtrl.rotatePoints(0, -90, 0)
            self.legIKCtrl.translatePoints(Vec3(1.0, 0.0, 0.0))

        self.legUpVCtrlSpace.xfo = data['upVXfo']
        self.legUpVCtrl.xfo = data['upVXfo']

        self.rightSideInputAttr.setValue(self.getLocation() is 'R')
        self.legBone0LenInputAttr.setMin(0.0)
        self.legBone0LenInputAttr.setMax(data['femurLen'] * 3.0)
        self.legBone0LenInputAttr.setValue(data['femurLen'])
        self.legBone1LenInputAttr.setMin(0.0)
        self.legBone1LenInputAttr.setMax(data['shinLen'] * 3.0)
        self.legBone1LenInputAttr.setValue(data['shinLen'])

        self.legPelvisInputTgt.xfo = data['femurXfo']

        # Eval Constraints
        self.legIKCtrlSpaceInputConstraint.evaluate()
        self.legUpVCtrlSpaceInputConstraint.evaluate()
        self.legRootInputConstraint.evaluate()
        self.footOutputConstraint.evaluate()
        self.toeOutputConstraint.evaluate()

        # Eval Operators
        self.legIKSpliceOp.evaluate()
        self.outputsToDeformersSpliceOp.evaluate()
        self.footDefSpliceOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(LegComponentGuide)
ks.registerComponent(LegComponentRig)
