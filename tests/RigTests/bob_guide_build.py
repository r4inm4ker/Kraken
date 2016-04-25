import json

from kraken import plugins
from kraken_examples.bob_guide import BobGuideRig
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy

Profiler.getInstance().push("bob_guide_build")

bobGuide = BobGuideRig("char_bob_guide")

builder = plugins.getBuilder()
builder.buildRig(bobGuide)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(bobGuide)
