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
from kraken.core.objects.layer import Layer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class InsectLegComponentGuide(Component):
    """InsectLeg Component Guide"""

    def __init__(self, name='InsectLeg', parent=None):
        super(InsectLegComponentGuide, self).__init__(name, parent)

        self.legCtrls = []
        for i in xrange(5):
            self.legCtrls.append(Control('leg' + str(i).zfill(2), parent=self, shape="sphere"))

        self.loadData({
                       "name": name,
                       "location": "L",
                       "jointPositions": [
                                          Vec3(0.9811, 9.769, -1.237),
                                          Vec3(5.4488, 8.4418, -1.237),
                                          Vec3(4.0, 3.1516, -1.237),
                                          Vec3(6.841, 1.0, -1.237),
                                          Vec3(9.841, 0.0, -1.237)
                                         ]
                      })


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        jointPositions = []
        for i in xrange(5):
            jointPositions.append(self.legCtrls[i].xfo.tr)

        data = {
            "name": self.getName(),
            "location": self.getLocation(),
            "jointPositions": jointPositions
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

        for i in xrange(5):
            self.legCtrls[i].xfo.tr = data['jointPositions'][i]

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        # values

        # Calculate Xfos
        fw = Vec3(0, 0, 1)
        boneXfos = []
        boneLengths = []

        for i in xrange(4):
            boneVec = self.legCtrls[i + 1].xfo.tr.subtract(self.legCtrls[i].xfo.tr)
            boneLengths.append(boneVec.length())
            bone1Normal = fw.cross(boneVec).unit()
            bone1ZAxis = boneVec.cross(bone1Normal).unit()

            xfo = Xfo()
            xfo.setFromVectors(boneVec.unit(), bone1Normal, bone1ZAxis, self.legCtrls[i].xfo.tr)

            boneXfos.append(xfo)

        return {
                "class":"kraken.examples.insectleg_component.InsectLegComponent",
                "name": self.getName(),
                "location": self.getLocation(),
                "boneXfos": boneXfos,
                "endXfo": self.legCtrls[-1].xfo,
                "boneLengths": boneLengths
                }


class InsectLegComponent(Component):
    """Insect Leg Component"""

    def __init__(self, name='InsectLeg', parent=None):

        Profiler.getInstance().push("Construct InsectLeg Component:" + name)
        super(InsectLegComponent, self).__init__(name, parent)

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

        # FK
        self.fkCtrlSpaces = []
        self.boneFKCtrls = []
        for i in xrange(4):
            if i==0:
                parent = ctrlCmpGrp
            else:
                parent = self.boneFKCtrls[i - 1]

            boneName = 'bone' + str(i).zfill(2) + 'FK'
            boneFKCtrlSpace = CtrlSpace(boneName, parent=parent)

            boneFKCtrl = Control(boneName, parent=boneFKCtrlSpace, shape="cube")
            boneFKCtrl.alignOnXAxis()

            self.fkCtrlSpaces.append(boneFKCtrlSpace)
            self.boneFKCtrls.append(boneFKCtrl)

        # IK Control
        self.legIKCtrlSpace = CtrlSpace('IK', parent=ctrlCmpGrp)
        self.legIKCtrl = Control('IK', parent=self.legIKCtrlSpace, shape="pin")

        if self.getLocation() == 'R':
            self.legIKCtrl.rotatePoints(0, 90, 0)
            self.legIKCtrl.translatePoints(Vec3(-1.0, 0.0, 0.0))
        else:
            self.legIKCtrl.rotatePoints(0, -90, 0)
            self.legIKCtrl.translatePoints(Vec3(1.0, 0.0, 0.0))

        # Add Component Params to IK control
        legDebugInputAttr = BoolAttribute('debug', True)
        legFkikInputAttr = FloatAttribute('fkik', 1.0, maxValue=1.0)
        self.legTipBoneLenInputAttr = FloatAttribute('tipBoneLen', 1.0)

        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings")
        self.legIKCtrl.addAttributeGroup(legSettingsAttrGrp)
        legSettingsAttrGrp.addAttribute(legDebugInputAttr)
        legSettingsAttrGrp.addAttribute(legFkikInputAttr)
        legSettingsAttrGrp.addAttribute(self.legTipBoneLenInputAttr)

        # UpV
        self.legUpVCtrlSpace = CtrlSpace('UpV', parent=ctrlCmpGrp)
        self.legUpVCtrl = Control('UpV', parent=self.legUpVCtrlSpace, shape="triangle")
        self.legUpVCtrl.alignOnZAxis()

        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        self.boneDefs = []
        for i in xrange(4):
            boneDef = Joint('bone' + str(i).zfill(2), parent=defCmpGrp)
            boneDef.setComponent(self)
            self.boneDefs.append(boneDef)

        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        self.rootInput = Locator('rootInput', parent=inputHrcGrp)

        self.boneOutputs = []
        for i in xrange(4):
            boneOutput = Locator('bone' + str(i).zfill(2), parent=outputHrcGrp)
            self.boneOutputs.append(boneOutput)

        self.legEndXfoOutput = Locator('legEndXfo', parent=outputHrcGrp)

        self.legEndPosOutput = Locator('legEndPos', parent=outputHrcGrp)


        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        fkikInputAttr = FloatAttribute('fkik', 1.0, maxValue=1.0)
        self.tipBoneLenInputAttr = FloatAttribute('tipBoneLen', 1.0)

        cmpInputAttrGrp.addAttribute(debugInputAttr)
        cmpInputAttrGrp.addAttribute(fkikInputAttr)
        cmpInputAttrGrp.addAttribute(self.tipBoneLenInputAttr)

        # Connect attrs to control attrs
        debugInputAttr.connect(legDebugInputAttr)
        fkikInputAttr.connect(legFkikInputAttr)
        self.tipBoneLenInputAttr.connect(self.legTipBoneLenInputAttr)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([self.legIKCtrl.getName(), 'To', self.rootInput.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(self.rootInput)
        self.fkCtrlSpaces[0].addConstraint(legRootInputConstraint)

        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(self.rootInput)

        for i in xrange(4):
            self.addOutput(self.boneOutputs[i])

        self.addOutput(self.legEndXfoOutput)
        self.addOutput(self.legEndPosOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(fkikInputAttr)
        self.addInput(self.tipBoneLenInputAttr)

        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        spliceOp = SpliceOperator("legSpliceOp", "NBoneIKSolver", "Kraken")
        self.addOperator(spliceOp)

        # # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("ikblend", fkikInputAttr)
        spliceOp.setInput("tipBoneLen", self.tipBoneLenInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("ikgoal", self.legIKCtrl)
        # spliceOp.setInput("upV", legUpVCtrl)

        for i in xrange(len(self.boneFKCtrls)):
            spliceOp.setInput("fkcontrols", self.boneFKCtrls[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneOutputs)):
            spliceOp.setOutput("pose", self.boneOutputs[i])

        spliceOp.setOutput("legEnd", self.legEndPosOutput)

        # Add Deformer Splice Op
        outputsToDeformersSpliceOp = SpliceOperator("insectLegDeformerSpliceOp", "MultiPoseConstraintSolver", "Kraken")
        self.addOperator(outputsToDeformersSpliceOp)

        # Add Att Inputs
        outputsToDeformersSpliceOp.setInput("debug", debugInputAttr)

        # Add Xfo Inputs
        for i in xrange(len(self.boneOutputs)):
            outputsToDeformersSpliceOp.setInput("constrainers", self.boneOutputs[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneOutputs)):
            outputsToDeformersSpliceOp.setOutput("constrainees", self.boneDefs[i])

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'InsectLeg'))
        location = data.get('location', 'M')
        self.setLocation(location)

        boneXfos = data['boneXfos']
        boneLengths = data['boneLengths']

        for i, each in enumerate(self.fkCtrlSpaces):
            self.fkCtrlSpaces[i].xfo = boneXfos[i]
            self.boneFKCtrls[i].xfo = boneXfos[i]

            self.boneFKCtrls[i].scalePoints(Vec3(boneLengths[i], 1.75, 1.75))

        self.legIKCtrlSpace.xfo = data['endXfo']
        self.legIKCtrl.xfo = data['endXfo']

        tipBoneLen = boneLengths[len(boneLengths) - 1]
        self.legTipBoneLenInputAttr.setMax(tipBoneLen * 2.0)
        self.legTipBoneLenInputAttr.setValue(tipBoneLen)

        upVOffset = boneXfos[1].transformVector(Vec3(0, 0, 5))
        self.legUpVCtrlSpace.xfo.tr = upVOffset
        self.legUpVCtrl.xfo.tr = upVOffset


        # ============
        # Set IO Xfos
        # ============
        self.rootInput.xfo = boneXfos[0]

        for i in xrange(4):
            self.boneOutputs[i].xfo = boneXfos[i]

        self.legEndXfoOutput.xfo = data['endXfo']
        self.legEndPosOutput.xfo = data['endXfo']

        # =============
        # Set IO Attrs
        # =============
        self.tipBoneLenInputAttr.setMax(tipBoneLen * 2.0)
        self.tipBoneLenInputAttr.setValue(tipBoneLen)


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(InsectLegComponent)
