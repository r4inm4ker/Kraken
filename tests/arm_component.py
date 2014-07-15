from kraken.core.maths import *
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute
from kraken.core.objects.component import BaseComponent
from kraken.core.objects.controls.cube_control  import CubeControl
from kraken.core.objects.controls.circle_control  import  CircleControl
from kraken.core.objects.controls.square_control  import  SquareControl
from kraken.core.objects.controls.null_control  import  NullControl


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

        # Setup Xfos
        bicepXfo = Xfo()
        bicepXfo.tr = Vec3(5.0, 20.0, 0.0)

        forearmXfo = Xfo()
        forearmXfo.tr = Vec3(8.535533905932736, 16.46446609406726, -2.5)

        wristXfo = Xfo()
        wristXfo.tr = Vec3(12.071067811865474, 12.92893218813452, 0.0)

        # Add xfos
        self.addXfo("bicep", bicepXfo)
        self.addXfo("forearm", forearmXfo)
        self.addXfo("wrist", wristXfo)

        # Add Guide Controls
        bicepGuideCtrl = NullControl('bicepGuideCtrl')
        bicepGuideCtrl.setFlag("guide")
        self.addChild(bicepGuideCtrl)

        forearmGuideCtrl = NullControl('forearmGuideCtrl')
        forearmGuideCtrl.setFlag("guide")
        self.addChild(forearmGuideCtrl)

        wristGuideCtrl = NullControl('wristGuideCtrl')
        wristGuideCtrl.setFlag("guide")
        self.addChild(wristGuideCtrl)

        # Guide Splice Op Code
        guideSpliceOps = []

        guideSpliceCode = """
          drawLine(bicep.tr, forearm.tr, Color(1.0, 0.0, 0.0));
          drawLine(forearm.tr, wrist.tr, Color(1.0, 0.0, 0.0));

        """

    def buildRig(self):

        

        # # Add Rig Controls
        # bicepFKCtrl = SquareControl('bicepFKCtrl', parent=self)
        # bicepFKCtrl.xfo = bicepXfo
        # self.addChild(bicepFKCtrl)

        # forearmFKCtrl = NullControl('forearmFKCtrl', parent=self)
        # forearmFKCtrl.xfo = forearmXfo
        # self.addChild(forearmFKCtrl)

        # wristIKCtrl = CircleControl('wristIKCtrl', parent=self)
        # wristIKCtrl.xfo = wristXfo
        # self.addChild(wristIKCtrl)

        # componentSpliceCode = """require Math;"""

        return container


if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    print armLeft.getXfo("bicep")