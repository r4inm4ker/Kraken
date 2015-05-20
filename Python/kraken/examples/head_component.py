from kraken.core.maths import Vec3

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class HeadComponentGuide(Component):
    """Head Component Guide"""

    def __init__(self, name='head', parent=None, data=None):
        super(HeadComponentGuide, self).__init__(name, parent)

        # ================
        # Setup Hierarchy
        # ================
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs', parent=inputHrcGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs', parent=outputHrcGrp)


        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.headBaseInputTgt = self.createInput('headBase', dataType='Xfo', parent=inputHrcGrp)

        # Declare Output Xfos
        self.headOutputTgt = self.createOutput('head', dataType='Xfo', parent=outputHrcGrp)
        self.jawOutputTgt = self.createOutput('jaw', dataType='Xfo', parent=outputHrcGrp)
        self.eyeLOutputTgt = self.createOutput('eyeL', dataType='Xfo', parent=outputHrcGrp)
        self.eyeROutputTgt = self.createOutput('eyeR', dataType='Xfo', parent=outputHrcGrp)

        # Declare Input Attrs
        self.debugInputAttr = self.createInput('debug', dataType='Boolean', parent=cmpInputAttrGrp)

        # Declare Output Attrs

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs', parent=inputHrcGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs', parent=outputHrcGrp)

        # Guide Controls
        self.headCtrl = Control('head', parent=ctrlCmpGrp, shape="cube")
        self.headEndCtrl = Control('headEnd', parent=ctrlCmpGrp, shape="sphere")
        self.eyeLeftCtrl = Control('eyeLeft', parent=ctrlCmpGrp, shape="sphere")
        self.eyeRightCtrl = Control('eyeRight', parent=ctrlCmpGrp, shape="sphere")
        self.jawCtrl = Control('jaw', parent=ctrlCmpGrp, shape="cube")

        if data is None:
            data = {
                    "name": name,
                    "location": "M",
                    "headPosition": Vec3(0.0, 17.4756, -0.421),
                    "headEndPosition": Vec3(0.0, 19.5, -0.421),
                    "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
                    "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
                    "jawPosition": Vec3(0.0, 17.613, -0.2731)
                   }

        self.loadData(data)


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
                "headPosition": self.headCtrl.xfo.tr,
                "headEndPosition": self.headEndCtrl.xfo.tr,
                "eyeLeftPosition": self.eyeLeftCtrl.xfo.tr,
                "eyeRightPosition": self.eyeRightCtrl.xfo.tr,
                "jawPosition": self.jawCtrl.xfo.tr
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
        self.headCtrl.xfo.tr = data['headPosition']
        self.headEndCtrl.xfo.tr = data['headEndPosition']
        self.eyeLeftCtrl.xfo.tr = data['eyeLeftPosition']
        self.eyeRightCtrl.xfo.tr = data['eyeRightPosition']
        self.jawCtrl.xfo.tr = data['jawPosition']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = {
                "class":"kraken.examples.head_component.HeadComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "headPosition": self.headCtrl.xfo.tr,
                "headEndPosition": self.headEndCtrl.xfo.tr,
                "eyeLeftPosition": self.eyeLeftCtrl.xfo.tr,
                "eyeRightPosition": self.eyeRightCtrl.xfo.tr,
                "jawPosition": self.jawCtrl.xfo.tr
               }

        return data



