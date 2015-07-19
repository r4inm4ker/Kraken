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


class FKChainComponent(Component):
    """FK Chain Base"""

    def __init__(self, name='FKChainBase', parent=None):

        super(FKChainComponent, self).__init__(name, parent)

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

        self.chainEndXfoOutputTgt = self.createOutput('chainEndXfoOutput', dataType='Xfo', parent=self.outputHrcGrp)
        self.chainEndPosOutputTgt = self.createOutput('chainEndPosOutput', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class FKChainComponentGuide(FKChainComponent):
    """FKChain Component Guide"""

    def __init__(self, name='FKChain', parent=None, data=None):

        Profiler.getInstance().push("Construct FKCHain Guide Component:" + name)
        super(FKChainComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.numDigits = IntegerAttribute('numDigits', value=8, minValue=0, maxValue=20, parent=guideSettingsAttrGrp)


        numDigits = self.numDigits.getValue()
        halfPi = math.pi / 2.0
        step = halfPi / (numDigits - 1)

        yValues = []
        xValues = []
        for i in xrange(numDigits):
            yValues.append(math.sin((i * step) + halfPi) * 10)
            xValues.append(math.cos((i * step) + halfPi) * -10)

        self.legCtrls = []
        for i in xrange(numDigits):
            self.legCtrls.append(Control('leg' + str(i).zfill(2), parent=self.ctrlCmpGrp, shape="sphere"))

        if data is None:
            spacingY = 10.0 / numDigits - 1
            spacingZ = 5.0 / numDigits - 1

            jointPositions = []
            for i in xrange(numDigits):
                jointPositions.append(Vec3(xValues[i], yValues[i], 0.0))

            data = {
               "location": "L",
               "jointPositions": jointPositions
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

        data = super(FKChainComponentGuide, self).saveData()

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

        super(FKChainComponentGuide, self).loadData(data)

        numDigits = len(data['jointPositions'])
        if numDigits > len(self.legCtrls):
            for i in xrange(len(self.legCtrls), numDigits):
                self.legCtrls.append(Control('leg' + str(i).zfill(2), parent=self.ctrlCmpGrp, shape="sphere"))
        elif numDigits < len(self.legCtrls):
            numExtraCtrls = len(self.legCtrls) - numDigits
            for i in xrange(numExtraCtrls):
                self.legCtrls.pop()

        self.numDigits.setValue(numDigits)

        for i in xrange(len(data['jointPositions'])):
            self.legCtrls[i].xfo.tr = data['jointPositions'][i]

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(FKChainComponentGuide, self).getRigBuildData()

        numDigits = self.numDigits.getValue()

        # Calculate Xfos
        fw = Vec3(0, 0, 1)
        boneXfos = []
        boneLengths = []

        for i in xrange(numDigits - 1):
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

        return FKChainComponentRig


class FKChainComponentRig(FKChainComponent):
    """FK Chain Leg Rig"""

    def __init__(self, name='FKChain', parent=None):

        Profiler.getInstance().push("Construct FK Chain Rig Component:" + name)
        super(FKChainComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # FK
        self.fkCtrlSpaces = []
        self.fkCtrls = []
        self.setNumControls(4)

        # Add Component Params to IK control
        legSettingsAttrGrp = AttributeGroup("DisplayInfo_ChainSettings", parent=self.fkCtrls[0])
        legdrawDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=legSettingsAttrGrp)

        # Connect IO to controls
        self.drawDebugInputAttr.connect(legdrawDebugInputAttr)

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
        rootInputConstraint = PoseConstraint('_'.join([self.fkCtrlSpaces[0].getName(), 'To', self.rootInputTgt.getName()]))
        rootInputConstraint.setMaintainOffset(True)
        rootInputConstraint.addConstrainer(self.rootInputTgt)
        self.fkCtrlSpaces[0].addConstraint(rootInputConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Output Splice Op
        self.outputsToControlsSpliceOp = SpliceOperator('fkChainOutputSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToControlsSpliceOp)

        # Add Att Inputs
        self.outputsToControlsSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToControlsSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        for i in xrange(len(self.fkCtrls)):
            self.outputsToControlsSpliceOp.setInput('constrainers', self.fkCtrls[i])

        # Add Xfo Outputs
        for i in xrange(len(self.boneOutputsTgt)):
            self.outputsToControlsSpliceOp.setOutput('constrainees', self.boneOutputsTgt[i])

        # Add Deformer Splice Op
        self.deformersToOutputsSpliceOp = SpliceOperator('fkChainDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.deformersToOutputsSpliceOp)

        # Add Att Inputs
        self.deformersToOutputsSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.deformersToOutputsSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        for i in xrange(len(self.boneOutputsTgt)):
            self.deformersToOutputsSpliceOp.setInput('constrainers', self.boneOutputsTgt[i])

        # Add Xfo Outputs
        for i in xrange(len(self.deformerJoints)):
            self.deformersToOutputsSpliceOp.setOutput('constrainees', self.deformerJoints[i])

        Profiler.getInstance().pop()


    def setNumControls(self, numControls):

        # Add new control spaces and controls
        for i in xrange(len(self.fkCtrlSpaces), numControls):
            if i==0:
                parent = self.ctrlCmpGrp
            else:
                parent = self.fkCtrls[i - 1]

            boneName = 'bone' + str(i + 1).zfill(2) + 'FK'
            boneFKCtrlSpace = CtrlSpace(boneName, parent=parent)

            boneFKCtrl = Control(boneName, parent=boneFKCtrlSpace, shape="cube")
            boneFKCtrl.alignOnXAxis()

            self.fkCtrlSpaces.append(boneFKCtrlSpace)
            self.fkCtrls.append(boneFKCtrl)


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

        super(FKChainComponentRig, self).loadData( data )

        boneXfos = data['boneXfos']
        boneLengths = data['boneLengths']

        # Add extra controls and outputs
        self.setNumControls(len(boneLengths))
        self.setNumDeformers(len(boneLengths))

        for i, each in enumerate(self.fkCtrlSpaces):
            self.fkCtrlSpaces[i].xfo = boneXfos[i]
            self.fkCtrls[i].xfo = boneXfos[i]
            self.fkCtrls[i].scalePoints(Vec3(boneLengths[i], 1.75, 1.75))

        # ==================
        # Update Splice Ops
        # ==================
        # Outputs To Controls Op
        # Update Controls
        for i in xrange(len(self.fkCtrls)):
            constrainers = self.outputsToControlsSpliceOp.getInput('constrainers')
            if self.fkCtrls[i] not in constrainers:
                self.outputsToControlsSpliceOp.setInput('constrainers', self.fkCtrls[i])

        # Update Outputs
        for i in xrange(len(self.boneOutputsTgt)):
            constrainees = self.outputsToControlsSpliceOp.getOutput('constrainees')
            if self.boneOutputsTgt[i] not in constrainees:
                self.outputsToControlsSpliceOp.setOutput('constrainees', self.boneOutputsTgt[i])

        # Deformers To Outputs Op
        # Update Outputs
        for i in xrange(len(self.boneOutputsTgt)):
            constrainers = self.deformersToOutputsSpliceOp.getInput('constrainers')
            if self.boneOutputsTgt[i] not in constrainers:
                self.deformersToOutputsSpliceOp.setInput('constrainers', self.boneOutputsTgt[i])

        # Update Deformers
        for i in xrange(len(self.deformerJoints)):
            constrainees = self.deformersToOutputsSpliceOp.getOutput('constrainees')
            if self.deformerJoints[i] not in constrainees:
                self.deformersToOutputsSpliceOp.setOutput('constrainees', self.deformerJoints[i])

        # ============
        # Set IO Xfos
        # ============
        self.rootInputTgt.xfo = boneXfos[0]

        for i in xrange(len(boneLengths)):
            self.boneOutputsTgt[i].xfo = boneXfos[i]

        self.chainEndXfoOutputTgt.xfo = data['endXfo']
        self.chainEndPosOutputTgt.xfo = data['endXfo']

        # =============
        # Set IO Attrs
        # =============

        # ====================
        # Evaluate Splice Ops
        # ====================
        # Eval Outputs to Controls Op to evaulate with new outputs and controls
        self.outputsToControlsSpliceOp.evaluate()

        # evaluate the output splice op to evaluate with new outputs and deformers
        self.deformersToOutputsSpliceOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FKChainComponentGuide)
ks.registerComponent(FKChainComponentRig)
