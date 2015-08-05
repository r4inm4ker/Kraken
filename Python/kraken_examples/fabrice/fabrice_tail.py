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


class FabriceTail(BaseExampleComponent):
    """Fabrice Tail Component"""

    def __init__(self, name="fabriceTailBase", parent=None):
        super(FabriceTail, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.tailMainSrtInputTgt = self.createInput('mainSrt', dataType='Xfo', parent=self.inputHrcGrp)
        self.spineEndInputTgt = self.createInput('spineEnd', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.tailBaseOutputTgt = self.createOutput('tailBase', dataType='Xfo', parent=self.outputHrcGrp)
        self.tailEndOutputTgt = self.createOutput('tailEnd', dataType='Xfo', parent=self.outputHrcGrp)

        self.tailVertebraeOutput = self.addOutput('tailVertebrae', dataType='Xfo[]')

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)
        self.lengthInputAttr = self.createInput('length', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs


class FabriceTailGuide(FabriceTail):
    """Fabrice Tail Component Guide"""

    def __init__(self, name='tail', parent=None):

        Profiler.getInstance().push("Construct Fabrice Tail Guide Component:" + name)
        super(FabriceTailGuide, self).__init__(name, parent)

        # =========
        # Controls
        # ========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.numDeformersAttr = IntegerAttribute('numDeformers', value=1, minValue=0, maxValue=20, parent=guideSettingsAttrGrp)

        # Guide Controls
        self.spine01Ctrl = Control('spine01Position', parent=self.ctrlCmpGrp, shape='sphere')
        self.spine01Ctrl.scalePoints(Vec3(1.2, 1.2, 1.2))
        self.spine01Ctrl.setColor("turqoise")

        self.spine02Ctrl = Control('spine02Position', parent=self.ctrlCmpGrp, shape='sphere')
        self.spine02Ctrl.setColor("turqoise")

        self.spine03Ctrl = Control('spine03Position', parent=self.ctrlCmpGrp, shape='sphere')
        self.spine03Ctrl.setColor("turqoise")

        self.spine04Ctrl = Control('spine04Position', parent=self.ctrlCmpGrp, shape='sphere')
        self.spine04Ctrl.setColor("turqoise")

        self.spineOutputs = []
        for i in xrange(6):
            debugCtrl = Locator('tail' + str(i+1).zfill(2), parent=self.outputHrcGrp)
            self.spineOutputs.append(debugCtrl)

        # ===============
        # Add Splice Ops
        # ===============
        # Add Tail Splice Op
        self.bezierSpineSpliceOp = SpliceOperator('spineGuideSpliceOp', 'BezierSpineSolver', 'Kraken')
        self.addOperator(self.bezierSpineSpliceOp)

        # Add Att Inputs
        self.bezierSpineSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.bezierSpineSpliceOp.setInput('rigScale', self.rigScaleInputAttr)
        self.bezierSpineSpliceOp.setInput('length', self.lengthInputAttr)

        # Add Xfo Inputs
        self.bezierSpineSpliceOp.setInput('base', self.spine01Ctrl)
        self.bezierSpineSpliceOp.setInput('baseHandle', self.spine02Ctrl)
        self.bezierSpineSpliceOp.setInput('tipHandle', self.spine03Ctrl)
        self.bezierSpineSpliceOp.setInput('tip', self.spine04Ctrl)

        # Add Xfo Outputs
        for spineOutput in self.spineOutputs:
            self.bezierSpineSpliceOp.setOutput('outputs', spineOutput)

        self.loadData({
            'name': name,
            'location': 'M',
            'spine01Position': Vec3(0.0, 0.65, -3.1),
            'spine02Position': Vec3(0.0, 0.157, -4.7),
            'spine03Position': Vec3(0.0, 0.0625, -6.165),
            'spine04Position': Vec3(0.0, -0.22, -7.42),
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

        data = super(FabriceTailGuide, self).saveData()

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

        super(FabriceTailGuide, self).loadData( data )

        self.spine01Ctrl.xfo.tr = data["spine01Position"]
        self.spine02Ctrl.xfo.tr = data["spine02Position"]
        self.spine03Ctrl.xfo.tr = data["spine03Position"]
        self.spine04Ctrl.xfo.tr = data["spine04Position"]
        self.numDeformersAttr.setValue(data["numDeformers"])

        length = data["spine01Position"].distanceTo(data["spine02Position"]) + data["spine02Position"].distanceTo(data["spine03Position"]) + data["spine03Position"].distanceTo(data["spine04Position"])
        self.lengthInputAttr.setMax(length * 3.0)
        self.lengthInputAttr.setValue(length)

        self.bezierSpineSpliceOp.evaluate()

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(FabriceTailGuide, self).getRigBuildData()

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

        return FabriceTailRig


class FabriceTailRig(FabriceTail):
    """Fabrice Tail Component"""

    def __init__(self, name="fabriceTail", parent=None):

        Profiler.getInstance().push("Construct Tail Rig Component:" + name)
        super(FabriceTailRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========

        # Tail Base
        self.tailBaseCtrlSpace = CtrlSpace('tailBase', parent=self.ctrlCmpGrp)
        self.tailBaseCtrl = Control('tailBase', parent=self.tailBaseCtrlSpace, shape="circle")
        self.tailBaseCtrl.rotatePoints(90, 0, 0)
        self.tailBaseCtrl.scalePoints(Vec3(2.0, 2.0, 2.0))
        self.tailBaseCtrl.setColor("greenBlue")

        # Tail Base Handle
        self.tailBaseHandleCtrlSpace = CtrlSpace('tailBaseHandle', parent=self.tailBaseCtrl)
        self.tailBaseHandleCtrl = Control('tailBaseHandle', parent=self.tailBaseHandleCtrlSpace, shape="circle")
        self.tailBaseHandleCtrl.rotatePoints(90, 0, 0)
        self.tailBaseHandleCtrl.scalePoints(Vec3(2.0, 2.0, 2.0))
        self.tailBaseHandleCtrl.setColor("turqoise")

        # Tail End
        self.tailEndCtrlSpace = CtrlSpace('tailEnd', parent=self.ctrlCmpGrp)
        self.tailEndCtrl = Control('tailEnd', parent=self.tailEndCtrlSpace, shape="circle")
        self.tailEndCtrl.rotatePoints(90, 0, 0)
        self.tailEndCtrl.scalePoints(Vec3(2.0, 2.0, 2.0))
        self.tailEndCtrl.setColor("greenBlue")

        # Tail End Handle
        self.tailEndHandleCtrlSpace = CtrlSpace('tailEndHandle', parent=self.tailEndCtrl)
        self.tailEndHandleCtrl = Control('tailEndHandle', parent=self.tailEndHandleCtrlSpace, shape="circle")
        self.tailEndHandleCtrl.rotatePoints(90, 0, 0)
        self.tailEndHandleCtrl.scalePoints(Vec3(2.0, 2.0, 2.0))
        self.tailEndHandleCtrl.setColor("turqoise")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.deformerJoints = []
        self.tailOutputs = []
        self.setNumDeformers(1)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        self.tailVertebraeOutput.setTarget(self.tailOutputs)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.tailBaseInputConstraint = PoseConstraint('_'.join([self.tailBaseCtrlSpace.getName(), 'To', self.spineEndInputTgt.getName()]))
        self.tailBaseInputConstraint.addConstrainer(self.spineEndInputTgt)
        self.tailBaseInputConstraint.setMaintainOffset(True)
        self.tailBaseCtrlSpace.addConstraint(self.tailBaseInputConstraint)

        # Constraint outputs
        self.tailBaseOutputConstraint = PoseConstraint('_'.join([self.tailBaseOutputTgt.getName(), 'To', 'spineBase']))
        self.tailBaseOutputConstraint.addConstrainer(self.tailOutputs[0])
        self.tailBaseOutputTgt.addConstraint(self.tailBaseOutputConstraint)

        self.tailEndOutputConstraint = PoseConstraint('_'.join([self.tailEndOutputTgt.getName(), 'To', 'spineEnd']))
        self.tailEndOutputConstraint.addConstrainer(self.tailOutputs[0])
        self.tailEndOutputTgt.addConstraint(self.tailEndOutputConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Tail Splice Op
        self.bezierTailSpliceOp = SpliceOperator('tailSpliceOp', 'BezierSpineSolver', 'Kraken')
        self.addOperator(self.bezierTailSpliceOp)

        # Add Att Inputs
        self.bezierTailSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.bezierTailSpliceOp.setInput('rigScale', self.rigScaleInputAttr)
        self.bezierTailSpliceOp.setInput('length', self.lengthInputAttr)

        # Add Xfo Inputs
        self.bezierTailSpliceOp.setInput('base', self.tailBaseCtrl)
        self.bezierTailSpliceOp.setInput('baseHandle', self.tailBaseHandleCtrl)
        self.bezierTailSpliceOp.setInput('tipHandle', self.tailEndHandleCtrl)
        self.bezierTailSpliceOp.setInput('tip', self.tailEndCtrl)

        # Add Xfo Outputs
        for tailOutput in self.tailOutputs:
            self.bezierTailSpliceOp.setOutput('outputs', tailOutput)

        # Add Deformer Splice Op
        self.deformersToOutputsSpliceOp = SpliceOperator('tailDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.deformersToOutputsSpliceOp)

        # Add Att Inputs
        self.deformersToOutputsSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.deformersToOutputsSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Outputs
        for tailOutput in self.tailOutputs:
            self.deformersToOutputsSpliceOp.setInput('constrainers', tailOutput)

        # Add Xfo Outputs
        for joint in self.deformerJoints:
            self.deformersToOutputsSpliceOp.setOutput('constrainees', joint)

        Profiler.getInstance().pop()


    def setNumDeformers(self, numDeformers):

        # Add new deformers and outputs
        for i in xrange(len(self.tailOutputs), numDeformers):
            name = 'tail' + str(i + 1).zfill(2)
            tailOutput = ComponentOutput(name, parent=self.outputHrcGrp)
            self.tailOutputs.append(tailOutput)

        for i in xrange(len(self.deformerJoints), numDeformers):
            name = 'tail' + str(i + 1).zfill(2)
            tailDef = Joint(name, parent=self.defCmpGrp)
            tailDef.setComponent(self)
            self.deformerJoints.append(tailDef)

        return True


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FabriceTailRig, self).loadData( data )

        spine01Position = data['spine01Position']
        spine02Position = data['spine02Position']
        spine03Position = data['spine03Position']
        spine04Position = data['spine04Position']
        numDeformers = data['numDeformers']

        self.tailBaseCtrlSpace.xfo.tr = spine01Position
        self.tailBaseCtrl.xfo.tr = spine01Position

        self.tailBaseHandleCtrlSpace.xfo.tr = spine02Position
        self.tailBaseHandleCtrl.xfo.tr = spine02Position

        self.tailEndHandleCtrlSpace.xfo.tr = spine03Position
        self.tailEndHandleCtrl.xfo.tr = spine03Position

        self.tailEndCtrlSpace.xfo.tr = spine04Position
        self.tailEndCtrl.xfo.tr = spine04Position

        length = spine01Position.distanceTo(spine02Position) + spine02Position.distanceTo(spine03Position) + spine03Position.distanceTo(spine04Position)
        self.lengthInputAttr.setMax(length * 3.0)
        self.lengthInputAttr.setValue(length)

        # Update number of deformers and outputs
        self.setNumDeformers(numDeformers)

        for tailOutput in self.tailOutputs:
            if tailOutput not in self.bezierTailSpliceOp.getOutput("outputs"):
                self.bezierTailSpliceOp.setOutput("outputs", tailOutput)

        # Update Deformers Splice Op
        for tailOutput in self.tailOutputs:
            if tailOutput not in self.deformersToOutputsSpliceOp.getInput("constrainers"):
                self.deformersToOutputsSpliceOp.setInput("constrainers", tailOutput)

        for joint in self.deformerJoints:
            if joint not in self.deformersToOutputsSpliceOp.getOutput("constrainees"):
                self.deformersToOutputsSpliceOp.setOutput("constrainees", joint)

        # Updating constraint to use the updated last output.
        self.tailEndOutputConstraint.setConstrainer(self.tailOutputs[-1], index=0)

        # ============
        # Set IO Xfos
        # ============

        # ====================
        # Evaluate Splice Ops
        # ====================
        # evaluate the spine op so that all the output transforms are updated.
        self.bezierTailSpliceOp.evaluate()

        # evaluate the constraint op so that all the joint transforms are updated.
        self.deformersToOutputsSpliceOp.evaluate()

        # evaluate the constraints to ensure the outputs are now in the correct location.
        self.tailBaseOutputConstraint.evaluate()
        self.tailEndOutputConstraint.evaluate()



from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FabriceTailGuide)
ks.registerComponent(FabriceTailRig)