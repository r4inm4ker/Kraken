from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.float_attribute import FloatAttribute
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


class LegComponent(Component):
    """Leg Component"""

    def __init__(self, name='legBase', parent=None):

        super(LegComponent, self).__init__(name, parent)

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
        self.legPelvisInputTgt = self.createInput('pelvisInput', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.femurOutputTgt = self.createOutput('femur', dataType='Xfo', parent=self.outputHrcGrp)
        self.shinOutputTgt = self.createOutput('shin', dataType='Xfo', parent=self.outputHrcGrp)
        self.legEndXfoOutputTgt = self.createOutput('legEndXfo', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=True, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', parent=self.cmpInputAttrGrp)
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs
        self.drawDebugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', value=True, parent=self.cmpOutputAttrGrp)


class LegComponentGuide(LegComponent):
    """Leg Component Guide"""

    def __init__(self, name='legGuide', parent=None, data=None):

        Profiler.getInstance().push("Construct Leg Guide Component:" + name)
        super(LegComponentGuide, self).__init__(name, parent)


        # =========
        # Controls
        # ========

        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.nameAttr = StringAttribute('name', value=name, parent=guideSettingsAttrGrp, callback=self.setName)
        self.locationAttr = StringAttribute('location', value='L', parent=guideSettingsAttrGrp, callback=self.setLocation)

        # Guide Controls
        self.femurCtrl = Control('femur', parent=self.ctrlCmpGrp, shape="sphere")
        self.kneeCtrl = Control('knee', parent=self.ctrlCmpGrp, shape="sphere")
        self.ankleCtrl = Control('ankle', parent=self.ctrlCmpGrp, shape="sphere")

        if data is None:
            data = {
                    "name": name,
                    "location": "L",
                    "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
                    "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
                    "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237))
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
            'class':"kraken.examples.leg_component.LegComponentGuide",
            'name': self.getName(),
            'location': self.getLocation(),
            'femurXfo': self.femurCtrl.xfo,
            'kneeXfo': self.kneeCtrl.xfo,
            'ankleXfo': self.ankleCtrl.xfo
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
        self.femurCtrl.xfo = data['femurXfo']
        self.kneeCtrl.xfo = data['kneeXfo']
        self.ankleCtrl.xfo = data['ankleXfo']

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

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

        ankleXfo = Xfo()
        ankleXfo.tr = anklePosition
        ankleXfo.ori = kneeXfo.ori

        upVXfo = xfoFromDirAndUpV(femurPosition, anklePosition, kneePosition)
        upVXfo.tr = kneePosition
        upVXfo.tr = upVXfo.transformVector(Vec3(0, 0, 5))

        data = {
            'class':"kraken.examples.leg_component.LegComponentRig",
            'name': self.getName(),
            'location':self.getLocation(),
            'femurXfo': femurXfo,
            'kneeXfo': kneeXfo,
            'ankleXfo': ankleXfo,
            'upVXfo': upVXfo,
            'femurLen': femurLen,
            'shinLen': shinLen
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


        # Add Component Params to IK control
        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings", parent=self.legIKCtrl)
        legDrawDebugInputAttr = BoolAttribute('drawDebug', value=True, parent=legSettingsAttrGrp)
        self.legBone0LenInputAttr = FloatAttribute('bone0Len', value=1.0, parent=legSettingsAttrGrp)
        self.legBone1LenInputAttr = FloatAttribute('bone1Len', value=1.0, parent=legSettingsAttrGrp)
        legIKBlendInputAttr = FloatAttribute('ikblend', value=1.0, minValue=0.0, maxValue=1.0, parent=legSettingsAttrGrp)
        legSoftIKInputAttr = BoolAttribute('softIK', value=True, parent=legSettingsAttrGrp)
        legSoftDistInputAttr = FloatAttribute('softDist', value=0.0, minValue=0.0, parent=legSettingsAttrGrp)
        legStretchInputAttr = BoolAttribute('stretch', value=True, parent=legSettingsAttrGrp)
        legStretchBlendInputAttr = FloatAttribute('stretchBlend', value=0.0, minValue=0.0, maxValue=1.0, parent=legSettingsAttrGrp)

        self.drawDebugInputAttr.connect(legDrawDebugInputAttr)

        # UpV
        self.legUpVCtrlSpace = CtrlSpace('UpV', parent=self.ctrlCmpGrp)
        self.legUpVCtrl = Control('UpV', parent=self.legUpVCtrlSpace, shape="triangle")
        self.legUpVCtrl.alignOnZAxis()


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        femurDef = Joint('femur', parent=defCmpGrp)
        femurDef.setComponent(self)

        shinDef = Joint('shin', parent=defCmpGrp)
        shinDef.setComponent(self)

        ankleDef = Joint('ankle', parent=defCmpGrp)
        ankleDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([self.legIKCtrl.getName(), 'To', self.legPelvisInputTgt.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(self.legPelvisInputTgt)
        self.femurFKCtrlSpace.addConstraint(legRootInputConstraint)

        # Constraint outputs


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
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


        # Add Deformer Splice Op
        self.outputsToDeformersSpliceOp = SpliceOperator('legDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersSpliceOp)

        # Add Att Inputs
        self.outputsToDeformersSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersSpliceOp.setInput('constrainers', self.femurOutputTgt)
        self.outputsToDeformersSpliceOp.setInput('constrainers', self.shinOutputTgt)
        self.outputsToDeformersSpliceOp.setInput('constrainers', self.legEndXfoOutputTgt)

        # Add Xfo Outputs
        self.outputsToDeformersSpliceOp.setOutput('constrainees', femurDef)
        self.outputsToDeformersSpliceOp.setOutput('constrainees', shinDef)
        self.outputsToDeformersSpliceOp.setOutput('constrainees', ankleDef)

        Profiler.getInstance().pop()

    # =============
    # Data Methods
    # =============
    def loadData(self, data=None):

        self.setName(data.get('name', 'leg'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.femurFKCtrlSpace.xfo = data['femurXfo']
        self.femurFKCtrl.xfo = data['femurXfo']
        self.femurFKCtrl.scalePoints(Vec3(data['femurLen'], 1.75, 1.75))

        self.femurOutputTgt.xfo = data['femurXfo']
        self.shinOutputTgt.xfo = data['kneeXfo']

        self.shinFKCtrlSpace.xfo = data['kneeXfo']
        self.shinFKCtrl.xfo = data['kneeXfo']
        self.shinFKCtrl.scalePoints(Vec3(data['shinLen'], 1.5, 1.5))

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

        self.legIKSpliceOp.evaluate()
        self.outputsToDeformersSpliceOp.evaluate()
        # self.legEndXfoOutputTgt.xfo = data['ankleXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(LegComponentGuide)
ks.registerComponent(LegComponentRig)
