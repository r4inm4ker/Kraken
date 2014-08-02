from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer

from arm_component import ArmComponent
from clavicle_component import ClavicleComponent
from leg_component import LegComponent
from spine_component import SpineComponent
from neck_component import NeckComponent
from head_component import HeadComponent


class Rig(Container):
    """Test Arm Component"""

    def __init__(self, name):
        super(Rig, self).__init__(name)

        # Add rig layers
        deformerLayer = Layer('deformers', parent=self)
        controlsLayer = Layer('controls', parent=self)
        geometryLayer = Layer('geometry', parent=self)

        # Add Components to Layers
        spineComponent = SpineComponent("spine", controlsLayer)
        neckComponent = NeckComponent("neck", controlsLayer)
        headComponent = HeadComponent("head", controlsLayer)
        clavicleLeftComponent = ClavicleComponent("clavicle", controlsLayer, side="L")
        clavicleRightComponent = ClavicleComponent("clavicle", controlsLayer, side="R")
        armLeftComponent = ArmComponent("arm", controlsLayer, side="L")
        armRightComponent = ArmComponent("arm", controlsLayer, side="R")
        legLeftComponent = LegComponent("leg", controlsLayer, side="L")
        legRightComponent = LegComponent("leg", controlsLayer, side="R")

        # Neck to Spine
        spineEndOutput = spineComponent.getOutputByName('spineEnd')
        neckSpineEndInput = neckComponent.getInputByName('neckBase')
        neckSpineEndInput.setSource(spineEndOutput.getTarget())

        # Head to Neck
        neckEndOutput = neckComponent.getOutputByName('neckEnd')
        headBaseInput = headComponent.getInputByName('headBase')
        headBaseInput.setSource(neckEndOutput.getTarget())

        # Clavicle to Spine
        spineEndOutput = spineComponent.getOutputByName('spineEnd')
        clavicleLeftSpineEndInput = clavicleLeftComponent.getInputByName('spineEnd')
        clavicleLeftSpineEndInput.setSource(spineEndOutput.getTarget())
        clavicleRightSpineEndInput = clavicleRightComponent.getInputByName('spineEnd')
        clavicleRightSpineEndInput.setSource(spineEndOutput.getTarget())

        # Arm To Clavicle Connections
        clavicleLeftEndOutput = clavicleLeftComponent.getOutputByName('clavicleEnd')
        armLeftClavicleEndInput = armLeftComponent.getInputByName('clavicleEnd')
        armLeftClavicleEndInput.setSource(clavicleLeftEndOutput.getTarget())
        clavicleRightEndOutput = clavicleRightComponent.getOutputByName('clavicleEnd')
        armRightClavicleEndInput = armRightComponent.getInputByName('clavicleEnd')
        armRightClavicleEndInput.setSource(clavicleRightEndOutput.getTarget())

        # Leg To Pelvis Connections
        spineBaseOutput = spineComponent.getOutputByName('spineBase')
        legLeftPelvisInput = legLeftComponent.getInputByName('pelvisInput')
        legLeftPelvisInput.setSource(spineBaseOutput.getTarget())
        clavicleRightEndOutput = spineComponent.getOutputByName('spineBase')
        legRightPelvisInput = legRightComponent.getInputByName('pelvisInput')
        legRightPelvisInput.setSource(clavicleRightEndOutput.getTarget())

        # Arm Attributes to Clavicle
        # clavicleLeftFollowBodyOutput = clavicleLeftComponent.getOutputByName('followBody')
        # armLeftFollowBodyInput = armLeftComponent.getInputByName('followBody')
        # armLeftFollowBodyInput.setSource(clavicleLeftFollowBodyOutput.getTarget())
        # clavicleRightFollowBodyOutput = clavicleRightComponent.getOutputByName('followBody')
        # armRightFollowBodyInput = armRightComponent.getInputByName('followBody')
        # armRightFollowBodyInput.setSource(clavicleRightFollowBodyOutput.getTarget())



if __name__ == "__main__":
    bobRig = Rig("char_bob")