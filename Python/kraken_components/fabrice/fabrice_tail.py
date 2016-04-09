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

from kraken.core.objects.operators.kl_operator import KLOperator

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
        self.tailMainSrtInputTgt = self.createInput('mainSrt', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.cogInputTgt = self.createInput('cog', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.spineEndInputTgt = self.createInput('spineEnd', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.spineEndCtrlInputTgt = self.createInput('spineEndCtrl', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.tailBaseOutputTgt = self.createOutput('tailBase', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.tailEndOutputTgt = self.createOutput('tailEnd', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        self.tailVertebraeOutput = self.createOutput('tailVertebrae', dataType='Xfo[]')

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.lengthInputAttr = self.createInput('length', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

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
        self.numDeformersAttr.setValueChangeCallback(self.updateNumDeformers)


        # Guide Controls
        self.tailBaseCtrl = Control('tailBase', parent=self.ctrlCmpGrp, shape='sphere')
        self.tailBaseCtrl.scalePoints(Vec3(1.2, 1.2, 1.2))
        self.tailBaseCtrl.lockScale(x=True, y=True, z=True)
        self.tailBaseCtrl.setColor("turqoise")

        self.tailBaseHandleCtrl = Control('tailBaseHandle', parent=self.ctrlCmpGrp, shape='pin')
        self.tailBaseHandleCtrl.rotatePoints(90, 0, 0)
        self.tailBaseHandleCtrl.translatePoints(Vec3(0, 1.0, 0))
        self.tailBaseHandleCtrl.lockScale(x=True, y=True, z=True)
        self.tailBaseHandleCtrl.setColor("turqoise")

        self.tailEndHandleCtrl = Control('tailEndHandle', parent=self.ctrlCmpGrp, shape='pin')
        self.tailEndHandleCtrl.rotatePoints(90, 0, 0)
        self.tailEndHandleCtrl.translatePoints(Vec3(0, 1.0, 0))
        self.tailEndHandleCtrl.lockScale(x=True, y=True, z=True)
        self.tailEndHandleCtrl.setColor("turqoise")

        self.tailEndCtrl = Control('tailEnd', parent=self.ctrlCmpGrp, shape='pin')
        self.tailEndCtrl.rotatePoints(90, 0, 0)
        self.tailEndCtrl.translatePoints(Vec3(0, 1.0, 0))
        self.tailEndCtrl.lockScale(x=True, y=True, z=True)
        self.tailEndCtrl.setColor("turqoise")

        # ===============
        # Add Splice Ops
        # ===============
        # Add Tail Splice Op
        self.bezierSpineKLOp = KLOperator('spineGuideKLOp', 'BezierSpineSolver', 'Kraken')
        self.bezierSpineKLOp.setOutput('outputs', self.tailVertebraeOutput.getTarget())

        self.addOperator(self.bezierSpineKLOp)

        # Add Att Inputs
        self.bezierSpineKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.bezierSpineKLOp.setInput('rigScale', self.rigScaleInputAttr)
        self.bezierSpineKLOp.setInput('length', self.lengthInputAttr)

        # Add Xfo Inputs
        self.bezierSpineKLOp.setInput('base', self.tailBaseCtrl)
        self.bezierSpineKLOp.setInput('baseHandle', self.tailBaseHandleCtrl)
        self.bezierSpineKLOp.setInput('tipHandle', self.tailEndHandleCtrl)
        self.bezierSpineKLOp.setInput('tip', self.tailEndCtrl)

        data = {
            'name': name,
            'location': 'M',
            'tailBasePos': Vec3(0.0, 0.65, -3.1),
            'tailBaseHandlePos': Vec3(0.0, 0.157, -4.7),
            'tailBaseHandleCtrlCrvData': self.tailBaseHandleCtrl.getCurveData(),
            'tailEndHandlePos': Vec3(0.0, 0.0625, -6.165),
            'tailEndHandleCtrlCrvData': self.tailEndHandleCtrl.getCurveData(),
            'tailEndPos': Vec3(0.0, -0.22, -7.42),
            'tailEndCtrlCrvData': self.tailEndCtrl.getCurveData(),
            'numDeformers': 6
        }

        self.loadData(data)

        Profiler.getInstance().pop()


    # ==========
    # Callbacks
    # ==========
    def updateNumDeformers(self, count):
        """Generate the guide controls for the variable outputes array.

        Arguments:
        count -- object, The number of joints inthe chain.

        Return:
        True if successful.

        """

        if count == 0:
            raise IndexError("'count' must be > 0")


        vertebraeOutputs = self.tailVertebraeOutput.getTarget()
        if count > len(vertebraeOutputs):
            for i in xrange(len(vertebraeOutputs), count):
                debugCtrl = Control('spine' + str(i+1).zfill(2), parent=self.outputHrcGrp, shape="vertebra")
                debugCtrl.rotatePoints(0, -90, 0)
                debugCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
                debugCtrl.setColor('turqoise')
                vertebraeOutputs.append(debugCtrl)

        elif count < len(vertebraeOutputs):
            numExtraCtrls = len(vertebraeOutputs) - count
            for i in xrange(numExtraCtrls):
                extraCtrl = vertebraeOutputs.pop()
                self.outputHrcGrp.removeChild(extraCtrl)

        return True

    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = super(FabriceTailGuide, self).saveData()

        data['tailBasePos'] = self.tailBaseCtrl.xfo.tr

        data['tailBaseHandlePos'] = self.tailBaseHandleCtrl.xfo.tr
        data['tailBaseHandleCtrlCrvData'] = self.tailBaseHandleCtrl.getCurveData()

        data['tailEndHandlePos'] = self.tailEndHandleCtrl.xfo.tr
        data['tailEndHandleCtrlCrvData'] = self.tailEndHandleCtrl.getCurveData()

        data['tailEndPos'] = self.tailEndCtrl.xfo.tr
        data['tailEndCtrlCrvData'] = self.tailEndCtrl.getCurveData()

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

        self.tailBaseCtrl.xfo.tr = data["tailBasePos"]

        self.tailBaseHandleCtrl.xfo.tr = data["tailBaseHandlePos"]
        self.tailBaseHandleCtrl.setCurveData(data['tailBaseHandleCtrlCrvData'])

        self.tailEndHandleCtrl.xfo.tr = data["tailEndHandlePos"]
        self.tailEndHandleCtrl.setCurveData(data['tailEndHandleCtrlCrvData'])

        self.tailEndCtrl.xfo.tr = data["tailEndPos"]
        self.tailEndCtrl.setCurveData(data['tailEndCtrlCrvData'])

        self.numDeformersAttr.setValue(data["numDeformers"])

        length = data["tailBasePos"].distanceTo(data["tailBaseHandlePos"]) + data["tailBaseHandlePos"].distanceTo(data["tailEndHandlePos"]) + data["tailEndHandlePos"].distanceTo(data["tailEndPos"])
        self.lengthInputAttr.setMax(length * 3.0)
        self.lengthInputAttr.setValue(length)

        self.bezierSpineKLOp.evaluate()

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(FabriceTailGuide, self).getRigBuildData()

        data['tailBasePos'] = self.tailBaseCtrl.xfo.tr

        data['tailBaseHandlePos'] = self.tailBaseHandleCtrl.xfo.tr
        data['tailBaseHandleCtrlCrvData'] = self.tailBaseHandleCtrl.getCurveData()

        data['tailEndHandlePos'] = self.tailEndHandleCtrl.xfo.tr
        data['tailEndHandleCtrlCrvData'] = self.tailEndHandleCtrl.getCurveData()

        data['tailEndPos'] = self.tailEndCtrl.xfo.tr
        data['tailEndCtrlCrvData'] = self.tailEndCtrl.getCurveData()

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
        # self.tailBaseCtrlSpace = CtrlSpace('tailBase', parent=self.ctrlCmpGrp)
        # self.tailBaseCtrl = Control('tailBase', parent=self.tailBaseCtrlSpace, shape="circle")
        # self.tailBaseCtrl.rotatePoints(90, 0, 0)
        # self.tailBaseCtrl.scalePoints(Vec3(2.0, 2.0, 2.0))
        # self.tailBaseCtrl.setColor("greenBlue")

        # Tail Base Handle
        self.tailBaseHandleCtrlSpace = CtrlSpace('tailBaseHandle', parent=self.ctrlCmpGrp)
        self.tailBaseHandleCtrl = Control('tailBaseHandle', parent=self.tailBaseHandleCtrlSpace, shape="pin")
        self.tailBaseHandleCtrl.lockScale(x=True, y=True, z=True)
        self.tailBaseHandleCtrl.setColor("turqoise")

        # Tail End Handle
        self.tailEndHandleCtrlSpace = CtrlSpace('tailEndHandle', parent=self.ctrlCmpGrp)
        self.tailEndHandleCtrl = Control('tailEndHandle', parent=self.tailEndHandleCtrlSpace, shape="pin")
        self.tailEndHandleCtrl.lockScale(x=True, y=True, z=True)
        self.tailEndHandleCtrl.setColor("turqoise")

        # Tail End
        self.tailEndCtrlSpace = CtrlSpace('tailEnd', parent=self.tailEndHandleCtrl)
        self.tailEndCtrl = Control('tailEnd', parent=self.tailEndCtrlSpace, shape="pin")
        self.tailEndCtrl.lockScale(x=True, y=True, z=True)
        self.tailEndCtrl.setColor("greenBlue")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

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
        self.tailBaseHandleInputConstraint = PoseConstraint('_'.join([self.tailBaseHandleCtrlSpace.getName(), 'To', self.spineEndCtrlInputTgt.getName()]))
        self.tailBaseHandleInputConstraint.addConstrainer(self.spineEndCtrlInputTgt)
        self.tailBaseHandleInputConstraint.setMaintainOffset(True)
        self.tailBaseHandleCtrlSpace.addConstraint(self.tailBaseHandleInputConstraint)

        self.tailEndHandleInputConstraint = PoseConstraint('_'.join([self.tailEndHandleCtrlSpace.getName(), 'To', self.cogInputTgt.getName()]))
        self.tailEndHandleInputConstraint.addConstrainer(self.cogInputTgt)
        self.tailEndHandleInputConstraint.setMaintainOffset(True)
        self.tailEndHandleCtrlSpace.addConstraint(self.tailEndHandleInputConstraint)

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
        self.bezierTailKLOp = KLOperator('tailKLOp', 'BezierSpineSolver', 'Kraken')
        self.addOperator(self.bezierTailKLOp)

        # Add Att Inputs
        self.bezierTailKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.bezierTailKLOp.setInput('rigScale', self.rigScaleInputAttr)
        self.bezierTailKLOp.setInput('length', self.lengthInputAttr)

        # Add Xfo Inputs
        self.bezierTailKLOp.setInput('base', self.spineEndInputTgt)
        self.bezierTailKLOp.setInput('baseHandle', self.tailBaseHandleCtrl)
        self.bezierTailKLOp.setInput('tipHandle', self.tailEndHandleCtrl)
        self.bezierTailKLOp.setInput('tip', self.tailEndCtrl)

        # Add Xfo Outputs
        self.bezierTailKLOp.setOutput('outputs', self.tailOutputs)

        # Add Deformer Splice Op
        self.deformersToOutputsKLOp = KLOperator('tailDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.deformersToOutputsKLOp)

        # Add Att Inputs
        self.deformersToOutputsKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.deformersToOutputsKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Outputs
        self.deformersToOutputsKLOp.setInput('constrainers', self.tailOutputs)

        # Add Xfo Outputs
        self.deformersToOutputsKLOp.setOutput('constrainees', self.deformerJoints)

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

        tailBasePos = data['tailBasePos']

        tailBaseHandlePos = data['tailBaseHandlePos']
        tailBaseHandleCtrlCrvData = data['tailBaseHandleCtrlCrvData']

        tailEndHandlePos = data['tailEndHandlePos']
        tailEndHandleCtrlCrvData = data['tailEndHandleCtrlCrvData']

        tailEndPos = data['tailEndPos']
        tailEndCtrlCrvData = data['tailEndCtrlCrvData']

        numDeformers = data['numDeformers']

        # Set Xfos
        self.spineEndInputTgt.xfo.tr = tailBasePos
        self.spineEndCtrlInputTgt.xfo.tr = tailBasePos

        self.tailBaseHandleCtrlSpace.xfo.tr = tailBaseHandlePos
        self.tailBaseHandleCtrl.xfo.tr = tailBaseHandlePos
        self.tailBaseHandleCtrl.setCurveData(tailBaseHandleCtrlCrvData)

        self.tailEndHandleCtrlSpace.xfo.tr = tailEndHandlePos
        self.tailEndHandleCtrl.xfo.tr = tailEndHandlePos
        self.tailEndHandleCtrl.setCurveData(tailEndHandleCtrlCrvData)

        self.tailEndCtrlSpace.xfo.tr = tailEndPos
        self.tailEndCtrl.xfo.tr = tailEndPos
        self.tailEndCtrl.setCurveData(tailEndCtrlCrvData)

        length = tailBasePos.distanceTo(tailBaseHandlePos) + tailBaseHandlePos.distanceTo(tailEndHandlePos) + tailEndHandlePos.distanceTo(tailEndPos)
        self.lengthInputAttr.setMax(length * 3.0)
        self.lengthInputAttr.setValue(length)

        # Update number of deformers and outputs
        self.setNumDeformers(numDeformers)

        # Updating constraint to use the updated last output.
        self.tailEndOutputConstraint.setConstrainer(self.tailOutputs[-1], index=0)

        # ============
        # Set IO Xfos
        # ============

        # ====================
        # Evaluate Splice Ops
        # ====================
        # evaluate the spine op so that all the output transforms are updated.
        self.bezierTailKLOp.evaluate()

        # evaluate the constraint op so that all the joint transforms are updated.
        self.deformersToOutputsKLOp.evaluate()

        # evaluate the constraints to ensure the outputs are now in the correct location.
        self.tailBaseHandleInputConstraint.evaluate()
        self.tailBaseOutputConstraint.evaluate()
        self.tailEndOutputConstraint.evaluate()



from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FabriceTailGuide)
ks.registerComponent(FabriceTailRig)