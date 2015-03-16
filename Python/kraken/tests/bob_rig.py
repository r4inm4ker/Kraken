from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer
from kraken.helpers.utility_methods import logHierarchy

from arm_component import ArmComponent
from hand_component import HandComponent
from clavicle_component import ClavicleComponent
from leg_component import LegComponent
from foot_component import FootComponent
from spine_component import SpineComponent
from neck_component import NeckComponent
from head_component import HeadComponent

from kraken.core.profiler import Profiler

class Rig(Container):
    """Test Arm Component"""

    def __init__(self, name):
        Profiler.getInstance().push("Construct BobRig:" + name)
        super(Rig, self).__init__(name)

        # Add rig layers
        deformerLayer = Layer('deformers', parent=self)
        controlsLayer = Layer('controls', parent=self)
        geometryLayer = Layer('geometry', parent=self)

        # Add Components to Layers
        spineComponent = SpineComponent("spine", controlsLayer)
        neckComponent = NeckComponent("neck", controlsLayer)
        headComponent = HeadComponent("head", controlsLayer)
        clavicleLeftComponent = ClavicleComponent("clavicle", controlsLayer, location="L")
        clavicleRightComponent = ClavicleComponent("clavicle", controlsLayer, location="R")
        armLeftComponent = ArmComponent("arm", controlsLayer, location="L")
        armRightComponent = ArmComponent("arm", controlsLayer, location="R")
        handLeftComponent = HandComponent("hand", controlsLayer, location="L")
        handRightComponent = HandComponent("hand", controlsLayer, location="R")
        legLeftComponent = LegComponent("leg", controlsLayer, location="L")
        legRightComponent = LegComponent("leg", controlsLayer, location="R")
        footLeftComponent = FootComponent("foot", controlsLayer, location="L")
        footRightComponent = FootComponent("foot", controlsLayer, location="R")

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

        # Hand To Arm Connections
        armLeftEndOutput = armLeftComponent.getOutputByName('armEndXfo')
        handLeftArmEndInput = handLeftComponent.getInputByName('armEndXfo')
        handLeftArmEndInput.setSource(armLeftEndOutput.getTarget())
        armLeftEndPosOutput = armLeftComponent.getOutputByName('armEndPos')
        handLeftArmEndPosInput = handLeftComponent.getInputByName('armEndPos')
        handLeftArmEndPosInput.setSource(armLeftEndPosOutput.getTarget())

        armRightEndOutput = armRightComponent.getOutputByName('armEndXfo')
        handRightArmEndInput = handRightComponent.getInputByName('armEndXfo')
        handRightArmEndInput.setSource(armRightEndOutput.getTarget())
        armRightEndPosOutput = armRightComponent.getOutputByName('armEndPos')
        handRightArmEndPosInput = handRightComponent.getInputByName('armEndPos')
        handRightArmEndPosInput.setSource(armRightEndPosOutput.getTarget())

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

        # Foot To Arm Connections
        legLeftEndOutput = legLeftComponent.getOutputByName('legEndXfo')
        footLeftArmEndInput = footLeftComponent.getInputByName('legEndXfo')
        footLeftArmEndInput.setSource(legLeftEndOutput.getTarget())
        legLeftEndPosOutput = legLeftComponent.getOutputByName('legEndPos')
        footLeftArmEndPosInput = footLeftComponent.getInputByName('legEndPos')
        footLeftArmEndPosInput.setSource(legLeftEndPosOutput.getTarget())

        legRightEndOutput = legRightComponent.getOutputByName('legEndXfo')
        footRightArmEndInput = footRightComponent.getInputByName('legEndXfo')
        footRightArmEndInput.setSource(legRightEndOutput.getTarget())
        legRightEndPosOutput = legRightComponent.getOutputByName('legEndPos')
        footRightArmEndPosInput = footRightComponent.getInputByName('legEndPos')
        footRightArmEndPosInput.setSource(legRightEndPosOutput.getTarget())

        # Arm Attributes to Clavicle
        # clavicleLeftFollowBodyOutput = clavicleLeftComponent.getOutputByName('followBody')
        # armLeftFollowBodyInput = armLeftComponent.getInputByName('followBody')
        # armLeftFollowBodyInput.setSource(clavicleLeftFollowBodyOutput.getTarget())
        # clavicleRightFollowBodyOutput = clavicleRightComponent.getOutputByName('followBody')
        # armRightFollowBodyInput = armRightComponent.getInputByName('followBody')
        # armRightFollowBodyInput.setSource(clavicleRightFollowBodyOutput.getTarget())

        Profiler.getInstance().pop()


if __name__ == "__main__":
    bobRig = Rig("char_bob")
    logHierarchy(bobRig)
