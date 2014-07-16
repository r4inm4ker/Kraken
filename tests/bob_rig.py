from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer
from arm_component import ArmComponent
from clavicle_component import ClavicleComponent


class Rig(Container):
    """Test Arm Component"""

    def __init__(self, name):
        super(Rig, self).__init__(name)

        # Add rig layers
        armatureLayer = Layer('armature', parent=self)
        self.addChild(armatureLayer)

        controlsLayer = Layer('controls', parent=self)
        self.addChild(controlsLayer)

        geometryLayer = Layer('geometry', parent=self)
        self.addChild(geometryLayer)

        # Add Components to Layers
        clavicleComponent = ClavicleComponent("clavicle", self, side="L")
        armComponent = ArmComponent("arm", self, side="L")

        controlsLayer.addComponent(clavicleComponent)
        controlsLayer.addComponent(armComponent)

        # Create component connections
        clavicleEndOutput = clavicleComponent.getOutputByName('clavicleEnd')
        armClavicleEndInput = armComponent.getInputByName('clavicleEnd')

        armClavicleEndInput.setConnection(clavicleEndOutput)



if __name__ == "__main__":
    bobRig = Rig("char_bob")