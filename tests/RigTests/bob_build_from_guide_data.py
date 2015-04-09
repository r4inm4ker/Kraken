
from kraken import plugins
from kraken.core.objects.rig import Rig
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy
import json
from kraken.examples.bob_guide_data import bob_guide_data

Profiler.getInstance().push("bob_build")

bobRig = Rig("char_bob")
bobRig.loadRigDefinition(bob_guide_data)

builder = plugins.getBuilder()
builder.build(bobRig)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print json.dumps(Profiler.getInstance().generateReport(), sort_keys=False, indent=4, separators=(',', ': '))
else:
    logHierarchy(bobRig)