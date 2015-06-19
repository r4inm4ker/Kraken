from kraken.core.maths import Vec3

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
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


class SpineComponent(Component):
    """Spine Component"""

    def __init__(self, name="spineBase", parent=None):
        super(SpineComponent, self).__init__(name, parent)

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


class SpineComponentGuide(SpineComponent):
    """Spine Component Guide"""

    def __init__(self, name='spine', parent=None):

        Profiler.getInstance().push("Construct Spine Guide Component:" + name)
        super(SpineComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # ========

        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.numDeformersAttr = IntegerAttribute('numDeformers', value=1, minValue=0, maxValue=20, parent=guideSettingsAttrGrp)

        # Guide Controls
        self.cog = Control('cogPosition', parent=self.ctrlCmpGrp, shape="sphere")
        self.cog.setColor("red")

        self.spine01Ctrl = Control('spine01Position', parent=self.ctrlCmpGrp, shape="sphere")
        self.spine02Ctrl = Control('spine02Position', parent=self.ctrlCmpGrp, shape="sphere")
        self.spine03Ctrl = Control('spine03Position', parent=self.ctrlCmpGrp, shape="sphere")
        self.spine04Ctrl = Control('spine04Position', parent=self.ctrlCmpGrp, shape="sphere")

        self.loadData({
            "name": name,
            "location": "M",
            "cogPosition": Vec3(0.0, 11.1351, -0.1382),
            "spine01Position": Vec3(0.0, 11.1351, -0.1382),
            "spine02Position": Vec3(0.0, 11.8013, -0.1995),
            "spine03Position": Vec3(0.0, 12.4496, -0.3649),
            "spine04Position": Vec3(0.0, 13.1051, -0.4821),
            "numDeformers": 6
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

        data = {
            'class':"kraken.examples.spine_component.SpineComponentGuide",
            'name': self.getName(),
            'location': self.getLocation(),
            'cogPosition': self.cog.xfo.tr,
            'spine01Position': self.spine01Ctrl.xfo.tr,
            'spine02Position': self.spine02Ctrl.xfo.tr,
            'spine03Position': self.spine03Ctrl.xfo.tr,
            'spine04Position': self.spine04Ctrl.xfo.tr,
            'numDeformers': self.numDeformersAttr.getValue()
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

        self.setLocation(data.get('location', 'M'))
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

        data = {
            'class':"kraken.examples.spine_component.SpineComponentRig",
            'name': self.getName(),
            'location':self.getLocation(),
            'cogPosition': self.cog.xfo.tr,
            'spine01Position': self.spine01Ctrl.xfo.tr,
            'spine02Position': self.spine02Ctrl.xfo.tr,
            'spine03Position': self.spine03Ctrl.xfo.tr,
            'spine04Position': self.spine04Ctrl.xfo.tr,
            'numDeformers': self.numDeformersAttr.getValue()
           }

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


class SpineComponentRig(SpineComponent):
    """Spine Component"""

    def __init__(self, name="spine", parent=None):

        Profiler.getInstance().push("Construct Spine Rig Component:" + name)
        super(SpineComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # COG
        self.cogCtrlSpace = CtrlSpace('cog', parent=self.ctrlCmpGrp)
        self.cogCtrl = Control('cog', parent=self.cogCtrlSpace, shape="circle")
        self.cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        self.cogCtrl.setColor("orange")

        # Spine01
        self.spine01CtrlSpace = CtrlSpace('spine01', parent=self.cogCtrl)
        self.spine01Ctrl = Control('spine01', parent=self.spine01CtrlSpace, shape="circle")
        self.spine01Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))

        # Spine02
        self.spine02CtrlSpace = CtrlSpace('spine02', parent=self.spine01Ctrl)
        self.spine02Ctrl = Control('spine02', parent=self.spine02CtrlSpace, shape="circle")
        self.spine02Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))


        # Spine03
        self.spine03CtrlSpace = CtrlSpace('spine03', parent=self.spine02Ctrl)
        self.spine03Ctrl = Control('spine03', parent=self.spine03CtrlSpace, shape="circle")
        self.spine03Ctrl.scalePoints(Vec3(4.5, 4.5, 4.5))
        self.spine03Ctrl.setColor("blue")

        # Spine04
        self.spine04CtrlSpace = CtrlSpace('spine04', parent=self.cogCtrl)
        self.spine04Ctrl = Control('spine04', parent=self.spine04CtrlSpace, shape="circle")
        self.spine04Ctrl.scalePoints(Vec3(6.0, 6.0, 6.0))

        # Pelvis
        self.pelvisCtrlSpace = CtrlSpace('pelvis', parent=self.cogCtrl)
        self.pelvisCtrl = Control('pelvis', parent=self.pelvisCtrlSpace, shape="cube")
        self.pelvisCtrl.alignOnYAxis(negative=True)
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
        self.bezierSpineSpliceOp.setInput('base', self.spine01Ctrl)
        self.bezierSpineSpliceOp.setInput('baseHandle', self.spine02Ctrl)
        self.bezierSpineSpliceOp.setInput('tipHandle', self.spine03Ctrl)
        self.bezierSpineSpliceOp.setInput('tip', self.spine04Ctrl)

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
            spineOutput = Locator(name, parent=self.outputHrcGrp)
            self.spineOutputs.append(spineOutput)

        for i in xrange(len(self.deformerJoints), numDeformers):
            name = 'spine' + str(i + 1).zfill(2)
            spineDef = Joint(name, parent=self.defCmpGrp)
            spineDef.setComponent(self)
            self.deformerJoints.append(spineDef)

        return True


    def loadData(self, data=None):

        self.setName(data.get('name', 'spine'))
        location = data.get('location', 'M')
        self.setLocation(location)

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

        self.spine01CtrlSpace.xfo.tr = spine01Position
        self.spine01Ctrl.xfo.tr = spine01Position

        self.spine02CtrlSpace.xfo.tr = spine02Position
        self.spine02Ctrl.xfo.tr = spine02Position

        self.spine03CtrlSpace.xfo.tr = spine03Position
        self.spine03Ctrl.xfo.tr = spine03Position

        self.spine04CtrlSpace.xfo.tr = spine04Position
        self.spine04Ctrl.xfo.tr = spine04Position

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
ks.registerComponent(SpineComponentGuide)
ks.registerComponent(SpineComponentRig)
