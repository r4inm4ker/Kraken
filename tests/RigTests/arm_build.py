
from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat
from kraken.core.profiler import Profiler
from kraken.examples.arm_component import ArmComponentGuide, ArmComponent
from kraken.helpers.utility_methods import logHierarchy
import json


Profiler.getInstance().push("arm_build")

armGuide = ArmComponentGuide("arm")
armGuide.loadData({
    'bicep': Xfo(Vec3(3,4,5)),
    'forearm': Xfo(Vec3(2,4,5)),
    'wrist': Xfo(Vec3(1,4,5))
    })

arm = ArmComponent()

armGuideData = armGuide.getGuideData()
arm.loadData(armGuideData)

builder = plugins.getBuilder()
builder.build(arm)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(arm)