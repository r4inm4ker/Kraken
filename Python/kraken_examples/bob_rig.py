from kraken.core.maths import Vec3, Quat, Xfo

from kraken.core.objects.container import Container

from kraken_components.generic.mainSrt_component import MainSrtComponentRig
from kraken_components.biped.head_component import HeadComponentRig
from kraken_components.biped.clavicle_component import ClavicleComponentGuide, ClavicleComponentRig
from kraken_components.biped.arm_component import ArmComponentGuide, ArmComponentRig
from kraken_components.biped.leg_component import LegComponentGuide, LegComponentRig
from kraken_components.biped.spine_component import SpineComponentRig
from kraken_components.biped.neck_component import NeckComponentGuide, NeckComponentRig

from kraken.core.profiler import Profiler


class BobRig(Container):
    """Simple biped test rig.

    This example shows how to create a simple scripted biped rig that loads data
    onto component rig classes and also onto guide classes. It also demonstrates
    how to make connections between components.

    """

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

        neckComponentGuide = NeckComponentGuide("neck")
        neckComponentGuide.loadData({
            "location": "M",
            "neckPosition": Vec3(0.0, 16.5572, -0.6915),
            "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
        })

        neckComponent = NeckComponentRig("neck", self)
        neckComponent.loadData(neckComponentGuide.getRigBuildData())

        headComponent = HeadComponentRig("head", self)
        headComponent.loadData(data={
            "headPosition": Vec3(0.0, 17.4756, -0.421),
            "headEndPosition": Vec3(0.0, 19.5, -0.421),
            "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
            "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
            "jawPosition": Vec3(0.0, 17.613, -0.2731)
        })

        clavicleLeftComponentGuide = ClavicleComponentGuide("clavicle")
        clavicleLeftComponentGuide.loadData({
            "location": "L",
            "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
        })

        clavicleLeftComponent = ClavicleComponentRig("clavicle", self)
        clavicleLeftComponent.loadData(data=clavicleLeftComponentGuide.getRigBuildData())

        clavicleRightComponentGuide = ClavicleComponentGuide("clavicle")
        clavicleRightComponentGuide.loadData({
            "location": "R",
            "clavicleXfo": Xfo(Vec3(-0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(-2.27, 15.295, -0.753))
        })

        clavicleRightComponent = ClavicleComponentRig("clavicle", self)
        clavicleRightComponent.loadData(data=clavicleRightComponentGuide.getRigBuildData())

        armLeftComponentGuide = ArmComponentGuide("arm")
        armLeftComponentGuide.loadData({
            "location":"L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                           ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        armLeftComponent = ArmComponentRig("arm", self)
        armLeftComponent.loadData(data=armLeftComponentGuide.getRigBuildData())

        armRightComponentGuide = ArmComponentGuide("arm")
        armRightComponentGuide.loadData({
            "location":"R",
            "bicepXfo": Xfo(Vec3(-2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(-5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(-7.1886, 12.2819, 0.4906)),
            "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906),
                           ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        armRightComponent = ArmComponentRig("arm", self)
        armRightComponent.loadData(data=armRightComponentGuide.getRigBuildData() )

        legLeftComponentGuide = LegComponentGuide("leg")
        legLeftComponentGuide.loadData({
            "name":"Leg",
            "location": "L",
            "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237)),
            "toeXfo": Xfo(Vec3(1.85, 0.4, 0.25)),
            "toeTipXfo": Xfo(Vec3(1.85, 0.4, 1.5))
        })

        legLeftComponent = LegComponentRig("leg", self)
        legLeftComponent.loadData(data=legLeftComponentGuide.getRigBuildData())

        legRightComponentGuide = LegComponentGuide("leg")
        legRightComponentGuide.loadData({
            "name":"Leg",
            "location": "R",
            "femurXfo": Xfo(Vec3(-0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(-1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(-1.85, 1.1516, -1.237)),
            "toeXfo": Xfo(Vec3(-1.85, 0.4, 0.25)),
            "toeTipXfo": Xfo(Vec3(-1.85, 0.4, 1.5))
        })

        legRightComponent = LegComponentRig("leg", self)
        legRightComponent.loadData(data=legRightComponentGuide.getRigBuildData() )

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

        # Arm To Clavicle Connections
        clavicleLeftEndOutput = clavicleLeftComponent.getOutputByName('clavicleEnd')
        armLeftClavicleEndInput = armLeftComponent.getInputByName('root')
        armLeftClavicleEndInput.setConnection(clavicleLeftEndOutput)
        clavicleRightEndOutput = clavicleRightComponent.getOutputByName('clavicleEnd')
        armRightClavicleEndInput = armRightComponent.getInputByName('root')
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
        spinePelvisOutput = spineComponent.getOutputByName('pelvis')
        legLeftPelvisInput = legLeftComponent.getInputByName('pelvisInput')
        legLeftPelvisInput.setConnection(spinePelvisOutput)
        legRightPelvisInput = legRightComponent.getInputByName('pelvisInput')
        legRightPelvisInput.setConnection(spinePelvisOutput)

        Profiler.getInstance().pop()
