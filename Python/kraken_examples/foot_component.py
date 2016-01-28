from kraken.core.maths import *

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.position_constraint import PositionConstraint
from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control  import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class FootComponent(BaseExampleComponent):
    """Foot Component"""

    def __init__(self, name="footBase", parent=None):
        super(FootComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.ikHandleInputTgt = self.createInput('ikHandle', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.legEndInputTgt = self.createInput('legEnd', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.ikTargetOutputTgt = self.createOutput('ikTarget', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.ankleOutputTgt = self.createOutput('ankle', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.toeOutputTgt = self.createOutput('toe', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class FootComponentGuide(FootComponent):
    """Foot Component Guide"""

    def __init__(self, name='foot', parent=None):

        Profiler.getInstance().push("Construct Foot Component:" + name)
        super(FootComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # ========

        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        # Guide Controls
        # self.footCtrl = Control('foot', parent=self.ctrlCmpGrp, shape="circle")
        # self.footCtrl.lockTranslation(True, True, True)
        # self.footCtrl.lockRotation(True, True, True)
        # self.footCtrl.lockScale(True, True, True)

        self.ankleCtrl = Control('ankle', parent=self.ctrlCmpGrp, shape="pin")
        self.toeCtrl = Control('toe', parent=self.ctrlCmpGrp, shape="pin")
        self.toeTipCtrl = Control('toeTip', parent=self.ctrlCmpGrp, shape="pin")

        # TODO: Add pivot controls (spheres) to mark offsets from foot control
        # for where the foot rock and banking should happen

        # self.footCtrlConstraint = PositionConstraint('_'.join([self.footCtrl.getName(), 'To', self.ankleCtrl.getName()]))
        # self.footCtrlConstraint.addConstrainer(self.ankleCtrl)
        # self.footCtrl.addConstraint(self.footCtrlConstraint)

        data = {
            'name': name,
            'location': 'M',
            # 'footCtrlCrvData': self.footCtrl.getCurveData(),
            'ankleXfo': Xfo(Vec3(1.841, 1.1516, -1.237)),
            'toeXfo': Xfo(Vec3(1.85, 0.4, 0.25)),
            'toeTipXfo': Xfo(Vec3(1.85, 0.4, 1.5))
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

        data = super(FootComponentGuide, self).saveData()

        # data['footCtrlCrvData'] = self.footCtrl.getCurveData()
        data['ankleXfo'] = self.ankleCtrl.xfo
        data['toeXfo'] = self.toeCtrl.xfo
        data['toeTipXfo'] = self.toeTipCtrl.xfo

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FootComponentGuide, self).loadData(data)

        # self.footCtrl.setCurveData(data['footCtrlCrvData'])
        # self.footCtrl.xfo = data['ankleXfo']
        self.ankleCtrl.xfo = data['ankleXfo']
        self.toeCtrl.xfo = data['toeXfo']
        self.toeTipCtrl.xfo = data['toeTipXfo']

        # self.footCtrlConstraint.evaluate()

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(FootComponentGuide, self).getRigBuildData()

        # values
        # footPos = self.footCtrl.xfo.tr
        anklePos = self.ankleCtrl.xfo.tr
        toePos = self.toeCtrl.xfo.tr
        toeTipPos = self.toeTipCtrl.xfo.tr

        # Calculate Foot Xfo
        # tempToeTipVec = toeTipPos.clone()
        # tempToeTipVec.y = footPos.y
        # dirVec = tempToeTipVec.subtract(footPos).unit()
        # footQuat = Quat()
        # footQuat.setFromDirectionAndUpvector(dirVec, Vec3(0.0, 1.0, 0.0))
        # footXfo = Xfo(tr=footPos, ori=footQuat)

        # Calculate Ankle Xfo
        rootToEnd = toePos.subtract(anklePos).unit()
        rootToUpV = Vec3(0.0, -1.0, 0.0).add(anklePos).subtract(anklePos).unit()
        zAxis = rootToUpV.cross(rootToEnd).unit()
        normal = zAxis.cross(rootToEnd).unit()

        ankleXfo = Xfo()
        ankleXfo.setFromVectors(rootToEnd, normal, zAxis, toePos)

        # Calculate Toe Xfo
        rootToEnd = toeTipPos.subtract(toePos).unit()
        rootToUpV = Vec3(0.0, -1.0, 0.0).add(toePos).subtract(toePos).unit()
        zAxis = rootToUpV.cross(rootToEnd).unit()
        normal = zAxis.cross(rootToEnd).unit()

        toeXfo = Xfo()
        toeXfo.setFromVectors(rootToEnd, normal, zAxis, toePos)

        # Rotate points via the different in ori between footCtrl and footXfo
        # quatDiff = self.footCtrl.xfo.ori.multiply(footXfo.ori.inverse())
        # eulerDiff = quatDiff.toEuler(RotationOrder())
        # self.footCtrl.rotatePoints(Math_radToDeg(eulerDiff.x), Math_radToDeg(eulerDiff.y), Math_radToDeg(eulerDiff.z))

        data['footXfo'] = self.ankleCtrl.xfo
        # data['footCtrlCrvData'] = self.footCtrl.getCurveData()
        data['ankleXfo'] = ankleXfo
        data['ankleLen'] = anklePos.subtract(toePos).length()
        data['toeXfo'] = toeXfo
        data['toeLen'] = toePos.subtract(toeTipPos).length()

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

        return FootComponentRig


class FootComponentRig(FootComponent):
    """Foot Component"""

    def __init__(self, name="foot", parent=None):

        Profiler.getInstance().push("Construct Neck Rig Component:" + name)
        super(FootComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Neck
        # self.footOffsetCtrlSpace = CtrlSpace('footOffset', parent=self.ctrlCmpGrp)
        # self.footCtrlSpace = CtrlSpace('foot', parent=self.footOffsetCtrlSpace)
        # self.footCtrl = Control('foot', parent=self.footCtrlSpace, shape="circle")
        # self.footCtrl.lockScale(True, True, True)

        self.ankleCtrlSpace = CtrlSpace('ankle', parent=self.ctrlCmpGrp)
        self.ankleCtrl = Control('ankle', parent=self.ankleCtrlSpace, shape="square")
        self.ankleCtrl.alignOnXAxis(negative=True)
        self.ankleCtrl.lockTranslation(True, True, True)
        self.ankleCtrl.lockScale(True, True, True)

        self.toeCtrlSpace = CtrlSpace('toe', parent=self.ctrlCmpGrp)
        self.toeCtrl = Control('toe', parent=self.toeCtrlSpace, shape="square")
        self.toeCtrl.alignOnXAxis()
        self.toeCtrl.lockTranslation(True, True, True)
        self.toeCtrl.lockScale(True, True, True)

        # self.neckCtrl.scalePoints(Vec3(1.25, 1.25, 1.25))
        # self.neckCtrl.translatePoints(Vec3(0, 0, -0.5))
        # self.neckCtrl.rotatePoints(90, 0, 90)
        # self.neckCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        self.ankleDef = Joint('ankle', parent=defCmpGrp)
        self.ankleDef.setComponent(self)

        self.toeDef = Joint('toe', parent=defCmpGrp)
        self.toeDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        # self.footOffsetInputConstraint = PoseConstraint('_'.join([self.footOffsetCtrlSpace.getName(), 'To', self.globalSRTInputTgt.getName()]))
        # self.footOffsetInputConstraint.setMaintainOffset(True)
        # self.footOffsetInputConstraint.addConstrainer(self.globalSRTInputTgt)
        # self.footOffsetCtrlSpace.addConstraint(self.footOffsetInputConstraint)

        # Constraint outputs
        self.ikTargetOutputConstraint = PoseConstraint('_'.join([self.ikTargetOutputTgt.getName(), 'To', self.ankleCtrl.getName()]))
        self.ikTargetOutputConstraint.setMaintainOffset(True)
        self.ikTargetOutputConstraint.addConstrainer(self.ankleCtrl)
        self.ikTargetOutputTgt.addConstraint(self.ikTargetOutputConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        # spliceOp = KLOperator('neckDeformerKLOp', 'PoseConstraintSolver', 'Kraken')
        # self.addOperator(spliceOp)

        # Add Att Inputs
        # spliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        # spliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputstrl)
        # spliceOp.setInput('constrainer', self.neckEndOutputTgt)

        # Add Xfo Outputs
        # spliceOp.setOutput('constrainee', neckDef)

        # Add Deformer Splice Op
        self.outputsToDeformersKLOp = KLOperator('foot' + self.getLocation() + 'DeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)

        # Add Att Inputs
        self.outputsToDeformersKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersKLOp.setInput('constrainers', [self.ankleOutputTgt, self.toeOutputTgt])

        # Add Xfo Outputs
        self.outputsToDeformersKLOp.setOutput('constrainees', [self.ankleDef, self.toeDef])

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FootComponentRig, self).loadData( data )

        footXfo = data['footXfo']
        # footCtrlCrvData = data['footCtrlCrvData']
        ankleXfo = data['ankleXfo']
        toeXfo = data['toeXfo']
        ankleLen = data['ankleLen']
        toeLen = data['toeLen']

        # self.footOffsetCtrlSpace.xfo = footXfo
        # self.footCtrl.xfo = footXfo
        # self.footCtrl.setCurveData(footCtrlCrvData)
        self.ankleCtrlSpace.xfo = ankleXfo
        self.ankleCtrl.xfo = ankleXfo
        self.toeCtrlSpace.xfo = toeXfo
        self.toeCtrl.xfo = toeXfo

        self.ankleCtrl.scalePoints(Vec3(ankleLen, 1.0, 1.5))
        self.toeCtrl.scalePoints(Vec3(toeLen, 1.0, 1.5))

        # Set IO Xfos
        self.legEndInputTgt.xfo.tr = footXfo.tr
        self.legEndInputTgt.xfo.ori = ankleXfo.ori

        self.ikTargetOutputTgt.xfo.tr = footXfo.tr
        self.ikTargetOutputTgt.xfo.ori = ankleXfo.ori
        self.ankleOutputTgt.xfo.tr = footXfo.tr
        self.ankleOutputTgt.xfo.ori = ankleXfo.ori
        self.toeOutputTgt.xfo = toeXfo

        # Eval Constraints
        # self.footOffsetInputConstraint.evaluate()
        self.ikTargetOutputConstraint.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FootComponentGuide)
ks.registerComponent(FootComponentRig)
