from kraken.core.maths.vec import Vec3

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.sphere_control import SphereControl


class LegComponent(BaseComponent):
    """Leg Component"""

    def __init__(self, name, parent=None, side='M'):
        super(LegComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        femurGuideCtrl = SphereControl('femurGuideCtrl')
        femurGuideCtrl.xfo.tr = Vec3(2.0, 10.0, 0.0)
        femurGuideCtrl.setColor("greenBright")
        self.addChild(femurGuideCtrl)

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
        pass


if __name__ == "__main__":
    legLeft = LegComponent("myArm", side='L')
    print legLeft.getNumChildren()