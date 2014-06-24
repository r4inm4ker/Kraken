from kraken.core.maths import *
from kraken.core.objects.Attributes import FloatAttribute
from kraken.core.objects.Attributes import BoolAttribute
from kraken.core.objects.Attributes import StringAttribute
from kraken.core.objects.Component import Component


class ArmComponent(Component):
    """Arm Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(ArmComponent, self).__init__(name, parent, side)

        self.addAttribute(FloatAttribute("bone1Len", 1.0, minValue=0.0, maxValue=100.0))
        self.addAttribute(FloatAttribute("bone2Len", 1.0, minValue=0.0, maxValue=100.0))
        self.addAttribute(FloatAttribute("fkik", 1.0, minValue=0.0, maxValue=1.0))
        self.addAttribute(FloatAttribute("softDist", 0.5, minValue=0.0, maxValue=1.0))
        self.addAttribute(BoolAttribute("softIK", True))
        self.addAttribute(BoolAttribute("stretch", True))
        self.addAttribute(FloatAttribute("stretchBlend", 1.0, minValue=0.0, maxValue=1.0))
        self.addAttribute(StringAttribute("Side", self.side))
        self.addAttribute(BoolAttribute("toggleDebugging", True))

        bicepXfo = self.addComponentXfo()
        forearmXfo = self.addComponentXfo()
        wristXfo = self.addComponentXfo()


if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    print armLeft.getComponentXfoByIndex(2)