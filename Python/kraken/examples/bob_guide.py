from kraken.core.maths import Vec3, Quat, Xfo

from kraken.core.objects.container import Container
from kraken.core.objects.layer import Layer

from kraken.examples.hand_component import HandComponentGuide
from kraken.examples.head_component import HeadComponentGuide
from kraken.examples.clavicle_component import ClavicleComponentGuide
from kraken.examples.arm_component import ArmComponentGuide
from kraken.examples.leg_component import LegComponentGuide
from kraken.examples.foot_component import FootComponentGuide
from kraken.examples.spine_component import SpineComponentGuide
from kraken.examples.neck_component import NeckComponentGuide

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class BobGuide(Container):
    """Bobe Guide Rig"""

    def __init__(self, name):

        Profiler.getInstance().push("Construct BobGuide:" + name)
        super(BobGuide, self).__init__(name)

        # Add Components to Layers
        spineComponent = SpineComponentGuide('spine', self)
        neckComponentGuide = NeckComponentGuide('neck', self)
        headComponent = HeadComponentGuide("head", self)

        clavicleLeftComponentGuide = ClavicleComponentGuide("clavicle", self, data={
            "location": "L",
            "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
        })

        armLeftComponentGuide = ArmComponentGuide("arm", self, data={
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5})

        handLeftComponent = HandComponentGuide("hand", self, data={
            "location": "L",
            "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                            ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331))
        })

        clavicleRightComponentGuide = ClavicleComponentGuide("clavicle", self, data={
            "location": "R",
            "clavicleXfo": Xfo(Vec3(-0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(-2.27, 15.295, -0.753))
        })

        armRightComponentGuide = ArmComponentGuide("arm", self, data={
            "location": "R",
            "bicepXfo": Xfo(Vec3(-2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(-5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(-7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        handRightComponent = HandComponentGuide("hand", self, data={
            "location": "R",
            "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906),
                            ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623))
        })

        legLeftComponentGuide = LegComponentGuide("leg", self, data={
            "location": "L",
            "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237))
        })

        footLeftComponentGuide = FootComponentGuide("foot", self, data={
            "location": "L",
            "footXfo": Xfo(tr=Vec3(1.841, 1.1516, -1.237),
                           ori=Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190))
        })

        legRightComponentGuide = LegComponentGuide("leg", self, data={
            "location": "R",
            "femurXfo": Xfo(Vec3(-0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(-1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(-1.841, 1.1516, -1.237))
        })

        footRightComponentGuide = FootComponentGuide("foot", self, data={
            "location": "R",
            "footXfo": Xfo(tr=Vec3(-1.841, 1.1516, -1.237),
                           ori=Quat(Vec3(0.5695, -0.6377, 0.4190), 0.3053))
        })

        Profiler.getInstance().pop()
