from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

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


class LegComponentGuide(Component):
    """Leg Component Guide"""

    def __init__(self, name='legGuide', parent=None, data=None):
        super(LegComponentGuide, self).__init__(name, parent)

        # Declare Inputs Xfos

        # Declare Output Xfos

        # Declare Input Attrs

        # Declare Output Attrs

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs')
        inputHrcGrp.addAttributeGroup(cmpInputAttrGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs')
        outputHrcGrp.addAttributeGroup(cmpOutputAttrGrp)

        # Guide Controls
        self.femurCtrl = Control('femur', parent=ctrlCmpGrp, shape="sphere")
        self.kneeCtrl = Control('knee', parent=ctrlCmpGrp, shape="sphere")
        self.ankleCtrl = Control('ankle', parent=ctrlCmpGrp, shape="sphere")

        if data is None:
            data = {
                    "name": name,
                    "location": "L",
                    "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
                    "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
                    "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237))
                   }

        self.loadData(data)


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.


        Return:
        The JSON data object

        """


        data = {
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


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        # values
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

        return {
                "class":"kraken.examples.leg_component.LegComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "femurXfo": femurXfo,
                "kneeXfo": kneeXfo,
                "ankleXfo": ankleXfo,
                "upVXfo": upVXfo,
                "femurLen": femurLen,
                "shinLen": shinLen
               }


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(LegComponentGuide)


class LegComponent(Component):
    """Leg Component"""

    def __init__(self, name='leg', parent=None):

        Profiler.getInstance().push("Construct Leg Component:" + name)
        super(LegComponent, self).__init__(name, parent)

        # Declare Inputs Xfos
        self.legPelvisInput = self.addInput('pelvisInput', dataType='Xfo')

        # Declare Output Xfos
        self.femurOutput = self.addOutput('femur', dataType='Xfo')
        self.shinOutput = self.addOutput('shin', dataType='Xfo')
        self.legEndXfoOutput = self.addOutput('legEndXfo', dataType='Xfo')
        self.legEndPosOutput = self.addOutput('legEndPos', dataType='Xfo')

        # Declare Input Attrs

        # Declare Output Attrs
        self.debugOutput = self.addOutput('debug', dataType='Boolean')

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs')
        inputHrcGrp.addAttributeGroup(cmpInputAttrGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs')
        outputHrcGrp.addAttributeGroup(cmpOutputAttrGrp)

        # Femur
        self.femurFKCtrlSpace = CtrlSpace('femurFK', parent=ctrlCmpGrp)

        self.femurFKCtrl = Control('femurFK', parent=self.femurFKCtrlSpace, shape="cube")
        self.femurFKCtrl.alignOnXAxis()


        # Shin
        self.shinFKCtrlSpace = CtrlSpace('shinFK', parent=self.femurFKCtrl)

        self.shinFKCtrl = Control('shinFK', parent=self.shinFKCtrlSpace, shape="cube")
        self.shinFKCtrl.alignOnXAxis()


        # Ankle
        self.legIKCtrlSpace = CtrlSpace('IK', parent=ctrlCmpGrp)

        self.legIKCtrl = Control('IK', parent=self.legIKCtrlSpace, shape="pin")


        # Add Component Params to IK control
        legDebugInputAttr = BoolAttribute('debug', True)
        self.legBone1LenInputAttr = FloatAttribute('bone1Len', 1.0)
        self.legBone2LenInputAttr = FloatAttribute('bone2Len', 1.0)
        legFkikInputAttr = FloatAttribute('fkik', 1.0, maxValue=1.0)
        legSoftIKInputAttr = BoolAttribute('softIK', True)
        legSoftDistInputAttr = FloatAttribute('softDist', 0.0)
        legStretchInputAttr = BoolAttribute('stretch', True)
        legStretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)

        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings")
        self.legIKCtrl.addAttributeGroup(legSettingsAttrGrp)
        legSettingsAttrGrp.addAttribute(legDebugInputAttr)
        legSettingsAttrGrp.addAttribute(self.legBone1LenInputAttr)
        legSettingsAttrGrp.addAttribute(self.legBone2LenInputAttr)
        legSettingsAttrGrp.addAttribute(legFkikInputAttr)
        legSettingsAttrGrp.addAttribute(legSoftIKInputAttr)
        legSettingsAttrGrp.addAttribute(legSoftDistInputAttr)
        legSettingsAttrGrp.addAttribute(legStretchInputAttr)
        legSettingsAttrGrp.addAttribute(legStretchBlendInputAttr)

        # UpV
        self.legUpVCtrlSpace = CtrlSpace('UpV', parent=ctrlCmpGrp)

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


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        self.legPelvisInputTgt = Locator('pelvisInput', parent=inputHrcGrp)

        self.femurOutputTgt = Locator('femur', parent=outputHrcGrp)
        self.shinOutputTgt = Locator('shin', parent=outputHrcGrp)
        self.legEndXfoOutputTgt = Locator('legEndXfo', parent=outputHrcGrp)
        self.legEndPosOutputTgt = Locator('legEndPos', parent=outputHrcGrp)

        # Set IO Targets
        self.legPelvisInput.setTarget(self.legPelvisInputTgt)

        self.femurOutput.setTarget(self.femurOutputTgt)
        self.shinOutput.setTarget(self.shinOutputTgt)
        self.legEndXfoOutput.setTarget(self.legEndXfoOutputTgt)
        self.legEndPosOutput.setTarget(self.legEndPosOutputTgt)


        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        self.bone1LenInputAttr = FloatAttribute('bone1Len', 1.0)
        self.bone2LenInputAttr = FloatAttribute('bone2Len', 1.0)
        fkikInputAttr = FloatAttribute('fkik', 1.0, maxValue=1.0)
        softIKInputAttr = BoolAttribute('softIK', True)
        softDistInputAttr = FloatAttribute('softDist', 0.0)
        stretchInputAttr = BoolAttribute('stretch', True)
        stretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)
        rightSideInputAttr = BoolAttribute('rightSide', self.getLocation() is 'R')

        cmpInputAttrGrp.addAttribute(debugInputAttr)

        # Set IO Targets
        self.debugOutput.setTarget(debugInputAttr)


        # Connect attrs to control attrs
        debugInputAttr.connect(legDebugInputAttr)
        self.bone1LenInputAttr.connect(self.legBone1LenInputAttr)
        self.bone2LenInputAttr.connect(self.legBone2LenInputAttr)
        fkikInputAttr.connect(legFkikInputAttr)
        softIKInputAttr.connect(legSoftIKInputAttr)
        softDistInputAttr.connect(legSoftDistInputAttr)
        stretchInputAttr.connect(legStretchInputAttr)
        stretchBlendInputAttr.connect(legStretchBlendInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([self.legIKCtrl.getName(), 'To', self.legPelvisInputTgt.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(self.legPelvisInputTgt)
        self.femurFKCtrlSpace.addConstraint(legRootInputConstraint)

        # Constraint outputs


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        # self.addInput(self.legPelvisInputTgt)
        # self.addOutput(self.femurOutputTgt)
        # self.addOutput(self.shinOutputTgt)
        # self.addOutput(self.legEndXfoOutputTgt)
        # self.addOutput(self.legEndPosOutputTgt)

        # Add Attribute I/O's
        # self.addInput(debugInputAttr)
        # self.addInput(self.bone1LenInputAttr)
        # self.addInput(self.bone2LenInputAttr)
        # self.addInput(fkikInputAttr)
        # self.addInput(softIKInputAttr)
        # self.addInput(softDistInputAttr)
        # self.addInput(stretchInputAttr)
        # self.addInput(stretchBlendInputAttr)
        # self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        # spliceOp = SpliceOperator("legSpliceOp", "LimbSolver", "KrakenLimbSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("bone1Len", self.bone1LenInputAttr)
        # spliceOp.setInput("bone2Len", self.bone2LenInputAttr)
        # spliceOp.setInput("fkik", fkikInputAttr)
        # spliceOp.setInput("softIK", softIKInputAttr)
        # spliceOp.setInput("softDist", softDistInputAttr)
        # spliceOp.setInput("stretch", stretchInputAttr)
        # spliceOp.setInput("stretchBlend", stretchBlendInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # # Add Xfo Inputs
        # spliceOp.setInput("root", self.legPelvisInputTgt)
        # spliceOp.setInput("bone1FK", femurFKCtrl)
        # spliceOp.setInput("bone2FK", shinFKCtrl)
        # spliceOp.setInput("ikHandle", self.legIKCtrl)
        # spliceOp.setInput("upV", self.legUpVCtrl)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Out", self.femurOutputTgt)
        # spliceOp.setOutput("bone02Out", self.shinOutputTgt)
        # spliceOp.setOutput("bone03Out", self.legEndXfoOutputTgt)
        # spliceOp.setOutput("bone03PosOut", self.legEndPosOutputTgt)


        # # Add Deformer Splice Op
        # spliceOp = SpliceOperator("legDeformerSpliceOp", "LimbConstraintSolver", "KrakenLimbSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)

        # # Add Xfo Inputstrl)
        # spliceOp.setInput("bone01Constrainer", self.femurOutputTgt)
        # spliceOp.setInput("bone02Constrainer", self.shinOutputTgt)
        # spliceOp.setInput("bone03Constrainer", self.legEndXfoOutputTgt)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Deformer", femurDef)
        # spliceOp.setOutput("bone02Deformer", shinDef)
        # spliceOp.setOutput("bone03Deformer", ankleDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'leg'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.femurFKCtrlSpace.xfo = data['femurXfo']

        self.femurFKCtrl.xfo = data['femurXfo']
        self.femurFKCtrl.scalePoints(Vec3(data['femurLen'], 1.75, 1.75))

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

        # ============
        # Set IO Xfos
        # ============
        self.legBone1LenInputAttr.setMax(data['femurLen'] * 3.0)
        self.legBone1LenInputAttr.setValue(data['femurLen'])

        self.legBone2LenInputAttr.setMax(data['shinLen'] * 3.0)
        self.legBone2LenInputAttr.setValue(data['shinLen'])

        self.legUpVCtrlSpace.xfo = data['upVXfo']
        self.legUpVCtrl.xfo = data['upVXfo']

        self.legPelvisInputTgt.xfo = data['femurXfo']
        self.femurOutputTgt.xfo = data['femurXfo']

        self.shinOutputTgt.xfo = data['kneeXfo']

        self.legEndXfoOutputTgt.xfo = data['ankleXfo']
        self.legEndPosOutputTgt.xfo.tr = data['ankleXfo'].tr

        self.bone1LenInputAttr.setMax(data['femurLen'] * 3.0)
        self.bone1LenInputAttr.setValue(data['femurLen'])

        self.bone2LenInputAttr.setMax(data['shinLen'] * 3.0)
        self.bone2LenInputAttr.setValue(data['shinLen'])


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(LegComponent)
