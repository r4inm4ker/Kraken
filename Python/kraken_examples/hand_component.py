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
        self.clavicleOutputTgt = self.createOutput('hand', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

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

        self.numJoints = IntegerAttribute('numJoints', value=4, minValue=2, maxValue=20, parent=self.guideSettingsAttrGrp)
        self.numJoints.setValueChangeCallback(self.resizeDigits)

        self.fingers = OrderedDict()

        self.handCtrl = Control('hand', parent=self.ctrlCmpGrp, shape="sphere")
        self.handCtrl.setColor('yellow')

        self.default_data = {
            "name": name,
            "location": "L",
            "handXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "digitNames": self.digitNamesAttr.getValue(),
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
        data['fingers'] = self.fingers

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(HandComponentGuide, self).loadData( data )

        self.handCtrl.xfo = data['handXfo']
        self.digitNamesAttr.setValue(data['digitNames'])
        # self.fingers = data['fingers']

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(HandComponentGuide, self).getRigBuildData()


        # Values
        claviclePosition = self.clavicleCtrl.xfo.tr
        clavicleUpV = self.clavicleUpVCtrl.xfo.tr
        clavicleEndPosition = self.clavicleEndCtrl.xfo.tr

        # Calculate Hand Xfo
        rootToEnd = clavicleEndPosition.subtract(claviclePosition).unit()
        rootToUpV = clavicleUpV.subtract(claviclePosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()

        clavicleXfo = Xfo()
        clavicleXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, claviclePosition)

        clavicleLen = claviclePosition.subtract(clavicleEndPosition).length()

        data['clavicleXfo'] = clavicleXfo
        data['clavicleLen'] = clavicleLen

        return data


    # ==========
    # Callbacks
    # ==========
    def addFinger(self, name):
        firstDigitCtrl = Control(name + "01", parent=self.ctrlCmpGrp, shape='sphere')
        firstDigitCtrl.setColor('orange')
        firstDigitCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))

        self.fingers[name] = []
        self.fingers[name].append(firstDigitCtrl)

        parent = firstDigitCtrl
        for i in xrange(2, self.numJoints.getValue() + 2):
            print i
            digitCtrl = Control(name + str(i).zfill(2), parent=parent, shape='sphere')
            digitCtrl.setColor('orange')
            digitCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))

            self.fingers[name].append(digitCtrl)

            parent = digitCtrl

        return firstDigitCtrl

    def removeFinger(self, name):
        del self.fingers[name]
        self.ctrlCmpGrp.removeChild(extraCtrl)

    def placeFingers(self):

        spacing = 0.75
        length = spacing * (len(self.fingers.keys()) - 1)
        mid = length / 2.0
        startOffset = length - mid

        for i, finger in enumerate(self.fingers.keys()):

            for y in xrange(self.numJoints.getValue() + 1):
                fingerPos = self.handCtrl.xfo.transformVector(Vec3(y * 1.0, 0, startOffset - (i * spacing)))
                fingerXfo = Xfo(tr=fingerPos, ori=self.handCtrl.xfo.ori)

                self.fingers[finger][y].xfo = fingerXfo

    def updateFingers(self, fingers):

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
                    digitCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
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
        self.clavicleCtrlSpace = CtrlSpace('clavicle', parent=self.ctrlCmpGrp)
        self.clavicleCtrl = Control('clavicle', parent=self.clavicleCtrlSpace, shape="cube")
        self.clavicleCtrl.alignOnXAxis()


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.ctrlCmpGrp.setComponent(self)

        self.clavicleDef = Joint('clavicle', parent=defCmpGrp)
        self.clavicleDef.setComponent(self)


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([self.clavicleCtrl.getName(), 'To', self.armEndInputTgt.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(self.armEndInputTgt)
        self.clavicleCtrlSpace.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        clavicleConstraint = PoseConstraint('_'.join([self.clavicleOutputTgt.getName(), 'To', self.clavicleCtrl.getName()]))
        clavicleConstraint.addConstrainer(self.clavicleCtrl)
        self.clavicleOutputTgt.addConstraint(clavicleConstraint)

        clavicleEndConstraint = PoseConstraint('_'.join([self.clavicleEndOutputTgt.getName(), 'To', self.clavicleCtrl.getName()]))
        clavicleEndConstraint.addConstrainer(self.clavicleCtrl)
        self.clavicleEndOutputTgt.addConstraint(clavicleEndConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        spliceOp = KLOperator('clavicleDeformerKLOp', 'PoseConstraintSolver', 'Kraken')
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        spliceOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        spliceOp.setInput('constrainer', self.clavicleOutputTgt)

        # Add Xfo Outputs
        spliceOp.setOutput('constrainee', self.clavicleDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(HandComponentRig, self).loadData( data )

        self.clavicleCtrlSpace.xfo = data['clavicleXfo']
        self.clavicleCtrl.xfo = data['clavicleXfo']
        self.clavicleCtrl.scalePoints(Vec3(data['clavicleLen'], 0.75, 0.75))

        if data['location'] == "R":
            self.clavicleCtrl.translatePoints(Vec3(0.0, 0.0, -1.0))
        else:
            self.clavicleCtrl.translatePoints(Vec3(0.0, 0.0, 1.0))

        # ============
        # Set IO Xfos
        # ============
        self.armEndInputTgt.xfo = data['clavicleXfo']
        self.clavicleEndOutputTgt.xfo = data['clavicleXfo']
        self.clavicleOutputTgt.xfo = data['clavicleXfo']


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(HandComponentGuide)
ks.registerComponent(HandComponentRig)