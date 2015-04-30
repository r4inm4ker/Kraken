
from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat
from kraken.core.profiler import Profiler
from kraken.examples.arm_component import ArmComponentGuide, ArmComponent
from kraken.helpers.utility_methods import logHierarchy
import json


Profiler.getInstance().push("arm_build")

armGuide = ArmComponentGuide("arm")
armGuide.loadData({
        "name": "L_Arm",
        "location": "L",
        "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
        "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
        "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
        "bicepFKCtrlSize": 1.75,
        "forearmFKCtrlSize": 1.5
    })

# Save the arm guid data for persistence. 
saveData = armGuide.saveData()

armGuideData = armGuide.getGuideData()

arm = ArmComponent()
arm.loadData(armGuideData)

builder = plugins.getBuilder()
builder.build(arm)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(arm)