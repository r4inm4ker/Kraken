
from kraken import plugins
from kraken.examples.arm_component import ArmComponent
from kraken.core.profiler import Profiler
import json


Profiler.getInstance().push("arm_build")

arm = ArmComponent("arm")

builder = plugins.getBuilder()
builder.build(arm)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(bobRig)