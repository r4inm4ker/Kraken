import json

from kraken import plugins
from kraken_examples.bob_guide import BobGuide
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy

Profiler.getInstance().push("bob_guide_build")

bobGuide = BobGuide("char_bob_guide")

builder = plugins.getBuilder()
builder.build(bobGuide)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(bobGuide)
