
from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer
from arm_component import ArmComponent

class ArmRig(Container):
    """Test Arm Component"""

    def __init__(self, name):
        super(ArmRig, self).__init__(name)

        # Add rig layers
        armatureLayer = Layer('armature', parent=self)
        self.addChild(armatureLayer)

        controlsLayer = Layer('controls', parent=self)
        self.addChild(controlsLayer)

        geometryLayer = Layer('geometry', parent=self)
        self.addChild(geometryLayer)

        # Add Components to Layers
        controlsLayer.addComponent(ArmComponent("arm", self, side="L"))


if __name__ == "__main__":
    armRig = ArmRig("myArm")