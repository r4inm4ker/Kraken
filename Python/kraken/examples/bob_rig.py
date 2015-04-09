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

from kraken.core.maths import Vec3, Quat

from kraken.core.profiler import Profiler

class BobRig(Container):
    """Test Arm Component"""

    def __init__(self, name):
        Profiler.getInstance().push("Construct BobRig:" + name)
        super(BobRig, self).__init__(name)

        # Add rig layers
        deformersLayer = Layer('deformers', parent=self)
        controlsLayer = Layer('controls', parent=self)
        geometryLayer = Layer('geometry', parent=self)

        # Add Components to Layers
        spineComponent = SpineComponent("spine", controlsLayer, data={
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 4
        })
        neckComponent = NeckComponent("neck", controlsLayer, data={
            'neckPosition': Vec3(0.0, 16.5572, -0.6915),
            'neckUpVOffset': Vec3(0.0, 0.0, -1.0),
            'neckEndPosition': Vec3(0.0, 17.4756, -0.421)
        })
        headComponent = HeadComponent("head", controlsLayer, data={
            "headPosition": Vec3(0.0, 17.4756, -0.421),
            "headEndPosition": Vec3(0.0, 19.5, -0.421),
            "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
            "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
            "jawPosition": Vec3(0.0, 17.613, -0.2731)
        })
        clavicleLeftComponent = ClavicleComponent("clavicle", controlsLayer, data={
            "name": "L_ClavicleComponent",
            "location": "L",
            "claviclePosition": Vec3(0.1322, 15.403, -0.5723),
            "clavicleUpVOffset": Vec3(0.0, 1.0, 0.0),
            "clavicleEndPosition": Vec3(2.27, 15.295, -0.753)
        })
        clavicleRightComponent = ClavicleComponent("clavicle", controlsLayer, data={
            "name":"R_ClavicleComponent",
            "location": "R",
            "claviclePosition": Vec3(-0.1322, 15.403, -0.5723),
            "clavicleUpVOffset": Vec3(0.0, 1.0, 0.0),
            "clavicleEndPosition": Vec3(-2.27, 15.295, -0.753)
        })
        armLeftComponent = ArmComponent("arm", controlsLayer, data={ 
            "location":"L",
            "bicepPosition": Vec3(2.27, 15.295, -0.753),
            "forearmPosition": Vec3(5.039, 13.56, -0.859),
            "wristPosition": Vec3(7.1886, 12.2819, 0.4906),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
            } )
        armRightComponent = ArmComponent("arm", controlsLayer, data={ 
            "location":"R",
            "bicepPosition": Vec3(-2.27, 15.295, -0.753),
            "forearmPosition": Vec3(-5.039, 13.56, -0.859),
            "wristPosition": Vec3(-7.1886, 12.2819, 0.4906),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
            } )
        handLeftComponent = HandComponent("hand", controlsLayer, data={
            "name":"L_HandComponent",
            "location": "L",
            "handQuat": Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331),
            "handPos": Vec3(7.1886, 12.2819, 0.4906)
        } )
        handRightComponent = HandComponent("hand", controlsLayer, data={
            "name":"R_HandComponent",
            "location": "R",
            "handQuat": Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623),
            "handPos": Vec3(-7.1886, 12.2819, 0.4906)
        } )
        legLeftComponent = LegComponent("leg", controlsLayer, data={
            "name":"L_LegComponent",
            "location": "L",
            "femurPosition": Vec3(0.9811, 9.769, -0.4572),
            "kneePosition": Vec3(1.4488, 5.4418, -0.5348),
            "anklePosition": Vec3(1.841, 1.1516, -1.237)
        } )
        legRightComponent = LegComponent("leg", controlsLayer, data={
            "name":"R_LegComponent",
            "location": "R",
            "femurPosition": Vec3(-0.9811, 9.769, -0.4572),
            "kneePosition": Vec3(-1.4488, 5.4418, -0.5348),
            "anklePosition": Vec3(-1.841, 1.1516, -1.237)
        } )
        footLeftComponent = FootComponent("foot", controlsLayer, data={
            "name":"L_FootComponent",
            "location": "L",
            "footQuat": Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190),
            "footPos": Vec3(1.841, 1.1516, -1.237)
        } )
        footRightComponent = FootComponent("foot", controlsLayer, data={
            "name":"R_FootComponent",
            "location": "R",
            "footQuat": Quat(Vec3(0.5695, -0.6377, 0.4190), 0.3053),
            "footPos": Vec3(-1.841, 1.1516, -1.237)
        } )

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
        legRightPelvisInput = legRightComponent.getInputByName('pelvisInput')
        legRightPelvisInput.setSource(spineBaseOutput.getTarget())

        # Foot To Arm Connections
        legLeftEndOutput = legLeftComponent.getOutputByName('legEndXfo')
        footLeftEndInput = footLeftComponent.getInputByName('legEndXfo')
        footLeftEndInput.setSource(legLeftEndOutput.getTarget())
        legLeftEndPosOutput = legLeftComponent.getOutputByName('legEndPos')
        footLeftEndPosInput = footLeftComponent.getInputByName('legEndPos')
        footLeftEndPosInput.setSource(legLeftEndPosOutput.getTarget())

        legRightEndOutput = legRightComponent.getOutputByName('legEndXfo')
        footRightEndInput = footRightComponent.getInputByName('legEndXfo')
        footRightEndInput.setSource(legRightEndOutput.getTarget())
        legRightEndPosOutput = legRightComponent.getOutputByName('legEndPos')
        footRightEndPosInput = footRightComponent.getInputByName('legEndPos')
        footRightEndPosInput.setSource(legRightEndPosOutput.getTarget())

        # Arm Attributes to Clavicle
        # clavicleLeftFollowBodyOutput = clavicleLeftComponent.getOutputByName('followBody')
        # armLeftFollowBodyInput = armLeftComponent.getInputByName('followBody')
        # armLeftFollowBodyInput.setSource(clavicleLeftFollowBodyOutput.getTarget())
        # clavicleRightFollowBodyOutput = clavicleRightComponent.getOutputByName('followBody')
        # armRightFollowBodyInput = armRightComponent.getInputByName('followBody')
        # armRightFollowBodyInput.setSource(clavicleRightFollowBodyOutput.getTarget())

        Profiler.getInstance().pop()
