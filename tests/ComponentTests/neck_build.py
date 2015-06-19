from kraken import plugins
from kraken.core.maths import Vec3

from kraken_examples.neck_component import NeckComponentGuide, NeckComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("neck_build")

neckGuide = NeckComponentGuide("neck")
neckGuide.loadData({
                    "name": "Neck",
                    "location": "L",
                    "neckPosition": Vec3(0.0, 16.5572, -0.6915),
                    "neckUpVOffset": Vec3(0.0, 0.0, -1.0),
                    "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
                   })


# Save the hand guide data for persistence.
saveData = neckGuide.saveData()

neckGuideData = neckGuide.getRigBuildData()

neck = NeckComponentRig()
neck.loadData(neckGuideData)

builder = plugins.getBuilder()
builder.build(neck)

Profiler.getInstance().pop()


if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(neck)
