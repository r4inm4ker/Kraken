from kraken.core.maths import Vec3, Xfo, Quat

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.joint import Joint
from kraken.core.objects.control import Control
from kraken.core.objects.component_group import ComponentGroup

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler


class NeckComponent(BaseExampleComponent):
    """Neck Component"""

    def __init__(self, name="neckBase", parent=None):
        super(NeckComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.neckBaseInputTgt = self.createInput(
            'neckBase', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.neck01OutputTgt = self.createOutput(
            'neck01', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        self.neck02OutputTgt = self.createOutput(
            'neck02', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        self.neckEndOutputTgt = self.createOutput(
            'neckEnd', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput(
            'drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()

        self.rigScaleInputAttr = self.createInput(
            'rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class NeckComponentGuide(NeckComponent):
    """Neck Component Guide"""

    def __init__(self, name='neck', parent=None):

        Profiler.getInstance().push('Construct Neck Component:' + name)
        super(NeckComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # =========

        # Guide Controls
        self.neckCtrl = Control('neck', parent=self.ctrlCmpGrp, shape='sphere')
        self.neckCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.neckMidCtrl = Control('neckMid', parent=self.ctrlCmpGrp, shape='sphere')
        self.neckMidCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.neckEndCtrl = Control('neckEnd', parent=self.ctrlCmpGrp, shape='sphere')
        self.neckEndCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))

        self.neckCtrlShape = Control('neck', parent=self.ctrlCmpGrp, shape='pin')
        self.neckCtrlShape.rotatePoints(90.0, 0.0, 0.0)
        self.neckCtrlShape.rotatePoints(0.0, 90.0, 0.0)
        self.neckCtrlShape.setColor('orange')
        self.neckMidCtrlShape = Control('neckMid', parent=self.ctrlCmpGrp, shape='pin')
        self.neckMidCtrlShape.rotatePoints(90.0, 0.0, 0.0)
        self.neckMidCtrlShape.rotatePoints(0.0, 90.0, 0.0)
        self.neckMidCtrlShape.setColor('orange')

        # Guide Operator
        self.neckGuideKLOp = KLOperator(name + 'GuideKLOp', 'NeckGuideSolver', 'Kraken')
        self.addOperator(self.neckGuideKLOp)

        # Add Att Inputs
        self.neckGuideKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.neckGuideKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Source Inputs
        self.neckGuideKLOp.setInput('sources', [self.neckCtrl, self.neckMidCtrl, self.neckEndCtrl])

        # Add Target Outputs
        self.neckGuideKLOp.setOutput('targets', [self.neckCtrlShape, self.neckMidCtrlShape])


        # Calculate default values
        neckVec = Vec3(0.0, 16.00, -0.75)
        neckMidVec = Vec3(0.0, 16.50, -0.50)
        neckEndVec = Vec3(0.0, 17.00, -0.25)
        upVector = Vec3(0.0, 0.0, -1.0)

        neckOri = Quat()
        neckOri.setFromDirectionAndUpvector((neckMidVec - neckVec).unit(),
                                            ((neckVec + upVector) - neckVec).unit())

        neckMidOri = Quat()
        neckMidOri.setFromDirectionAndUpvector((neckEndVec - neckMidVec).unit(),
                                               ((neckMidVec + upVector) - neckMidVec).unit())

        self.default_data = {
            "name": name,
            "location": "M",
            "neckXfo": Xfo(tr=neckVec, ori=neckOri),
            "neckMidXfo": Xfo(tr=neckMidVec, ori=neckMidOri),
            "neckEndXfo": Xfo(tr=neckEndVec, ori=neckMidOri),
            "neckCrvData": self.neckCtrlShape.getCurveData(),
            "neckMidCrvData": self.neckMidCtrlShape.getCurveData()
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

        data = super(NeckComponentGuide, self).saveData()

        data['neckXfo'] = self.neckCtrl.xfo
        data['neckMidXfo'] = self.neckMidCtrl.xfo
        data['neckEndXfo'] = self.neckEndCtrl.xfo

        data['neckCrvData'] = self.neckCtrlShape.getCurveData()
        data['neckMidCrvData'] = self.neckMidCtrlShape.getCurveData()

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
            data (object): The JSON data object.

        Returns:
            bool: True if successful.

        """

        super(NeckComponentGuide, self).loadData(data)

        self.neckCtrl.xfo = data.get('neckXfo')
        self.neckMidCtrl.xfo = data.get('neckMidXfo')
        self.neckEndCtrl.xfo = data.get('neckEndXfo')

        self.neckCtrlShape.setCurveData(data.get('neckCrvData'))
        self.neckMidCtrlShape.setCurveData(data.get('neckMidCrvData'))

        # Evaluate guide operators
        self.neckGuideKLOp.evaluate()

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout
        of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(NeckComponentGuide, self).getRigBuildData()

        neckEndXfo = Xfo(tr=self.neckEndCtrl.xfo.tr,
                         ori=self.neckMidCtrlShape.xfo.ori)

        data['neckXfo'] = self.neckCtrlShape.xfo
        data['neckCrvData'] = self.neckCtrlShape.getCurveData()
        data['neckMidXfo'] = self.neckMidCtrlShape.xfo
        data['neckMidCrvData'] = self.neckMidCtrlShape.getCurveData()
        data['neckEndXfo'] = neckEndXfo

        return data


    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):
        """Enables introspection of the class prior to construction to determine
        if it is a guide component.

        Returns:
            bool: Whether the component is a guide component.

        """

        return 'Guide'


    @classmethod
    def getRigComponentClass(cls):
        """Returns the corresponding rig component class for this guide
        component class.

        Returns:
            class: The rig component class.

        """

        return NeckComponentRig


class NeckComponentRig(NeckComponent):
    """Neck Component"""

    def __init__(self, name="neck", parent=None):

        Profiler.getInstance().push("Construct Neck Rig Component:" + name)
        super(NeckComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Neck
        self.neck01Ctrl = Control('neck01', parent=self.ctrlCmpGrp, shape="pin")
        self.neck01Ctrl.setColor("orange")

        self.neck01CtrlSpace = self.neck01Ctrl.insertCtrlSpace(name='neck01')

        self.neck02Ctrl = Control('neck02', parent=self.ctrlCmpGrp, shape="pin")
        self.neck02Ctrl.setColor("orange")

        self.neck02CtrlSpace = self.neck02Ctrl.insertCtrlSpace(name='neck02')


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        self.neck01Def = Joint('neck01', parent=self.defCmpGrp)
        self.neck01Def.setComponent(self)

        self.neck02Def = Joint('neck02', parent=self.defCmpGrp)
        self.neck02Def.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        neckInputConstraintName = '_'.join([self.neck01CtrlSpace.getName(),
                                            'To',
                                            self.neckBaseInputTgt.getName()])

        self.neckInputCnstr = self.neck01CtrlSpace.constrainTo(
            self.neckBaseInputTgt,
            'Pose',
            maintainOffset=False,
            name=neckInputConstraintName)


        # Constraint outputs
        neck01OutCnstrName = '_'.join([self.neck01OutputTgt.getName(),
                                       'To',
                                       self.neck01Ctrl.getName()])

        self.neck01OutCnstr = self.neck01OutputTgt.constrainTo(
            self.neck01Ctrl,
            'Pose',
            maintainOffset=False,
            name=neck01OutCnstrName)

        neck02OutCnstrName = '_'.join([self.neck02OutputTgt.getName(),
                                       'To',
                                       self.neck02Ctrl.getName()])

        self.neck02OutCnstr = self.neck02OutputTgt.constrainTo(
            self.neck02Ctrl,
            'Pose',
            maintainOffset=False,
            name=neck02OutCnstrName)

        neckEndCnstrName = '_'.join([self.neckEndOutputTgt.getName(),
                                     'To',
                                     self.neck02Ctrl.getName()])

        self.neckEndCnstr = self.neckEndOutputTgt.constrainTo(
            self.neck01Ctrl,
            'Pose',
            maintainOffset=True,
            name=neckEndCnstrName)


        # ==============
        # Add Operators
        # ==============
        # Add Deformer KL Op
        self.neckDeformerKLOp = KLOperator('neckDeformerKLOp',
                                           'MultiPoseConstraintSolver',
                                           'Kraken')

        self.addOperator(self.neckDeformerKLOp)

        # Add Att Inputs
        self.neckDeformerKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.neckDeformerKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputstrl)
        self.neckDeformerKLOp.setInput('constrainers',
                                       [self.neck01Ctrl, self.neck02Ctrl])

        # Add Xfo Outputs
        self.neckDeformerKLOp.setOutput('constrainees',
                                        [self.neck01Def, self.neck02Def])

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(NeckComponentRig, self).loadData(data)
        neckXfo = data.get('neckXfo')
        neckCrvData = data.get('neckCrvData')
        neckMidXfo = data.get('neckMidXfo')
        neckMidCrvData = data.get('neckMidCrvData')
        neckEndXfo = data.get('neckEndXfo')

        self.neck01CtrlSpace.xfo = neckXfo
        self.neck01Ctrl.xfo = neckXfo
        self.neck01Ctrl.setCurveData(neckCrvData)

        self.neck02CtrlSpace.xfo = neckMidXfo
        self.neck02Ctrl.xfo = neckMidXfo
        self.neck02Ctrl.setCurveData(neckMidCrvData)


        # ============
        # Set IO Xfos
        # ============
        self.neckBaseInputTgt.xfo = neckXfo
        self.neck01OutputTgt.xfo = neckXfo
        self.neck02OutputTgt.xfo = neckMidXfo
        self.neckEndOutputTgt.xfo = neckEndXfo

        # Evaluate Constraints
        self.neckInputCnstr.evaluate()
        self.neck01OutCnstr.evaluate()
        self.neck02OutCnstr.evaluate()
        self.neckEndCnstr.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(NeckComponentGuide)
ks.registerComponent(NeckComponentRig)
