from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler




class ArmComponent(Component):
    """Arm Component"""

    def __init__(self, name, parent=None):

        # location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Arm Component:" + name)
        super(ArmComponent, self).__init__(name, parent)

        # =========
        # Controls
        # =========

        # Bicep
        self.bicepFKCtrlSrtBuffer = SrtBuffer('bicepFK', parent=self)

        self.bicepFKCtrl = Control('bicepFK', parent=self.bicepFKCtrlSrtBuffer, shape="cube")
        self.bicepFKCtrl.alignOnXAxis()

        # Forearm
        self.forearmFKCtrlSrtBuffer = SrtBuffer('forearmFK', parent=self.bicepFKCtrl)

        self.forearmFKCtrl = Control('forearmFK', parent=self.forearmFKCtrlSrtBuffer, shape="cube")
        self.forearmFKCtrl.alignOnXAxis()

        # Arm IK
        self.armIKCtrlSrtBuffer = SrtBuffer('IK', parent=self)
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

        self.armUpVCtrlSrtBuffer = SrtBuffer('UpV', parent=self)

        self.armUpVCtrl = Control('UpV', parent=self.armUpVCtrlSrtBuffer, shape="triangle")
        self.armUpVCtrl.alignOnZAxis()
        self.armUpVCtrl.rotatePoints(180, 0, 0)


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getLayer('deformers')

        bicepDef = Joint('bicep')
        bicepDef.setComponent(self)

        forearmDef = Joint('forearm')
        forearmDef.setComponent(self)

        wristDef = Joint('wrist')
        wristDef.setComponent(self)

        deformersLayer.addChild(bicepDef)
        deformersLayer.addChild(forearmDef)
        deformersLayer.addChild(wristDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        clavicleEndInput = Locator('clavicleEnd')

        self.bicepOutput = Locator('bicep')
        self.forearmOutput = Locator('forearm')

        self.armEndXfoOutput = Locator('armEndXfo')
        self.armEndPosOutput = Locator('armEndPos')


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

        location = data.get('location', 'M')
        self.setLocation(location)

        # values
        bicepPosition = data['bicepPosition']
        forearmPosition = data['forearmPosition']
        wristPosition = data['wristPosition']
        bicepFKCtrlSize = data['bicepFKCtrlSize']
        forearmFKCtrlSize = data['forearmFKCtrlSize']

        # Calculate Bicep Xfo
        rootToWrist = wristPosition.subtract(bicepPosition).unit()
        rootToElbow = forearmPosition.subtract(bicepPosition).unit()

        bone1Normal = rootToWrist.cross(rootToElbow).unit()
        bone1ZAxis = rootToElbow.cross(bone1Normal).unit()

        bicepLen = bicepPosition.subtract(forearmPosition).length()
        self.bicepFKCtrl.scalePoints(Vec3(bicepLen, bicepFKCtrlSize, bicepFKCtrlSize))

        bicepXfo = Xfo()
        bicepXfo.setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, bicepPosition)

        # Calculate Forearm Xfo
        elbowToWrist = wristPosition.subtract(forearmPosition).unit()
        elbowToRoot = bicepPosition.subtract(forearmPosition).unit()
        bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
        bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()
        forearmXfo = Xfo()
        forearmXfo.setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, forearmPosition)

        self.bicepFKCtrlSrtBuffer.xfo = bicepXfo
        self.bicepFKCtrl.xfo = bicepXfo

        self.bicepOutput.xfo = bicepXfo
        self.forearmOutput.xfo = forearmXfo

        self.forearmFKCtrlSrtBuffer.xfo = forearmXfo
        self.forearmFKCtrl.xfo = forearmXfo
        self.armIKCtrlSrtBuffer.xfo.tr = wristPosition
        self.armIKCtrl.xfo = self.armIKCtrlSrtBuffer.xfo
        if self.getLocation() == "R":
            self.armIKCtrl.rotatePoints(0, 90, 0)
        else:
            self.armIKCtrl.rotatePoints(0, -90, 0)

        forearmLen = forearmPosition.subtract(wristPosition).length()
        self.forearmFKCtrl.scalePoints(Vec3(forearmLen, forearmFKCtrlSize, forearmFKCtrlSize))

        armEndXfo = Xfo()
        armEndXfo.tr = wristPosition
        armEndXfo.ori = forearmXfo.ori
        self.armEndXfoOutput.xfo = armEndXfo
        self.armEndPosOutput.xfo = armEndXfo

        upVXfo = xfoFromDirAndUpV(bicepPosition, wristPosition, forearmPosition)
        upVXfo.tr = forearmPosition
        upVOffset = Vec3(0, 0, 5)
        upVOffset = upVXfo.transformVector(upVOffset)
        self.armUpVCtrlSrtBuffer.xfo.tr = upVOffset
        self.armUpVCtrl.xfo.tr = upVOffset
        
        self.rightSideInputAttr.setValue(location is 'R')
        self.armBone1LenInputAttr.setMin(bicepLen)
        self.armBone1LenInputAttr.setMax(bicepLen)
        self.armBone1LenInputAttr.setValue(bicepLen)
        self.armBone2LenInputAttr.setMin(forearmLen)
        self.armBone2LenInputAttr.setMax(forearmLen)
        self.armBone2LenInputAttr.setValue(forearmLen)



    def buildRig(self, parent):
        pass

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(ArmComponent)
