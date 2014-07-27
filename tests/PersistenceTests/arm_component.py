import json
from kraken.core.maths import *
from kraken.core.objects.kraken_factory import KrakenFactory

from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.components.base_component import BaseComponent

from kraken.core.objects.locator import Locator

from kraken.core.objects.controls.cube_control  import CubeControl
from kraken.core.objects.controls.circle_control  import  CircleControl
from kraken.core.objects.controls.square_control  import  SquareControl
from kraken.core.objects.controls.null_control  import  NullControl


class ArmComponent(BaseComponent):
    """Arm Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(ArmComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        bicepGuideCtrl = NullControl('bicepGuideCtrl')
        bicepGuideCtrl.xfo.tr = Vec3(5.0, 20.0, 0.0)
        bicepGuideCtrl.setColor("yellow")
        self.addChild(bicepGuideCtrl)

        forearmGuideCtrl = NullControl('forearmGuideCtrl')
        forearmGuideCtrl.xfo.tr = Vec3(8.5, 16.4, -2.5)
        forearmGuideCtrl.setColor("yellow")
        self.addChild(forearmGuideCtrl)

        wristGuideCtrl = NullControl('wristGuideCtrl')
        wristGuideCtrl.xfo.tr = Vec3(12.0, 12.9, 0.0)
        wristGuideCtrl.setColor("yellow")
        self.addChild(wristGuideCtrl)


        # Setup component Xfo I/O's
        clavicleEndInput = Locator('clavicleEnd')
        armEndOutput = Locator('armEnd')

        # Setup componnent Attribute I/O's
        armFollowBodyInputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint outputs
        armEndOutputConstraint = PoseConstraint('_'.join([armEndOutput.getName(), 'To', wristGuideCtrl.getName()]))
        armEndOutputConstraint.addConstrainer(wristGuideCtrl)
        armEndOutput.addConstraint(armEndOutputConstraint)

        # Add Xfo I/O's
        self.addInput(clavicleEndInput)
        self.addOutput(armEndOutput)

        # Add Attribute I/O's
        self.addInput(armFollowBodyInputAttr)


    def buildRig(self, parent):

        # component = super(ArmComponent, self).buildRig()
        component = BaseComponent(self.getName(), parent, self.getSide())

        # Setup component attributes
        component.addAttribute(FloatAttribute("bone1Len", 1.0, minValue=0.0, maxValue=100.0))
        component.addAttribute(FloatAttribute("bone2Len", 1.0, minValue=0.0, maxValue=100.0))
        component.addAttribute(FloatAttribute("fkik", 1.0, minValue=0.0, maxValue=1.0))
        component.addAttribute(FloatAttribute("softDist", 0.5, minValue=0.0, maxValue=1.0))
        component.addAttribute(BoolAttribute("softIK", True))
        component.addAttribute(BoolAttribute("stretch", True))
        component.addAttribute(FloatAttribute("stretchBlend", 1.0, minValue=0.0, maxValue=1.0))
        component.addAttribute(StringAttribute("Side", self.side))
        component.addAttribute(BoolAttribute("toggleDebugging", True))

        bicepGuideCtrl = self.getChildByName('bicepGuideCtrl')
        forearmGuideCtrl = self.getChildByName('forearmGuideCtrl')
        wristGuideCtrl = self.getChildByName('wristGuideCtrl')


        # ===================================================================
        # Process data from guide / json data to calculate xfos for objects.
        # ===================================================================


        # Add Rig Controls
        bicepFKCtrl = SquareControl('bicepFKCtrl', parent=self)
        bicepFKCtrl.xfo = bicepGuideCtrl.xfo
        self.addChild(bicepFKCtrl)

        forearmFKCtrl = NullControl('forearmFKCtrl', parent=self)
        forearmFKCtrl.xfo = forearmGuideCtrl.xfo
        self.addChild(forearmFKCtrl)

        wristIKCtrl = CircleControl('wristIKCtrl', parent=self)
        wristIKCtrl.xfo = wristGuideCtrl.xfo
        self.addChild(wristIKCtrl)

        return container


if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    
    saver = KrakenFactory()
    jsonData = armLeft.jsonEncode(saver)
    print json.dumps(jsonData, indent=2)

    loader = KrakenFactory()