class HeadComponent(Component):
    """Head Component"""

    def __init__(self, name='head', parent=None):

        Profiler.getInstance().push("Construct Head Component:" + name)
        super(HeadComponent, self).__init__(name, parent)

        # ================
        # Setup Hierarchy
        # ================
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs', parent=inputHrcGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs', parent=outputHrcGrp)


        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.headBaseInputTgt = self.createInput('headBase', dataType='Xfo', parent=inputHrcGrp)

        # Declare Output Xfos
        self.headOutputTgt = self.createOutput('head', dataType='Xfo', parent=outputHrcGrp)
        self.jawOutputTgt = self.createOutput('jaw', dataType='Xfo', parent=outputHrcGrp)
        self.eyeLOutputTgt = self.createOutput('eyeL', dataType='Xfo', parent=outputHrcGrp)
        self.eyeROutputTgt = self.createOutput('eyeR', dataType='Xfo', parent=outputHrcGrp)

        # Declare Input Attrs
        self.debugInputAttr = self.createInput('debug', dataType='Boolean', parent=cmpInputAttrGrp)

        # Declare Output Attrs


        # =========
        # Controls
        # =========
        # Head
        self.headCtrlSpace = CtrlSpace('head', parent=ctrlCmpGrp)
        self.headCtrl = Control('head', parent=self.headCtrlSpace, shape="circle")
        self.headCtrl.rotatePoints(0, 0, 90)
        self.headCtrl.scalePoints(Vec3(3, 3, 3))
        self.headCtrl.translatePoints(Vec3(0, 1, 0.25))

        # Eye Left
        self.eyeLeftCtrlSpace = CtrlSpace('eyeLeft', parent=self.headCtrl)
        self.eyeLeftCtrl = Control('eyeLeft', parent=self.eyeLeftCtrlSpace, shape="sphere")
        self.eyeLeftCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.eyeLeftCtrl.setColor("blueMedium")

        # Eye Right
        self.eyeRightCtrlSpace = CtrlSpace('eyeRight', parent=self.headCtrl)
        self.eyeRightCtrl = Control('eyeRight', parent=self.eyeRightCtrlSpace, shape="sphere")
        self.eyeRightCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.eyeRightCtrl.setColor("blueMedium")

        # Jaw
        self.jawCtrlSpace = CtrlSpace('jawCtrlSpace', parent=self.headCtrl)
        self.jawCtrl = Control('jaw', parent=self.jawCtrlSpace, shape="cube")
        self.jawCtrl.alignOnYAxis(negative=True)
        self.jawCtrl.alignOnZAxis()
        self.jawCtrl.scalePoints(Vec3(1.45, 0.65, 1.25))
        self.jawCtrl.translatePoints(Vec3(0, -0.25, 0))
        self.jawCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        headDef = Joint('head', parent=defCmpGrp)
        headDef.setComponent(self)

        jawDef = Joint('jaw', parent=defCmpGrp)
        jawDef.setComponent(self)

        eyeLeftDef = Joint('eyeLeft', parent=defCmpGrp)
        eyeLeftDef.setComponent(self)

        eyeRightDef = Joint('eyeRight', parent=defCmpGrp)
        eyeRightDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        headInputConstraint = PoseConstraint('_'.join([self.headCtrlSpace.getName(), 'To', self.headBaseInputTgt.getName()]))
        headInputConstraint.setMaintainOffset(True)
        headInputConstraint.addConstrainer(self.headBaseInputTgt)
        self.headCtrlSpace.addConstraint(headInputConstraint)

        # Constraint outputs
        headOutputConstraint = PoseConstraint('_'.join([self.headOutputTgt.getName(), 'To', self.headCtrl.getName()]))
        headOutputConstraint.setMaintainOffset(True)
        headOutputConstraint.addConstrainer(self.headCtrl)
        self.headOutputTgt.addConstraint(headOutputConstraint)

        jawOutputConstraint = PoseConstraint('_'.join([self.jawOutputTgt.getName(), 'To', self.jawCtrl.getName()]))
        jawOutputConstraint.setMaintainOffset(True)
        jawOutputConstraint.addConstrainer(self.jawCtrl)
        self.jawOutputTgt.addConstraint(jawOutputConstraint)

        eyeLOutputConstraint = PoseConstraint('_'.join([self.eyeLOutputTgt.getName(), 'To', self.eyeLeftCtrl.getName()]))
        eyeLOutputConstraint.setMaintainOffset(True)
        eyeLOutputConstraint.addConstrainer(self.eyeLeftCtrl)
        self.eyeLOutputTgt.addConstraint(eyeLOutputConstraint)

        eyeROutputConstraint = PoseConstraint('_'.join([self.eyeROutputTgt.getName(), 'To', self.eyeRightCtrl.getName()]))
        eyeROutputConstraint.setMaintainOffset(True)
        eyeROutputConstraint.addConstrainer(self.eyeRightCtrl)
        self.eyeROutputTgt.addConstraint(eyeROutputConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        # self.addInput(self.headBaseInputTgt)

        # self.addOutput(self.headOutputTgt)
        # self.addOutput(self.jawOutputTgt)
        # self.addOutput(self.eyeLOutputTgt)
        # self.addOutput(self.eyeROutputTgt)

        # Add Attribute I/O's
        # self.addInput(self.debugInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        # spliceOp = SpliceOperator("headDeformerSpliceOp", "HeadConstraintSolver", "KrakenHeadConstraintSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", self.debugInputAttr)

        # # Add Xfo Inputstrl)
        # spliceOp.setInput("headConstrainer", self.headOutputTgt)
        # spliceOp.setInput("jawConstrainer", self.jawOutputTgt)
        # spliceOp.setInput("eyeLeftConstrainer", self.eyeLOutputTgt)
        # spliceOp.setInput("eyeRightConstrainer", self.eyeROutputTgt)

        # # Add Xfo Outputs
        # spliceOp.setOutput("headDeformer", headDef)
        # spliceOp.setOutput("jawDeformer", jawDef)
        # spliceOp.setOutput("eyeLeftDeformer", eyeLeftDef)
        # spliceOp.setOutput("eyeRightDeformer", eyeRightDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'head'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.headCtrlSpace.xfo.tr = data['headPosition']
        self.headCtrl.xfo.tr = data['headPosition']
        self.eyeLeftCtrlSpace.xfo.tr = data['eyeLeftPosition']
        self.eyeLeftCtrl.xfo.tr = data['eyeLeftPosition']
        self.eyeRightCtrlSpace.xfo.tr = data['eyeRightPosition']
        self.eyeRightCtrl.xfo.tr = data['eyeRightPosition']
        self.jawCtrlSpace.xfo.tr = data['jawPosition']
        self.jawCtrl.xfo.tr = data['jawPosition']

        # ============
        # Set IO Xfos
        # ============
        self.headBaseInputTgt.xfo.tr = data['headPosition']
        self.headOutputTgt.xfo.tr = data['headPosition']
        self.jawOutputTgt.xfo.tr = data['jawPosition']
        self.eyeLOutputTgt.xfo.tr = data['eyeLeftPosition']
        self.eyeROutputTgt.xfo.tr = data['eyeRightPosition']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(HeadComponent)
ks.registerComponent(HeadComponentGuide)
