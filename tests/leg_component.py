from kraken.core.maths import *

from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.components.base_component import BaseComponent

from kraken.core.objects.locator import Locator

from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.circle_control import CircleControl
from kraken.core.objects.controls.square_control import SquareControl
from kraken.core.objects.controls.sphere_control import SphereControl
from kraken.core.objects.controls.null_control import NullControl


class LegComponent(BaseComponent):
    """Leg Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(LegComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        femureGuideCtrl = SphereControl('femureGuideCtrl')
        femureGuideCtrl.xfo.tr = Vec3(2.0, 10.0, 0.0)
        femureGuideCtrl.setColor("greenBright")
        self.addChild(femureGuideCtrl)

        shinGuideCtrl = SphereControl('shinGuideCtrl')
        shinGuideCtrl.xfo.tr = Vec3(2.0, 5.5, 1)
        shinGuideCtrl.setColor("greenBright")
        self.addChild(shinGuideCtrl)

        ankleGuideCtrl = SphereControl('ankleGuideCtrl')
        ankleGuideCtrl.xfo.tr = Vec3(2.0, 1.0, 0.0)
        ankleGuideCtrl.setColor("greenBright")
        self.addChild(ankleGuideCtrl)


        # Setup component Xfo I/O's
        legPelvisInput = Locator('pelvisInput')
        legEndOutput = Locator('legEnd')

        # Setup componnent Attribute I/O's
        legFollowPelvisInputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint outputs
        legEndOutputConstraint = PoseConstraint('_'.join([legEndOutput.getName(), 'To', ankleGuideCtrl.getName()]))
        legEndOutputConstraint.addConstrainer(ankleGuideCtrl)
        legEndOutput.addConstraint(legEndOutputConstraint)

        # Add Xfo I/O's
        self.addInput(legPelvisInput)
        self.addOutput(legEndOutput)

        # Add Attribute I/O's
        self.addInput(legFollowPelvisInputAttr)


    def buildRig(self, parent):

        # component = super(LegComponent, self).buildRig()
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

        femureGuideCtrl = self.getChildByName('femureGuideCtrl')
        shinGuideCtrl = self.getChildByName('shinGuideCtrl')
        ankleGuideCtrl = self.getChildByName('ankleGuideCtrl')


        # ===================================================================
        # Process data from guide / json data to calculate xfos for objects.
        # ===================================================================


        # Add Rig Controls
        bicepFKCtrl = SquareControl('bicepFKCtrl', parent=self)
        bicepFKCtrl.xfo = femureGuideCtrl.xfo
        self.addChild(bicepFKCtrl)

        forearmFKCtrl = NullControl('forearmFKCtrl', parent=self)
        forearmFKCtrl.xfo = shinGuideCtrl.xfo
        self.addChild(forearmFKCtrl)

        wristIKCtrl = CircleControl('wristIKCtrl', parent=self)
        wristIKCtrl.xfo = ankleGuideCtrl.xfo
        self.addChild(wristIKCtrl)

        return container


if __name__ == "__main__":
    armLeft = LegComponent("myArm", side='L')
    print armLeft.getNumChildren()