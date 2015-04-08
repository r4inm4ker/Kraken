
from kraken import plugins
from kraken.core.maths import Vec3, Quat
from kraken.core.profiler import Profiler
from kraken.examples.arm_component import ArmComponent
from kraken.helpers.utility_methods import logHierarchy
import json


Profiler.getInstance().push("arm_build")

arm = ArmComponent("arm", data={ 
            "location":"R",
            "bicepPosition": Vec3(-2.27, 15.295, -0.753),
            "forearmPosition": Vec3(-5.039, 13.56, -0.859),
            "wristPosition": Vec3(-7.1886, 12.2819, 0.4906),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
            })

builder = plugins.getBuilder()
builder.build(arm)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(arm)