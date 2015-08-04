import math

from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_example_component import BaseExampleComponent

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


class TentacleComponent(BaseExampleComponent):
    """Insect Leg Base"""

    def __init__(self, name='TentacleBase', parent=None):

        super(TentacleComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.rootInputTgt = self.createInput('rootInput', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.boneOutputs = self.addOutput('boneOutputs', dataType='Xfo[]')

        self.tentacleEndXfoOutputTgt = self.createOutput('tentacleEndXfoOutput', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)
        self.tipBoneLenInputAttr = self.createInput('tipBoneLen', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class TentacleComponentGuide(TentacleComponent):
    """Tentacle Component Guide"""

    def __init__(self, name='Tentacle', parent=None, data=None):

        Profiler.getInstance().push("Construct Tentacle Guide Component:" + name)
        super(TentacleComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.numJoints = IntegerAttribute('numJoints', value=12, minValue=2, maxValue=20, parent=guideSettingsAttrGrp)
        self.numJoints.setValueChangeCallback(self.updateNumLegControls)

        self.jointCtrls = []
        if data is None:
            numJoints = self.numJoints.getValue()
            jointPositions = self.generateGuidePositions(numJoints)

            for i in xrange(numJoints):
                self.jointCtrls.append(Control('tentacle' + str(i + 1).zfill(2), parent=self.ctrlCmpGrp, shape="sphere"))

            data = {
               "location": "L",
               "jointPositions": jointPositions,
               "numJoints": self.numJoints.getValue()
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

        data = super(TentacleComponentGuide, self).saveData()

        jointPositions = []
        for i in xrange(len(self.jointCtrls)):
            jointPositions.append(self.jointCtrls[i].xfo.tr)

        data['jointPositions'] = jointPositions

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(TentacleComponentGuide, self).loadData(data)

        for i in xrange(len(data['jointPositions'])):
            self.jointCtrls[i].xfo.tr = data['jointPositions'][i]

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(TentacleComponentGuide, self).getRigBuildData()

        numJoints = self.numJoints.getValue()

        # Calculate FW
        toFirst = self.jointCtrls[0].xfo.tr.subtract(self.jointCtrls[1].xfo.tr).unit()
        toTip = self.jointCtrls[0].xfo.tr.subtract(self.jointCtrls[-1].xfo.tr).unit()
        fw = toTip.cross(toFirst).unit()

        # Calculate Xfos
        boneXfos = []
        boneLengths = []
        for i in xrange(numJoints):
            boneVec = self.jointCtrls[i + 1].xfo.tr.subtract(self.jointCtrls[i].xfo.tr)
            boneLengths.append(boneVec.length())
            bone1Normal = fw.cross(boneVec).unit()
            bone1ZAxis = boneVec.cross(bone1Normal).unit()

            xfo = Xfo()
            xfo.setFromVectors(boneVec.unit(), bone1Normal, bone1ZAxis, self.jointCtrls[i].xfo.tr)

            boneXfos.append(xfo)

        data['boneXfos'] = boneXfos
        data['endXfo'] = self.jointCtrls[-1].xfo
        data['boneLengths'] = boneLengths

        return data

    # ==========
    # Callbacks
    # ==========
    def updateNumLegControls(self, numJoints):
        """Load a saved guide representation from persisted data.

        Arguments:
        numJoints -- object, The number of joints inthe chain.

        Return:
        True if successful.

        """

        if numJoints == 0:
            raise IndexError("'numJoints' must be > 0")

        if numJoints + 1 > len(self.jointCtrls):
            for i in xrange(len(self.jointCtrls), numJoints + 1):
                newCtrl = Control('tentacle' + str(i + 1).zfill(2), parent=self.ctrlCmpGrp, shape="sphere")
                self.jointCtrls.append(newCtrl)

        elif numJoints + 1 < len(self.jointCtrls):
            numExtraCtrls = len(self.jointCtrls) - (numJoints + 1)
            for i in xrange(numExtraCtrls):
                extraCtrl = self.jointCtrls.pop()
                self.ctrlCmpGrp.removeChild(extraCtrl)

        # Reset the control positions based on new number of joints
        jointPositions = self.generateGuidePositions(numJoints)
        for i in xrange(len(self.jointCtrls)):
            self.jointCtrls[i].xfo.tr = jointPositions[i]

        return True

    def generateGuidePositions(self, numJoints):
        """Generates the positions for the guide controls based on the number
        of joints.

        Args:
            numJoints (int): Number of joints to generate a transform for.

        Returns:
            list: Guide control positions.

        """

        halfPi = math.pi / 2.0
        step = halfPi / numJoints

        guidePositions = []
        for i in xrange(numJoints + 1):
            x = math.cos((i * step) + halfPi) * -10
            y = math.sin((i * step) + halfPi) * 10
            guidePositions.append(Vec3(x, y, 0.0))

        return guidePositions


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

        return TentacleComponentRig


class TentacleComponentRig(TentacleComponent):
    """Insect Leg Rig"""

    def __init__(self, name='Tentacle', parent=None):

        Profiler.getInstance().push("Construct Tentacle Rig Component:" + name)
        super(TentacleComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========

        # Chain Base
        self.chainBase = Locator('ChainBase', parent=self.ctrlCmpGrp)
        self.chainBase.setShapeVisibility(False)

        # FK
        self.fkCtrlSpaces = []
        self.fkCtrls = []
        self.setNumControls(4)

        # IK Control
        self.tentacleIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.tentacleIKCtrl = Control('IK', parent=self.tentacleIKCtrlSpace, shape="pin")

        if self.getLocation() == 'R':
            self.tentacleIKCtrl.rotatePoints(0, 90, 0)
            self.tentacleIKCtrl.translatePoints(Vec3(-1.0, 0.0, 0.0))
        else:
            self.tentacleIKCtrl.rotatePoints(0, -90, 0)
            self.tentacleIKCtrl.translatePoints(Vec3(1.0, 0.0, 0.0))

        # Add Component Params to IK control
        tentacleSettingsAttrGrp = AttributeGroup("DisplayInfo_LegSettings", parent=self.tentacleIKCtrl)
        tentacledrawDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=tentacleSettingsAttrGrp)
        fkikInputAttr = ScalarAttribute('fkik', value=1.0, minValue=0.0, maxValue=1.0, parent=tentacleSettingsAttrGrp)
        waveLengthInputAttr = ScalarAttribute('waveLength', value=1.0, minValue=0.0, maxValue=5.0, parent=tentacleSettingsAttrGrp)
        waveAmplitudeInputAttr = ScalarAttribute('waveAmplitude', value=0.6, minValue=-3.0, maxValue=3.0, parent=tentacleSettingsAttrGrp)
        waveFrequencyInputAttr = ScalarAttribute('waveFrequency', value=2.0, minValue=0.0, maxValue=10.0, parent=tentacleSettingsAttrGrp)
        tipBiasInputAttr = ScalarAttribute('tipBias', value=1.0, minValue=0.0, maxValue=1.0, parent=tentacleSettingsAttrGrp)

        # Connect IO to controls
        self.drawDebugInputAttr.connect(tentacledrawDebugInputAttr)

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
        tentacleRootInputConstraint = PoseConstraint('_'.join([self.fkCtrlSpaces[0].getName(), 'To', self.rootInputTgt.getName()]))
        tentacleRootInputConstraint.setMaintainOffset(True)
        tentacleRootInputConstraint.addConstrainer(self.rootInputTgt)
        self.fkCtrlSpaces[0].addConstraint(tentacleRootInputConstraint)


        chainBaseInputConstraint = PoseConstraint('_'.join([self.chainBase.getName(), 'To', self.rootInputTgt.getName()]))
        chainBaseInputConstraint.setMaintainOffset(True)
        chainBaseInputConstraint.addConstrainer(self.rootInputTgt)
        self.chainBase.addConstraint(chainBaseInputConstraint)

        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        self.tentacleSolverSpliceOp = SpliceOperator('tentacleSpliceOp', 'TentacleSolver', 'Kraken')
        self.addOperator(self.tentacleSolverSpliceOp)

        # # Add Att Inputs
        self.tentacleSolverSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.tentacleSolverSpliceOp.setInput('rigScale', self.rigScaleInputAttr)
        self.tentacleSolverSpliceOp.setInput('ikblend', fkikInputAttr)
        self.tentacleSolverSpliceOp.setInput('waveLength', waveLengthInputAttr)
        self.tentacleSolverSpliceOp.setInput('waveAmplitude', waveAmplitudeInputAttr)
        self.tentacleSolverSpliceOp.setInput('waveFrequency', waveFrequencyInputAttr)
        self.tentacleSolverSpliceOp.setInput('tipBias', tipBiasInputAttr)
        self.tentacleSolverSpliceOp.setInput('tipBoneLen', self.tipBoneLenInputAttr)

        # Add Xfo Inputs
        self.tentacleSolverSpliceOp.setInput('chainBase', self.chainBase)
        self.tentacleSolverSpliceOp.setInput('ikgoal', self.tentacleIKCtrl)

        for i in xrange(len(self.fkCtrls)):
            self.tentacleSolverSpliceOp.setInput('fkcontrols', self.fkCtrls[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneOutputsTgt)):
            self.tentacleSolverSpliceOp.setOutput('pose', self.boneOutputsTgt[i])

        self.tentacleSolverSpliceOp.setOutput('tentacleEnd', self.tentacleEndXfoOutputTgt)


        # Add Deformer Splice Op
        self.outputsToDeformersSpliceOp = SpliceOperator('TentacleDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
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
            tentacleOutput = Locator(name, parent=self.outputHrcGrp)
            self.boneOutputsTgt.append(tentacleOutput)

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

        super(TentacleComponentRig, self).loadData( data )

        boneXfos = data['boneXfos']
        boneLengths = data['boneLengths']
        numJoints = data['numJoints']
        endXfo = data['endXfo']

        # Add extra controls and outputs
        self.setNumControls(numJoints)
        self.setNumDeformers(numJoints)

        # Scale controls based on bone lengths
        for i, each in enumerate(self.fkCtrlSpaces):
            self.fkCtrlSpaces[i].xfo = boneXfos[i]
            self.fkCtrls[i].xfo = boneXfos[i]
            self.fkCtrls[i].scalePoints(Vec3(boneLengths[i], 1.75, 1.75))

        self.chainBase.xfo = boneXfos[0]

        self.tentacleIKCtrlSpace.xfo = endXfo
        self.tentacleIKCtrl.xfo = endXfo

        # ==================
        # Update Splice Ops
        # ==================
        # N Bone Op
        # Add Controls
        for i in xrange(len(self.fkCtrls)):
            controls = self.tentacleSolverSpliceOp.getInput('fkcontrols')
            if self.fkCtrls[i] not in controls:
                self.tentacleSolverSpliceOp.setInput('fkcontrols', self.fkCtrls[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneOutputsTgt)):
            outputs = self.tentacleSolverSpliceOp.getOutput('pose')
            if self.boneOutputsTgt[i] not in outputs:
                self.tentacleSolverSpliceOp.setOutput('pose', self.boneOutputsTgt[i])

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

        self.tentacleEndXfoOutputTgt.xfo = endXfo

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
        self.tentacleSolverSpliceOp.evaluate()
        self.outputsToDeformersSpliceOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(TentacleComponentGuide)
ks.registerComponent(TentacleComponentRig)
