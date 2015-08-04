from kraken.core.maths import Vec3

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.components.component_output import ComponentOutput
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.layer import Layer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class FabriceSpine(BaseExampleComponent):
    """Spine Component"""

    def __init__(self, name="spineBase", parent=None):
        super(FabriceSpine, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.spineMainSrtInputTgt = self.createInput('mainSrt', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.spineCogOutputTgt = self.createOutput('cog', dataType='Xfo', parent=self.outputHrcGrp)
        self.spineBaseOutputTgt = self.createOutput('spineBase', dataType='Xfo', parent=self.outputHrcGrp)
        self.pelvisOutputTgt = self.createOutput('pelvis', dataType='Xfo', parent=self.outputHrcGrp)
        self.spineEndOutputTgt = self.createOutput('spineEnd', dataType='Xfo', parent=self.outputHrcGrp)

        self.spineVertebraeOutput = self.addOutput('spineVertebrae', dataType='Xfo[]')

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)
        self.lengthInputAttr = self.createInput('length', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class FabriceSpineGuide(FabriceSpine):
    """Fabrice Spine Component Guide"""

    def __init__(self, name='spine', parent=None):

        Profiler.getInstance().push("Construct Fabrice Spine Guide Component:" + name)
        super(FabriceSpineGuide, self).__init__(name, parent)

        # =========
        # Controls
        # ========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.numDeformersAttr = IntegerAttribute('numDeformers', value=1, minValue=0, maxValue=20, parent=guideSettingsAttrGrp)

        # Guide Controls
        self.cog = Control('cogPosition', parent=self.ctrlCmpGrp, shape="sphere")
        self.cog.setColor('red')

        self.spine01Ctrl = Control('spine01Position', parent=self.ctrlCmpGrp, shape='sphere')
        self.spine02Ctrl = Control('spine02Position', parent=self.ctrlCmpGrp, shape='sphere')
        self.spine03Ctrl = Control('spine03Position', parent=self.ctrlCmpGrp, shape='sphere')
        self.spine04Ctrl = Control('spine04Position', parent=self.ctrlCmpGrp, shape='sphere')

        self.loadData({
            'name': name,
            'location': 'M',
            'cogPosition': Vec3(0.0, 0.65, -3.1),
            'spine01Position': Vec3(0.0, 0.65, -3.1),
            'spine02Position': Vec3(0.0, 1.15, -2.0),
            'spine03Position': Vec3(0.0, 1.6, -0.7),
            'spine04Position': Vec3(0.0, 1.65, 0.75),
            'numDeformers': 6
        })

        Profiler.getInstance().pop()


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = super(FabriceSpineGuide, self).saveData()

        data['cogPosition'] = self.cog.xfo.tr
        data['spine01Position'] = self.spine01Ctrl.xfo.tr
        data['spine02Position'] = self.spine02Ctrl.xfo.tr
        data['spine03Position'] = self.spine03Ctrl.xfo.tr
        data['spine04Position'] = self.spine04Ctrl.xfo.tr
        data['numDeformers'] = self.numDeformersAttr.getValue()

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceSpineGuide, self).loadData( data )

        self.cog.xfo.tr = data["cogPosition"]
        self.spine01Ctrl.xfo.tr = data["spine01Position"]
        self.spine02Ctrl.xfo.tr = data["spine02Position"]
        self.spine03Ctrl.xfo.tr = data["spine03Position"]
        self.spine04Ctrl.xfo.tr = data["spine04Position"]
        self.numDeformersAttr.setValue(data["numDeformers"])

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(FabriceSpineGuide, self).getRigBuildData()

        data['cogPosition'] = self.cog.xfo.tr
        data['spine01Position'] = self.spine01Ctrl.xfo.tr
        data['spine02Position'] = self.spine02Ctrl.xfo.tr
        data['spine03Position'] = self.spine03Ctrl.xfo.tr
        data['spine04Position'] = self.spine04Ctrl.xfo.tr
        data['numDeformers'] = self.numDeformersAttr.getValue()

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

        return FabriceSpineRig


class FabriceSpineRig(FabriceSpine):
    """Fabrice Spine Component"""

    def __init__(self, name="spine", parent=None):

        Profiler.getInstance().push("Construct Spine Rig Component:" + name)
        super(FabriceSpineRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # COG
        self.cogCtrlSpace = CtrlSpace('cog', parent=self.ctrlCmpGrp)
        self.cogCtrl = Control('cog', parent=self.cogCtrlSpace, shape="circle")
        self.cogCtrl.rotatePoints(90, 0, 0)
        self.cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        self.cogCtrl.setColor("orange")

        # Spine Base
        self.spineBaseCtrlSpace = CtrlSpace('spineBase', parent=self.cogCtrl)
        self.spineBaseCtrl = Control('spineBase', parent=self.spineBaseCtrlSpace, shape="pin")
        self.spineBaseCtrl.rotatePoints(90, 0, 0)
        self.spineBaseCtrl.translatePoints(0, 1.5, 0)
        # self.spineBaseCtrl.scalePoints(Vec3(4.0, 4.0, 4.0))

        # Spine Base Handle
        self.spineBaseHandleCtrlSpace = CtrlSpace('spineBaseHandle', parent=self.spineBaseCtrl)
        self.spineBaseHandleCtrl = Control('spineBaseHandle', parent=self.spineBaseHandleCtrlSpace, shape="pin")
        self.spineBaseHandleCtrl.rotatePoints(90, 0, 0)
        self.spineBaseHandleCtrl.translatePoints(0, 1.5, 0)
        # self.spineBaseHandleCtrl.scalePoints(Vec3(4.5, 4.5, 4.5))

        # Spine End
        self.spineEndCtrlSpace = CtrlSpace('spineEnd', parent=self.cogCtrl)
        self.spineEndCtrl = Control('spineEnd', parent=self.spineEndCtrlSpace, shape="pin")
        self.spineEndCtrl.rotatePoints(90, 0, 0)
        self.spineEndCtrl.translatePoints(0, 1.5, 0)
        # self.spineEndCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))

        # Spine End Handle
        self.spineEndHandleCtrlSpace = CtrlSpace('spineEndHandle', parent=self.spineEndCtrl)
        self.spineEndHandleCtrl = Control('spineEndHandle', parent=self.spineEndHandleCtrlSpace, shape="pin")
        self.spineEndHandleCtrl.rotatePoints(90, 0, 0)
        self.spineEndHandleCtrl.translatePoints(0, 1.5, 0)
        # self.spineEndHandleCtrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        self.spineEndHandleCtrl.setColor("blue")

        # Pelvis
        self.pelvisCtrlSpace = CtrlSpace('pelvis', parent=self.cogCtrl)
        self.pelvisCtrl = Control('pelvis', parent=self.pelvisCtrlSpace, shape="cube")
        self.pelvisCtrl.alignOnYAxis(negative=True)
        self.pelvisCtrl.rotatePoints(90, 0, 0)
        self.pelvisCtrl.scalePoints(Vec3(2.0, 1.5, 1.5))


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.deformerJoints = []
        self.spineOutputs = []
        self.setNumDeformers(1)

        pelvisDef = Joint('pelvis', parent=self.defCmpGrp)
        pelvisDef.setComponent(self)

        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        self.spineVertebraeOutput.setTarget(self.spineOutputs)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.spineSrtInputConstraint = PoseConstraint('_'.join([self.cogCtrlSpace.getName(), 'To', self.spineMainSrtInputTgt.getName()]))
        self.spineSrtInputConstraint.addConstrainer(self.spineMainSrtInputTgt)
        self.spineSrtInputConstraint.setMaintainOffset(True)
        self.cogCtrlSpace.addConstraint(self.spineSrtInputConstraint)

        # Constraint outputs
        self.spineCogOutputConstraint = PoseConstraint('_'.join([self.spineCogOutputTgt.getName(), 'To', self.cogCtrl.getName()]))
        self.spineCogOutputConstraint.addConstrainer(self.cogCtrl)
        self.spineCogOutputTgt.addConstraint(self.spineCogOutputConstraint)

        self.spineBaseOutputConstraint = PoseConstraint('_'.join([self.spineBaseOutputTgt.getName(), 'To', 'spineBase']))
        self.spineBaseOutputConstraint.addConstrainer(self.spineOutputs[0])
        self.spineBaseOutputTgt.addConstraint(self.spineBaseOutputConstraint)

        self.pelvisOutputConstraint = PoseConstraint('_'.join([self.pelvisOutputTgt.getName(), 'To', self.pelvisCtrl.getName()]))
        self.pelvisOutputConstraint.addConstrainer(self.pelvisCtrl)
        self.pelvisOutputTgt.addConstraint(self.pelvisOutputConstraint)

        self.spineEndOutputConstraint = PoseConstraint('_'.join([self.spineEndOutputTgt.getName(), 'To', 'spineEnd']))
        self.spineEndOutputConstraint.addConstrainer(self.spineOutputs[0])
        self.spineEndOutputTgt.addConstraint(self.spineEndOutputConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Spine Splice Op
        self.bezierSpineSpliceOp = SpliceOperator('spineSpliceOp', 'BezierSpineSolver', 'Kraken')
        self.addOperator(self.bezierSpineSpliceOp)

        # Add Att Inputs
        self.bezierSpineSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.bezierSpineSpliceOp.setInput('rigScale', self.rigScaleInputAttr)
        self.bezierSpineSpliceOp.setInput('length', self.lengthInputAttr)

        # Add Xfo Inputs
        self.bezierSpineSpliceOp.setInput('base', self.spineBaseCtrl)
        self.bezierSpineSpliceOp.setInput('baseHandle', self.spineBaseHandleCtrl)
        self.bezierSpineSpliceOp.setInput('tipHandle', self.spine03Ctrl)
        self.bezierSpineSpliceOp.setInput('tip', self.spineEndCtrl)

        # Add Xfo Outputs
        for spineOutput in self.spineOutputs:
            self.bezierSpineSpliceOp.setOutput('outputs', spineOutput)

        # Add Deformer Splice Op
        self.deformersToOutputsSpliceOp = SpliceOperator('spineDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.deformersToOutputsSpliceOp)

        # Add Att Inputs
        self.deformersToOutputsSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.deformersToOutputsSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Outputs
        for spineOutput in self.spineOutputs:
            self.deformersToOutputsSpliceOp.setInput('constrainers', spineOutput)

        # Add Xfo Outputs
        for joint in self.deformerJoints:
            self.deformersToOutputsSpliceOp.setOutput('constrainees', joint)

        # Add Pelvis Splice Op
        self.pelvisDefSpliceOp = SpliceOperator('pelvisDeformerSpliceOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(self.pelvisDefSpliceOp)

        # Add Att Inputs
        self.pelvisDefSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.pelvisDefSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.pelvisDefSpliceOp.setInput('constrainer', self.pelvisOutputTgt)

        # Add Xfo Outputs
        self.pelvisDefSpliceOp.setOutput('constrainee', pelvisDef)


        Profiler.getInstance().pop()


    def setNumDeformers(self, numDeformers):

        # Add new deformers and outputs
        for i in xrange(len(self.spineOutputs), numDeformers):
            name = 'spine' + str(i + 1).zfill(2)
            spineOutput = ComponentOutput(name, parent=self.outputHrcGrp)
            self.spineOutputs.append(spineOutput)

        for i in xrange(len(self.deformerJoints), numDeformers):
            name = 'spine' + str(i + 1).zfill(2)
            spineDef = Joint(name, parent=self.defCmpGrp)
            spineDef.setComponent(self)
            self.deformerJoints.append(spineDef)

        return True


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceSpineRig, self).loadData( data )

        cogPosition = data['cogPosition']
        spine01Position = data['spine01Position']
        spine02Position = data['spine02Position']
        spine03Position = data['spine03Position']
        spine04Position = data['spine04Position']
        numDeformers = data['numDeformers']

        self.cogCtrlSpace.xfo.tr = cogPosition
        self.cogCtrl.xfo.tr = cogPosition

        self.pelvisCtrlSpace.xfo.tr = cogPosition
        self.pelvisCtrl.xfo.tr = cogPosition

        self.spineBaseCtrlSpace.xfo.tr = spine01Position
        self.spineBaseCtrl.xfo.tr = spine01Position

        self.spineBaseHandleCtrlSpace.xfo.tr = spine02Position
        self.spineBaseHandleCtrl.xfo.tr = spine02Position

        self.spineEndHandleCtrlSpace.xfo.tr = spine03Position
        self.spineEndHandleCtrl.xfo.tr = spine03Position

        self.spineEndCtrlSpace.xfo.tr = spine04Position
        self.spineEndCtrl.xfo.tr = spine04Position

        length = spine01Position.distanceTo(spine02Position) + spine02Position.distanceTo(spine03Position) + spine03Position.distanceTo(spine04Position)
        self.lengthInputAttr.setMax(length * 3.0)
        self.lengthInputAttr.setValue(length)

        # Update number of deformers and outputs
        self.setNumDeformers(numDeformers)

        for spineOutput in self.spineOutputs:
            if spineOutput not in self.bezierSpineSpliceOp.getOutput("outputs"):
                self.bezierSpineSpliceOp.setOutput("outputs", spineOutput)

        # Update Deformers Splice Op
        for spineOutput in self.spineOutputs:
            if spineOutput not in self.deformersToOutputsSpliceOp.getInput("constrainers"):
                self.deformersToOutputsSpliceOp.setInput("constrainers", spineOutput)

        for joint in self.deformerJoints:
            if joint not in self.deformersToOutputsSpliceOp.getOutput("constrainees"):
                self.deformersToOutputsSpliceOp.setOutput("constrainees", joint)

        # Updating constraint to use the updated last output.
        self.spineEndOutputConstraint.setConstrainer(self.spineOutputs[-1], index=0)

        # ============
        # Set IO Xfos
        # ============

        # ====================
        # Evaluate Splice Ops
        # ====================
        # evaluate the spine op so that all the output transforms are updated.
        self.bezierSpineSpliceOp.evaluate()

        # evaluate the constraint op so that all the joint transforms are updated.
        self.deformersToOutputsSpliceOp.evaluate()
        self.pelvisDefSpliceOp.evaluate()

        # evaluate the constraints to ensure the outputs are now in the correct location.
        self.spineCogOutputConstraint.evaluate()
        self.spineBaseOutputConstraint.evaluate()
        self.pelvisOutputConstraint.evaluate()
        self.spineEndOutputConstraint.evaluate()



from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FabriceSpineGuide)
ks.registerComponent(FabriceSpineRig)
