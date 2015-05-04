from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler


class ArmComponentGuide(Component):
    """Arm Component Guide"""

    def __init__(self, name='Arm', parent=None):
        super(ArmComponentGuide, self).__init__(name, parent)

        self.bicep = Control('bicepFK', parent=self, shape="sphere")
        self.forearm = Control('bicepFK', parent=self, shape="sphere")
        self.wrist = Control('bicepFK', parent=self, shape="sphere")

        self.bicepFKCtrlSizeInputAttr = FloatAttribute('bicepFKCtrlSize', 2.0)
        self.forearmFKCtrlSizeInputAttr = FloatAttribute('forearmFKCtrlSize', 2.0)

        self.addInput(self.bicepFKCtrlSizeInputAttr)
        self.addInput(self.forearmFKCtrlSizeInputAttr)

        self.loadData({
            "name": name,
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })


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
                'bicepXfo': self.bicep.xfo,
                'forearmXfo': self.forearm.xfo,
                'wristXfo': self.wrist.xfo,
                "bicepFKCtrlSize": self.bicepFKCtrlSizeInputAttr.getValue(),
                "forearmFKCtrlSize": self.forearmFKCtrlSizeInputAttr.getValue()
                }

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        self.setName(data['name'])
        self.setLocation(data['location'])
        self.bicep.xfo = data['bicepXfo']
        self.forearm.xfo = data['forearmXfo']
        self.wrist.xfo = data['wristXfo']

        self.bicepFKCtrlSizeInputAttr.setValue(data['bicepFKCtrlSize'])
        self.forearmFKCtrlSizeInputAttr.setValue(data['forearmFKCtrlSize'])

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        # values
        bicepPosition = self.bicep.xfo.tr
        forearmPosition = self.forearm.xfo.tr
        wristPosition = self.wrist.xfo.tr

        # Calculate Bicep Xfo
        rootToWrist = wristPosition.subtract(bicepPosition).unit()
        rootToElbow = forearmPosition.subtract(bicepPosition).unit()

        bone1Normal = rootToWrist.cross(rootToElbow).unit()
        bone1ZAxis = rootToElbow.cross(bone1Normal).unit()

        bicepXfo = Xfo()
        bicepXfo.setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, bicepPosition)

        # Calculate Forearm Xfo
        elbowToWrist = wristPosition.subtract(forearmPosition).unit()
        elbowToRoot = bicepPosition.subtract(forearmPosition).unit()
        bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
        bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()
        forearmXfo = Xfo()
        forearmXfo.setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, forearmPosition)

        bicepLen = bicepPosition.subtract(forearmPosition).length()
        forearmLen = forearmPosition.subtract(wristPosition).length()

        armEndXfo = Xfo()
        armEndXfo.tr = wristPosition
        armEndXfo.ori = forearmXfo.ori

        upVXfo = xfoFromDirAndUpV(bicepPosition, wristPosition, forearmPosition)
        upVXfo.tr = forearmPosition
        upVXfo.tr = upVXfo.transformVector(Vec3(0, 0, 5))

        return {
            "class":"kraken.examples.arm_component.ArmComponent",
            "name": self.getName(),
            "location":self.getLocation(),
            "bicepXfo": bicepXfo,
            "forearmXfo": forearmXfo,
            "armEndXfo": armEndXfo,
            "upVXfo": upVXfo,
            "forearmLen": forearmLen,
            "bicepLen": bicepLen,
            "bicepFKCtrlSize": self.bicepFKCtrlSizeInputAttr.getValue(),
            "forearmFKCtrlSize": self.forearmFKCtrlSizeInputAttr.getValue()
            }


