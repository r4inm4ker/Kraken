import math

from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

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
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)
        self.tipBoneLenInputAttr = self.createInput('tipBoneLen', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class InsectLegComponentGuide(InsectLegComponent):
    """InsectLeg Component Guide"""

    def __init__(self, name='InsectLeg', parent=None, data=None):

        Profiler.getInstance().push("Construct InsectLeg Guide Component:" + name)
        super(InsectLegComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.numDigits = IntegerAttribute('numDigits', value=8, minValue=0, maxValue=20, parent=guideSettingsAttrGrp)
        self.numDigits.setValueChangeCallback(self.updateNumLegControls)

        self.legCtrls = []
        if data is None:
            numDigits = self.numDigits.getValue() + 1
            halfPi = math.pi / 2.0
            step = halfPi / (numDigits - 1)

            yValues = []
            xValues = []
            for i in xrange(numDigits):
                yValues.append(math.sin((i * step) + halfPi) * 10)
                xValues.append(math.cos((i * step) + halfPi) * -10)

            for i in xrange(numDigits):
                self.legCtrls.append(Control('leg' + str(i).zfill(2), parent=self.ctrlCmpGrp, shape="sphere"))

            spacingY = 10.0 / numDigits - 1
            spacingZ = 5.0 / numDigits - 1

            jointPositions = []
            for i in xrange(numDigits):
                jointPositions.append(Vec3(xValues[i], yValues[i], 0.0))

            data = {
               "location": "L",
               "jointPositions": jointPositions,
               "numDigits": self.numDigits.getValue()
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

        data = super(InsectLegComponentGuide, self).saveData()

        jointPositions = []
        for i in xrange(len(self.legCtrls)):
            jointPositions.append(self.legCtrls[i].xfo.tr)

        data['jointPositions'] = jointPositions

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(InsectLegComponentGuide, self).loadData(data)

        numDigits = data['numDigits']
        numPositions = len(data['jointPositions'])
        if numPositions <= numDigits:
            raise IndexError("'jointPositions' (" + str(numPositions) + ") should be 1 more than 'numDigits' (" + str(numDigits) + ").")

        if numPositions > len(self.legCtrls):
            for i in xrange(len(self.legCtrls), numPositions):
                self.legCtrls.append(Control('leg' + str(i + 1).zfill(2), parent=self.ctrlCmpGrp, shape="sphere"))
        elif numPositions < len(self.legCtrls):
            numExtraCtrls = len(self.legCtrls) - numPositions
            for i in xrange(numExtraCtrls):
                self.legCtrls.pop()

        self.numDigits.setValue(numDigits)

        for i in xrange(numPositions):
            print i
            self.legCtrls[i].xfo.tr = data['jointPositions'][i]

        return True


    def updateNumLegControls(self, numDigits):
        """Load a saved guide representation from persisted data.

        Arguments:
        numDigits -- object, The number of joints inthe chain.

        Return:
        True if successful.

        """
        if numDigits == 0:
            raise IndexError("'numDigits' must be > 0")


        if numDigits > len(self.legCtrls):
            for i in xrange(len(self.legCtrls), numDigits):
                newCtrl = Control('leg' + str(i + 1).zfill(2), parent=self.ctrlCmpGrp, shape="sphere")
                # Generate thew new ctrl off the end of the existing one.
                newCtrl.xfo = self.legCtrls[i-1].xfo.multiply(Xfo(Vec3(10.0, 0.0, 0.0)))
                self.legCtrls.append(newCtrl)

        elif numDigits < len(self.legCtrls):
            numExtraCtrls = len(self.legCtrls) - numDigits
            for i in xrange(numExtraCtrls):
                self.legCtrls.pop()

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(InsectLegComponentGuide, self).getRigBuildData()

        numDigits = self.numDigits.getValue()

        # Calculate Xfos
        fw = Vec3(0, 0, 1)
        boneXfos = []
        boneLengths = []

        for i in xrange(numDigits):
            boneVec = self.legCtrls[i + 1].xfo.tr.subtract(self.legCtrls[i].xfo.tr)
            boneLengths.append(boneVec.length())
            bone1Normal = fw.cross(boneVec).unit()
            bone1ZAxis = boneVec.cross(bone1Normal).unit()

            xfo = Xfo()
            xfo.setFromVectors(boneVec.unit(), bone1Normal, bone1ZAxis, self.legCtrls[i].xfo.tr)

            boneXfos.append(xfo)

        data['boneXfos'] = boneXfos
        data['endXfo'] = self.legCtrls[-1].xfo
        data['boneLengths'] = boneLengths

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

        return InsectLegComponentRig


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
        self.fkCtrls = []
        self.setNumControls(4)

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
        legdrawDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=legSettingsAttrGrp)
        legUseInitPoseInputAttr = BoolAttribute('useInitPose', value=True, parent=legSettingsAttrGrp)
        self.rootIndexInputAttr = IntegerAttribute('rootIndex', value=0, parent=legSettingsAttrGrp)
        legFkikInputAttr = ScalarAttribute('fkik', value=1.0, minValue=0.0, maxValue=1.0, parent=legSettingsAttrGrp)

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
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.deformerJoints = []
        self.boneOutputsTgt = []
        self.setNumDeformers(4)

        # =====================
        # Create Component I/O
        # =====================

        # Set IO Targets
        self.boneOutputs.setTarget(self.boneOutputsTgt)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([self.fkCtrlSpaces[0].getName(), 'To', self.rootInputTgt.getName()]))
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
        self.NBoneSolverSpliceOp.setInput('rigScale', self.rigScaleInputAttr)
        self.NBoneSolverSpliceOp.setInput('useInitPose', legUseInitPoseInputAttr)
        self.NBoneSolverSpliceOp.setInput('ikblend', legFkikInputAttr)
        self.NBoneSolverSpliceOp.setInput('rootIndex', self.rootIndexInputAttr)
        self.NBoneSolverSpliceOp.setInput('tipBoneLen', self.tipBoneLenInputAttr)

        # Add Xfo Inputs
        self.NBoneSolverSpliceOp.setInput('ikgoal', self.legIKCtrl)
        self.NBoneSolverSpliceOp.setInput('upVector', self.legUpVCtrl)

        for i in xrange(len(self.fkCtrls)):
            self.NBoneSolverSpliceOp.setInput('fkcontrols', self.fkCtrls[i])

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
        for i in xrange(len(self.deformerJoints)):
            self.outputsToDeformersSpliceOp.setOutput('constrainees', self.deformerJoints[i])

        Profiler.getInstance().pop()


    def setNumControls(self, numControls):

        # Add new control spaces and controls
        for i in xrange(len(self.fkCtrlSpaces), numControls):
            if i==0:
                parent = self.ctrlCmpGrp
            else:
                parent = self.fkCtrls[i - 1]

            boneName = 'bone' + str(i + 1).zfill(2) + 'FK'
            fkCtrlSpace = CtrlSpace(boneName, parent=parent)

            fkCtrl = Control(boneName, parent=fkCtrlSpace, shape="cube")
            fkCtrl.alignOnXAxis()
            fkCtrl.lockScale(x=True, y=True, z=True)
            fkCtrl.lockTranslation(x=True, y=True, z=True)

            self.fkCtrlSpaces.append(fkCtrlSpace)
            self.fkCtrls.append(fkCtrl)


    def setNumDeformers(self, numDeformers):

        # Add new deformers and outputs
        for i in xrange(len(self.boneOutputsTgt), numDeformers):
            name = 'bone' + str(i + 1).zfill(2)
            legOutput = Locator(name, parent=self.outputHrcGrp)
            self.boneOutputsTgt.append(legOutput)

        for i in xrange(len(self.deformerJoints), numDeformers):
            name = 'bone' + str(i + 1).zfill(2)
            boneDef = Joint(name, parent=self.defCmpGrp)
            boneDef.setComponent(self)
            self.deformerJoints.append(boneDef)

        return True


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(InsectLegComponentRig, self).loadData( data )

        boneXfos = data['boneXfos']
        boneLengths = data['boneLengths']
        numDigits = data['numDigits']

        # Add extra controls and outputs
        self.setNumControls(numDigits)
        self.setNumDeformers(numDigits)

        for i, each in enumerate(self.fkCtrlSpaces):
            self.fkCtrlSpaces[i].xfo = boneXfos[i]
            self.fkCtrls[i].xfo = boneXfos[i]
            self.fkCtrls[i].scalePoints(Vec3(boneLengths[i], 1.75, 1.75))

        self.legIKCtrlSpace.xfo = data['endXfo']
        self.legIKCtrl.xfo = data['endXfo']

        upVPos = boneXfos[0].transformVector(Vec3(5, 3, 0))
        self.legUpVCtrlSpace.xfo.tr = upVPos
        self.legUpVCtrl.xfo.tr = upVPos

        # Set max on the rootIndex attribute
        self.rootIndexInputAttr.setMax(len(boneXfos))

        # ==================
        # Update Splice Ops
        # ==================
        # N Bone Op
        # Add Controls
        for i in xrange(len(self.fkCtrls)):
            controls = self.NBoneSolverSpliceOp.getInput('fkcontrols')
            if self.fkCtrls[i] not in controls:
                self.NBoneSolverSpliceOp.setInput('fkcontrols', self.fkCtrls[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneOutputsTgt)):
            outputs = self.NBoneSolverSpliceOp.getOutput('pose')
            if self.boneOutputsTgt[i] not in outputs:
                self.NBoneSolverSpliceOp.setOutput('pose', self.boneOutputsTgt[i])

        # ==================

        # Outputs To Deformers Op
        # Add Xfo Inputs
        for i in xrange(len(self.boneOutputsTgt)):
            constrainers = self.outputsToDeformersSpliceOp.getInput('constrainers')
            if self.boneOutputsTgt[i] not in constrainers:
                self.outputsToDeformersSpliceOp.setInput('constrainers', self.boneOutputsTgt[i])

        # Add Xfo Outputs
        for i in xrange(len(self.deformerJoints)):
            constrainees = self.outputsToDeformersSpliceOp.getOutput('constrainees')
            if self.deformerJoints[i] not in constrainees:
                self.outputsToDeformersSpliceOp.setOutput('constrainees', self.deformerJoints[i])

        # ============
        # Set IO Xfos
        # ============
        self.rootInputTgt.xfo = boneXfos[0]

        for i in xrange(len(boneLengths)):
            self.boneOutputsTgt[i].xfo = boneXfos[i]

        self.legEndXfoOutputTgt.xfo = data['endXfo']
        self.legEndPosOutputTgt.xfo = data['endXfo']

        # =============
        # Set IO Attrs
        # =============
        tipBoneLen = boneLengths[len(boneLengths) - 1]
        self.tipBoneLenInputAttr.setMax(tipBoneLen * 2.0)
        self.tipBoneLenInputAttr.setValue(tipBoneLen)

        # ====================
        # Evaluate Splice Ops
        # ====================
        # evaluate the nbone op so that all the output transforms are updated.
        self.NBoneSolverSpliceOp.evaluate()
        self.outputsToDeformersSpliceOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(InsectLegComponentGuide)
ks.registerComponent(InsectLegComponentRig)
