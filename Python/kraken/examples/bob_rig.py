from kraken.core.maths import Vec3, Quat, Xfo

from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer

from kraken.examples.mainSrt_component import MainSrtComponentRig
from kraken.examples.hand_component import HandComponentRig
from kraken.examples.head_component import HeadComponentRig
from kraken.examples.clavicle_component import ClavicleComponentGuide, ClavicleComponentRig
from kraken.examples.arm_component import ArmComponentGuide, ArmComponentRig
from kraken.examples.leg_component import LegComponentGuide, LegComponentRig
from kraken.examples.foot_component import FootComponentGuide, FootComponentRig
from kraken.examples.spine_component import SpineComponentRig
from kraken.examples.pelvis_component import PelvisComponentRig
from kraken.examples.neck_component import NeckComponentGuide, NeckComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class BobRig(Container):
    """Test Arm Component"""

    def __init__(self, name):

        Profiler.getInstance().push("Construct BobRig:" + name)
        super(BobRig, self).__init__(name)

        # Add Components
        mainSrtComponent = MainSrtComponentRig("mainSrt", self)

        spineComponent = SpineComponentRig("spine", self)
        spineComponent.loadData(data={
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 4
        })

        pelvisComponent = PelvisComponentRig('pelvis', self)
        pelvisComponent.loadData(data={
            "pelvisXfo": Xfo(tr=Vec3(0.0, 11.1351, -0.1382))
        })

        neckComponentGuide = NeckComponentGuide(data={
            "location": "M",
            "neckPosition": Vec3(0.0, 16.5572, -0.6915),
            "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
        })

        neckComponent = NeckComponentRig("neck", self)
        neckComponent.loadData(data=neckComponentGuide.getGuideData())

        headComponent = HeadComponentRig("head", self)
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

        clavicleLeftComponent = ClavicleComponentRig("clavicle", self)
        clavicleLeftComponent.loadData(data=clavicleLeftComponentGuide.getGuideData())

        clavicleRightComponentGuide = ClavicleComponentGuide("clavicle", data={
            "location": "R",
            "clavicleXfo": Xfo(Vec3(-0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(-2.27, 15.295, -0.753))
        })

        clavicleRightComponent = ClavicleComponentRig("clavicle", self)
        clavicleRightComponent.loadData(data=clavicleRightComponentGuide.getGuideData())

        armLeftComponentGuide = ArmComponentGuide("arm", data={
            "location":"L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        armLeftComponent = ArmComponentRig("arm", self)
        armLeftComponent.loadData(data=armLeftComponentGuide.getGuideData())

        armRightComponentGuide = ArmComponentGuide("arm", data={
            "location":"R",
            "bicepXfo": Xfo(Vec3(-2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(-5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(-7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        armRightComponent = ArmComponentRig("arm", self)
        armRightComponent.loadData(data=armRightComponentGuide.getGuideData() )

        handLeftComponent = HandComponentRig("hand", self)
        handLeftComponent.loadData(data={
            "name":"L_HandComponent",
            "location": "L",
            "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906), ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
        })

        handRightComponent = HandComponentRig("hand", self)
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

        legLeftComponent = LegComponentRig("leg", self)
        legLeftComponent.loadData(data= legLeftComponentGuide.getGuideData())

        legRightComponentGuide = LegComponentGuide("leg", data={
            "name":"R_LegComponent",
            "location": "R",
            "femurXfo": Xfo(Vec3(-0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(-1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(-1.841, 1.1516, -1.237))
        })

        legRightComponent = LegComponentRig("leg", self)
        legRightComponent.loadData(data=legRightComponentGuide.getGuideData() )

        footLeftComponentGuide = FootComponentGuide("foot", data={
            "name":"L_FootComponent",
            "location": "L",
            "footXfo": Xfo(tr=Vec3(1.841, 1.1516, -1.237), ori=Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190))
        })

        footLeftComponent = FootComponentRig("foot", self)
        footLeftComponent.loadData(data=footLeftComponentGuide.getGuideData() )

        footRightComponentGuide = FootComponentGuide("foot", data={
            "name":"R_FootComponent",
            "location": "R",
            "footXfo": Xfo(tr= Vec3(-1.841, 1.1516, -1.237), ori=Quat(Vec3(0.5695, -0.6377, 0.4190), 0.3053))
        })

        footRightComponent = FootComponentRig("foot", self)
        footRightComponent.loadData(data=footRightComponentGuide.getGuideData() )

        # ============
        # Connections
        # ============
        # Spine to Main SRT
        mainSrtRigScaleOutput = mainSrtComponent.getOutputByName('rigScale')
        mainSrtOffsetOutput = mainSrtComponent.getOutputByName('offset')
        spineInput = spineComponent.getInputByName('mainSrt')
        spineInput.setConnection(mainSrtOffsetOutput)

        spineRigScaleInput = spineComponent.getInputByName('rigScale')
        spineRigScaleInput.setConnection(mainSrtRigScaleOutput)

        # Pelvis to Spine
        spineCogOutput = spineComponent.getOutputByName('cog')
        pelvisCogInput = pelvisComponent.getInputByName('cog')
        pelvisCogInput.setConnection(spineCogOutput)

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

        # Arm to Global SRT
        mainSrtOffsetOutput = mainSrtComponent.getOutputByName('offset')
        armLeftGlobalSRTInput = armLeftComponent.getInputByName('globalSRT')
        armLeftGlobalSRTInput.setConnection(mainSrtOffsetOutput)

        armLeftRigScaleInput = armLeftComponent.getInputByName('rigScale')
        armLeftRigScaleInput.setConnection(mainSrtRigScaleOutput)

        armRightGlobalSRTInput = armRightComponent.getInputByName('globalSRT')
        armRightGlobalSRTInput.setConnection(mainSrtOffsetOutput)

        armRightRigScaleInput = armRightComponent.getInputByName('rigScale')
        armRightRigScaleInput.setConnection(mainSrtRigScaleOutput)

        # Hand To Arm Connections
        armLeftEndOutput = armLeftComponent.getOutputByName('armEndXfo')
        handLeftArmEndInput = handLeftComponent.getInputByName('armEndXfo')
        handLeftArmEndInput.setConnection(armLeftEndOutput)

        armLeftDrawDebugOutput = armLeftComponent.getOutputByName('drawDebug')
        handLeftDrawDebugInput = handLeftComponent.getInputByName('drawDebug')
        handLeftDrawDebugInput.setConnection(armLeftDrawDebugOutput)

        armRightEndOutput = armRightComponent.getOutputByName('armEndXfo')
        handRightArmEndInput = handRightComponent.getInputByName('armEndXfo')
        handRightArmEndInput.setConnection(armRightEndOutput)

        armRightDrawDebugOutput = armRightComponent.getOutputByName('drawDebug')
        handRightDrawDebugInput = handRightComponent.getInputByName('drawDebug')
        handRightDrawDebugInput.setConnection(armRightDrawDebugOutput)

        # Arm To Clavicle Connections
        clavicleLeftEndOutput = clavicleLeftComponent.getOutputByName('clavicleEnd')
        armLeftClavicleEndInput = armLeftComponent.getInputByName('clavicleEnd')
        armLeftClavicleEndInput.setConnection(clavicleLeftEndOutput)
        clavicleRightEndOutput = clavicleRightComponent.getOutputByName('clavicleEnd')
        armRightClavicleEndInput = armRightComponent.getInputByName('clavicleEnd')
        armRightClavicleEndInput.setConnection(clavicleRightEndOutput)

        # Leg to Global SRT
        mainSrtOffsetOutput = mainSrtComponent.getOutputByName('offset')
        legLeftGlobalSRTInput = legLeftComponent.getInputByName('globalSRT')
        legLeftGlobalSRTInput.setConnection(mainSrtOffsetOutput)

        legLeftRigScaleInput = legLeftComponent.getInputByName('rigScale')
        legLeftRigScaleInput.setConnection(mainSrtRigScaleOutput)

        legRightGlobalSRTInput = legRightComponent.getInputByName('globalSRT')
        legRightGlobalSRTInput.setConnection(mainSrtOffsetOutput)

        legRightRigScaleInput = legRightComponent.getInputByName('rigScale')
        legRightRigScaleInput.setConnection(mainSrtRigScaleOutput)

        # Leg To Pelvis Connections
        pelvisOutput = pelvisComponent.getOutputByName('pelvis')
        legLeftPelvisInput = legLeftComponent.getInputByName('pelvisInput')
        legLeftPelvisInput.setConnection(pelvisOutput)
        legRightPelvisInput = legRightComponent.getInputByName('pelvisInput')
        legRightPelvisInput.setConnection(pelvisOutput)

        # Foot To Leg Connections
        legLeftEndOutput = legLeftComponent.getOutputByName('legEndXfo')
        footLeftEndInput = footLeftComponent.getInputByName('legEndXfo')
        footLeftEndInput.setConnection(legLeftEndOutput)

        legLeftDrawDebugOutput = legLeftComponent.getOutputByName('drawDebug')
        footLeftDrawDebugInput = footLeftComponent.getInputByName('drawDebug')
        footLeftDrawDebugInput.setConnection(legLeftDrawDebugOutput)

        legRightEndOutput = legRightComponent.getOutputByName('legEndXfo')
        footRightEndInput = footRightComponent.getInputByName('legEndXfo')
        footRightEndInput.setConnection(legRightEndOutput)

        legLeftDrawDebugOutput = legRightComponent.getOutputByName('drawDebug')
        footLeftDrawDebugInput = footRightComponent.getInputByName('drawDebug')
        footLeftDrawDebugInput.setConnection(legLeftDrawDebugOutput)

        Profiler.getInstance().pop()
