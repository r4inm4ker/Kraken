import json

from kraken import plugins
from kraken_examples.spineClav_rig import SpineClavRig
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("spineClav_build")

spineClavRig = SpineClavRig("char_bob")

builder = plugins.getBuilder()
builder.build(spineClavRig)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
   logHierarchy(spineClavRig)
