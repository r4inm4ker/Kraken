
from kraken import plugins
from kraken.examples.neck_component import NeckComponent
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy
import json


Profiler.getInstance().push("neck_build")

neck = NeckComponent("neck")
logHierarchy(neck)

builder = plugins.getBuilder()
builder.build(neck)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print json.dumps(Profiler.getInstance().generateReport(), sort_keys=False, indent=4, separators=(',', ': '))
else:
    logHierarchy(neck)