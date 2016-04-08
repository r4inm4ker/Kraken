from kraken.core.maths import *

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute

from kraken.core.objects.constraints.position_constraint import PositionConstraint
from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control
from kraken.core.objects.locator import Locator

from kraken.core.objects.operators.canvas_operator import CanvasOperator
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
        self.legEndFKInputTgt = self.createInput('legEndFK', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.ankleOutputTgt = self.createOutput('ankle', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.ikTargetOutputTgt = self.createOutput('ikTarget', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.toeOutputTgt = self.createOutput('toe', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.ikBlendInputAttr = self.createInput('ikBlend', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

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
        self.ankleCtrl = Control('ankle', parent=self.ctrlCmpGrp, shape="pin")
        self.toeCtrl = Control('toe', parent=self.ctrlCmpGrp, shape="pin")
        self.toeTipCtrl = Control('toeTip', parent=self.ctrlCmpGrp, shape="pin")

        self.backPivotCtrl = Control('backPivot', parent=self.ctrlCmpGrp, shape="axesHalfTarget")
        self.backPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))

        self.frontPivotCtrl = Control('frontPivot', parent=self.ctrlCmpGrp, shape="axesHalfTarget")
        self.frontPivotCtrl.rotatePoints(0.0, 180.0, 0.0)
        self.frontPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))

        self.outerPivotCtrl = Control('outerPivot', parent=self.ctrlCmpGrp, shape="axesHalfTarget")
        self.outerPivotCtrl.rotatePoints(0.0, -90.0, 0.0)
        self.outerPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))

        self.innerPivotCtrl = Control('innerPivot', parent=self.ctrlCmpGrp, shape="axesHalfTarget")
        self.innerPivotCtrl.rotatePoints(0.0, 90.0, 0.0)
        self.innerPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))


        self.default_data = {
            'name': name,
            'location': 'L',
            'ankleXfo': Xfo(Vec3(1.75, 1.15, -1.25)),
            'toeXfo': Xfo(Vec3(1.75, 0.4, 0.25)),
            'toeTipXfo': Xfo(Vec3(1.75, 0.4, 1.5)),
            'backPivotXfo': Xfo(Vec3(1.75, 0.0, -2.5)),
            'frontPivotXfo': Xfo(Vec3(1.75, 0.0, 2.0)),
            'outerPivotXfo': Xfo(Vec3(2.5, 0.0, -1.25)),
            'innerPivotXfo': Xfo(Vec3(1.0, 0.0, -1.25))
        }

        self.loadData(self.default_data)

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
        data['backPivotXfo'] = self.backPivotCtrl.xfo
        data['frontPivotXfo'] = self.frontPivotCtrl.xfo
        data['outerPivotXfo'] = self.outerPivotCtrl.xfo
        data['innerPivotXfo'] = self.innerPivotCtrl.xfo

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(FootComponentGuide, self).loadData(data)

        self.ankleCtrl.xfo = data.get('ankleXfo')
        self.toeCtrl.xfo = data.get('toeXfo')
        self.toeTipCtrl.xfo = data.get('toeTipXfo')
        self.backPivotCtrl.xfo = data.get('backPivotXfo')
        self.frontPivotCtrl.xfo = data.get('frontPivotXfo')
        self.outerPivotCtrl.xfo = data.get('outerPivotXfo')
        self.innerPivotCtrl.xfo = data.get('innerPivotXfo')

        if self.getLocation() == 'R':
            self.outerPivotCtrl.rotatePoints(0.0, 180, 0.0)
            self.innerPivotCtrl.rotatePoints(0.0, 180, 0.0)

            if self.outerPivotCtrl.xfo.toMat44().equal(self.default_data['outerPivotXfo'].toMat44()):
                self.outerPivotCtrl.xfo = self.default_data['innerPivotXfo']

            if self.innerPivotCtrl.xfo.toMat44().equal(self.default_data['innerPivotXfo'].toMat44()):
                self.innerPivotCtrl.xfo = self.default_data['outerPivotXfo']

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(FootComponentGuide, self).getRigBuildData()

        # Values
        anklePos = self.ankleCtrl.xfo.tr
        toePos = self.toeCtrl.xfo.tr
        toeTipPos = self.toeTipCtrl.xfo.tr
        backPivotXfo = self.backPivotCtrl.xfo
        frontPivotXfo = self.frontPivotCtrl.xfo
        outerPivotXfo = self.outerPivotCtrl.xfo
        innerPivotXfo = self.innerPivotCtrl.xfo

        # Calculate Ankle Xfo
        rootToEnd = toePos.subtract(anklePos).unit()
        rootToUpV = Vec3(0.0, -1.0, 0.0).add(anklePos).subtract(anklePos).unit()
        zAxis = rootToUpV.cross(rootToEnd).unit()
        normal = zAxis.cross(rootToEnd).unit()

        fkOffsetQuat = Quat()
        fkOffsetQuat.setFromAxisAndAngle(Vec3(1.0, 0., 0.0), (PI / 2))

        ankleXfo = Xfo()
        ankleXfo.setFromVectors(rootToEnd, normal, zAxis, toePos)
        ankleFKXfo = Xfo(ankleXfo)
        ankleFKXfo.ori = ankleFKXfo.ori.multiply(fkOffsetQuat)

        # Calculate Toe Xfo
        rootToEnd = toeTipPos.subtract(toePos).unit()
        rootToUpV = Vec3(0.0, -1.0, 0.0).add(toePos).subtract(toePos).unit()
        zAxis = rootToUpV.cross(rootToEnd).unit()
        normal = zAxis.cross(rootToEnd).unit()

        toeXfo = Xfo()
        toeXfo.setFromVectors(rootToEnd, normal, zAxis, toePos)
        toeFKXfo = Xfo(toeXfo)
        toeFKXfo.ori = toeFKXfo.ori.multiply(fkOffsetQuat)

        data['footXfo'] = self.ankleCtrl.xfo
        data['ankleXfo'] = ankleXfo
        data['ankleFKXfo'] = ankleFKXfo
        data['ankleLen'] = anklePos.subtract(toePos).length()
        data['toeXfo'] = toeXfo
        data['toeFKXfo'] = toeFKXfo
        data['toeLen'] = toePos.subtract(toeTipPos).length()
        data['backPivotXfo'] = backPivotXfo
        data['frontPivotXfo'] = frontPivotXfo
        data['outerPivotXfo'] = outerPivotXfo
        data['innerPivotXfo'] = innerPivotXfo

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
        self.ankleLenInputAttr = ScalarAttribute('ankleLen', 1.0, maxValue=1.0, parent=self.cmpInputAttrGrp)
        self.toeLenInputAttr = ScalarAttribute('toeLen', 1.0, maxValue=1.0, parent=self.cmpInputAttrGrp)
        self.rightSideInputAttr = BoolAttribute('rightSide', False, parent=self.cmpInputAttrGrp)

        self.footAll = Locator('footAll', parent=self.ctrlCmpGrp)
        self.footAll.setShapeVisibility(False)

        self.ankleIKCtrlSpace = CtrlSpace('ankleIK', parent=self.footAll)
        self.ankleIKCtrl = Control('ankleIK', parent=self.ankleIKCtrlSpace, shape="square")
        self.ankleIKCtrl.alignOnXAxis(negative=True)
        self.ankleIKCtrl.lockTranslation(True, True, True)
        self.ankleIKCtrl.lockScale(True, True, True)

        self.toeIKCtrlSpace = CtrlSpace('toeIK', parent=self.footAll)
        self.toeIKCtrl = Control('toeIK', parent=self.toeIKCtrlSpace, shape="square")
        self.toeIKCtrl.alignOnXAxis()
        self.toeIKCtrl.lockTranslation(True, True, True)
        self.toeIKCtrl.lockScale(True, True, True)

        self.ankleFKCtrlSpace = CtrlSpace('ankleFK', parent=self.ctrlCmpGrp)
        self.ankleFKCtrl = Control('ankleFK', parent=self.ankleFKCtrlSpace, shape="cube")
        self.ankleFKCtrl.alignOnXAxis()
        self.ankleFKCtrl.lockTranslation(True, True, True)
        self.ankleFKCtrl.lockScale(True, True, True)

        self.toeFKCtrlSpace = CtrlSpace('toeFK', parent=self.ankleFKCtrl)
        self.toeFKCtrl = Control('toeFK', parent=self.toeFKCtrlSpace, shape="cube")
        self.toeFKCtrl.alignOnXAxis()
        self.toeFKCtrl.lockTranslation(True, True, True)
        self.toeFKCtrl.lockScale(True, True, True)

        self.footSettingsAttrGrp = AttributeGroup("DisplayInfo_FootSettings", parent=self.ankleIKCtrl)
        self.footDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=self.footSettingsAttrGrp)
        self.footRockInputAttr = ScalarAttribute('footRock', value=0.0, minValue=-1.0, maxValue=1.0, parent=self.footSettingsAttrGrp)
        self.footBankInputAttr = ScalarAttribute('footBank', value=0.0, minValue=-1.0, maxValue=1.0, parent=self.footSettingsAttrGrp)

        self.drawDebugInputAttr.connect(self.footDebugInputAttr)

        self.pivotAll = Locator('pivotAll', parent=self.ctrlCmpGrp)
        self.pivotAll.setShapeVisibility(False)

        self.backPivotCtrl = Control('backPivot', parent=self.pivotAll, shape="axesHalfTarget")
        self.backPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.frontPivotCtrl = Control('frontPivot', parent=self.pivotAll, shape="axesHalfTarget")
        self.frontPivotCtrl.rotatePoints(0.0, 180.0, 0.0)
        self.frontPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.outerPivotCtrl = Control('outerPivot', parent=self.pivotAll, shape="axesHalfTarget")
        self.outerPivotCtrl.rotatePoints(0.0, -90.0, 0.0)
        self.outerPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.innerPivotCtrl = Control('innerPivot', parent=self.pivotAll, shape="axesHalfTarget")
        self.innerPivotCtrl.rotatePoints(0.0, 90.0, 0.0)
        self.innerPivotCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        self.ankleDef = Joint('ankle', parent=self.defCmpGrp)
        self.ankleDef.setComponent(self)

        self.toeDef = Joint('toe', parent=self.defCmpGrp)
        self.toeDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint to inputs
        self.pivotAllInputConstraint = PoseConstraint('_'.join([self.pivotAll.getName(), 'To', self.ikHandleInputTgt.getName()]))
        self.pivotAllInputConstraint.setMaintainOffset(True)
        self.pivotAllInputConstraint.addConstrainer(self.ikHandleInputTgt)
        self.pivotAll.addConstraint(self.pivotAllInputConstraint)

        self.ankleFKInputConstraint = PoseConstraint('_'.join([self.ankleFKCtrlSpace.getName(), 'To', self.legEndFKInputTgt.getName()]))
        self.ankleFKInputConstraint.setMaintainOffset(True)
        self.ankleFKInputConstraint.addConstrainer(self.legEndFKInputTgt)
        self.ankleFKCtrlSpace.addConstraint(self.ankleFKInputConstraint)

        # Constraint outputs
        self.ikTargetOutputConstraint = PoseConstraint('_'.join([self.ikTargetOutputTgt.getName(), 'To', self.ankleIKCtrl.getName()]))
        self.ikTargetOutputConstraint.setMaintainOffset(True)
        self.ikTargetOutputConstraint.addConstrainer(self.ankleIKCtrl)
        self.ikTargetOutputTgt.addConstraint(self.ikTargetOutputConstraint)


        # =========================
        # Add Foot Pivot Canvas Op
        # =========================
        # self.footPivotCanvasOp = CanvasOperator('footPivotCanvasOp', 'Kraken.Solvers.Biped.BipedFootPivotSolver')
        self.footPivotCanvasOp = KLOperator('footPivotKLOp', 'BipedFootPivotSolver', 'Kraken')

        self.addOperator(self.footPivotCanvasOp)

        # Add Att Inputs
        self.footPivotCanvasOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.footPivotCanvasOp.setInput('rigScale', self.rigScaleInputAttr)
        self.footPivotCanvasOp.setInput('rightSide', self.rightSideInputAttr)
        self.footPivotCanvasOp.setInput('footRock', self.footRockInputAttr)
        self.footPivotCanvasOp.setInput('footBank', self.footBankInputAttr)

        # Add Xfo Inputs
        self.footPivotCanvasOp.setInput('pivotAll', self.pivotAll)
        self.footPivotCanvasOp.setInput('backPivot', self.backPivotCtrl)
        self.footPivotCanvasOp.setInput('frontPivot', self.frontPivotCtrl)
        self.footPivotCanvasOp.setInput('outerPivot', self.outerPivotCtrl)
        self.footPivotCanvasOp.setInput('innerPivot', self.innerPivotCtrl)

        # Add Xfo Outputs
        self.footPivotCanvasOp.setOutput('result', self.footAll)


        # =========================
        # Add Foot Solver Canvas Op
        # =========================
        # self.footSolverCanvasOp = CanvasOperator('footSolverCanvasOp', 'Kraken.Solvers.Biped.BipedFootSolver')
        self.footSolverCanvasOp = KLOperator('footSolverKLOp', 'BipedFootSolver', 'Kraken')
        self.addOperator(self.footSolverCanvasOp)

        # Add Att Inputs
        self.footSolverCanvasOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.footSolverCanvasOp.setInput('rigScale', self.rigScaleInputAttr)
        self.footSolverCanvasOp.setInput('ikBlend', self.ikBlendInputAttr)
        self.footSolverCanvasOp.setInput('ankleLen', self.ankleLenInputAttr)
        self.footSolverCanvasOp.setInput('toeLen', self.toeLenInputAttr)

        # Add Xfo Inputs
        self.footSolverCanvasOp.setInput('legEnd', self.legEndInputTgt)
        self.footSolverCanvasOp.setInput('ankleIK', self.ankleIKCtrl)
        self.footSolverCanvasOp.setInput('toeIK', self.toeIKCtrl)
        self.footSolverCanvasOp.setInput('ankleFK', self.ankleFKCtrl)
        self.footSolverCanvasOp.setInput('toeFK', self.toeFKCtrl)

        # Add Xfo Outputs
        self.footSolverCanvasOp.setOutput('ankle_result', self.ankleOutputTgt)
        self.footSolverCanvasOp.setOutput('toe_result', self.toeOutputTgt)


        # ===================
        # Add Deformer KL Op
        # ===================
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

        footXfo = data.get('footXfo')
        ankleXfo = data.get('ankleXfo')
        toeXfo = data.get('toeXfo')
        ankleFKXfo = data.get('ankleFKXfo')
        toeFKXfo = data.get('toeFKXfo')
        ankleLen = data.get('ankleLen')
        toeLen = data.get('toeLen')
        backPivotXfo = data.get('backPivotXfo')
        frontPivotXfo = data.get('frontPivotXfo')
        outerPivotXfo = data.get('outerPivotXfo')
        innerPivotXfo = data.get('innerPivotXfo')

        self.footAll.xfo = footXfo
        self.ankleIKCtrlSpace.xfo = ankleXfo
        self.ankleIKCtrl.xfo = ankleXfo
        self.toeIKCtrlSpace.xfo = toeXfo
        self.toeIKCtrl.xfo = toeXfo

        self.ankleFKCtrl.scalePoints(Vec3(ankleLen, 1.0, 1.0))
        self.toeFKCtrl.scalePoints(Vec3(toeLen, 1.0, 1.0))

        self.ankleFKCtrlSpace.xfo.tr = footXfo.tr
        self.ankleFKCtrlSpace.xfo.ori = ankleFKXfo.ori
        self.ankleFKCtrl.xfo.tr = footXfo.tr
        self.ankleFKCtrl.xfo.ori = ankleFKXfo.ori
        self.toeFKCtrlSpace.xfo = toeFKXfo
        self.toeFKCtrl.xfo = toeFKXfo

        self.pivotAll.xfo = footXfo
        self.backPivotCtrl.xfo = backPivotXfo
        self.frontPivotCtrl.xfo = frontPivotXfo
        self.outerPivotCtrl.xfo = outerPivotXfo
        self.innerPivotCtrl.xfo = innerPivotXfo

        if self.getLocation() == 'R':
            self.outerPivotCtrl.rotatePoints(0.0, 180.0, 0.0)
            self.innerPivotCtrl.rotatePoints(0.0, 180.0, 0.0)

        self.ankleIKCtrl.scalePoints(Vec3(ankleLen, 1.0, 1.5))
        self.toeIKCtrl.scalePoints(Vec3(toeLen, 1.0, 1.5))

        # Set Attribute Values
        self.rightSideInputAttr.setValue(self.getLocation() is 'R')
        self.ankleLenInputAttr.setValue(ankleLen)
        self.ankleLenInputAttr.setMax(ankleLen * 3.0)
        self.toeLenInputAttr.setValue(toeLen)
        self.toeLenInputAttr.setMax(toeLen * 3.0)

        # Set IO Xfos
        self.ikHandleInputTgt.xfo = footXfo
        self.legEndInputTgt.xfo.tr = footXfo.tr
        self.legEndInputTgt.xfo.ori = ankleXfo.ori
        self.legEndFKInputTgt.xfo.tr = footXfo.tr
        self.legEndFKInputTgt.xfo.ori = ankleXfo.ori

        self.ikTargetOutputTgt.xfo.tr = footXfo.tr
        self.ikTargetOutputTgt.xfo.ori = ankleXfo.ori

        # Eval Canvas Ops
        self.footPivotCanvasOp.evaluate()
        self.footSolverCanvasOp.evaluate()

        # Eval Constraints
        self.ikTargetOutputConstraint.evaluate()
        self.ankleFKInputConstraint.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(FootComponentGuide)
ks.registerComponent(FootComponentRig)
