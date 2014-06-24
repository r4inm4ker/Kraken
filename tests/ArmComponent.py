from kraken.core.maths import *
from kraken.core.objects.Attributes.FloatAttribute import FloatAttribute
from kraken.core.objects.Attributes.BoolAttribute import BoolAttribute
from kraken.core.objects.Attributes.StringAttribute import StringAttribute
from kraken.core.objects.Component import BaseComponent


class ArmComponent(BaseComponent):
    """Arm Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(ArmComponent, self).__init__(name, parent, side)

        # Setup component attributes
        self.addAttribute(FloatAttribute("bone1Len", 1.0, minValue=0.0, maxValue=100.0))
        self.addAttribute(FloatAttribute("bone2Len", 1.0, minValue=0.0, maxValue=100.0))
        self.addAttribute(FloatAttribute("fkik", 1.0, minValue=0.0, maxValue=1.0))
        self.addAttribute(FloatAttribute("softDist", 0.5, minValue=0.0, maxValue=1.0))
        self.addAttribute(BoolAttribute("softIK", True))
        self.addAttribute(BoolAttribute("stretch", True))
        self.addAttribute(FloatAttribute("stretchBlend", 1.0, minValue=0.0, maxValue=1.0))
        self.addAttribute(StringAttribute("Side", self.side))
        self.addAttribute(BoolAttribute("toggleDebugging", True))

        # Setup component xfos
        bicepXfo = self.addComponentXfo()
        forearmXfo = self.addComponentXfo()
        wristXfo = self.addComponentXfo()

        # Set default component xfo values
        bicepXfo.tr = Vec3(5.0, 20.0, 0.0)
        forearmXfo.tr = Vec3(8.535533905932736, 16.46446609406726, -2.5)
        wristXfo.tr = Vec3(12.071067811865474, 12.92893218813452, 0.0)



if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    print armLeft.getComponentXfoByIndex(2)