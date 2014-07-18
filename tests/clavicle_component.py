from kraken.core.maths import *

from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.components.component_inputXfo import ComponentInputXfo
from kraken.core.objects.components.component_inputAttribute import ComponentInputAttr
from kraken.core.objects.components.component_outputXfo import ComponentOutputXfo
from kraken.core.objects.components.component_outputAttribute import ComponentOutputAttr

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

        # Setup Component Inputs and Outputs
        spineEndInput = ComponentInputXfo('spineEnd')
        clavicleEndOutput = ComponentOutputXfo('clavicleEnd')

        self.addInput(spineEndInput)
        self.addOutput(clavicleEndOutput)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        clavicleOriginGuideCtrl = SphereControl('clavicleOriginGuideCtrl')
        clavicleOriginGuideCtrl.xfo.tr = Vec3(1.0, 18.0, 1.0)
        self.addChild(clavicleOriginGuideCtrl)

        clavicleInsertGuideCtrl = CircleControl('clavicleInsertGuideCtrl')
        clavicleInsertGuideCtrl.xfo.tr = Vec3(5.0, 20.0, 0.0)
        self.addChild(clavicleInsertGuideCtrl)


    def buildRig(self, parent):

        # component = super(ClavicleComponent, self).buildRig()
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
    armLeft = ClavicleComponent("myClavicle", side='L')
    print armLeft.getNumChildren()