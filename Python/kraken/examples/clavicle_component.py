from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

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
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.plugins import getInspector

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class ClavicleComponentGuide(Component):
    """Clavicle Component Guide"""

    def __init__(self, name='clavicle', parent=None, data=None):
        super(ClavicleComponentGuide, self).__init__(name, parent)

        # Declare Inputs Xfos
        self.spineEndInput = self.addInput('spineEnd', dataType='Xfo')

        # Declare Output Xfos
        self.clavicleOutput = self.addOutput('clavicle', dataType='Xfo')
        self.clavicleEndOutput = self.addOutput('clavicleEnd', dataType='Xfo')

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
        self.clavicleCtrl = Control('clavicle', parent=ctrlCmpGrp, shape="sphere")
        self.clavicleUpVCtrl = Control('clavicleUpV', parent=ctrlCmpGrp, shape="sphere")
        self.clavicleEndCtrl = Control('clavicleEnd', parent=ctrlCmpGrp, shape="sphere")

        if data is None:
            data = {
                    "name": name,
                    "location": "L",
                    "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
                    "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
                    "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
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
            'name': self.getName(),
            'location': self.getLocation(),
            'clavicleXfo': self.clavicleCtrl.xfo,
            'clavicleUpVXfo': self.clavicleUpVCtrl.xfo,
            'clavicleEndXfo': self.clavicleEndCtrl.xfo
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
        self.clavicleCtrl.xfo = data['clavicleXfo']
        self.clavicleUpVCtrl.xfo = self.clavicleCtrl.xfo.multiply(data['clavicleUpVXfo'])
        self.clavicleEndCtrl.xfo = data['clavicleEndXfo']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        # values
        claviclePosition = self.clavicleCtrl.xfo.tr
        clavicleUpV = self.clavicleUpVCtrl.xfo.tr
        clavicleEndPosition = self.clavicleEndCtrl.xfo.tr

        # Calculate Clavicle Xfo
        rootToEnd = clavicleEndPosition.subtract(claviclePosition).unit()
        rootToUpV = clavicleUpV.subtract(claviclePosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()

        clavicleXfo = Xfo()
        clavicleXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, claviclePosition)

        clavicleLen = claviclePosition.subtract(clavicleEndPosition).length()

        return {
                "class":"kraken.examples.clavicle_component.ClavicleComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "clavicleXfo": clavicleXfo,
                "clavicleLen": clavicleLen
                }


    # ==========
    # Sync Data
    # ==========
    def syncData(self):

        guideInspector = getInspector()
        guideInspector.createHierarchyMap(self)

        hrcMap = guideInspector.getHierarchyMap()

        print "Mapping: "
        for k, v, in hrcMap.iteritems():
            print k
            print v
            print "\n"

        return


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(ClavicleComponentGuide)


class ClavicleComponent(Component):
    """Clavicle Component"""

    def __init__(self, name='Clavicle', parent=None):

        Profiler.getInstance().push("Construct Clavicle Component:" + name)
        super(ClavicleComponent, self).__init__(name, parent)

        # Declare Inputs Xfos
        self.spineEndInput = self.addInput('spineEnd', dataType='Xfo')

        # Declare Output Xfos
        self.clavicleOutput = self.addOutput('clavicle', dataType='Xfo')
        self.clavicleEndOutput = self.addOutput('clavicleEnd', dataType='Xfo')

        # Declare Input Attrs

        # Declare Output Attrs

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

        # Clavicle
        self.clavicleCtrlSpace = CtrlSpace('clavicle', parent=ctrlCmpGrp)
        self.clavicleCtrl = Control('clavicle', parent=self.clavicleCtrlSpace, shape="cube")
        self.clavicleCtrl.alignOnXAxis()


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        ctrlCmpGrp.setComponent(self)

        self.clavicleDef = Joint('clavicle', parent=defCmpGrp)
        self.clavicleDef.setComponent(self)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        self.spineEndInputTgt = Locator('spineEnd', parent=inputHrcGrp)

        self.clavicleOutputTgt = Locator('clavicle', parent=outputHrcGrp)
        self.clavicleEndOutputTgt = Locator('clavicleEnd', parent=outputHrcGrp)

        # Set IO Targets
        self.spineEndInput.setTarget(self.spineEndInputTgt)

        self.clavicleOutput.setTarget(self.clavicleOutputTgt)
        self.clavicleEndOutput.setTarget(self.clavicleEndOutputTgt)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', self.getLocation() is 'R')

        armFollowBodyOutputAttr = FloatAttribute('followBody', 0.0)

        cmpInputAttrGrp.addAttribute(debugInputAttr)
        cmpInputAttrGrp.addAttribute(rightSideInputAttr)

        cmpOutputAttrGrp.addAttribute(armFollowBodyOutputAttr)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([self.clavicleCtrl.getName(), 'To', self.spineEndInput.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(self.spineEndInputTgt)
        self.clavicleCtrlSpace.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        clavicleConstraint = PoseConstraint('_'.join([self.clavicleOutputTgt.getName(), 'To', self.clavicleCtrl.getName()]))
        clavicleConstraint.addConstrainer(self.clavicleCtrl)
        self.clavicleOutputTgt.addConstraint(clavicleConstraint)

        clavicleEndConstraint = PoseConstraint('_'.join([self.clavicleEndOutputTgt.getName(), 'To', self.clavicleCtrl.getName()]))
        clavicleEndConstraint.addConstrainer(self.clavicleCtrl)
        self.clavicleEndOutputTgt.addConstraint(clavicleEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        # self.addInput(self.spineEndInputTgt)
        # self.addOutput(self.clavicleEndOutputTgt)
        # self.addOutput(self.clavicleOutputTgt)

        # Add Attribute I/O's
        # self.addInput(debugInputAttr)
        # self.addInput(rightSideInputAttr)
        # self.addOutput(armFollowBodyOutputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        spliceOp = SpliceOperator("clavicleDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput("constrainer", self.clavicleOutputTgt)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", self.clavicleDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'clavicle'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.clavicleCtrlSpace.xfo = data['clavicleXfo']
        self.clavicleCtrl.xfo = data['clavicleXfo']
        self.clavicleCtrl.scalePoints(Vec3(data['clavicleLen'], 0.75, 0.75))

        if location == "R":
            self.clavicleCtrl.translatePoints(Vec3(0.0, 0.0, -1.0))
        else:
            self.clavicleCtrl.translatePoints(Vec3(0.0, 0.0, 1.0))

        # ============
        # Set IO Xfos
        # ============
        self.spineEndInputTgt.xfo = data['clavicleXfo']
        self.clavicleEndOutputTgt.xfo = data['clavicleXfo']
        self.clavicleOutputTgt.xfo = data['clavicleXfo']

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(ClavicleComponent)
