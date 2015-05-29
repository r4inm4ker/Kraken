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


class InsectLegComponent(Component):
    """Insect Leg Base"""

    def __init__(self, name='InsectLegBase', parent=None):

        super(InsectLegComponent, self).__init__(name, parent)

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
        self.rootInputTgt = self.createInput('rootInput', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.boneOutputs = self.addOutput('boneOutputs', dataType='Xfo[]')

        self.legEndXfoOutputTgt = self.createOutput('legEndXfoOutput', dataType='Xfo', parent=self.outputHrcGrp)
        self.legEndPosOutputTgt = self.createOutput('legEndPosOutput', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=True, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)
        self.tipBoneLenInputAttr = self.createInput('tipBoneLen', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs



class InsectLegComponentGuide(InsectLegComponent):
    """InsectLeg Component Guide"""

    def __init__(self, name='InsectLeg', parent=None, data=None):

        Profiler.getInstance().push("Construct InsectLeg Guide Component:" + name)
        super(InsectLegComponentGuide, self).__init__(name, parent)

        self.legCtrls = []
        for i in xrange(5):
            self.legCtrls.append(Control('leg' + str(i).zfill(2), parent=self, shape="sphere"))

        if data is None:
            data = {
               "location": "L",
               "jointPositions": [
                  Vec3(0.9811, 9.769, -1.237),
                  Vec3(5.4488, 8.4418, -1.237),
                  Vec3(4.0, 3.1516, -1.237),
                  Vec3(6.841, 1.0, -1.237),
                  Vec3(9.841, 0.0, -1.237)
                 ]
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

        if 'name' in data:
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

        data = {
                "class":"kraken.examples.insectleg_component.InsectLegComponentRig",
                "name": self.getName(),
                "location": self.getLocation(),
                "boneXfos": boneXfos,
                "endXfo": self.legCtrls[-1].xfo,
                "boneLengths": boneLengths
               }

        return data


class InsectLegComponentRig(InsectLegComponent):
    """Insect Leg Rig"""

    def __init__(self, name='InsectLeg', parent=None):

        Profiler.getInstance().push("Construct InsectLeg Rig Component:" + name)
        super(InsectLegComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # FK
        self.fkCtrlSpaces = []
        self.boneFKCtrls = []
        for i in xrange(4):
            if i==0:
                parent = self.ctrlCmpGrp
            else:
                parent = self.boneFKCtrls[i - 1]

            boneName = 'bone' + str(i).zfill(2) + 'FK'
            boneFKCtrlSpace = CtrlSpace(boneName, parent=parent)

            boneFKCtrl = Control(boneName, parent=boneFKCtrlSpace, shape="cube")
            boneFKCtrl.alignOnXAxis()

            self.fkCtrlSpaces.append(boneFKCtrlSpace)
            self.boneFKCtrls.append(boneFKCtrl)

        # IK Control
        self.legIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.legIKCtrl = Control('IK', parent=self.legIKCtrlSpace, shape="pin")

        if self.getLocation() == 'R':
            self.legIKCtrl.rotatePoints(0, 90, 0)
            self.legIKCtrl.translatePoints(Vec3(-1.0, 0.0, 0.0))
        else:
            self.legIKCtrl.rotatePoints(0, -90, 0)
            self.legIKCtrl.translatePoints(Vec3(1.0, 0.0, 0.0))

        # Add Component Params to IK control
        legSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings", parent=self.legIKCtrl)
        legdrawDebugInputAttr = BoolAttribute('drawDebug', value=True, parent=legSettingsAttrGrp)
        legUseInitPoseInputAttr = BoolAttribute('useInitPose', value=False, parent=legSettingsAttrGrp)
        legFkikInputAttr = FloatAttribute('fkik', value=1.0, minValue=0.0,
            maxValue=1.0, parent=legSettingsAttrGrp)

        # Connect IO to controls
        self.drawDebugInputAttr.connect(legdrawDebugInputAttr)

        # UpV
        self.legUpVCtrlSpace = CtrlSpace('UpV', parent=self.ctrlCmpGrp)
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
        self.boneOutputsTgt = []
        for i in xrange(4):
            boneOutput = Locator('bone' + str(i).zfill(2), parent=self.outputHrcGrp)
            self.boneOutputsTgt.append(boneOutput)

        # Set IO Targets
        self.boneOutputs.setTarget(self.boneOutputsTgt)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([self.legIKCtrl.getName(), 'To', self.rootInputTgt.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(self.rootInputTgt)
        self.fkCtrlSpaces[0].addConstraint(legRootInputConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        self.NBoneSolverSpliceOp = SpliceOperator('legSpliceOp', 'NBoneIKSolver', 'Kraken')
        self.addOperator(self.NBoneSolverSpliceOp)

        # # Add Att Inputs
        self.NBoneSolverSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.NBoneSolverSpliceOp.setInput('useInitPose', legUseInitPoseInputAttr)
        self.NBoneSolverSpliceOp.setInput('ikblend', legFkikInputAttr)
        self.NBoneSolverSpliceOp.setInput('tipBoneLen', self.tipBoneLenInputAttr)

        # Add Xfo Inputs
        self.NBoneSolverSpliceOp.setInput('ikgoal', self.legIKCtrl)
        # self.NBoneSolverSpliceOp.setInput('upV', legUpVCtrl)

        for i in xrange(len(self.boneFKCtrls)):
            self.NBoneSolverSpliceOp.setInput('fkcontrols', self.boneFKCtrls[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneOutputsTgt)):
            self.NBoneSolverSpliceOp.setOutput('pose', self.boneOutputsTgt[i])

        self.NBoneSolverSpliceOp.setOutput('legEnd', self.legEndPosOutputTgt)

        # Add Deformer Splice Op
        self.outputsToDeformersSpliceOp = SpliceOperator('insectLegDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersSpliceOp)

        # Add Att Inputs
        self.outputsToDeformersSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        for i in xrange(len(self.boneOutputsTgt)):
            self.outputsToDeformersSpliceOp.setInput('constrainers', self.boneOutputsTgt[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneDefs)):
            self.outputsToDeformersSpliceOp.setOutput('constrainees', self.boneDefs[i])

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

        upVOffset = boneXfos[1].transformVector(Vec3(0, 0, 5))
        self.legUpVCtrlSpace.xfo.tr = upVOffset
        self.legUpVCtrl.xfo.tr = upVOffset


        # ============
        # Set IO Xfos
        # ============
        self.rootInputTgt.xfo = boneXfos[0]

        for i in xrange(4):
            self.boneOutputsTgt[i].xfo = boneXfos[i]

        self.legEndXfoOutputTgt.xfo = data['endXfo']
        self.legEndPosOutputTgt.xfo = data['endXfo']

        # =============
        # Set IO Attrs
        # =============
        tipBoneLen = boneLengths[len(boneLengths) - 1]
        self.tipBoneLenInputAttr.setMax(tipBoneLen * 2.0)
        self.tipBoneLenInputAttr.setValue(tipBoneLen)


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(InsectLegComponentGuide)
ks.registerComponent(InsectLegComponentRig)
