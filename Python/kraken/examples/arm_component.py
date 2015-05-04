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
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler


class ArmComponent(Component):
    """Arm Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Arm Component:" + name + " location:" + location)
        super(ArmComponent, self).__init__(name, parent, location)
        # =========
        # Controls
        # =========
        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

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
        bicepXfo = Xfo()
        bicepXfo.setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, bicepPosition)

        # Calculate Forearm Xfo
        elbowToWrist = wristPosition.subtract(forearmPosition).unit()
        elbowToRoot = bicepPosition.subtract(forearmPosition).unit()
        bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
        bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()
        forearmXfo = Xfo()
        forearmXfo.setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, forearmPosition)

        # Bicep
        bicepFKCtrlSpace = CtrlSpace('bicepFK', parent=self)
        bicepFKCtrlSpace.xfo = bicepXfo

        bicepFKCtrl = Control('bicepFK', parent=bicepFKCtrlSpace, shape="cube")
        bicepFKCtrl.alignOnXAxis()
        bicepLen = bicepPosition.subtract(forearmPosition).length()
        bicepFKCtrl.scalePoints(Vec3(bicepLen, bicepFKCtrlSize, bicepFKCtrlSize))
        bicepFKCtrl.xfo = bicepXfo

        # Forearm
        forearmFKCtrlSpace = CtrlSpace('forearmFK', parent=bicepFKCtrl)
        forearmFKCtrlSpace.xfo = forearmXfo

        forearmFKCtrl = Control('forearmFK', parent=forearmFKCtrlSpace, shape="cube")
        forearmFKCtrl.alignOnXAxis()
        forearmLen = forearmPosition.subtract(wristPosition).length()
        forearmFKCtrl.scalePoints(Vec3(forearmLen, forearmFKCtrlSize, forearmFKCtrlSize))
        forearmFKCtrl.xfo = forearmXfo

        # Arm IK
        armIKCtrlSpace = CtrlSpace('IK', parent=self)
        armIKCtrlSpace.xfo.tr = wristPosition

        armIKCtrl = Control('IK', parent=armIKCtrlSpace, shape="pin")
        armIKCtrl.xfo = armIKCtrlSpace.xfo

        if self.getLocation() == "R":
            armIKCtrl.rotatePoints(0, 90, 0)
        else:
            armIKCtrl.rotatePoints(0, -90, 0)


        # Add Component Params to IK control
        armDebugInputAttr = BoolAttribute('debug', True)
        armBone1LenInputAttr = FloatAttribute('bone1Len', bicepLen)
        armBone2LenInputAttr = FloatAttribute('bone2Len', forearmLen)
        armFkikInputAttr = FloatAttribute('fkik', 0.0)
        armSoftIKInputAttr = BoolAttribute('softIK', True)
        armSoftDistInputAttr = FloatAttribute('softDist', 0.0)
        armStretchInputAttr = BoolAttribute('stretch', True)
        armStretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)

        armSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings")
        armIKCtrl.addAttributeGroup(armSettingsAttrGrp)
        armSettingsAttrGrp.addAttribute(armDebugInputAttr)
        armSettingsAttrGrp.addAttribute(armBone1LenInputAttr)
        armSettingsAttrGrp.addAttribute(armBone2LenInputAttr)
        armSettingsAttrGrp.addAttribute(armFkikInputAttr)
        armSettingsAttrGrp.addAttribute(armSoftIKInputAttr)
        armSettingsAttrGrp.addAttribute(armSoftDistInputAttr)
        armSettingsAttrGrp.addAttribute(armStretchInputAttr)
        armSettingsAttrGrp.addAttribute(armStretchBlendInputAttr)

        # UpV
        upVXfo = xfoFromDirAndUpV(bicepPosition, wristPosition, forearmPosition)
        upVXfo.tr = forearmPosition
        upVOffset = Vec3(0, 0, 5)
        upVOffset = upVXfo.transformVector(upVOffset)

        armUpVCtrlSpace = CtrlSpace('UpV', parent=self)
        armUpVCtrlSpace.xfo.tr = upVOffset

        armUpVCtrl = Control('UpV', parent=armUpVCtrlSpace, shape="triangle")
        armUpVCtrl.xfo.tr = upVOffset
        armUpVCtrl.alignOnZAxis()
        armUpVCtrl.rotatePoints(180, 0, 0)


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
        clavicleEndInput.xfo = bicepXfo

        bicepOutput = Locator('bicep')
        bicepOutput.xfo = bicepXfo
        forearmOutput = Locator('forearm')
        forearmOutput.xfo = forearmXfo

        armEndXfo = Xfo()
        armEndXfo.ori = forearmXfo.ori
        armEndXfo.tr = wristPosition
        armEndXfoOutput = Locator('armEndXfo')
        armEndXfoOutput.xfo = armEndXfo

        armEndPosOutput = Locator('armEndPos')
        armEndPosOutput.xfo = armEndXfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        bone1LenInputAttr = FloatAttribute('bone1Len', bicepLen)
        bone2LenInputAttr = FloatAttribute('bone2Len', forearmLen)
        fkikInputAttr = FloatAttribute('fkik', 0.0)
        softIKInputAttr = BoolAttribute('softIK', True)
        softDistInputAttr = FloatAttribute('softDist', 0.5)
        stretchInputAttr = BoolAttribute('stretch', True)
        stretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')

        # Connect attrs to control attrs
        debugInputAttr.connect(armDebugInputAttr)
        bone1LenInputAttr.connect(armBone1LenInputAttr)
        bone2LenInputAttr.connect(armBone2LenInputAttr)
        fkikInputAttr.connect(armFkikInputAttr)
        softIKInputAttr.connect(armSoftIKInputAttr)
        softDistInputAttr.connect(armSoftDistInputAttr)
        stretchInputAttr.connect(armStretchInputAttr)
        stretchBlendInputAttr.connect(armStretchBlendInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        armRootInputConstraint = PoseConstraint('_'.join([armIKCtrl.getName(), 'To', clavicleEndInput.getName()]))
        armRootInputConstraint.setMaintainOffset(True)
        armRootInputConstraint.addConstrainer(clavicleEndInput)
        bicepFKCtrlSpace.addConstraint(armRootInputConstraint)

        # Constraint outputs


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(clavicleEndInput)
        self.addOutput(bicepOutput)
        self.addOutput(forearmOutput)
        self.addOutput(armEndXfoOutput)
        self.addOutput(armEndPosOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(bone1LenInputAttr)
        self.addInput(bone2LenInputAttr)
        self.addInput(fkikInputAttr)
        self.addInput(softIKInputAttr)
        self.addInput(softDistInputAttr)
        self.addInput(stretchInputAttr)
        self.addInput(stretchBlendInputAttr)
        self.addInput(rightSideInputAttr)


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
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # # Add Xfo Inputs
        # spliceOp.setInput("root", clavicleEndInput)
        # spliceOp.setInput("bone1FK", bicepFKCtrl)
        # spliceOp.setInput("bone2FK", forearmFKCtrl)
        # spliceOp.setInput("ikHandle", armIKCtrl)
        # spliceOp.setInput("upV", armUpVCtrl)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Out", bicepOutput)
        # spliceOp.setOutput("bone02Out", forearmOutput)
        # spliceOp.setOutput("bone03Out", armEndXfoOutput)
        # spliceOp.setOutput("bone03PosOut", armEndPosOutput)


        # # Add Deformer Splice Op
        # spliceOp = SpliceOperator("armDeformerSpliceOp", "LimbConstraintSolver", "KrakenLimbSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)

        # # Add Xfo Inputs
        # spliceOp.setInput("bone01Constrainer", bicepOutput)
        # spliceOp.setInput("bone02Constrainer", forearmOutput)
        # spliceOp.setInput("bone03Constrainer", armEndXfoOutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Deformer", bicepDef)
        # spliceOp.setOutput("bone02Deformer", forearmDef)
        # spliceOp.setOutput("bone03Deformer", wristDef)


        Profiler.getInstance().pop()

    def buildRig(self, parent):
        pass

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(ArmComponent)
