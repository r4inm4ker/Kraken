from collections import OrderedDict

from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy



class HandComponent(BaseExampleComponent):
    """Hand Component Base"""

    def __init__(self, name='hand', parent=None):
        super(HandComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.armEndInputTgt = self.createInput('armEnd', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.handOutputTgt = self.createOutput('hand', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', value=self.getLocation() is 'R', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs



class HandComponentGuide(HandComponent):
    """Hand Component Guide"""

    def __init__(self, name='hand', parent=None):

        Profiler.getInstance().push("Construct Hand Guide Component:" + name)
        super(HandComponentGuide, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Guide Controls
        self.guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.digitNamesAttr = StringAttribute('digitNames', value="thumb,index,middle,ring,pinky", parent=self.guideSettingsAttrGrp)
        self.digitNamesAttr.setValueChangeCallback(self.updateFingers)

        self.numJointsAttr = IntegerAttribute('numJoints', value=4, minValue=2, maxValue=20, parent=self.guideSettingsAttrGrp)
        self.numJointsAttr.setValueChangeCallback(self.resizeDigits)

        self.fingers = OrderedDict()

        self.handCtrl = Control('hand', parent=self.ctrlCmpGrp, shape="sphere")
        self.handCtrl.setColor('yellow')

        self.default_data = {
            "name": name,
            "location": "L",
            "handXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "digitNames": self.digitNamesAttr.getValue(),
            "numJoints": self.numJointsAttr.getValue(),
            "fingers": self.fingers
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

        data = super(HandComponentGuide, self).saveData()

        data['handXfo'] = self.handCtrl.xfo
        data['digitNames'] = self.digitNamesAttr.getValue()
        data['numJoints'] = self.numJointsAttr.getValue()

        fingerXfos = {}
        for finger in self.fingers.keys():
            fingerXfos[finger] = [x.xfo for x in self.fingers[finger]]

        data['fingersGuideXfos'] = fingerXfos

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(HandComponentGuide, self).loadData( data )

        self.handCtrl.xfo = data.get('handXfo')
        self.digitNamesAttr.setValue(data.get('digitNames'))
        self.numJointsAttr.setValue(data.get('numJoints'))

        fingersGuideXfos = data.get('fingersGuideXfos')
        if fingersGuideXfos is not None:

            for finger in self.fingers.keys():
                for i in xrange(len(self.fingers[finger])):
                    self.fingers[finger][i].xfo = fingersGuideXfos[finger][i]

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(HandComponentGuide, self).getRigBuildData()

        data['handXfo'] = self.handCtrl.xfo

        fingerData = {}
        for finger in self.fingers.keys():

            utilXfo = Xfo()

            fingerData[finger] = []
            for i, joint in enumerate(self.fingers[finger]):
                if i == len(self.fingers[finger]) - 1:
                    continue

                # Calculate Xfo
                boneVec = self.fingers[finger][i].xfo.tr - self.fingers[finger][i+1].xfo.tr
                bone1Normal = self.fingers[finger][i].xfo.ori.getZaxis().cross(boneVec).unit()
                bone1ZAxis = boneVec.cross(bone1Normal).unit()

                utilXfo.setFromVectors(boneVec.unit(), bone1Normal, bone1ZAxis, self.fingers[finger][i].xfo.tr)

                jointData = {
                    'length': self.fingers[finger][i].xfo.tr.distanceTo(self.fingers[finger][i+1].xfo.tr),
                    'xfo': utilXfo
                }

                fingerData[finger].append(jointData)

        data['fingerData'] = fingerData

        return data


    # ==========
    # Callbacks
    # ==========
    def addFinger(self, name):
        firstDigitCtrl = Control(name + "01", parent=self.handCtrl, shape='sphere')
        firstDigitCtrl.setColor('orange')
        firstDigitCtrl.scalePoints(Vec3(0.25, 0.25, 0.25))
        firstDigitCtrl.lockScale(True, True, True)

        self.fingers[name] = []
        self.fingers[name].append(firstDigitCtrl)

        parent = firstDigitCtrl
        numJoints = self.numJointsAttr.getValue()
        if name == "thumb":
            numJoints = 3
        for i in xrange(2, numJoints + 2):
            digitCtrl = Control(name + str(i).zfill(2), parent=parent, shape='sphere')
            digitCtrl.setColor('orange')
            digitCtrl.scalePoints(Vec3(0.25, 0.25, 0.25))
            digitCtrl.lockScale(True, True, True)

            self.fingers[name].append(digitCtrl)

            parent = digitCtrl

        return firstDigitCtrl

    def removeFinger(self, name):
        self.handCtrl.removeChild(self.fingers[name][0])
        del self.fingers[name]

    def placeFingers(self):

        spacing = 0.5
        length = spacing * (len(self.fingers.keys()) - 1)
        mid = length / 2.0
        startOffset = length - mid

        for i, finger in enumerate(self.fingers.keys()):

            parentCtrl = self.handCtrl
            numJoints = self.numJointsAttr.getValue()
            if finger == "thumb":
                numJoints = 3
            for y in xrange(numJoints + 1):
                if y == 1:
                    xOffset = 2
                else:
                    xOffset = 0.5

                if y == 0:
                    offsetVec = Vec3(xOffset, 0, startOffset - (i * spacing))
                else:
                    offsetVec = Vec3(xOffset, 0, 0)

                fingerPos = parentCtrl.xfo.transformVector(offsetVec)
                fingerXfo = Xfo(tr=fingerPos, ori=self.handCtrl.xfo.ori)

                self.fingers[finger][y].xfo = fingerXfo
                parentCtrl = self.fingers[finger][y]

    def updateFingers(self, fingers):

        if " " in fingers:
            self.digitNamesAttr.setValue(fingers.replace(" ", ""))
            return

        fingerNames = fingers.split(',')

        # Delete fingers that don't exist any more
        for finger in list(set(self.fingers.keys()) - set(fingerNames)):
            self.removeFinger(finger)

        # Add Fingers
        for finger in fingerNames:
            if finger in self.fingers.keys():
                continue

            newFinger = self.addFinger(finger)

        self.placeFingers()

    def resizeDigits(self, numJoints):

        for finger in self.fingers.keys():
            if numJoints + 1 == len(self.fingers[finger]):
                continue

            elif numJoints + 1 > len(self.fingers[finger]):
                for i in xrange(len(self.fingers[finger]), numJoints + 1):
                    prevDigit = self.fingers[finger][i - 1]
                    digitCtrl = Control(finger + str(i + 1).zfill(2), parent=prevDigit, shape='sphere')
                    digitCtrl.setColor('orange')
                    digitCtrl.scalePoints(Vec3(0.25, 0.25, 0.25))
                    digitCtrl.lockScale(True, True, True)

                    self.fingers[finger].append(digitCtrl)

            elif numJoints + 1 < len(self.fingers[finger]):
                numExtraCtrls = len(self.fingers[finger]) - (numJoints + 1)
                for i in xrange(numExtraCtrls):
                    removedJoint = self.fingers[finger].pop()
                    removedJoint.getParent().removeChild(removedJoint)

        self.placeFingers()


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

        return HandComponentRig


class HandComponentRig(HandComponent):
    """Hand Component"""

    def __init__(self, name='Hand', parent=None):

        Profiler.getInstance().push("Construct Hand Rig Component:" + name)
        super(HandComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Hand
        self.handCtrlSpace = CtrlSpace('hand', parent=self.ctrlCmpGrp)
        self.handCtrl = Control('hand', parent=self.handCtrlSpace, shape="cube")
        self.handCtrl.alignOnXAxis()


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.ctrlCmpGrp.setComponent(self)

        self.handDef = Joint('hand', parent=defCmpGrp)
        self.handDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.armEndInputConstraint = PoseConstraint('_'.join([self.handCtrlSpace.getName(), 'To', self.armEndInputTgt.getName()]))
        self.armEndInputConstraint.setMaintainOffset(True)
        self.armEndInputConstraint.addConstrainer(self.armEndInputTgt)
        self.handCtrlSpace.addConstraint(self.armEndInputConstraint)

        # Constraint outputs
        self.handOutputConstraint = PoseConstraint('_'.join([self.handOutputTgt.getName(), 'To', self.handCtrl.getName()]))
        self.handOutputConstraint.addConstrainer(self.handCtrl)
        self.handOutputTgt.addConstraint(self.handOutputConstraint)

        # Constraint deformers
        self.handDefConstraint = PoseConstraint('_'.join([self.handDef.getName(), 'To', self.handCtrl.getName()]))
        self.handDefConstraint.addConstrainer(self.handCtrl)
        self.handDef.addConstraint(self.handDefConstraint)

        Profiler.getInstance().pop()


    def addFinger(self, fingerData):
        pass


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(HandComponentRig, self).loadData( data )

        fingerData = data.get('fingerData')

        # TODO: Implement procedural addition of fingers including controls,
        # deformers, and multi-pose constraint KL ops.

        handXfo = data.get('handXfo', Xfo())

        self.armEndInputTgt.xfo = handXfo

        self.handCtrlSpace.xfo = handXfo
        self.handCtrl.xfo = handXfo
        # self.handCtrl.scalePoints(Vec3(data['clavicleLen'], 0.75, 0.75))

        # ============
        # Set IO Xfos
        # ============
        # self.armEndInputTgt.xfo = data['clavicleXfo']
        # self.clavicleEndOutputTgt.xfo = data['clavicleXfo']
        # self.handOutputTgt.xfo = data['clavicleXfo']

        # Eval Constraints
        self.armEndInputConstraint.evaluate()
        self.handOutputConstraint.evaluate()
        self.handDefConstraint.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(HandComponentGuide)
ks.registerComponent(HandComponentRig)