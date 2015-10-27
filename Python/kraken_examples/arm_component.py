from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV
from kraken.core.maths.quat import Quat

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class ArmComponent(BaseExampleComponent):
    """Arm Component Base"""

    def __init__(self, name='arm', parent=None, data=None):
        super(ArmComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.clavicleEndInputTgt = self.createInput('clavicleEnd', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.bicepOutputTgt = self.createOutput('bicep', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.forearmOutputTgt = self.createOutput('forearm', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.armEndXfoOutputTgt = self.createOutput('armEndXfo', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.handOutputTgt = self.createOutput('hand', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs
        self.debugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', parent=self.cmpOutputAttrGrp).getTarget()


class ArmComponentGuide(ArmComponent):
    """Arm Component Guide"""

    def __init__(self, name='arm', parent=None):

        Profiler.getInstance().push("Construct Arm Guide Component:" + name)
        super(ArmComponentGuide, self).__init__(name, parent)

        # ===========
        # Attributes
        # ===========
        # Add Component Params to IK control
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.bicepFKCtrlSizeInputAttr = ScalarAttribute('bicepFKCtrlSize', value=1.75, minValue=0.0,   maxValue=10.0, parent=guideSettingsAttrGrp)
        self.forearmFKCtrlSizeInputAttr = ScalarAttribute('forearmFKCtrlSize', value=1.5, minValue=0.0,   maxValue=10.0, parent=guideSettingsAttrGrp)

        # =========
        # Controls
        # =========
        # Guide Controls
        self.bicepCtrl = Control('bicepFK', parent=self.ctrlCmpGrp, shape="sphere")
        self.bicepCtrl.setColor('blue')
        self.forearmCtrl = Control('forearmFK', parent=self.ctrlCmpGrp, shape="sphere")
        self.forearmCtrl.setColor('blue')
        self.wristCtrl = Control('wristFK', parent=self.ctrlCmpGrp, shape="sphere")
        self.wristCtrl.setColor('blue')
        self.handCtrl = Control('hand', parent=self.ctrlCmpGrp, shape="cube")
        self.handCtrl.setColor('blue')

        data = {
            "name": name,
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                           ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
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

        data = super(ArmComponentGuide, self).saveData()

        data['bicepXfo'] = self.bicepCtrl.xfo
        data['forearmXfo'] = self.forearmCtrl.xfo
        data['wristXfo'] = self.wristCtrl.xfo
        data['handXfo'] = self.handCtrl.xfo

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(ArmComponentGuide, self).loadData( data )

        self.bicepCtrl.xfo = data['bicepXfo']
        self.forearmCtrl.xfo = data['forearmXfo']
        self.wristCtrl.xfo = data['wristXfo']
        self.handCtrl.xfo = data['handXfo']

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(ArmComponentGuide, self).getRigBuildData()

        # values
        bicepPosition = self.bicepCtrl.xfo.tr
        forearmPosition = self.forearmCtrl.xfo.tr
        wristPosition = self.wristCtrl.xfo.tr

        # Calculate Bicep Xfo
        rootToWrist = wristPosition.subtract(bicepPosition).unit()
        rootToElbow = forearmPosition.subtract(bicepPosition).unit()

        bone1Normal = rootToWrist.cross(rootToElbow).unit()
        bone1ZAxis = rootToElbow.cross(bone1Normal).unit()

        bicepXfo = Xfo()
        bicepXfo.setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, bicepPosition)

        # Calculate Forearm Xfo
        elbowToWrist = wristPosition.subtract(forearmPosition).unit()
        elbowToRoot = bicepPosition.subtract(forearmPosition).unit()
        bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
        bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()
        forearmXfo = Xfo()
        forearmXfo.setFromVectors(elbowToWrist, bone2Normal, bone2ZAxis, forearmPosition)

        handXfo = Xfo()
        handXfo.tr = self.handCtrl.xfo.tr
        handXfo.ori = self.handCtrl.xfo.ori

        bicepLen = bicepPosition.subtract(forearmPosition).length()
        forearmLen = forearmPosition.subtract(wristPosition).length()

        armEndXfo = Xfo()
        armEndXfo.tr = wristPosition
        armEndXfo.ori = forearmXfo.ori

        upVXfo = xfoFromDirAndUpV(bicepPosition, wristPosition, forearmPosition)
        upVXfo.tr = forearmPosition
        upVXfo.tr = upVXfo.transformVector(Vec3(0, 0, 5))

        data['bicepXfo'] = bicepXfo
        data['forearmXfo'] = forearmXfo
        data['handXfo'] = handXfo
        data['armEndXfo'] = armEndXfo
        data['upVXfo'] = upVXfo
        data['forearmLen'] = forearmLen
        data['bicepLen'] = bicepLen

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

        return ArmComponentRig


class ArmComponentRig(ArmComponent):
    """Arm Component Rig"""

    def __init__(self, name='arm', parent=None):

        Profiler.getInstance().push("Construct Arm Rig Component:" + name)
        super(ArmComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Bicep
        self.bicepFKCtrlSpace = CtrlSpace('bicepFK', parent=self.ctrlCmpGrp)

        self.bicepFKCtrl = Control('bicepFK', parent=self.bicepFKCtrlSpace, shape="cube")
        self.bicepFKCtrl.alignOnXAxis()

        # Forearm
        self.forearmFKCtrlSpace = CtrlSpace('forearmFK', parent=self.bicepFKCtrl)

        self.forearmFKCtrl = Control('forearmFK', parent=self.forearmFKCtrlSpace, shape="cube")
        self.forearmFKCtrl.alignOnXAxis()

        self.handCtrlSpace = CtrlSpace('hand', parent=self.ctrlCmpGrp)
        self.handCtrl = Control('hand', parent=self.handCtrlSpace, shape="circle")
        self.handCtrl.rotatePoints(0, 0, 90)
        self.handCtrl.scalePoints(Vec3(1.0, 0.75, 0.75))

        # Arm IK
        self.armIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.armIKCtrl = Control('IK', parent=self.armIKCtrlSpace, shape="pin")

        # Add Params to IK control
        armSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings", parent=self.armIKCtrl)
        armDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=armSettingsAttrGrp)
        self.armBone0LenInputAttr = ScalarAttribute('bone1Len', value=0.0, parent=armSettingsAttrGrp)
        self.armBone1LenInputAttr = ScalarAttribute('bone2Len', value=0.0, parent=armSettingsAttrGrp)
        armIKBlendInputAttr = ScalarAttribute('fkik', value=0.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)
        armSoftIKInputAttr = BoolAttribute('softIK', value=True, parent=armSettingsAttrGrp)
        armSoftDistInputAttr = ScalarAttribute('softDist', value=0.0, minValue=0.0, parent=armSettingsAttrGrp)
        armStretchInputAttr = BoolAttribute('stretch', value=True, parent=armSettingsAttrGrp)
        armStretchBlendInputAttr = ScalarAttribute('stretchBlend', value=0.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)

        # Hand Params
        handSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings", parent=self.handCtrl)
        handLinkToWorldInputAttr = ScalarAttribute('linkToWorld', 0.0, maxValue=1.0, parent=handSettingsAttrGrp)

        self.drawDebugInputAttr.connect(armDebugInputAttr)

        # UpV
        self.armUpVCtrlSpace = CtrlSpace('UpV', parent=self.ctrlCmpGrp)
        self.armUpVCtrl = Control('UpV', parent=self.armUpVCtrlSpace, shape="triangle")
        self.armUpVCtrl.alignOnZAxis()
        self.armUpVCtrl.rotatePoints(180, 0, 0)


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)

        bicepDef = Joint('bicep', parent=defCmpGrp)
        bicepDef.setComponent(self)

        forearmDef = Joint('forearm', parent=defCmpGrp)
        forearmDef.setComponent(self)

        wristDef = Joint('wrist', parent=defCmpGrp)
        wristDef.setComponent(self)

        handDef = Joint('hand', parent=defCmpGrp)
        handDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.armIKCtrlSpaceInputConstraint = PoseConstraint('_'.join([self.armIKCtrlSpace.getName(), 'To', self.globalSRTInputTgt.getName()]))
        self.armIKCtrlSpaceInputConstraint.setMaintainOffset(True)
        self.armIKCtrlSpaceInputConstraint.addConstrainer(self.globalSRTInputTgt)
        self.armIKCtrlSpace.addConstraint(self.armIKCtrlSpaceInputConstraint)

        self.armUpVCtrlSpaceInputConstraint = PoseConstraint('_'.join([self.armUpVCtrlSpace.getName(), 'To', self.globalSRTInputTgt.getName()]))
        self.armUpVCtrlSpaceInputConstraint.setMaintainOffset(True)
        self.armUpVCtrlSpaceInputConstraint.addConstrainer(self.globalSRTInputTgt)
        self.armUpVCtrlSpace.addConstraint(self.armUpVCtrlSpaceInputConstraint)

        self.armRootInputConstraint = PoseConstraint('_'.join([self.bicepFKCtrlSpace.getName(), 'To', self.clavicleEndInputTgt.getName()]))
        self.armRootInputConstraint.setMaintainOffset(True)
        self.armRootInputConstraint.addConstrainer(self.clavicleEndInputTgt)
        self.bicepFKCtrlSpace.addConstraint(self.armRootInputConstraint)

        # Constraint outputs
        self.handConstraint = PoseConstraint('_'.join([self.handOutputTgt.getName(), 'To', self.handCtrl.getName()]))
        self.handConstraint.addConstrainer(self.handCtrl)
        self.handOutputTgt.addConstraint(self.handConstraint)

        self.handCtrlSpaceConstraint = PoseConstraint('_'.join([self.handCtrlSpace.getName(), 'To', self.armEndXfoOutputTgt.getName()]))
        self.handCtrlSpaceConstraint.setMaintainOffset(True)
        self.handCtrlSpaceConstraint.addConstrainer(self.armEndXfoOutputTgt)
        self.handCtrlSpace.addConstraint(self.handCtrlSpaceConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        self.spliceOp = KLOperator('armKLOp', 'TwoBoneIKSolver', 'Kraken')
        self.addOperator(self.spliceOp)

        # Add Att Inputs
        self.spliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.spliceOp.setInput('rigScale', self.rigScaleInputAttr)

        self.spliceOp.setInput('bone0Len', self.armBone0LenInputAttr)
        self.spliceOp.setInput('bone1Len', self.armBone1LenInputAttr)
        self.spliceOp.setInput('ikblend', armIKBlendInputAttr)
        self.spliceOp.setInput('softIK', armSoftIKInputAttr)
        self.spliceOp.setInput('softDist', armSoftDistInputAttr)
        self.spliceOp.setInput('stretch', armStretchInputAttr)
        self.spliceOp.setInput('stretchBlend', armStretchBlendInputAttr)
        self.spliceOp.setInput('rightSide', self.rightSideInputAttr)

        # Add Xfo Inputs
        self.spliceOp.setInput('root', self.clavicleEndInputTgt)
        self.spliceOp.setInput('bone0FK', self.bicepFKCtrl)
        self.spliceOp.setInput('bone1FK', self.forearmFKCtrl)
        self.spliceOp.setInput('ikHandle', self.armIKCtrl)
        self.spliceOp.setInput('upV', self.armUpVCtrl)

        # Add Xfo Outputs
        self.spliceOp.setOutput('bone0Out', self.bicepOutputTgt)
        self.spliceOp.setOutput('bone1Out', self.forearmOutputTgt)
        self.spliceOp.setOutput('bone2Out', self.armEndXfoOutputTgt)


        # Add Deformer Splice Op
        self.outputsToDeformersKLOp = KLOperator('armDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)

        # Add Att Inputs
        self.outputsToDeformersKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersKLOp.setInput('constrainers', [self.bicepOutputTgt, self.forearmOutputTgt, self.armEndXfoOutputTgt, self.handOutputTgt])

        # Add Xfo Outputs
        self.outputsToDeformersKLOp.setOutput('constrainees', [bicepDef, forearmDef, wristDef, handDef])

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(ArmComponentRig, self).loadData( data )

        self.clavicleEndInputTgt.xfo.tr = data['bicepXfo'].tr

        self.bicepFKCtrlSpace.xfo = data['bicepXfo']
        self.bicepFKCtrl.xfo = data['bicepXfo']
        self.bicepFKCtrl.scalePoints(Vec3(data['bicepLen'], data['bicepFKCtrlSize'], data['bicepFKCtrlSize']))

        self.bicepOutputTgt.xfo = data['bicepXfo']
        self.forearmOutputTgt.xfo = data['forearmXfo']

        self.forearmFKCtrlSpace.xfo = data['forearmXfo']
        self.forearmFKCtrl.xfo = data['forearmXfo']
        self.forearmFKCtrl.scalePoints(Vec3(data['forearmLen'], data['forearmFKCtrlSize'], data['forearmFKCtrlSize']))

        self.handCtrlSpace.xfo = data['handXfo']
        self.handCtrl.xfo = data['handXfo']

        self.armIKCtrlSpace.xfo.tr = data['armEndXfo'].tr
        self.armIKCtrl.xfo.tr = data['armEndXfo'].tr

        if self.getLocation() == "R":
            self.armIKCtrl.rotatePoints(0, 90, 0)
        else:
            self.armIKCtrl.rotatePoints(0, -90, 0)

        self.armUpVCtrlSpace.xfo = data['upVXfo']
        self.armUpVCtrl.xfo = data['upVXfo']

        self.rightSideInputAttr.setValue(self.getLocation() is 'R')
        self.armBone0LenInputAttr.setMin(0.0)
        self.armBone0LenInputAttr.setMax(data['bicepLen'] * 3.0)
        self.armBone0LenInputAttr.setValue(data['bicepLen'])
        self.armBone1LenInputAttr.setMin(0.0)
        self.armBone1LenInputAttr.setMax(data['forearmLen'] * 3.0)
        self.armBone1LenInputAttr.setValue(data['forearmLen'])

        # Outputs
        self.handOutputTgt.xfo = data['handXfo']

        # Eval Constraints
        self.armIKCtrlSpaceInputConstraint.evaluate()
        self.armUpVCtrlSpaceInputConstraint.evaluate()
        self.armRootInputConstraint.evaluate()
        self.armRootInputConstraint.evaluate()
        self.handConstraint.evaluate()
        self.handCtrlSpaceConstraint.evaluate()

        # Eval Operators
        self.spliceOp.evaluate()
        self.outputsToDeformersKLOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(ArmComponentGuide)
ks.registerComponent(ArmComponentRig)
