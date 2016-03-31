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
from kraken.core.objects.transform import Transform
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class ArmComponent(BaseExampleComponent):
    """Arm Component Base"""

    def __init__(self, name='arm', parent=None):
        super(ArmComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.rootInputTgt = self.createInput('root', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.bicepOutputTgt = self.createOutput('bicep', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.forearmOutputTgt = self.createOutput('forearm', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.wristOutputTgt = self.createOutput('wrist', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs
        self.drawDebugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', value=False, parent=self.cmpOutputAttrGrp).getTarget()
        self.ikBlendOutputAttr = self.createOutput('ikBlend', dataType='Float', value=0.0, parent=self.cmpOutputAttrGrp).getTarget()



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
        self.bicepCtrl = Control('bicep', parent=self.ctrlCmpGrp, shape="sphere")
        self.bicepCtrl.setColor('blue')
        self.forearmCtrl = Control('forearm', parent=self.ctrlCmpGrp, shape="sphere")
        self.forearmCtrl.setColor('blue')
        self.wristCtrl = Control('wrist', parent=self.ctrlCmpGrp, shape="sphere")
        self.wristCtrl.setColor('blue')


        self.default_data = {
            "name": name,
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": self.bicepFKCtrlSizeInputAttr.getValue(),
            "forearmFKCtrlSize": self.forearmFKCtrlSizeInputAttr.getValue()
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

        data = super(ArmComponentGuide, self).saveData()

        data['bicepXfo'] = self.bicepCtrl.xfo
        data['forearmXfo'] = self.forearmCtrl.xfo
        data['wristXfo'] = self.wristCtrl.xfo

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

        # Calculate Wrist Xfo
        wristXfo = Xfo()
        wristXfo.tr = self.wristCtrl.xfo.tr
        wristXfo.ori = forearmXfo.ori

        upVXfo = xfoFromDirAndUpV(bicepPosition, wristPosition, forearmPosition)
        upVXfo.tr = forearmPosition
        upVXfo.tr = upVXfo.transformVector(Vec3(0, 0, 5))

        # Lengths
        bicepLen = bicepPosition.subtract(forearmPosition).length()
        forearmLen = forearmPosition.subtract(wristPosition).length()

        data['bicepXfo'] = bicepXfo
        data['forearmXfo'] = forearmXfo
        data['wristXfo'] = wristXfo
        data['upVXfo'] = upVXfo
        data['bicepLen'] = bicepLen
        data['forearmLen'] = forearmLen

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

        # Arm IK
        self.armIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.armIKCtrl = Control('IK', parent=self.armIKCtrlSpace, shape="pin")

        # Add Params to IK control
        armSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings", parent=self.armIKCtrl)
        self.armDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=armSettingsAttrGrp)
        self.armBone0LenInputAttr = ScalarAttribute('bone1Len', value=0.0, parent=armSettingsAttrGrp)
        self.armBone1LenInputAttr = ScalarAttribute('bone2Len', value=0.0, parent=armSettingsAttrGrp)
        self.armIKBlendInputAttr = ScalarAttribute('fkik', value=0.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)
        self.armSoftIKInputAttr = BoolAttribute('softIK', value=True, parent=armSettingsAttrGrp)
        self.armSoftDistInputAttr = ScalarAttribute('softDist', value=0.0, minValue=0.0, parent=armSettingsAttrGrp)
        self.armStretchInputAttr = BoolAttribute('stretch', value=True, parent=armSettingsAttrGrp)
        self.armStretchBlendInputAttr = ScalarAttribute('stretchBlend', value=0.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)

        # Util Objects
        self.ikRootPosition = Transform("ikPosition", parent=self.ctrlCmpGrp)

        # Connect Input Attrs
        self.drawDebugInputAttr.connect(self.armDebugInputAttr)

        # Connect Output Attrs
        self.drawDebugOutputAttr.connect(self.armDebugInputAttr)
        self.ikBlendOutputAttr.connect(self.armIKBlendInputAttr)

        # UpV
        self.armUpVCtrlSpace = CtrlSpace('UpV', parent=self.ctrlCmpGrp)
        self.armUpVCtrl = Control('UpV', parent=self.armUpVCtrlSpace, shape="triangle")
        self.armUpVCtrl.alignOnZAxis()
        self.armUpVCtrl.rotatePoints(180, 0, 0)


        # ==========
        # Deformers
        # ==========
        self.deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=self.deformersLayer)
        self.defCmpGrp.setComponent(self)
        self.addItem('defCmpGrp', self.defCmpGrp)

        self.bicepDef = Joint('bicep', parent=self.defCmpGrp)
        self.bicepDef.setComponent(self)

        self.forearmDef = Joint('forearm', parent=self.defCmpGrp)
        self.forearmDef.setComponent(self)

        self.wristDef = Joint('wrist', parent=self.defCmpGrp)
        self.wristDef.setComponent(self)


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

        self.armRootInputConstraint = PoseConstraint('_'.join([self.bicepFKCtrlSpace.getName(), 'To', self.rootInputTgt.getName()]))
        self.armRootInputConstraint.setMaintainOffset(True)
        self.armRootInputConstraint.addConstrainer(self.rootInputTgt)
        self.bicepFKCtrlSpace.addConstraint(self.armRootInputConstraint)

        self.ikPosInputConstraint = PoseConstraint('_'.join([self.ikRootPosition.getName(), 'To', self.rootInputTgt.getName()]))
        self.ikPosInputConstraint.setMaintainOffset(True)
        self.ikPosInputConstraint.addConstrainer(self.rootInputTgt)
        self.ikRootPosition.addConstraint(self.ikPosInputConstraint)

        # Constraint outputs


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        self.armSolverKLOperator = KLOperator('armKLOp', 'TwoBoneIKSolver', 'Kraken')
        self.addOperator(self.armSolverKLOperator)

        # Add Att Inputs
        self.armSolverKLOperator.setInput('drawDebug', self.drawDebugInputAttr)
        self.armSolverKLOperator.setInput('rigScale', self.rigScaleInputAttr)

        self.armSolverKLOperator.setInput('bone0Len', self.armBone0LenInputAttr)
        self.armSolverKLOperator.setInput('bone1Len', self.armBone1LenInputAttr)
        self.armSolverKLOperator.setInput('ikblend', self.armIKBlendInputAttr)
        self.armSolverKLOperator.setInput('softIK', self.armSoftIKInputAttr)
        self.armSolverKLOperator.setInput('softDist', self.armSoftDistInputAttr)
        self.armSolverKLOperator.setInput('stretch', self.armStretchInputAttr)
        self.armSolverKLOperator.setInput('stretchBlend', self.armStretchBlendInputAttr)
        self.armSolverKLOperator.setInput('rightSide', self.rightSideInputAttr)

        # Add Xfo Inputs
        self.armSolverKLOperator.setInput('root', self.ikRootPosition)
        self.armSolverKLOperator.setInput('bone0FK', self.bicepFKCtrl)
        self.armSolverKLOperator.setInput('bone1FK', self.forearmFKCtrl)
        self.armSolverKLOperator.setInput('ikHandle', self.armIKCtrl)
        self.armSolverKLOperator.setInput('upV', self.armUpVCtrl)

        # Add Xfo Outputs
        self.armSolverKLOperator.setOutput('bone0Out', self.bicepOutputTgt)
        self.armSolverKLOperator.setOutput('bone1Out', self.forearmOutputTgt)
        self.armSolverKLOperator.setOutput('bone2Out', self.wristOutputTgt)


        # Add Deformer Splice Op
        self.outputsToDeformersKLOp = KLOperator('armDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)

        # Add Att Inputs
        self.outputsToDeformersKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersKLOp.setInput('constrainers', [self.bicepOutputTgt, self.forearmOutputTgt, self.wristOutputTgt])

        # Add Xfo Outputs
        self.outputsToDeformersKLOp.setOutput('constrainees', [self.bicepDef, self.forearmDef, self.wristDef])

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(ArmComponentRig, self).loadData( data )

        bicepXfo = data.get('bicepXfo')
        forearmXfo = data.get('forearmXfo')
        wristXfo = data.get('wristXfo')
        upVXfo = data.get('upVXfo')
        bicepLen = data.get('bicepLen')
        forearmLen = data.get('forearmLen')
        bicepFKCtrlSize = data.get('bicepFKCtrlSize')
        forearmFKCtrlSize = data.get('forearmFKCtrlSize')


        self.rootInputTgt.xfo.tr = bicepXfo.tr

        self.bicepFKCtrlSpace.xfo = bicepXfo
        self.bicepFKCtrl.xfo = bicepXfo
        self.bicepFKCtrl.scalePoints(Vec3(bicepLen, bicepFKCtrlSize, bicepFKCtrlSize))

        self.forearmFKCtrlSpace.xfo = forearmXfo
        self.forearmFKCtrl.xfo = forearmXfo
        self.forearmFKCtrl.scalePoints(Vec3(forearmLen, forearmFKCtrlSize, forearmFKCtrlSize))

        self.ikRootPosition.xfo = bicepXfo

        self.armIKCtrlSpace.xfo.tr = wristXfo.tr
        self.armIKCtrl.xfo.tr = wristXfo.tr

        if self.getLocation() == "R":
            self.armIKCtrl.rotatePoints(0, 90, 0)
        else:
            self.armIKCtrl.rotatePoints(0, -90, 0)

        self.armUpVCtrlSpace.xfo.tr = upVXfo.tr
        self.armUpVCtrl.xfo.tr = upVXfo.tr

        self.rightSideInputAttr.setValue(self.getLocation() is 'R')
        self.armBone0LenInputAttr.setMin(0.0)
        self.armBone0LenInputAttr.setMax(bicepLen * 3.0)
        self.armBone0LenInputAttr.setValue(bicepLen)
        self.armBone1LenInputAttr.setMin(0.0)
        self.armBone1LenInputAttr.setMax(forearmLen * 3.0)
        self.armBone1LenInputAttr.setValue(forearmLen)

        # Outputs
        self.bicepOutputTgt.xfo = bicepXfo
        self.forearmOutputTgt.xfo = forearmXfo
        self.wristOutputTgt.xfo = wristXfo

        # Eval Constraints
        self.ikPosInputConstraint.evaluate()
        self.armIKCtrlSpaceInputConstraint.evaluate()
        self.armUpVCtrlSpaceInputConstraint.evaluate()
        self.armRootInputConstraint.evaluate()
        self.armRootInputConstraint.evaluate()

        # Eval Operators
        self.armSolverKLOperator.evaluate()
        self.outputsToDeformersKLOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(ArmComponentGuide)
ks.registerComponent(ArmComponentRig)
