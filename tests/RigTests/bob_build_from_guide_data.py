from kraken import plugins
from kraken.core.objects.rig import Rig
from kraken_examples.bob_guide_data import bob_guide_data
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("bob_build")

bobGuideRig = Rig("char_bob")
bobGuideRig.loadRigDefinition(bob_guide_data)

bobRigData = bobGuideRig.getRigBuildData()
bobRig = Rig()
bobRig.loadRigDefinition(bobRigData)

builder = plugins.getBuilder()
builder.build(bobRig)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(bobRig)
