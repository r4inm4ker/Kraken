
from kraken import plugins
from kraken.core.maths import Vec3
from kraken.examples.head_component import HeadComponentGuide, HeadComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("head_build")

headGuide = HeadComponentGuide("head")
headGuide.loadData({
                    "name": "Head",
                    "location": "M",
                    "headPosition": Vec3(0.0, 17.4756, -0.421),
                    "headEndPosition": Vec3(0.0, 19.5, -0.421),
                    "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
                    "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
                    "jawPosition": Vec3(0.0, 17.613, -0.2731)
                   })

# Save the hand guide data for persistence.
saveData = headGuide.saveData()

headGuideData = headGuide.getRigBuildData()

head = HeadComponentRig()
head.loadData(headGuideData)

builder = plugins.getBuilder()
builder.build(head)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(head)