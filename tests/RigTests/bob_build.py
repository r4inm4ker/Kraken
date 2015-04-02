
from kraken import plugins
from kraken.examples.bob_rig import Rig
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy
import json

Profiler.getInstance().push("bob_build")

bobRig = Rig("char_bob")

builder = plugins.getBuilder()
builder.build(bobRig)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print json.dumps(Profiler.getInstance().generateReport(), sort_keys=False, indent=4, separators=(',', ': '))
else:
    logHierarchy(bobRig)