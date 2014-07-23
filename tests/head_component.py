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
from kraken.core.objects.controls.sphere_control import SphereControl
from kraken.core.objects.controls.pin_control import PinControl
from kraken.core.objects.controls.square_control import SquareControl
from kraken.core.objects.controls.null_control import NullControl


class HeadComponent(BaseComponent):
    """Head Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(HeadComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        headGuideCtrl = CubeControl('headGuideCtrl')
        headGuideCtrl.xfo.tr = Vec3(0.0, 22.0, 0.0)
        headGuideCtrl.setColor("yellow")
        self.addChild(headGuideCtrl)

        headEndGuideCtrl = CubeControl('headEndGuideCtrl')
        headEndGuideCtrl.xfo.tr = Vec3(0.0, 25.0, 0.0)
        headEndGuideCtrl.setColor("yellow")
        headGuideCtrl.addChild(headEndGuideCtrl)



        eyeLeftGuideCtrl = SphereControl('eyeLeftGuideCtrl')
        eyeLeftGuideCtrl.xfo.tr = Vec3(1.0, 24.0, 1.5)
        eyeLeftGuideCtrl.setColor("blueMedium")
        headGuideCtrl.addChild(eyeLeftGuideCtrl)

        eyeRightGuideCtrl = SphereControl('eyeRightGuideCtrl')
        eyeRightGuideCtrl.xfo.tr = Vec3(-1.0, 24.0, 1.5)
        eyeRightGuideCtrl.setColor("blueMedium")
        headGuideCtrl.addChild(eyeRightGuideCtrl)



        jawGuideCtrl = CubeControl('jawGuideCtrl')
        jawGuideCtrl.xfo.tr = Vec3(0.0, 23.0, 0.5)
        jawGuideCtrl.setColor("orange")
        self.addChild(jawGuideCtrl)

        jawEndGuideCtrl = CubeControl('jawEndGuideCtrl')
        jawEndGuideCtrl.xfo.tr = Vec3(0.0, 21.5, 2.5)
        jawEndGuideCtrl.setColor("orange")
        jawGuideCtrl.addChild(jawEndGuideCtrl)

        # Setup Component Xfo I/O's
        spineEndInput = Locator('spineEnd')
        clavicleEndOutput = Locator('clavicleEnd')

        # Setup componnent Attribute I/O's
        armFollowBodyOutputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint outputs
        clavicleEndConstraint = PoseConstraint('_'.join([clavicleEndOutput.getName(), 'To', jawGuideCtrl.getName()]))
        clavicleEndConstraint.addConstrainer(jawGuideCtrl)
        clavicleEndOutput.addConstraint(clavicleEndConstraint)

        # Add Xfo I/O's
        self.addInput(spineEndInput)
        self.addOutput(clavicleEndOutput)

        self.addOutput(armFollowBodyOutputAttr)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    head = HeadComponent("myClavicle")
    print head.getNumChildren()