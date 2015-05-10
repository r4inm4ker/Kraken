from kraken.core.maths import Vec3, Quat, Xfo

from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer

from kraken.examples.hand_component import HandComponent
from kraken.examples.head_component import HeadComponent
from kraken.examples.clavicle_component import ClavicleComponentGuide, ClavicleComponent
from kraken.examples.arm_component import ArmComponentGuide, ArmComponent
from kraken.examples.leg_component import LegComponentGuide, LegComponent
from kraken.examples.foot_component import FootComponentGuide, FootComponent
from kraken.examples.spine_component import SpineComponent
from kraken.examples.neck_component import NeckComponentGuide, NeckComponent

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class BobRig(Container):
    """Test Arm Component"""

    def __init__(self, name):

        Profiler.getInstance().push("Construct BobRig:" + name)
        super(BobRig, self).__init__(name)

        # Add Components to Layers
        spineComponent = SpineComponent("spine", self)
        spineComponent.loadData(data={
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 4
        })

        neckComponentGuide = NeckComponentGuide(data={
            "location": "M",
            "neckPosition": Vec3(0.0, 16.5572, -0.6915),
            "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
        })

        neckComponent = NeckComponent("neck", self)
        neckComponent.loadData(data=neckComponentGuide.getGuideData())

        headComponent = HeadComponent("head", self)
        headComponent.loadData(data={
            "headPosition": Vec3(0.0, 17.4756, -0.421),
            "headEndPosition": Vec3(0.0, 19.5, -0.421),
            "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
            "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
            "jawPosition": Vec3(0.0, 17.613, -0.2731)
        })

        clavicleLeftComponentGuide = ClavicleComponentGuide("clavicle", data={
            "location": "L",
            "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
        })

        clavicleLeftComponent = ClavicleComponent("clavicle", self)
        clavicleLeftComponent.loadData(data=clavicleLeftComponentGuide.getGuideData())

        clavicleRightComponentGuide = ClavicleComponentGuide("clavicle", data={
            "location": "R",
            "clavicleXfo": Xfo(Vec3(-0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(-2.27, 15.295, -0.753))
        })

        clavicleRightComponent = ClavicleComponent("clavicle", self)
        clavicleRightComponent.loadData(data=clavicleRightComponentGuide.getGuideData())

        armLeftComponentGuide = ArmComponentGuide("arm", data={
            "location":"L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        armLeftComponent = ArmComponent("arm", self)
        armLeftComponent.loadData(data=armLeftComponentGuide.getGuideData())

        armRightComponentGuide = ArmComponentGuide("arm", data={
            "location":"R",
            "bicepXfo": Xfo(Vec3(-2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(-5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(-7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        armRightComponent = ArmComponent("arm", self)
        armRightComponent.loadData(data=armRightComponentGuide.getGuideData() )

        handLeftComponent = HandComponent("hand", self)
        handLeftComponent.loadData(data={
            "name":"L_HandComponent",
            "location": "L",
            "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906), ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
        })

        handRightComponent = HandComponent("hand", self)
        handRightComponent.loadData(data={
            "name":"R_HandComponent",
            "location": "R",
            "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906), ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623)),
        })

        legLeftComponentGuide = LegComponentGuide("leg", data={
            "name":"L_LegComponent",
            "location": "L",
            "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237))
        })

        legLeftComponent = LegComponent("leg", self)
        legLeftComponent.loadData(data= legLeftComponentGuide.getGuideData())

        legRightComponentGuide = LegComponentGuide("leg", data={
            "name":"R_LegComponent",
            "location": "R",
            "femurXfo": Xfo(Vec3(-0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(-1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(-1.841, 1.1516, -1.237))
        })

        legRightComponent = LegComponent("leg", self)
        legRightComponent.loadData(data=legRightComponentGuide.getGuideData() )

        footLeftComponentGuide = FootComponentGuide("foot", data={
            "name":"L_FootComponent",
            "location": "L",
            "footXfo": Xfo(tr=Vec3(1.841, 1.1516, -1.237), ori=Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190))
        })

        footLeftComponent = FootComponent("foot", self)
        footLeftComponent.loadData(data=footLeftComponentGuide.getGuideData() )

        footRightComponentGuide = FootComponentGuide("foot", data={
            "name":"R_FootComponent",
            "location": "R",
            "footXfo": Xfo(tr= Vec3(-1.841, 1.1516, -1.237), ori=Quat(Vec3(0.5695, -0.6377, 0.4190), 0.3053))
        })

        footRightComponent = FootComponent("foot", self)
        footRightComponent.loadData(data=footRightComponentGuide.getGuideData() )

        # Neck to Spine
        spineEndOutput = spineComponent.getOutputByName('spineEnd')
        neckSpineEndInput = neckComponent.getInputByName('neckBase')
        neckSpineEndInput.setConnection(spineEndOutput)

        # Head to Neck
        neckEndOutput = neckComponent.getOutputByName('neckEnd')
        headBaseInput = headComponent.getInputByName('headBase')
        headBaseInput.setConnection(neckEndOutput)

        # Clavicle to Spine
        spineEndOutput = spineComponent.getOutputByName('spineEnd')
        clavicleLeftSpineEndInput = clavicleLeftComponent.getInputByName('spineEnd')
        clavicleLeftSpineEndInput.setConnection(spineEndOutput)
        clavicleRightSpineEndInput = clavicleRightComponent.getInputByName('spineEnd')
        clavicleRightSpineEndInput.setConnection(spineEndOutput)

        # Hand To Arm Connections
        armLeftEndOutput = armLeftComponent.getOutputByName('armEndXfo')
        handLeftArmEndInput = handLeftComponent.getInputByName('armEndXfo')
        handLeftArmEndInput.setConnection(armLeftEndOutput)
        armLeftEndPosOutput = armLeftComponent.getOutputByName('armEndPos')
        handLeftArmEndPosInput = handLeftComponent.getInputByName('armEndPos')
        handLeftArmEndPosInput.setConnection(armLeftEndPosOutput)

        armLeftDebugOutput = armLeftComponent.getOutputByName('debug')
        handLeftDebugInput = handLeftComponent.getInputByName('debug')
        handLeftDebugInput.setConnection(armLeftDebugOutput)

        armRightEndOutput = armRightComponent.getOutputByName('armEndXfo')
        handRightArmEndInput = handRightComponent.getInputByName('armEndXfo')
        handRightArmEndInput.setConnection(armRightEndOutput)
        armRightEndPosOutput = armRightComponent.getOutputByName('armEndPos')
        handRightArmEndPosInput = handRightComponent.getInputByName('armEndPos')
        handRightArmEndPosInput.setConnection(armRightEndPosOutput)

        armRightDebugOutput = armRightComponent.getOutputByName('debug')
        handRightDebugInput = handRightComponent.getInputByName('debug')
        handRightDebugInput.setConnection(armRightDebugOutput)

        # Arm To Clavicle Connections
        clavicleLeftEndOutput = clavicleLeftComponent.getOutputByName('clavicleEnd')
        armLeftClavicleEndInput = armLeftComponent.getInputByName('clavicleEnd')
        armLeftClavicleEndInput.setConnection(clavicleLeftEndOutput)
        clavicleRightEndOutput = clavicleRightComponent.getOutputByName('clavicleEnd')
        armRightClavicleEndInput = armRightComponent.getInputByName('clavicleEnd')
        armRightClavicleEndInput.setConnection(clavicleRightEndOutput)

        # Leg To Pelvis Connections
        spineBaseOutput = spineComponent.getOutputByName('spineBase')
        legLeftPelvisInput = legLeftComponent.getInputByName('pelvisInput')
        legLeftPelvisInput.setConnection(spineBaseOutput)
        legRightPelvisInput = legRightComponent.getInputByName('pelvisInput')
        legRightPelvisInput.setConnection(spineBaseOutput)

        # Foot To Leg Connections
        legLeftEndOutput = legLeftComponent.getOutputByName('legEndXfo')
        footLeftEndInput = footLeftComponent.getInputByName('legEndXfo')
        footLeftEndInput.setConnection(legLeftEndOutput)
        legLeftEndPosOutput = legLeftComponent.getOutputByName('legEndPos')
        footLeftEndPosInput = footLeftComponent.getInputByName('legEndPos')
        footLeftEndPosInput.setConnection(legLeftEndPosOutput)

        legLeftDebugOutput = legLeftComponent.getOutputByName('debug')
        footLeftDebugInput = footLeftComponent.getInputByName('debug')
        footLeftDebugInput.setConnection(legLeftDebugOutput)

        legRightEndOutput = legRightComponent.getOutputByName('legEndXfo')
        footRightEndInput = footRightComponent.getInputByName('legEndXfo')
        footRightEndInput.setConnection(legRightEndOutput)
        legRightEndPosOutput = legRightComponent.getOutputByName('legEndPos')
        footRightEndPosInput = footRightComponent.getInputByName('legEndPos')
        footRightEndPosInput.setConnection(legRightEndPosOutput)

        legLeftDebugOutput = legRightComponent.getOutputByName('debug')
        footLeftDebugInput = footRightComponent.getInputByName('debug')
        footLeftDebugInput.setConnection(legLeftDebugOutput)

        # Arm Attributes to Clavicle
        # clavicleLeftFollowBodyOutput = clavicleLeftComponent.getOutputByName('followBody')
        # armLeftFollowBodyInput = armLeftComponent.getInputByName('followBody')
        # armLeftFollowBodyInput.setConnection(clavicleLeftFollowBodyOutput)
        # clavicleRightFollowBodyOutput = clavicleRightComponent.getOutputByName('followBody')
        # armRightFollowBodyInput = armRightComponent.getInputByName('followBody')
        # armRightFollowBodyInput.setConnection(clavicleRightFollowBodyOutput)

        Profiler.getInstance().pop()
