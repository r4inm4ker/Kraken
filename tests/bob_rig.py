from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer

from arm_component import ArmComponent
from clavicle_component import ClavicleComponent
from leg_component import LegComponent
from spine_component import SpineComponent
from head_component import HeadComponent


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
        spineComponent = SpineComponent("spine", self)
        headComponent = HeadComponent("head", self)
        clavicleLeftComponent = ClavicleComponent("clavicleLeft", self, side="L")
        armLeftComponent = ArmComponent("armLeft", self, side="L")
        legLeftComponent = LegComponent("legLeft", self, side="L")

        controlsLayer.addComponent(spineComponent)
        controlsLayer.addComponent(headComponent)
        controlsLayer.addComponent(clavicleLeftComponent)
        controlsLayer.addComponent(armLeftComponent)
        controlsLayer.addComponent(legLeftComponent)

        # Create component connections
        clavicleEndOutput = clavicleLeftComponent.getOutputByName('clavicleEnd')
        armClavicleEndInput = armLeftComponent.getInputByName('clavicleEnd')
        armClavicleEndInput.setSource(clavicleEndOutput.getTarget())

        clavicleFollowBodyOutput = clavicleLeftComponent.getOutputByName('followBody')
        armFollowBodyInput = armLeftComponent.getInputByName('followBody')
        armFollowBodyInput.setSource(clavicleFollowBodyOutput.getTarget())



if __name__ == "__main__":
    bobRig = Rig("char_bob")