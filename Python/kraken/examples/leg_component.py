from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class LegComponent(Component):
    """Leg Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Leg Component:" + name + " location:" + location)
        super(LegComponent, self).__init__(name, parent, location)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Input values
        femurPosition = data['femurPosition']
        kneePosition = data['kneePosition']
        anklePosition = data['anklePosition']

        # Calculate Femur Xfo
        rootToAnkle = anklePosition.subtract(femurPosition).unit()
        rootToKnee = kneePosition.subtract(femurPosition).unit()
        bone1Normal = rootToAnkle.cross(rootToKnee).unit()
        bone1ZAxis = rootToKnee.cross(bone1Normal).unit()
        femurXfo = Xfo()
        femurXfo.setFromVectors(rootToKnee, bone1Normal, bone1ZAxis, femurPosition)

        # Calculate Shin Xfo
        kneeToAnkle = anklePosition.subtract(kneePosition).unit()
        kneeToRoot = femurPosition.subtract(kneePosition).unit()
        bone2Normal = kneeToRoot.cross(kneeToAnkle).unit()
        bone2ZAxis = kneeToAnkle.cross(bone2Normal).unit()
        shinXfo = Xfo()
        shinXfo.setFromVectors(kneeToAnkle, bone2Normal, bone2ZAxis, kneePosition)


        # Femur
        femurFKCtrlSpace = CtrlSpace('femurFK', parent=self)
        femurFKCtrlSpace.xfo = femurXfo

        femurFKCtrl = Control('femurFK', parent=femurFKCtrlSpace, shape="cube")
        femurFKCtrl.alignOnXAxis()
        femurLen = femurPosition.subtract(kneePosition).length()
        femurFKCtrl.scalePoints(Vec3(femurLen, 1.75, 1.75))
        femurFKCtrl.xfo = femurXfo


        # Shin
        shinFKCtrlSpace = CtrlSpace('shinFK', parent=femurFKCtrl)
        shinFKCtrlSpace.xfo = shinXfo

        shinFKCtrl = Control('shinFK', parent=shinFKCtrlSpace, shape="cube")
        shinFKCtrl.alignOnXAxis()
        shinLen = kneePosition.subtract(anklePosition).length()
        shinFKCtrl.scalePoints(Vec3(shinLen, 1.5, 1.5))
        shinFKCtrl.xfo = shinXfo


        # Ankle
        legIKCtrlSpace = CtrlSpace('IK', parent=self)
        legIKCtrlSpace.xfo.tr = anklePosition

        legIKCtrl = Control('IK', parent=legIKCtrlSpace, shape="pin")
        legIKCtrl.xfo.tr = anklePosition

        if self.getLocation() == "R":
            legIKCtrl.rotatePoints(0, 90, 0)
            legIKCtrl.translatePoints(Vec3(-1.0, 0.0, 0.0))
        else:
            legIKCtrl.rotatePoints(0, -90, 0)
            legIKCtrl.translatePoints(Vec3(1.0, 0.0, 0.0))


        # Add Component Params to IK control
        legDebugInputAttr = BoolAttribute('debug', True)
        legBone1LenInputAttr = FloatAttribute('bone1Len', femurLen)
        legBone1LenInputAttr.setMax(100.0)
        legBone2LenInputAttr = FloatAttribute('bone2Len', shinLen)
        legBone2LenInputAttr.setMax(100.0)
        legFkikInputAttr = FloatAttribute('fkik', 1.0)
        legFkikInputAttr.setMax(1.0)
        legSoftIKInputAttr = BoolAttribute('softIK', True)
        legSoftDistInputAttr = FloatAttribute('softDist', 0.0)
        legStretchInputAttr = BoolAttribute('stretch', True)
        legStretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)

        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings")
        legIKCtrl.addAttributeGroup(legSettingsAttrGrp)
        legSettingsAttrGrp.addAttribute(legDebugInputAttr)
        legSettingsAttrGrp.addAttribute(legBone1LenInputAttr)
        legSettingsAttrGrp.addAttribute(legBone2LenInputAttr)
        legSettingsAttrGrp.addAttribute(legFkikInputAttr)
        legSettingsAttrGrp.addAttribute(legSoftIKInputAttr)
        legSettingsAttrGrp.addAttribute(legSoftDistInputAttr)
        legSettingsAttrGrp.addAttribute(legStretchInputAttr)
        legSettingsAttrGrp.addAttribute(legStretchBlendInputAttr)


        # UpV
        upVXfo = xfoFromDirAndUpV(femurPosition, anklePosition, kneePosition)
        upVXfo.tr = kneePosition
        upVOffset = Vec3(0, 0, 5)
        upVOffset = upVXfo.transformVector(upVOffset)

        legUpVCtrlSpace = CtrlSpace('UpV', parent=self)
        legUpVCtrlSpace.xfo.tr = upVOffset

        legUpVCtrl = Control('UpV', parent=legUpVCtrlSpace, shape="triangle")
        legUpVCtrl.xfo.tr = upVOffset
        legUpVCtrl.alignOnZAxis()
        legUpVCtrl.rotatePoints(0, 0, 0)


        # ==========
        # Deformers
        # ==========

        femurDef = Joint('femur')
        femurDef.setComponent(self)

        shinDef = Joint('shin')
        shinDef.setComponent(self)

        ankleDef = Joint('ankle')
        ankleDef.setComponent(self)

        deformersLayer = self.getLayer('deformers')
        deformersLayer.addChild(femurDef)
        deformersLayer.addChild(shinDef)
        deformersLayer.addChild(ankleDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        legPelvisInput = Locator('pelvisInput')
        legPelvisInput.xfo = femurXfo

        femurOutput = Locator('femur')
        femurOutput.xfo = femurXfo
        shinOutput = Locator('shin')
        shinOutput.xfo = shinXfo

        legEndXfo = Xfo()
        legEndXfo.ori = shinXfo.ori
        legEndXfo.tr = anklePosition
        legEndXfoOutput = Locator('legEndXfo')
        legEndXfoOutput.xfo = legEndXfo

        legEndPosOutput = Locator('legEndPos')
        legEndPosOutput.xfo = legEndXfo


        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        bone1LenInputAttr = FloatAttribute('bone1Len', femurLen)
        bone1LenInputAttr.setMax(100.0)
        bone2LenInputAttr = FloatAttribute('bone2Len', shinLen)
        bone2LenInputAttr.setMax(100.0)
        fkikInputAttr = FloatAttribute('fkik', 1.0)
        fkikInputAttr.setMax(1.0)
        softIKInputAttr = BoolAttribute('softIK', True)
        softDistInputAttr = FloatAttribute('softDist', 0.0)
        stretchInputAttr = BoolAttribute('stretch', True)
        stretchBlendInputAttr = FloatAttribute('stretchBlend', 0.0)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')


        # Connect attrs to control attrs
        debugInputAttr.connect(legDebugInputAttr)
        bone1LenInputAttr.connect(legBone1LenInputAttr)
        bone2LenInputAttr.connect(legBone2LenInputAttr)
        fkikInputAttr.connect(legFkikInputAttr)
        softIKInputAttr.connect(legSoftIKInputAttr)
        softDistInputAttr.connect(legSoftDistInputAttr)
        stretchInputAttr.connect(legStretchInputAttr)
        stretchBlendInputAttr.connect(legStretchBlendInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([legIKCtrl.getName(), 'To', legPelvisInput.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(legPelvisInput)
        femurFKCtrlSpace.addConstraint(legRootInputConstraint)

        # Constraint outputs


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(legPelvisInput)
        self.addOutput(femurOutput)
        self.addOutput(shinOutput)
        self.addOutput(legEndXfoOutput)
        self.addOutput(legEndPosOutput)

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
        # Add Splice Op
        # spliceOp = SpliceOperator("legSpliceOp", "LimbSolver", "KrakenLimbSolver")
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
        # spliceOp.setInput("root", legPelvisInput)
        # spliceOp.setInput("bone1FK", femurFKCtrl)
        # spliceOp.setInput("bone2FK", shinFKCtrl)
        # spliceOp.setInput("ikHandle", legIKCtrl)
        # spliceOp.setInput("upV", legUpVCtrl)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Out", femurOutput)
        # spliceOp.setOutput("bone02Out", shinOutput)
        # spliceOp.setOutput("bone03Out", legEndXfoOutput)
        # spliceOp.setOutput("bone03PosOut", legEndPosOutput)


        # # Add Deformer Splice Op
        # spliceOp = SpliceOperator("legDeformerSpliceOp", "LimbConstraintSolver", "KrakenLimbSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)

        # # Add Xfo Inputstrl)
        # spliceOp.setInput("bone01Constrainer", femurOutput)
        # spliceOp.setInput("bone02Constrainer", shinOutput)
        # spliceOp.setInput("bone03Constrainer", legEndXfoOutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("bone01Deformer", femurDef)
        # spliceOp.setOutput("bone02Deformer", shinDef)
        # spliceOp.setOutput("bone03Deformer", ankleDef)

        Profiler.getInstance().pop()


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(LegComponent)
