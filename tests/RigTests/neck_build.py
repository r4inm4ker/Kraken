import json

from kraken import plugins
from kraken.core.maths import Vec3
from kraken.examples.neck_component import NeckComponent
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("neck_build")

data = {
        "neckPosition": Vec3(0.0, 16.5572, -0.6915),
        "neckUpVOffset": Vec3(0.0, 0.0, -1.0),
        "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
       }

neck = NeckComponent("neck", data=data)

builder = plugins.getBuilder()
builder.build(neck)

Profiler.getInstance().pop()


if __name__ == "__main__":
    print json.dumps(Profiler.getInstance().generateReport(), sort_keys=False,
                     indent=4, separators=(',', ': '))
else:
    logHierarchy(neck)
