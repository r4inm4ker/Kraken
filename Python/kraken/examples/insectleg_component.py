from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.base_component import BaseComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.layer import Layer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator


from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler

class InsectLegComponent(BaseComponent):
    """Leg Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')
        
        Profiler.getInstance().push("Construct InsectLeg Component:" + name + " location:" + location)
        super(InsectLegComponent, self).__init__(name, parent, location)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        jointPositions = []

        if self.getLocation() == "R":
            jointPositions.append(Vec3(-0.9811, 9.769, -0.4572))
            jointPositions.append(Vec3(-5.4488, 8.4418, -0.5348))
            jointPositions.append(Vec3(-4.0, 3.1516, -1.237))
            jointPositions.append(Vec3(-6.841, 1.0, -1.237))
            jointPositions.append(Vec3(-9.841, 0.0, -1.237))
        else:
            jointPositions.append(Vec3(0.9811, 9.769, -0.4572))
            jointPositions.append(Vec3(5.4488, 8.4418, -0.5348))
            jointPositions.append(Vec3(4.0, 3.1516, -1.237))
            jointPositions.append(Vec3(6.841, 1.0, -1.237))
            jointPositions.append(Vec3(9.841, 0.0, -1.237))

        # Calculate Xfos
        fw = Vec3(0, 0, 1)
        boneXfos = []
        boneLengths = []
        for i in range(len(jointPositions)-1):
            boneVec = jointPositions[i+1].subtract(jointPositions[i])
            boneLengths.append(boneVec.length())
            bone1Normal = fw.cross(boneVec).unit()
            bone1ZAxis = boneVec.cross(bone1Normal).unit()
            xfo = Xfo()
            xfo.setFromVectors(boneVec.unit(), bone1Normal, bone1ZAxis, jointPositions[i])
            boneXfos.append(xfo)


        fkCtrlSrtBuffers = []
        boneFKCtrls = []
        for i in range(len(boneXfos)):
            if i==0:
                parent = self
            else:
                parent = boneFKCtrls[i-1]

            boneFKCtrlSrtBuffer = SrtBuffer('bone'+str(i)+'FK', parent=parent)
            boneFKCtrlSrtBuffer.xfo = boneXfos[i]

            boneFKCtrl = Control('bone'+str(i)+'FK', parent=boneFKCtrlSrtBuffer, shape="cube")
            boneFKCtrl.alignOnXAxis()
            boneFKCtrl.scalePoints(Vec3(boneLengths[i], 1.75, 1.75))
            boneFKCtrl.xfo = boneXfos[i]

            fkCtrlSrtBuffers.append(boneFKCtrlSrtBuffer)
            boneFKCtrls.append(boneFKCtrl)


        # IKControl
        legIKCtrlSrtBuffer = SrtBuffer('IK', parent=self)
        legIKCtrlSrtBuffer.xfo.tr = jointPositions[-1]

        legIKCtrl = Control('IK', parent=legIKCtrlSrtBuffer, shape="pin")
        legIKCtrl.xfo.tr = jointPositions[-1]

        if self.getLocation() == "R":
            legIKCtrl.rotatePoints(0, 90, 0)
            legIKCtrl.translatePoints(Vec3(-1.0, 0.0, 0.0))
        else:
            legIKCtrl.rotatePoints(0, -90, 0)
            legIKCtrl.translatePoints(Vec3(1.0, 0.0, 0.0))

        # Add Component Params to IK control
        legDebugInputAttr = BoolAttribute('debug', True)
        legFkikInputAttr = FloatAttribute('fkik', 1.0, 0.0, 1.0)
        legSoftIKInputAttr = BoolAttribute('softIK', True)
        legSoftDistInputAttr = FloatAttribute('softDist', 0.0, 0.0, 1.0)
        legStretchInputAttr = BoolAttribute('stretch', True)
        legStretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0, 0.0, 1.0)

        tipBoneLen = boneLengths[len(boneLengths)-1]
        legTipBoneLenInputAttr = FloatAttribute('tipBoneLen', tipBoneLen, 0.0, tipBoneLen * 3.0)

        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings")
        legIKCtrl.addAttributeGroup(legSettingsAttrGrp)
        legSettingsAttrGrp.addAttribute(legDebugInputAttr)
        legSettingsAttrGrp.addAttribute(legFkikInputAttr)
        legSettingsAttrGrp.addAttribute(legSoftIKInputAttr)
        legSettingsAttrGrp.addAttribute(legSoftDistInputAttr)
        legSettingsAttrGrp.addAttribute(legStretchInputAttr)
        legSettingsAttrGrp.addAttribute(legStretchBlendInputAttr)
        legSettingsAttrGrp.addAttribute(legTipBoneLenInputAttr)

        # UpV
        upVOffset = boneXfos[1].transformVector(Vec3(0, 0, 5))

        legUpVCtrlSrtBuffer = SrtBuffer('UpV', parent=self)
        legUpVCtrlSrtBuffer.xfo.tr = upVOffset

        legUpVCtrl = Control('UpV', parent=legUpVCtrlSrtBuffer, shape="triangle")
        legUpVCtrl.xfo.tr = upVOffset
        legUpVCtrl.alignOnZAxis()
        legUpVCtrl.rotatePoints(0, 0, 0)

        # ==========
        # Deformers
        # ==========

        deformersLayer = self.getLayer('deformers')
        boneDefs = []
        for i in range(len(boneXfos)):
            boneDef = Joint('bone'+str(i))
            boneDef.setComponent(self)
            boneDefs.append(boneDef)
            deformersLayer.addChild(boneDef)

        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        rootInput = Locator('rootInput')
        rootInput.xfo = boneXfos[0]

        boneOutputs = []
        for i in range(len(boneXfos)):
            boneOutput = Locator('bone'+str(i))
            boneOutput.xfo = boneXfos[i]
            boneOutputs.append(boneOutput)

        legEndXfo = boneXfos[len(boneXfos)-1]
        legEndXfo.tr = jointPositions[len(jointPositions)-1]
        legEndXfoOutput = Locator('legEndXfo')
        legEndXfoOutput.xfo = legEndXfo

        legEndPosOutput = Locator('legEndPos')
        legEndPosOutput.xfo = legEndXfo


        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        fkikInputAttr = FloatAttribute('fkik', 1.0, 0.0, 1.0)
        softIKInputAttr = BoolAttribute('softIK', True)
        softDistInputAttr = FloatAttribute('softDist', 0.5, 0.0, 1.0)
        stretchInputAttr = BoolAttribute('stretch', True)
        stretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0, 0.0, 1.0)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')
        tipBoneLenInputAttr = FloatAttribute('tipBoneLen', tipBoneLen, 0.0, tipBoneLen * 2.0)

        # Connect attrs to control attrs
        debugInputAttr.connect(legDebugInputAttr)
        fkikInputAttr.connect(legFkikInputAttr)
        softIKInputAttr.connect(legSoftIKInputAttr)
        softDistInputAttr.connect(legSoftDistInputAttr)
        stretchInputAttr.connect(legStretchInputAttr)
        stretchBlendInputAttr.connect(legStretchBlendInputAttr)

        tipBoneLenInputAttr.connect(legTipBoneLenInputAttr)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([legIKCtrl.getName(), 'To', rootInput.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(rootInput)
        fkCtrlSrtBuffers[0].addConstraint(legRootInputConstraint)

        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(rootInput)
        for i in range(len(boneOutputs)):
            self.addOutput(boneOutputs[i])
        self.addOutput(legEndXfoOutput)
        self.addOutput(legEndPosOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(fkikInputAttr)
        self.addInput(softIKInputAttr)
        self.addInput(softDistInputAttr)
        self.addInput(stretchInputAttr)
        self.addInput(stretchBlendInputAttr)
        self.addInput(rightSideInputAttr)
        self.addInput(tipBoneLenInputAttr)

        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        spliceOp = SpliceOperator("legSpliceOp", "NBoneIKSolver", "Kraken")
        self.addOperator(spliceOp)

        # # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("bone1Len", bone1LenInputAttr)
        spliceOp.setInput("ikblend", fkikInputAttr)
        spliceOp.setInput("tipBoneLen", tipBoneLenInputAttr)
        # spliceOp.setInput("softIK", softIKInputAttr)
        # spliceOp.setInput("softDist", softDistInputAttr)
        # spliceOp.setInput("stretch", stretchInputAttr)
        # spliceOp.setInput("stretchBlend", stretchBlendInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("ikgoal", legIKCtrl)
        # spliceOp.setInput("upV", legUpVCtrl)

        for i in range(len(boneFKCtrls)):
            spliceOp.setInput("fkcontrols", boneFKCtrls[i])

        # Add Xfo Outputs
        for i in range(len(boneOutputs)):
            spliceOp.setOutput("pose", boneOutputs[i])
        spliceOp.setOutput("legEnd", legEndPosOutput)

        # Add Deformer Splice Op
        outputsToDeformersSpliceOp = SpliceOperator("spineDeformerSpliceOp", "MultiPoseConstraintSolver", "Kraken")
        self.addOperator(outputsToDeformersSpliceOp)

        # Add Att Inputs
        outputsToDeformersSpliceOp.setInput("debug", debugInputAttr)

        # Add Xfo Inputs
        for i in range(len(boneOutputs)):
            outputsToDeformersSpliceOp.setInput("constrainers", boneOutputs[i])

        # Add Xfo Outputs
        for i in range(len(boneOutputs)):
            outputsToDeformersSpliceOp.setOutput("constrainees", boneDefs[i])

        Profiler.getInstance().pop()

    def buildRig(self, parent):
        pass

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(InsectLegComponent)

