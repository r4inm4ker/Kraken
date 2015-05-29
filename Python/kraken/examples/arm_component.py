from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV
from kraken.core.maths.quat import Quat

from kraken.core.objects.components.component import Component


from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute

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


class ArmComponent(Component):
    """Arm Component Base"""

    def __init__(self, name='arm', parent=None, data=None):
        super(ArmComponent, self).__init__(name, parent)

        # ================
        # Setup Hierarchy
        # ================
        self.controlsLayer = self.getOrCreateLayer('controls')
        self.ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=self.controlsLayer)

        # IO Hierarchies
        self.inputHrcGrp = HierarchyGroup('inputs', parent=self.ctrlCmpGrp)
        self.cmpInputAttrGrp = AttributeGroup('inputs', parent=self.inputHrcGrp)

        self.outputHrcGrp = HierarchyGroup('outputs', parent=self.ctrlCmpGrp)
        self.cmpOutputAttrGrp = AttributeGroup('outputs', parent=self.outputHrcGrp)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp)
        self.clavicleEndInputTgt = self.createInput('clavicleEnd', dataType='Xfo', parent=self.inputHrcGrp)

        # Declare Output Xfos
        self.bicepOutputTgt = self.createOutput('bicep', dataType='Xfo', parent=self.outputHrcGrp)
        self.forearmOutputTgt = self.createOutput('forearm', dataType='Xfo', parent=self.outputHrcGrp)
        self.armEndXfoOutputTgt = self.createOutput('armEndXfo', dataType='Xfo', parent=self.outputHrcGrp)
        self.handOutputTgt = self.createOutput('hand', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', parent=self.cmpInputAttrGrp)
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp)
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=self.cmpInputAttrGrp)
        self.bicepFKCtrlSizeInputAttr = self.createInput('bicepFKCtrlSize', dataType='Float', parent=self.cmpInputAttrGrp)
        self.forearmFKCtrlSizeInputAttr = self.createInput('forearmFKCtrlSize', dataType='Float', parent=self.cmpInputAttrGrp)

        # Declare Output Attrs
        self.debugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', parent=self.cmpOutputAttrGrp)


class ArmComponentGuide(ArmComponent):
    """Arm Component Guide"""

    def __init__(self, name='armGuide', parent=None, data=None):

        Profiler.getInstance().push("Construct Arm Guide Component:" + name)
        super(ArmComponentGuide, self).__init__(name, parent)

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

        if data is None:
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

        data = {
                "name": self.getName(),
                "location": self.getLocation(),
                "bicepXfo": self.bicepCtrl.xfo,
                "forearmXfo": self.forearmCtrl.xfo,
                "wristXfo": self.wristCtrl.xfo,
                "handXfo": self.handCtrl.xfo,
                "bicepFKCtrlSize": self.bicepFKCtrlSizeInputAttr.getValue(),
                "forearmFKCtrlSize": self.forearmFKCtrlSizeInputAttr.getValue()
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
        self.bicepCtrl.xfo = data['bicepXfo']
        self.forearmCtrl.xfo = data['forearmXfo']
        self.wristCtrl.xfo = data['wristXfo']
        self.handCtrl.xfo = data['handXfo']

        self.bicepFKCtrlSizeInputAttr.setValue(data['bicepFKCtrlSize'])
        self.forearmFKCtrlSizeInputAttr.setValue(data['forearmFKCtrlSize'])

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

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

        data = {
            "class":"kraken.examples.arm_component.ArmComponentRig",
            "name": self.getName(),
            "location":self.getLocation(),
            "bicepXfo": bicepXfo,
            "forearmXfo": forearmXfo,
            "handXfo": handXfo,
            "armEndXfo": armEndXfo,
            "upVXfo": upVXfo,
            "forearmLen": forearmLen,
            "bicepLen": bicepLen,
            "bicepFKCtrlSize": self.bicepFKCtrlSizeInputAttr.getValue(),
            "forearmFKCtrlSize": self.forearmFKCtrlSizeInputAttr.getValue()
        }

        return data


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
        self.handCtrl = Control('hand', parent=self.handCtrlSpace, shape="cube")
        self.handCtrl.alignOnXAxis()
        self.handCtrl.scalePoints(Vec3(2.0, 0.75, 1.25))

        # Arm IK
        self.armIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.armIKCtrl = Control('IK', parent=self.armIKCtrlSpace, shape="pin")

        # Add Params to IK control
        armSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings", parent=self.armIKCtrl)
        armDebugInputAttr = BoolAttribute('drawDebug', value=True, parent=armSettingsAttrGrp)
        self.armBone0LenInputAttr = FloatAttribute('bone1Len', value=0.0, parent=armSettingsAttrGrp)
        self.armBone1LenInputAttr = FloatAttribute('bone2Len', value=0.0, parent=armSettingsAttrGrp)
        armIKBlendInputAttr = FloatAttribute('fkik', value=0.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)
        armSoftIKInputAttr = BoolAttribute('softIK', value=True, parent=armSettingsAttrGrp)
        armSoftDistInputAttr = FloatAttribute('softDist', value=0.0, minValue=0.0, parent=armSettingsAttrGrp)
        armStretchInputAttr = BoolAttribute('stretch', value=True, parent=armSettingsAttrGrp)
        armStretchBlendInputAttr = FloatAttribute('stretchBlend', value=0.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)

        # Hand Params
        handSettingsAttrGrp = AttributeGroup("DisplayInfo_HandSettings", parent=self.handCtrl)
        handLinkToWorldInputAttr = FloatAttribute('linkToWorld', 0.0, maxValue=1.0, parent=handSettingsAttrGrp)

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
        handConstraint = PoseConstraint('_'.join([self.handOutputTgt.getName(), 'To', self.handCtrl.getName()]))
        handConstraint.addConstrainer(self.handCtrl)
        self.handOutputTgt.addConstraint(handConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Splice Op
        self.spliceOp = SpliceOperator('armSpliceOp', 'TwoBoneIKSolver', 'Kraken')
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
        self.outputsToDeformersSpliceOp = SpliceOperator('armDeformerSpliceOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersSpliceOp)

        # Add Att Inputs
        self.outputsToDeformersSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersSpliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersSpliceOp.setInput('constrainers', self.bicepOutputTgt)
        self.outputsToDeformersSpliceOp.setInput('constrainers', self.forearmOutputTgt)
        self.outputsToDeformersSpliceOp.setInput('constrainers', self.armEndXfoOutputTgt)
        self.outputsToDeformersSpliceOp.setInput('constrainers', self.handOutputTgt)

        # Add Xfo Outputs
        self.outputsToDeformersSpliceOp.setOutput('constrainees', bicepDef)
        self.outputsToDeformersSpliceOp.setOutput('constrainees', forearmDef)
        self.outputsToDeformersSpliceOp.setOutput('constrainees', wristDef)
        self.outputsToDeformersSpliceOp.setOutput('constrainees', handDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'arm'))
        location = data.get('location', 'M')
        self.setLocation(location)

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

        # Eval Operators
        self.spliceOp.evaluate()
        self.outputsToDeformersSpliceOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(ArmComponentGuide)
ks.registerComponent(ArmComponentRig)
