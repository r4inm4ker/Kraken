import json

from kraken import plugins
from kraken.core.objects.rig import Rig
from kraken.examples.bob_guide_data import bob_guide_data
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("bob_build")

bobRig = Rig("char_bob")
bobRig.loadRigDefinition(bob_guide_data)

builder = plugins.getBuilder()
builder.build(bobRig)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print json.dumps(Profiler.getInstance().generateReport(),
                     sort_keys=False, indent=4, separators=(',', ': '))
else:
    logHierarchy(bobRig)
