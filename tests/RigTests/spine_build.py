from kraken import plugins
from kraken.core.maths import Vec3

from kraken.examples.spine_component import SpineComponentGuide, SpineComponent

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("spine_build")

spineGuide = SpineComponentGuide("spine")
spineGuide.loadData({
                     "name": "Spine",
                     "location": "M",
                     "cogPosition": Vec3(0.0, 11.1351, -0.1382),
                     "spine01Position": Vec3(0.0, 11.1351, -0.1382),
                     "spine02Position": Vec3(0.0, 11.8013, -0.1995),
                     "spine03Position": Vec3(0.0, 12.4496, -0.3649),
                     "spine04Position": Vec3(0.0, 13.1051, -0.4821),
                     "numDeformers": 6
                    })

# Save the hand guide data for persistence.
saveData = spineGuide.saveData()

spineGuideData = spineGuide.getGuideData()

spine = SpineComponent()
spine.loadData(spineGuideData)

builder = plugins.getBuilder()
builder.build(spine)

Profiler.getInstance().pop()


if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(spine)
