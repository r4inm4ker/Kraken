from kraken.core.maths.vec import Vec3

from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.components.base_component import BaseComponent

from kraken.core.objects.locator import Locator

from kraken.core.objects.controls.cube_control  import CubeControl
from kraken.core.objects.controls.circle_control  import  CircleControl
from kraken.core.objects.controls.sphere_control  import  SphereControl
from kraken.core.objects.controls.pin_control  import  PinControl
from kraken.core.objects.controls.square_control  import  SquareControl
from kraken.core.objects.controls.null_control  import  NullControl


class ClavicleComponent(BaseComponent):
    """Arm Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(ClavicleComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        clavicleOriginGuideCtrl = CircleControl('clavicleOriginGuideCtrl')
        clavicleOriginGuideCtrl.xfo.tr = Vec3(1.0, 18.0, 1.0)
        clavicleOriginGuideCtrl.setColor("greenBright")
        self.addChild(clavicleOriginGuideCtrl)

        clavicleInsertGuideCtrl = CircleControl('clavicleInsertGuideCtrl')
        clavicleInsertGuideCtrl.xfo.tr = Vec3(5.0, 20.0, 0.0)
        clavicleInsertGuideCtrl.setColor("greenBright")
        self.addChild(clavicleInsertGuideCtrl)

        # Setup Component Xfo I/O's
        spineEndInput = Locator('spineEnd')
        clavicleEndOutput = Locator('clavicleEnd')

        # Setup componnent Attribute I/O's
        armFollowBodyOutputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint outputs
        clavicleEndConstraint = PoseConstraint('_'.join([clavicleEndOutput.getName(), 'To', clavicleInsertGuideCtrl.getName()]))
        clavicleEndConstraint.addConstrainer(clavicleInsertGuideCtrl)
        clavicleEndOutput.addConstraint(clavicleEndConstraint)

        # Add Xfo I/O's
        self.addInput(spineEndInput)
        self.addOutput(clavicleEndOutput)

        self.addOutput(armFollowBodyOutputAttr)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    armLeft = ClavicleComponent("myClavicle", side='L')
    print armLeft.getNumChildren()