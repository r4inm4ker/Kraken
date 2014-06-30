
from kraken.core.objects.container import Container
from arm_component import ArmComponent

class ArmRig(Container):
    """Test Arm Component"""

    def __init__(self, name):
        super(ArmRig, self).__init__(name)

        self.addComponent(ArmComponent("arm", self, side="L"))


if __name__ == "__main__":
    armRig = ArmRig("myArm")
    print armRig.getComponent(0)