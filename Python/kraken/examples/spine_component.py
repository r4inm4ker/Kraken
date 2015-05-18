from kraken.core.maths import Vec3

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute

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


class SpineComponentGuide(Component):
    """Spine Component Guide"""

    def __init__(self, name='spine', parent=None):
        super(SpineComponentGuide, self).__init__(name, parent)

        # Declare Inputs Xfos

        # Declare Output Xfos
        self.spineBaseOutput = self.addOutput('spineBase', dataType='Xfo')
        self.spineEndOutput = self.addOutput('spineEnd', dataType='Xfo')
        self.spineVertebraeOutput = self.addOutput('spineVertebrae', dataType='Xfo[]')

        # Declare Input Attrs

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

        # Guide Controls
        self.cog = Control('cogPosition', parent=ctrlCmpGrp, shape="sphere")
        self.cog.setColor("red")


        self.spine01Ctrl = Control('spine01Position', parent=ctrlCmpGrp, shape="sphere")
        self.spine02Ctrl = Control('spine02Position', parent=ctrlCmpGrp, shape="sphere")
        self.spine03Ctrl = Control('spine03Position', parent=ctrlCmpGrp, shape="sphere")
        self.spine04Ctrl = Control('spine04Position', parent=ctrlCmpGrp, shape="sphere")

        self.numDeformersAttr = IntegerAttribute('numDeformers', 1)

        # self.addInput(self.numDeformersAttr)

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


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = {
                "name": self.getName(),
                "location": self.getLocation(),
                "cogPosition": self.cog.xfo.tr,
                "spine01Position": self.spine01Ctrl.xfo.tr,
                "spine02Position": self.spine02Ctrl.xfo.tr,
                "spine03Position": self.spine03Ctrl.xfo.tr,
                "spine04Position": self.spine04Ctrl.xfo.tr,
                "numDeformers": self.numDeformersAttr.getValue()
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


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        # values

        return {
                "class":"kraken.examples.spine_component.SpineComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "cogPosition": self.cog.xfo.tr,
                "spine01Position": self.spine01Ctrl.xfo.tr,
                "spine02Position": self.spine02Ctrl.xfo.tr,
                "spine03Position": self.spine03Ctrl.xfo.tr,
                "spine04Position": self.spine04Ctrl.xfo.tr,
                "numDeformers": self.numDeformersAttr.getValue()
               }


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(SpineComponentGuide)


class SpineComponent(Component):
    """Spine Component"""

    def __init__(self, name="spine", parent=None):

        Profiler.getInstance().push("Construct Spine Component:" + name)
        super(SpineComponent, self).__init__(name, parent)

        # Declare Inputs Xfos

        # Declare Output Xfos
        self.spineBaseOutput = self.addOutput('spineBase', dataType='Xfo')
        self.spineEndOutput = self.addOutput('spineEnd', dataType='Xfo')
        self.spineVertebraeOutput = self.addOutput('spineVertebrae', dataType='Xfo[]')

        # Declare Input Attrs

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs')
        inputHrcGrp.addAttributeGroup(cmpInputAttrGrp)

        self.outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs')
        self.outputHrcGrp.addAttributeGroup(cmpOutputAttrGrp)

        # COG
        self.cogCtrlSpace = CtrlSpace('cog', parent=ctrlCmpGrp)

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


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        self.deformerJoints = []
        self.spineOutputs = []
        self.spineVertebraeOutput.setTarget(self.spineOutputs)
        self.setNumDeformers(1)

        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's

        spineBaseOutputTgt = Locator('spineBase', parent=self.outputHrcGrp)
        spineEndOutputTgt = Locator('spineEnd', parent=self.outputHrcGrp)

        self.spineBaseOutput.setTarget(spineBaseOutputTgt)
        self.spineEndOutput.setTarget(spineEndOutputTgt)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)

        self.lengthInputAttr = FloatAttribute('length', 1.0)

        cmpInputAttrGrp.addAttribute(debugInputAttr)
        cmpInputAttrGrp.addAttribute(self.lengthInputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        self.spineBaseOutputConstraint = PoseConstraint('_'.join([spineBaseOutputTgt.getName(), 'To', 'spineBase']))
        self.spineBaseOutputConstraint.addConstrainer(self.spineOutputs[0])
        spineBaseOutputTgt.addConstraint(self.spineBaseOutputConstraint)

        self.spineEndOutputConstraint = PoseConstraint('_'.join([spineEndOutputTgt.getName(), 'To', 'spineEnd']))
        self.spineEndOutputConstraint.addConstrainer(self.spineOutputs[0])
        spineEndOutputTgt.addConstraint(self.spineEndOutputConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's

        # for spineOutput in self.spineOutputs:
        #     self.addOutput(spineOutput)

        # self.addOutput(spineBaseOutputTgt)
        # self.addOutput(spineEndOutputTgt)

        # # Add Attribute I/O's
        # self.addInput(debugInputAttr)
        # self.addInput(self.lengthInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        self.bezierSpineSpliceOp = SpliceOperator("spineSpliceOp", "BezierSpineSolver", "Kraken")
        self.addOperator(self.bezierSpineSpliceOp)

        # Add Att Inputs
        self.bezierSpineSpliceOp.setInput("debug", debugInputAttr)
        self.bezierSpineSpliceOp.setInput("length", self.lengthInputAttr)

        # Add Xfo Inputs
        self.bezierSpineSpliceOp.setInput("base", self.spine01Ctrl)
        self.bezierSpineSpliceOp.setInput("baseHandle", self.spine02Ctrl)
        self.bezierSpineSpliceOp.setInput("tipHandle", self.spine03Ctrl)
        self.bezierSpineSpliceOp.setInput("tip", self.spine04Ctrl)

        # Add Xfo Outputs
        for spineOutput in self.spineOutputs:
            self.bezierSpineSpliceOp.setOutput("outputs", spineOutput)

        # Add Deformer Splice Op
        self.outputsToDeformersSpliceOp = SpliceOperator("spineDeformerSpliceOp", "MultiPoseConstraintSolver", "Kraken")
        self.addOperator(self.outputsToDeformersSpliceOp)

        # Add Att Inputs
        self.outputsToDeformersSpliceOp.setInput("debug", debugInputAttr)

        # Add Xfo Outputs
        for spineOutput in self.spineOutputs:
            self.outputsToDeformersSpliceOp.setInput("constrainers", spineOutput)

        # Add Xfo Outputs
        for joint in self.deformerJoints:
            self.outputsToDeformersSpliceOp.setOutput("constrainees", joint)

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
            if spineOutput not in self.outputsToDeformersSpliceOp.getInput("constrainers"):
                self.outputsToDeformersSpliceOp.setInput("constrainers", spineOutput)

        for joint in self.deformerJoints:
            if joint not in self.outputsToDeformersSpliceOp.getOutput("constrainees"):
                self.outputsToDeformersSpliceOp.setOutput("constrainees", joint)

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
        self.outputsToDeformersSpliceOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(SpineComponent)
