from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control  import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class NeckComponentGuide(Component):
    """Neck Component Guide"""

    def __init__(self, name='neck', parent=None, data=None):
        super(NeckComponentGuide, self).__init__(name, parent)

        # Declare Inputs Xfos
        self.neckBaseInput = self.addInput('neckBase', dataType='Xfo')

        # Declare Output Xfos
        self.neckEndOutput = self.addOutput('neckEnd', dataType='Xfo')
        self.neckOutput = self.addOutput('neck', dataType='Xfo')

        # Declare Input Attrs

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
        self.neckCtrl = Control('neck', parent=ctrlCmpGrp, shape="sphere")
        self.neckEndCtrl = Control('neckEnd', parent=ctrlCmpGrp, shape="sphere")

        if data is None:
            data = {
                    "name": name,
                    "location": "M",
                    "neckPosition": Vec3(0.0, 16.5572, -0.6915),
                    "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
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
                "neckPosition": self.neckCtrl.xfo.tr,
                "neckEndPosition": self.neckEndCtrl.xfo.tr
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
        self.neckCtrl.xfo.tr = data['neckPosition']
        self.neckEndCtrl.xfo.tr = data['neckEndPosition']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        # values
        neckEndPosition = self.neckCtrl.xfo.tr
        neckPosition = self.neckEndCtrl.xfo.tr
        neckUpV = Vec3(0.0, 0.0, -1.0)

        # Calculate Neck Xfo
        rootToEnd = neckEndPosition.subtract(neckPosition).unit()
        rootToUpV = neckUpV.subtract(neckPosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()

        neckXfo = Xfo()
        neckXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, neckPosition)

        data = {
                "class":"kraken.examples.neck_component.NeckComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "neckXfo": neckXfo
               }

        return data


class NeckComponent(Component):
    """Neck Component"""

    def __init__(self, name="neck", parent=None):

        Profiler.getInstance().push("Construct Neck Component:" + name)
        super(NeckComponent, self).__init__(name, parent)

        # Declare Inputs Xfos
        self.neckBaseInput = self.addInput('neckBase', dataType='Xfo')

        # Declare Output Xfos
        self.neckEndOutput = self.addOutput('neckEnd', dataType='Xfo')
        self.neckOutput = self.addOutput('neck', dataType='Xfo')

        # Declare Input Attrs

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=controlsLayer)
        ctrlCmpGrp.setComponent(self)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs', parent=inputHrcGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs', parent=outputHrcGrp)

        # Neck
        self.neckCtrlSpace = CtrlSpace('neck', parent=ctrlCmpGrp)
        self.neckCtrl = Control('neck', parent=self.neckCtrlSpace, shape="pin")
        self.neckCtrl.scalePoints(Vec3(1.25, 1.25, 1.25))
        self.neckCtrl.translatePoints(Vec3(0, 0, -0.5))
        self.neckCtrl.rotatePoints(90, 0, 90)
        self.neckCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        neckDef = Joint('neck', parent=defCmpGrp)
        neckDef.setComponent(self)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        self.neckEndInputTgt = Locator('neckBase', parent=inputHrcGrp)
        self.neckEndOutputTgt = Locator('neckEnd', parent=outputHrcGrp)
        self.neckOutputTgt = Locator('neck', parent=outputHrcGrp)

        # Set IO Targets
        self.neckBaseInput.setTarget(self.neckEndInputTgt)
        self.neckEndOutput.setTarget(self.neckEndOutputTgt)
        self.neckOutput.setTarget(self.neckOutputTgt)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', value=True, parent=cmpInputAttrGrp)
        rightSideInputAttr = BoolAttribute('rightSide', value=self.getLocation() is 'R', parent=cmpInputAttrGrp)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([self.neckCtrlSpace.getName(), 'To', self.neckEndInputTgt.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(self.neckEndInputTgt)
        self.neckCtrlSpace.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        neckEndConstraint = PoseConstraint('_'.join([self.neckEndOutputTgt.getName(), 'To', self.neckCtrl.getName()]))
        neckEndConstraint.addConstrainer(self.neckCtrl)
        self.neckEndOutputTgt.addConstraint(neckEndConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        #Add Deformer Splice Op
        spliceOp = SpliceOperator("neckDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputstrl)
        spliceOp.setInput("constrainer", self.neckEndOutputTgt)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", neckDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'neck'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.neckCtrlSpace.xfo = data['neckXfo']
        self.neckCtrl.xfo = data['neckXfo']

        # ============
        # Set IO Xfos
        # ============
        self.neckEndInputTgt.xfo = data['neckXfo']
        self.neckEndOutputTgt.xfo = data['neckXfo']
        self.neckOutputTgt.xfo = data['neckXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(NeckComponent)
ks.registerComponent(NeckComponentGuide)