class ArmComponent(Component):
    """Arm Component"""

    def __init__(self, name='Arm', parent=None):

        # location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Arm Component:" + name)
        super(ArmComponent, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs')
        inputHrcGrp.addAttributeGroup(cmpInputAttrGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs')
        inputHrcGrp.addAttributeGroup(cmpOutputAttrGrp)

        # Bicep
        self.bicepFKCtrlSrtBuffer = SrtBuffer('bicepFK', parent=ctrlCmpGrp)

        self.bicepFKCtrl = Control('bicepFK', parent=self.bicepFKCtrlSrtBuffer, shape="cube")
        self.bicepFKCtrl.alignOnXAxis()

        # Forearm
        self.forearmFKCtrlSrtBuffer = SrtBuffer('forearmFK', parent=self.bicepFKCtrl)

        self.forearmFKCtrl = Control('forearmFK', parent=self.forearmFKCtrlSrtBuffer, shape="cube")
        self.forearmFKCtrl.alignOnXAxis()

        # Arm IK
        self.armIKCtrlSrtBuffer = SrtBuffer('IK', parent=ctrlCmpGrp)
        self.armIKCtrl = Control('IK', parent=self.armIKCtrlSrtBuffer, shape="pin")


        # Add Component Params to IK control
        armDebugInputAttr = BoolAttribute('debug', True)
        self.armBone1LenInputAttr = FloatAttribute('bone1Len', 0.0)
        self.armBone2LenInputAttr = FloatAttribute('bone2Len', 0.0)
        armFkikInputAttr = FloatAttribute('fkik', 0.0)
        armSoftIKInputAttr = BoolAttribute('softIK', True)
        armSoftDistInputAttr = FloatAttribute('softDist', 0.0)
        armStretchInputAttr = BoolAttribute('stretch', True)
        armStretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)

        armSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings")
        self.armIKCtrl.addAttributeGroup(armSettingsAttrGrp)
        armSettingsAttrGrp.addAttribute(armDebugInputAttr)
        armSettingsAttrGrp.addAttribute(self.armBone1LenInputAttr)
        armSettingsAttrGrp.addAttribute(self.armBone2LenInputAttr)
        armSettingsAttrGrp.addAttribute(armFkikInputAttr)
        armSettingsAttrGrp.addAttribute(armSoftIKInputAttr)
        armSettingsAttrGrp.addAttribute(armSoftDistInputAttr)
        armSettingsAttrGrp.addAttribute(armStretchInputAttr)
        armSettingsAttrGrp.addAttribute(armStretchBlendInputAttr)

        # UpV
        self.armUpVCtrlSrtBuffer = SrtBuffer('UpV', parent=ctrlCmpGrp)
        self.armUpVCtrl = Control('UpV', parent=self.armUpVCtrlSrtBuffer, shape="triangle")
        self.armUpVCtrl.alignOnZAxis()
        self.armUpVCtrl.rotatePoints(180, 0, 0)


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), parent=deformersLayer)

        bicepDef = Joint('bicep', parent=defCmpGrp)
        bicepDef.setComponent(self)

        forearmDef = Joint('forearm', parent=defCmpGrp)
        forearmDef.setComponent(self)

        wristDef = Joint('wrist', parent=defCmpGrp)
        wristDef.setComponent(self)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        clavicleEndInput = Locator('clavicleEnd', parent=inputHrcGrp)
        self.bicepOutput = Locator('bicep', parent=outputHrcGrp)
        self.forearmOutput = Locator('forearm', parent=outputHrcGrp)
        self.armEndXfoOutput = Locator('armEndXfo', parent=outputHrcGrp)
        self.armEndPosOutput = Locator('armEndPos', parent=outputHrcGrp)


        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        bone1LenInputAttr = FloatAttribute('bone1Len', 0.0)
        bone2LenInputAttr = FloatAttribute('bone2Len', 0.0)
        fkikInputAttr = FloatAttribute('fkik', 0.0)
        softIKInputAttr = BoolAttribute('softIK', True)
        softDistInputAttr = FloatAttribute('softDist', 0.5)
        stretchInputAttr = BoolAttribute('stretch', True)
        stretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)
        self.rightSideInputAttr = BoolAttribute('rightSide')

        cmpInputAttrGrp.addAttribute(debugInputAttr)
        cmpInputAttrGrp.addAttribute(bone1LenInputAttr)
        cmpInputAttrGrp.addAttribute(bone2LenInputAttr)
        cmpInputAttrGrp.addAttribute(fkikInputAttr)
        cmpInputAttrGrp.addAttribute(softIKInputAttr)
        cmpInputAttrGrp.addAttribute(softDistInputAttr)
        cmpInputAttrGrp.addAttribute(stretchInputAttr)
        cmpInputAttrGrp.addAttribute(stretchBlendInputAttr)
        cmpInputAttrGrp.addAttribute(self.rightSideInputAttr)


        # Connect attrs to control attrs
        debugInputAttr.connect(armDebugInputAttr)
        bone1LenInputAttr.connect(self.armBone1LenInputAttr)
        bone2LenInputAttr.connect(self.armBone2LenInputAttr)
        fkikInputAttr.connect(armFkikInputAttr)
        softIKInputAttr.connect(armSoftIKInputAttr)
        softDistInputAttr.connect(armSoftDistInputAttr)
        stretchInputAttr.connect(armStretchInputAttr)
        stretchBlendInputAttr.connect(armStretchBlendInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        armRootInputConstraint = PoseConstraint('_'.join([self.armIKCtrl.getName(), 'To', clavicleEndInput.getName()]))
        armRootInputConstraint.setMaintainOffset(True)
        armRootInputConstraint.addConstrainer(clavicleEndInput)
        self.bicepFKCtrlSrtBuffer.addConstraint(armRootInputConstraint)

        # Constraint outputs


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(clavicleEndInput)
        self.addOutput(self.bicepOutput)
        self.addOutput(self.forearmOutput)
        self.addOutput(self.armEndXfoOutput)
        self.addOutput(self.armEndPosOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(bone1LenInputAttr)
        self.addInput(bone2LenInputAttr)
        self.addInput(fkikInputAttr)
        self.addInput(softIKInputAttr)
        self.addInput(softDistInputAttr)
        self.addInput(stretchInputAttr)
        self.addInput(stretchBlendInputAttr)
        self.addInput(self.rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Solver Splice Op
        # spliceOp = SpliceOperator("armSpliceOp", "LimbSolver", "KrakenLimbSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("bone1Len", bone1LenInputAttr)
        # spliceOp.setInput("bone2Len", bone2LenInputAttr)
        # spliceOp.setInput("fkik", fkikInputAttr)
        # spliceOp.setInput("softIK", softIKInputAttr)
        # spliceOp.setInput("softDist", softDistInputAttr)
        # spliceOp.setInput("stretch", stretchInputAttr)
        # spliceOp.setInput("stretchBlend", stretchBlendInputAttr)
        # spliceOp.setInput("rightSide", self.rightSideInputAttr)

        # # Add Xfo Inputs
        # spliceOp.setInput("root", clavicleEndInput)
        # spliceOp.setInput("bone1FK", self.bicepFKCtrl)
        # spliceOp.setInput("bone2FK", forearmFKCtrl)
        # spliceOp.setInput("ikHandle", armIKCtrl)
        # spliceOp.setInput("upV", self.armUpVCtrl)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Out", self.bicepOutput)
        # spliceOp.setOutput("bone02Out", self.forearmOutput)
        # spliceOp.setOutput("bone03Out", self.armEndXfoOutput)
        # spliceOp.setOutput("bone03PosOut", self.armEndPosOutput)


        # # Add Deformer Splice Op
        # spliceOp = SpliceOperator("armDeformerSpliceOp", "LimbConstraintSolver", "KrakenLimbSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)

        # # Add Xfo Inputs
        # spliceOp.setInput("bone01Constrainer", self.bicepOutput)
        # spliceOp.setInput("bone02Constrainer", self.forearmOutput)
        # spliceOp.setInput("bone03Constrainer", self.armEndXfoOutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Deformer", bicepDef)
        # spliceOp.setOutput("bone02Deformer", forearmDef)
        # spliceOp.setOutput("bone03Deformer", wristDef)


        Profiler.getInstance().pop()

    def loadData(self, data=None):

        self.setName(data.get('name', 'Arm'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.bicepFKCtrl.scalePoints(Vec3(data['bicepLen'], data['bicepFKCtrlSize'], data['bicepFKCtrlSize']))
        self.bicepFKCtrlSrtBuffer.xfo = data['bicepXfo']
        self.bicepFKCtrl.xfo = data['bicepXfo']

        self.bicepOutput.xfo = data['bicepXfo']
        self.forearmOutput.xfo = data['forearmXfo']

        self.forearmFKCtrlSrtBuffer.xfo = data['forearmXfo']
        self.forearmFKCtrl.xfo = data['forearmXfo']
        self.armIKCtrlSrtBuffer.xfo.tr = data['armEndXfo'].tr
        self.armIKCtrl.xfo = data['armEndXfo']

        if location == "R":
            self.armIKCtrl.rotatePoints(0, 90, 0)
        else:
            self.armIKCtrl.rotatePoints(0, -90, 0)

        self.forearmFKCtrl.scalePoints(Vec3(data['forearmLen'], data['forearmFKCtrlSize'], data['forearmFKCtrlSize']))

        self.armEndXfoOutput.xfo = data['armEndXfo']
        self.armEndPosOutput.xfo = data['armEndXfo']


        self.armUpVCtrlSrtBuffer.xfo = data['upVXfo']
        self.armUpVCtrl.xfo = data['upVXfo']

        self.rightSideInputAttr.setValue(location is 'R')
        self.armBone1LenInputAttr.setMin(data['bicepLen'])
        self.armBone1LenInputAttr.setMax(data['bicepLen'] * 3.0)
        self.armBone1LenInputAttr.setValue(data['bicepLen'])
        self.armBone2LenInputAttr.setMin(data['forearmLen'])
        self.armBone2LenInputAttr.setMax(data['forearmLen'] * 3.0)
        self.armBone2LenInputAttr.setValue(data['forearmLen'])


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(ArmComponent)
