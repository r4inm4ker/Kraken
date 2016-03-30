from kraken.core.maths import Vec3, Quat, Xfo

from kraken.core.objects.rig import Rig
from kraken.core.objects.layer import Layer

from kraken_examples.head_component import HeadComponentGuide
from kraken_examples.clavicle_component import ClavicleComponentGuide
from kraken_examples.arm_component import ArmComponentGuide
from kraken_examples.leg_component import LegComponentGuide
from kraken_examples.spine_component import SpineComponentGuide
from kraken_examples.neck_component import NeckComponentGuide

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class BobGuide(Rig):
    """Bobe Guide Rig"""

    def __init__(self, name):

        Profiler.getInstance().push("Construct BobGuide:" + name)
        super(BobGuide, self).__init__(name)

        # Add Components to Layers
        spineComponent = SpineComponentGuide('spine', self)
        neckComponentGuide = NeckComponentGuide('neck', self)
        headComponent = HeadComponentGuide("head", self)

        clavicleLeftComponentGuide = ClavicleComponentGuide("clavicle", self)
        clavicleLeftComponentGuide.loadData({
            "location": "L",
            "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
        })

        armLeftComponentGuide = ArmComponentGuide("arm", self)
        armLeftComponentGuide.loadData({
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                           ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5})

        clavicleRightComponentGuide = ClavicleComponentGuide("clavicle", self)
        clavicleRightComponentGuide.loadData({
            "location": "R",
            "clavicleXfo": Xfo(Vec3(-0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(-2.27, 15.295, -0.753))
        })

        armRightComponentGuide = ArmComponentGuide("arm", self)
        armRightComponentGuide.loadData({
            "location": "R",
            "bicepXfo": Xfo(Vec3(-2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(-5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(-7.1886, 12.2819, 0.4906)),
            "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906),
                           ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

        legLeftComponentGuide = LegComponentGuide("leg", self)
        legLeftComponentGuide.loadData({
            "location": "L",
            "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237)),
            "toeXfo": Xfo(Vec3(1.85, 0.4, 0.25)),
            "toeTipXfo": Xfo(Vec3(1.85, 0.4, 1.5))
        })

        legRightComponentGuide = LegComponentGuide("leg", self)
        legRightComponentGuide.loadData({
            "location": "R",
            "femurXfo": Xfo(Vec3(-0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(-1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(-1.841, 1.1516, -1.237)),
            "toeXfo": Xfo(Vec3(-1.85, 0.4, 0.25)),
            "toeTipXfo": Xfo(Vec3(-1.85, 0.4, 1.5))
        })

        Profiler.getInstance().pop()
