
from Kraken.core.objects.Attributes import FloatAttribute
from Kraken.core.objects.Attributes import BoolAttribute
from Kraken.core.objects.Attributes import StringAttribute
from Kraken.core.objects.Component import Component


class ArmComponent(Component):
    """docstring for ArmComponent"""
    def __init__(self, name, parent=None):
        super(ArmComponent, self).__init__(name, parent)


    self.addAttribute(FloatAttribute("bone1Len", 1.0, minValue=0.0, maxValue=100.0))
    self.addAttribute(FloatAttribute("bone2Len", 1.0, minValue=0.0, maxValue=100.0))
    self.addAttribute(FloatAttribute("fkik", 1.0, minValue=0.0, maxValue=1.0))
    self.addAttribute(FloatAttribute("softDist", 0.5, minValue=0.0, maxValue=1.0))
    self.addAttribute(BoolAttribute("softIK", True))
    self.addAttribute(BoolAttribute("stretch", True))
    self.addAttribute(FloatAttribute("stretchBlend", 1.0, minValue=0.0, maxValue=1.0))
    self.addAttribute(StringAttribute("Side", self.side))
    self.addAttribute(BoolAttribute("toggleDebugging", True))