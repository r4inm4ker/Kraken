from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV
from kraken.core.maths.quat import Quat

from kraken.core.profiler import Profiler

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.components.component_output import ComponentOutput
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.kl_operator import KLOperator
from kraken.core.objects.operators.canvas_operator import CanvasOperator

from kraken.helpers.utility_methods import logHierarchy


class mjEyelidComponent(BaseExampleComponent):
    """Eyelid Component Base"""

    def __init__(self, name='mjEyelid', parent=None):
        super(mjEyelidComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.headInputTgt = self.createInput('head', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.eyeballInputTgt = self.createInput('eye', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.eyelidUpOutput = self.createOutput('upEyelidOutputs', dataType='Xfo[]')
        self.eyelidLowOutput = self.createOutput('lowEyelidOutputs', dataType='Xfo[]')

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.numUpDeformersInputAttr = self.createInput('upNumDeformers', dataType='Integer', parent=self.cmpInputAttrGrp).getTarget()
        self.upMedialFactorInputAttr = self.createInput('upMedialBlinkFactor', dataType='Float', parent=self.cmpInputAttrGrp).getTarget()
        self.upLateralFactorInputAttr = self.createInput('upLateralBlinkFactor', dataType='Float', parent=self.cmpInputAttrGrp).getTarget()

        self.numLowDeformersInputAttr = self.createInput('lowNumDeformers', dataType='Integer', parent=self.cmpInputAttrGrp).getTarget()
        self.lowMedialFactorInputAttr = self.createInput('lowMedialBlinkFactor', dataType='Float', parent=self.cmpInputAttrGrp).getTarget()
        self.lowLateralFactorInputAttr = self.createInput('lowLateralBlinkFactor', dataType='Float', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class mjEyelidComponentGuide(mjEyelidComponent):
    """Eyelid Component Guide"""

    def __init__(self, name='mjEyelid', parent=None):

        Profiler.getInstance().push("Construct Eyelid Guide Component:" + name)
        super(mjEyelidComponentGuide, self).__init__(name, parent)

        # =========
        # Attributes // Create Attributes Controls.
        # =========
        guideUpSettingsAttrGrp = AttributeGroup("Eyelid Up", parent=self)
        guideLowSettingsAttrGrp = AttributeGroup("Eyelid Low", parent=self)

        self.numUpDeformersAttr = IntegerAttribute('Num Deformers', value=10, minValue=1, maxValue=50, parent=guideUpSettingsAttrGrp)
        self.upMedialFactorAttr = ScalarAttribute('Medial Blink Factor', value=0.25, minValue=0, maxValue=1, parent=guideUpSettingsAttrGrp)
        self.upLateralFactorAttr = ScalarAttribute('Lateral Blink Factor', value=0.65, minValue=0, maxValue=1, parent=guideUpSettingsAttrGrp)

        self.numLowDeformersAttr = IntegerAttribute('Num Deformers', value=10, minValue=1, maxValue=50, parent=guideLowSettingsAttrGrp)
        self.lowMedialFactorAttr = ScalarAttribute('Medial Blink Factor', value=0.25, minValue=0, maxValue=1, parent=guideLowSettingsAttrGrp)
        self.lowLateralFactorAttr = ScalarAttribute('Lateral Blink Factor', value=0.65, minValue=0, maxValue=1, parent=guideLowSettingsAttrGrp)

        self.numUpDeformersAttr.setValueChangeCallback(self.updateNumUpDeformers)
        self.numLowDeformersAttr.setValueChangeCallback(self.updateNumLowDeformers)

        # =========
        # Controls // Create the Guide Controls, Name them, give them a shape, a color and scale it.
        # =========
        self.eyeballCtrl = Control('eyeball', parent=self.ctrlCmpGrp, shape="sphere")
        self.eyeballCtrl.scalePoints(Vec3(0.35, 0.35, 0.35))
        self.eyeballCtrl.setColor("red")

        self.lidMedialCtrl = Control('lidMedial', parent=self.eyeballCtrl, shape="sphere")
        self.lidMedialCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidMedialCtrl.setColor("peach")

        self.lidLateralCtrl = Control('lidLateral', parent=self.eyeballCtrl, shape="sphere")
        self.lidLateralCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidLateralCtrl.setColor("peach")


        self.lidUpCtrl = Control('lidUp', parent=self.eyeballCtrl, shape="sphere")
        self.lidUpCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidUpCtrl.setColor("peach")

        self.lidUpMedialCtrl = Control('lidUpMedial', parent=self.eyeballCtrl, shape="sphere")
        self.lidUpMedialCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidUpMedialCtrl.setColor("peach")

        self.lidUpLateralCtrl = Control('lidUpLateral', parent=self.eyeballCtrl, shape="sphere")
        self.lidUpLateralCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidUpLateralCtrl.setColor("peach")


        self.lidLowCtrl = Control('lidLow', parent=self.eyeballCtrl, shape="sphere")
        self.lidLowCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidLowCtrl.setColor("peach")

        self.lidLowMedialCtrl = Control('lidLowMedial', parent=self.eyeballCtrl, shape="sphere")
        self.lidLowMedialCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidLowMedialCtrl.setColor("peach")

        self.lidLowLateralCtrl = Control('lidLowLateral', parent=self.eyeballCtrl, shape="sphere")
        self.lidLowLateralCtrl.scalePoints(Vec3(0.025, 0.025, 0.025))
        self.lidLowLateralCtrl.setColor("peach")


        # ===============
        # Add Debug Splice Ops
        # ===============
        # Add Lid Up Canvas Op
        self.debugLidUpCanvasOp = CanvasOperator('Debug_Canvas_Eyelid_Up_Op', 'MJCG.Solvers.mjEyelidDebugSolver')
        self.addOperator(self.debugLidUpCanvasOp)

        # Add Attributes Inputs
        self.debugLidUpCanvasOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.debugLidUpCanvasOp.setInput('rigScale', self.rigScaleInputAttr)
        self.debugLidUpCanvasOp.setInput('Deformer_Count', self.numUpDeformersInputAttr)

        # Add Xfo Inputs
        self.debugLidUpCanvasOp.setInput('Eye_Center', self.eyeballCtrl)
        self.debugLidUpCanvasOp.setInput('Lid_Medial', self.lidMedialCtrl)
        self.debugLidUpCanvasOp.setInput('Lid_MedialCen', self.lidUpMedialCtrl)
        self.debugLidUpCanvasOp.setInput('Lid_Center_Ref', self.lidUpCtrl)
        self.debugLidUpCanvasOp.setInput('Lid_Center_Ctrl', self.lidUpCtrl)
        self.debugLidUpCanvasOp.setInput('Lid_LateralCen', self.lidUpLateralCtrl)
        self.debugLidUpCanvasOp.setInput('Lid_Lateral', self.lidLateralCtrl)

        # Add Xfo Outputs
        self.debugLidUpCanvasOp.setOutput('result', self.eyelidUpOutput.getTarget())


        # Add Lid Low Canvas Op
        self.debugLidLowCanvasOp = CanvasOperator('Debug_Canvas_Eyelid_Low_Op', 'MJCG.Solvers.mjEyelidDebugSolver')
        self.addOperator(self.debugLidLowCanvasOp)

        # Add Attributes Inputs
        self.debugLidLowCanvasOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.debugLidLowCanvasOp.setInput('rigScale', self.rigScaleInputAttr)
        self.debugLidLowCanvasOp.setInput('Deformer_Count', self.numLowDeformersInputAttr)

        # Add Xfo Inputs
        self.debugLidLowCanvasOp.setInput('Eye_Center', self.eyeballCtrl)
        self.debugLidLowCanvasOp.setInput('Lid_Medial', self.lidMedialCtrl)
        self.debugLidLowCanvasOp.setInput('Lid_MedialCen', self.lidLowMedialCtrl)
        self.debugLidLowCanvasOp.setInput('Lid_Center_Ref', self.lidLowCtrl)
        self.debugLidLowCanvasOp.setInput('Lid_Center_Ctrl', self.lidLowCtrl)
        self.debugLidLowCanvasOp.setInput('Lid_LateralCen', self.lidLowLateralCtrl)
        self.debugLidLowCanvasOp.setInput('Lid_Lateral', self.lidLateralCtrl)

        # Add Xfo Outputs
        self.debugLidLowCanvasOp.setOutput('result', self.eyelidLowOutput.getTarget())


        # =========
        # Position Data // Get the Guide Controls Position data, else set them at their initial position.
        # =========
        self.default_data = {
            "name": name,
            "location": "L",

            "eyeballXfo": Xfo(Vec3(0.322, 15.500, 0.390)),
            "lidMedialXfo": Xfo(Vec3(0.168, 15.445, 0.520)),
            "lidLateralXfo": Xfo(Vec3(0.465, 15.47, 0.465)),

            "lidUpXfo": Xfo(Vec3(0.322, 15.585, 0.605)),
            "lidUpMedialXfo": Xfo(Vec3(0.203, 15.515, 0.525)),
            "lidUpLateralXfo": Xfo(Vec3(0.432, 15.55, 0.538)),

            "lidLowXfo": Xfo(Vec3(0.322, 15.434, 0.6)),
            "lidLowMedialXfo": Xfo(Vec3(0.24, 15.45, 0.513)),
            "lidLowLateralXfo": Xfo(Vec3(0.413, 15.44, 0.525)),

            "lidUpMedialBlink": self.upMedialFactorAttr.getValue(),
            "lidUpLateralBlink": self.upLateralFactorAttr.getValue(),

            "lidLowMedialBlink": self.lowMedialFactorAttr.getValue(),
            "lidLowLateralBlink": self.lowLateralFactorAttr.getValue(),

            "numUpDeformers": self.numUpDeformersAttr.getValue(),
            "numLowDeformers": self.numLowDeformersAttr.getValue(),
        }

        self.loadData(self.default_data)

        Profiler.getInstance().pop()


   # ==========
    # Callbacks
    # ==========
    def updateNumUpDeformers(self, countUp):

        if countUp == 0:
            raise IndexError("'count' must be > 0")

        #Lip Up
        lidUpOutputs = self.eyelidUpOutput.getTarget()
        if countUp > len(lidUpOutputs):
            for i in xrange(len(lidUpOutputs), countUp):
                debugUpCtrl = Control('Lid_Up_' + str(i+1).zfill(2), parent=self.outputHrcGrp, shape="sphere")
                debugUpCtrl.rotatePoints(90, -90, 180)
                debugUpCtrl.scalePoints(Vec3(0.01, 0.01, 0.01))
                debugUpCtrl.setColor("yellowLight")
                lidUpOutputs.append(debugUpCtrl)

        elif countUp < len(lidUpOutputs):
            numExtraUpCtrls = len(lidUpOutputs) - countUp
            for i in xrange(numExtraUpCtrls):
                extraUpCtrl = lidUpOutputs.pop()
                self.outputHrcGrp.removeChild(extraUpCtrl)

        return True


    def updateNumLowDeformers(self, countLow):

        if countLow == 0:
            raise IndexError("'count' must be > 0")

        #Lip Low
        lidLowOutputs = self.eyelidLowOutput.getTarget()
        if countLow > len(lidLowOutputs):
            for i in xrange(len(lidLowOutputs), countLow):
                debugLowCtrl = Control('Lid_Low_' + str(i+1).zfill(2), parent=self.outputHrcGrp, shape="sphere")
                debugLowCtrl.rotatePoints(90, -90, 180)
                debugLowCtrl.scalePoints(Vec3(0.01, 0.01, 0.01))
                debugLowCtrl.setColor("yellowLight")
                lidLowOutputs.append(debugLowCtrl)

        elif countLow < len(lidLowOutputs):
            numExtraLowCtrls = len(lidLowOutputs) - countLow
            for i in xrange(numExtraLowCtrls):
                extraLowCtrl = lidLowOutputs.pop()
                self.outputHrcGrp.removeChild(extraLowCtrl)

        return True

    # =============
    # Data Methods
    # =============
    def saveData(self):

        data = super(mjEyelidComponentGuide, self).saveData()

        data['eyeballXfo'] = self.eyeballCtrl.xfo

        data['lidMedialXfo'] = self.lidMedialCtrl.xfo
        data['lidLateralXfo'] = self.lidLateralCtrl.xfo

        data['lidUpXfo'] = self.lidUpCtrl.xfo
        data['lidUpMedialXfo'] = self.lidUpMedialCtrl.xfo
        data['lidUpLateralXfo'] = self.lidUpLateralCtrl.xfo

        data['lidLowXfo'] = self.lidLowCtrl.xfo
        data['lidLowMedialXfo'] = self.lidLowMedialCtrl.xfo
        data['lidLowLateralXfo'] = self.lidLowLateralCtrl.xfo

        data['numUpDeformers'] = self.numUpDeformersAttr.getValue()
        data['numLowDeformers'] = self.numLowDeformersAttr.getValue()

        data['lidUpMedialBlink'] = self.upMedialFactorAttr.getValue()
        data['lidUpLateralBlink'] = self.upLateralFactorAttr.getValue()

        data['lidLowMedialBlink'] = self.lowMedialFactorAttr.getValue()
        data['lidLowLateralBlink'] = self.lowLateralFactorAttr.getValue()


        return data

    def loadData(self, data):

        super(mjEyelidComponentGuide, self).loadData( data )

        self.eyeballCtrl.xfo = data['eyeballXfo']

        self.lidMedialCtrl.xfo = data['lidMedialXfo']
        self.lidLateralCtrl.xfo = data['lidLateralXfo']

        self.lidUpCtrl.xfo = data['lidUpXfo']
        self.lidUpMedialCtrl.xfo = data['lidUpMedialXfo']
        self.lidUpLateralCtrl.xfo = data['lidUpLateralXfo']

        self.lidLowCtrl.xfo = data['lidLowXfo']
        self.lidLowMedialCtrl.xfo = data['lidLowMedialXfo']
        self.lidLowLateralCtrl.xfo = data['lidLowLateralXfo']

        self.numUpDeformersAttr.setValue(data["numUpDeformers"])
        self.numLowDeformersAttr.setValue(data["numLowDeformers"])

        self.numUpDeformersInputAttr.setValue(data["numUpDeformers"])
        self.numLowDeformersInputAttr.setValue(data["numLowDeformers"])

        self.upMedialFactorInputAttr.setValue(data['lidUpMedialBlink'])
        self.upLateralFactorInputAttr.setValue(data['lidUpLateralBlink'])

        self.lowMedialFactorInputAttr.setValue(data['lidLowMedialBlink'])
        self.lowLateralFactorInputAttr.setValue(data['lidLowLateralBlink'])

        self.debugLidUpCanvasOp.evaluate()
        self.debugLidLowCanvasOp.evaluate()

        return True


    def getRigBuildData(self):

        data = super(mjEyelidComponentGuide, self).getRigBuildData()

        eyeballPosition = self.eyeballCtrl.xfo.tr
        eyeballOriXfo = Xfo()
        eyeballOriXfo.tr = eyeballPosition
        eyeballOriOffset = Quat(Vec3(0.0, 0.894, 0.0), -0.448)
        if self.getLocation() == "R":
           eyeballOriXfo.ori.subtract(eyeballOriOffset)

        data['eyeballXfo'] = eyeballOriXfo

        eyelidUpVOffset = Vec3(0.0, 0.2, 0.0)
        eyelidUpVXfo = Xfo()
        eyelidUpVXfo.tr = eyeballPosition.add(eyelidUpVOffset)

        data['eyelidUpVXfo'] = eyelidUpVXfo

        data['lidMedialXfo'] = self.lidMedialCtrl.xfo
        data['lidLateralXfo'] = self.lidLateralCtrl.xfo

        data['lidUpXfo'] = self.lidUpCtrl.xfo
        data['lidUpMedialXfo'] = self.lidUpMedialCtrl.xfo
        data['lidUpLateralXfo'] = self.lidUpLateralCtrl.xfo

        data['lidLowXfo'] = self.lidLowCtrl.xfo
        data['lidLowMedialXfo'] = self.lidLowMedialCtrl.xfo
        data['lidLowLateralXfo'] = self.lidLowLateralCtrl.xfo

        data['numUpDeformers'] = self.numUpDeformersAttr.getValue()
        data['numLowDeformers'] = self.numLowDeformersAttr.getValue()

        data['lidUpMedialBlink'] = self.upMedialFactorAttr.getValue()
        data['lidUpLateralBlink'] = self.upLateralFactorAttr.getValue()

        data['lidLowMedialBlink'] = self.lowMedialFactorAttr.getValue()
        data['lidLowLateralBlink'] = self.lowLateralFactorAttr.getValue()

        return data


    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):

        return 'Guide'


    @classmethod
    def getRigComponentClass(cls):

        return mjEyelidComponentRig


class mjEyelidComponentRig(mjEyelidComponent):
    """Eyelid Component Rig"""

    def __init__(self, name='mjEyelid', parent=None):
        Profiler.getInstance().push("Construct Eyelid Rig Component:" + name)
        super(mjEyelidComponentRig, self).__init__(name, parent)

        # =========
        # Controls // Get the Guide Xfos data and create the final controllers, offset them if needed.
        # =========

        # Inputs
        self.eyelidCtrlSpace = CtrlSpace('eyelid', parent=self.ctrlCmpGrp)

        self.eyeballLocator = Locator('eyeball', parent=self.ctrlCmpGrp)
        self.eyeballLocator.setShapeVisibility(False)

        self.eyelidUpVLocator = Locator('eyelid_Upv', parent=self.eyelidCtrlSpace)
        self.eyelidUpVLocator.setShapeVisibility(False)

        # Lid Sides
        self.lidMedialLocator = Locator('lid_Medial', parent=self.eyelidCtrlSpace)
        self.lidMedialLocator.setShapeVisibility(False)

        self.lidLateralLocator = Locator('lid_Lateral', parent=self.eyelidCtrlSpace)
        self.lidLateralLocator.setShapeVisibility(False)

        # Lid Upper
        self.lidUpCtrlSpace = CtrlSpace('lid_Up', parent=self.eyelidCtrlSpace)
        self.lidUpCtrl = Control('lid_Up', parent=self.lidUpCtrlSpace, shape="cube")
        self.lidUpCtrl.scalePoints(Vec3(0.05, 0.05, 0.05))
        self.lidUpCtrl.lockTranslation(x=True, y=False, z=True)
        self.lidUpCtrl.setColor("yellow")

        self.lipUpMedialLocator = Locator('lid_Up_Medial', parent=self.eyelidCtrlSpace)
        self.lipUpMedialLocator.setShapeVisibility(False)
        self.lipUpLateralLocator = Locator('lid_Up_Lateral', parent=self.eyelidCtrlSpace)
        self.lipUpLateralLocator.setShapeVisibility(False)

        # Lid Lower
        self.lidLowCtrlSpace = CtrlSpace('lid_Low', parent=self.eyelidCtrlSpace)
        self.lidLowCtrl = Control('lid_Low', parent=self.lidLowCtrlSpace, shape="cube")
        self.lidLowCtrl.scalePoints(Vec3(0.05, 0.05, 0.05))
        self.lidLowCtrl.lockTranslation(x=True, y=False, z=True)
        self.lidLowCtrl.setColor("yellow")

        self.lidLowMedialLocator = Locator('lid_Low_Medial', parent=self.eyelidCtrlSpace)
        self.lidLowMedialLocator.setShapeVisibility(False)
        self.lidLowLateralLocator = Locator('lid_Low_Lateral', parent=self.eyelidCtrlSpace)
        self.lidLowLateralLocator.setShapeVisibility(False)

        # Lid Attributes
        lidUp_AttrGrp = AttributeGroup("Eyelid_Settings", parent=self.lidUpCtrl)
        lidLow_AttrGrp = AttributeGroup("Eyelid_Settings", parent=self.lidLowCtrl)

        self.lidUp_OffsetInputAttr = BoolAttribute('Eyeball_Offset', value=True, parent=lidUp_AttrGrp)
        self.lidUp_FollowFactorInputAttr = ScalarAttribute('Eyeball_Follow_Factor', value=1.0, parent=lidUp_AttrGrp)
        self.lidUp_DebugInputAttr = BoolAttribute('DrawDebug', value=False, parent=lidUp_AttrGrp)
        self.lidUp_MedialBlinkInputAttr = ScalarAttribute('Medial_Blink_Factor', value=0.25, parent=lidUp_AttrGrp)
        self.lidUp_LateralBlinkInputAttr = ScalarAttribute('Lateral_Blink_Factor', value=0.65, parent=lidUp_AttrGrp)
        self.lidUp_DefCountInputAttr = IntegerAttribute('numDeformers', value=10, parent=lidUp_AttrGrp)

        self.lidLow_OffsetInputAttr = BoolAttribute('Eyeball_Offset', value=True, parent=lidLow_AttrGrp)
        self.lidLow_FollowFactorInputAttr = ScalarAttribute('Eyeball_Follow_Factor', value=0.8, parent=lidLow_AttrGrp)
        self.lidLow_DebugInputAttr = BoolAttribute('DrawDebug', value=False, parent=lidLow_AttrGrp)
        self.lidLow_MedialBlinkInputAttr = ScalarAttribute('Medial_Blink_Factor', value=0.25, parent=lidLow_AttrGrp)
        self.lidLow_LateralBlinkInputAttr = ScalarAttribute('Lateral_Blink_Factor', value=0.65, parent=lidLow_AttrGrp)
        self.lidLow_DefCountInputAttr = IntegerAttribute('numDeformers', value=10, parent=lidLow_AttrGrp)

        self.lidUp_DebugInputAttr.connect(self.drawDebugInputAttr)
        self.lidLow_DebugInputAttr.connect(self.drawDebugInputAttr)
        self.lidUp_DefCountInputAttr.connect(self.numUpDeformersInputAttr)
        self.lidLow_DefCountInputAttr.connect(self.numLowDeformersInputAttr)

        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        # Lid Sides
        lidMedialDef = Joint('lid_Medial', parent=self.defCmpGrp)
        lidMedialDef.setComponent(self)

        lidLateralDef = Joint('lid_Lateral', parent=self.defCmpGrp)
        lidLateralDef.setComponent(self)

        # Lid Up
        self.eyelidUpDef = []
        self.eyelidUpOutputs = []
        self.setNumUpDeformers(1)

        # Lid Low
        self.eyelidLowDef = []
        self.eyelidLowOutputs = []
        self.setNumLowDeformers(1)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        self.eyelidUpOutput.setTarget(self.eyelidUpOutputs)
        self.eyelidLowOutput.setTarget(self.eyelidLowOutputs)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.headInputConstraint = PoseConstraint('_'.join([self.eyelidCtrlSpace.getName(), 'To', self.headInputTgt.getName()]))
        self.headInputConstraint.addConstrainer(self.headInputTgt)
        self.eyelidCtrlSpace.addConstraint(self.headInputConstraint)

        self.eyeballInputConstraint = PoseConstraint('_'.join([self.eyeballLocator.getName(), 'To', self.eyeballInputTgt.getName()]))
        self.eyeballInputConstraint.setMaintainOffset(True)
        self.eyeballInputConstraint.addConstrainer(self.eyeballInputTgt)
        self.eyeballLocator.addConstraint(self.eyeballInputConstraint)

        # ===============
        # Add Splice Ops
        # ===============
        # Add MultiPoseConstraint Joints Splice Op
        self.outputsToDeformersKLOp = KLOperator('Canvas_Eyelid_Side_Op', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)
        # Add Att Inputs
        self.outputsToDeformersKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersKLOp.setInput('rigScale', self.rigScaleInputAttr)
        # Add Xfo Inputs
        self.outputsToDeformersKLOp.setInput('constrainers', [self.lidMedialLocator,
                                                              self.lidLateralLocator,
                                                              ])
        # Add Xfo Outputs
        self.outputsToDeformersKLOp.setOutput('constrainees', [lidMedialDef,
                                                               lidLateralDef,
                                                               ])

        # Add Lid Up Canvas Op
        self.lidUpCanvasOp = CanvasOperator('Canvas_Eyelid_Up_Op', 'MJCG.Solvers.mjEyelidConstraintSolver')
        self.addOperator(self.lidUpCanvasOp)

        # Add Attributes Inputs
        self.lidUpCanvasOp.setInput('drawDebug', self.lidUp_DebugInputAttr)
        self.lidUpCanvasOp.setInput('rigScale', self.rigScaleInputAttr)
        self.lidUpCanvasOp.setInput('Eyeball_Offset', self.lidUp_OffsetInputAttr)
        self.lidUpCanvasOp.setInput('Eyeball_Follow_Factor', self.lidUp_FollowFactorInputAttr)
        self.lidUpCanvasOp.setInput('Medial_Blink_Factor', self.lidUp_MedialBlinkInputAttr)
        self.lidUpCanvasOp.setInput('Lateral_Blink_Factor', self.lidUp_LateralBlinkInputAttr)
        self.lidUpCanvasOp.setInput('Deformer_Count', self.lidUp_DefCountInputAttr)

        # Add Xfo Inputs
        self.lidUpCanvasOp.setInput('Eye_Center', self.eyeballLocator)
        self.lidUpCanvasOp.setInput('Lid_Global', self.eyelidCtrlSpace)
        self.lidUpCanvasOp.setInput('Lid_UpV', self.eyelidUpVLocator)
        self.lidUpCanvasOp.setInput('Lid_Medial', self.lidMedialLocator)
        self.lidUpCanvasOp.setInput('Lid_MedialCen', self.lipUpMedialLocator)
        self.lidUpCanvasOp.setInput('Lid_Center_Ref', self.lidUpCtrlSpace)
        self.lidUpCanvasOp.setInput('Lid_Center_Ctrl', self.lidUpCtrl)
        self.lidUpCanvasOp.setInput('Lid_LateralCen', self.lipUpLateralLocator)
        self.lidUpCanvasOp.setInput('Lid_Lateral', self.lidLateralLocator)
        #Add Xfo Outputs
        self.lidUpCanvasOp.setOutput('result', self.eyelidUpDef)


        # Add Lid Low Canvas Op
        self.lidLowCanvasOp = CanvasOperator('Canvas_Eyelid_Low_Op', 'MJCG.Solvers.mjEyelidConstraintSolver')
        self.addOperator(self.lidLowCanvasOp)

        # Add Attributes Inputs
        self.lidLowCanvasOp.setInput('drawDebug', self.lidLow_DebugInputAttr)
        self.lidLowCanvasOp.setInput('rigScale', self.rigScaleInputAttr)
        self.lidLowCanvasOp.setInput('Eyeball_Offset', self.lidLow_OffsetInputAttr)
        self.lidLowCanvasOp.setInput('Eyeball_Follow_Factor', self.lidLow_FollowFactorInputAttr)
        self.lidLowCanvasOp.setInput('Medial_Blink_Factor', self.lidLow_MedialBlinkInputAttr)
        self.lidLowCanvasOp.setInput('Lateral_Blink_Factor', self.lidLow_LateralBlinkInputAttr)
        self.lidLowCanvasOp.setInput('Deformer_Count', self.lidLow_DefCountInputAttr)

        # Add Xfo Inputs
        self.lidLowCanvasOp.setInput('Eye_Center', self.eyeballLocator)
        self.lidLowCanvasOp.setInput('Lid_Global', self.eyelidCtrlSpace)
        self.lidLowCanvasOp.setInput('Lid_UpV', self.eyelidUpVLocator)
        self.lidLowCanvasOp.setInput('Lid_Medial', self.lidMedialLocator)
        self.lidLowCanvasOp.setInput('Lid_MedialCen', self.lidLowMedialLocator)
        self.lidLowCanvasOp.setInput('Lid_Center_Ref', self.lidLowCtrlSpace)
        self.lidLowCanvasOp.setInput('Lid_Center_Ctrl', self.lidLowCtrl)
        self.lidLowCanvasOp.setInput('Lid_LateralCen', self.lidLowLateralLocator)
        self.lidLowCanvasOp.setInput('Lid_Lateral', self.lidLateralLocator)

        #Add Xfo Outputs
        self.lidLowCanvasOp.setOutput('result', self.eyelidLowDef)


        Profiler.getInstance().pop()


    def setNumUpDeformers(self, numUpDeformers):

        # Add Up Deformers and Outputs
        for i in xrange(len(self.eyelidUpOutputs), numUpDeformers):
            name = 'Lid_Up_' + str(i + 1).zfill(2)
            lidUpOutputs = ComponentOutput(name, parent=self.outputHrcGrp)
            self.eyelidUpOutputs.append(lidUpOutputs)

        for i in xrange(len(self.eyelidUpDef), numUpDeformers):
            name = 'Lid_Up_' + str(i + 1).zfill(2)
            lidUpDef = Joint(name, parent=self.defCmpGrp)
            lidUpDef.setComponent(self)
            self.eyelidUpDef.append(lidUpDef)

        return True

    def setNumLowDeformers(self, numLowDeformers):

        # Add Low Deformers and Outputs
        for i in xrange(len(self.eyelidLowOutputs), numLowDeformers):
            name = 'Lid_Low_' + str(i + 1).zfill(2)
            lidLowOutputs = ComponentOutput(name, parent=self.outputHrcGrp)
            self.eyelidLowOutputs.append(lidLowOutputs)

        for i in xrange(len(self.eyelidLowDef), numLowDeformers):
            name = 'Lid_Low_' + str(i + 1).zfill(2)
            lidLowDef = Joint(name, parent=self.defCmpGrp)
            lidLowDef.setComponent(self)
            self.eyelidLowDef.append(lidLowDef)

        return True


    def loadData(self, data=None):

        super(mjEyelidComponentRig, self).loadData( data )

        # Set CtrlSpace Xfos
        self.eyelidCtrlSpace.xfo = data['eyeballXfo']
        self.eyeballLocator.xfo = data['eyeballXfo']

        self.eyelidUpVLocator.xfo = data['eyelidUpVXfo']

        self.lidMedialLocator.xfo = data['lidMedialXfo']
        self.lidLateralLocator.xfo = data['lidLateralXfo']

        self.lidUpCtrlSpace.xfo = data['lidUpXfo']
        self.lidUpCtrl.xfo = data['lidUpXfo']
        self.lipUpMedialLocator.xfo = data['lidUpMedialXfo']
        self.lipUpLateralLocator.xfo = data['lidUpLateralXfo']

        self.lidLowCtrlSpace.xfo = data['lidLowXfo']
        self.lidLowCtrl.xfo = data['lidLowXfo']
        self.lidLowMedialLocator.xfo = data['lidLowMedialXfo']
        self.lidLowLateralLocator.xfo = data['lidLowLateralXfo']

        # Update number of deformers and outputs
        self.setNumUpDeformers(data['numUpDeformers'])
        self.setNumLowDeformers(data['numLowDeformers'])

        # Set Attributes
        self.upMedialFactorInputAttr.setValue(data['lidUpMedialBlink'])
        self.upLateralFactorInputAttr.setValue(data['lidUpLateralBlink'])
        self.numUpDeformersInputAttr.setValue(data['numUpDeformers'])

        self.lowMedialFactorInputAttr.setValue(data['lidLowMedialBlink'])
        self.lowLateralFactorInputAttr.setValue(data['lidLowLateralBlink'])
        self.numLowDeformersInputAttr.setValue(data['numLowDeformers'])

        self.lidUp_MedialBlinkInputAttr.setValue(data['lidUpMedialBlink'])
        self.lidUp_LateralBlinkInputAttr.setValue(data['lidUpLateralBlink'])
        self.lidLow_MedialBlinkInputAttr.setValue(data['lidLowMedialBlink'])
        self.lidLow_LateralBlinkInputAttr.setValue(data['lidLowLateralBlink'])

        # Set I/O Xfos
        self.headInputTgt.xfo = data['eyeballXfo']
        self.eyeballInputTgt.xfo = data['eyeballXfo']

        self.eyelidUpOutputTgt = self.eyelidUpDef
        self.eyelidLowOutputTgt = self.eyelidLowDef

        # Evaluate Constraints
        self.headInputConstraint.evaluate()
        self.eyeballInputConstraint.evaluate()

        # Evaluate Operators
        self.lidUpCanvasOp.evaluate()
        self.lidLowCanvasOp.evaluate()
        self.outputsToDeformersKLOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(mjEyelidComponentGuide)
ks.registerComponent(mjEyelidComponentRig)
