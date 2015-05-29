import json

from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat
from kraken.examples.leg_component import LegComponentGuide, LegComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("leg_build")

legGuide = LegComponentGuide("leg")
legGuide.loadData({
                   "name": "L_Leg",
                   "location": "L",
                   "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
                   "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
                   "ankleXfo": Xfo(Vec3(1.85, 1.1516, -1.237)),
                   "toeXfo": Xfo(Vec3(1.85, 0.4, 0.25)),
                   "toeTipXfo": Xfo(Vec3(1.85, 0.4, 1.5))
                  })

# Save the arm guid data for persistence.
saveData = legGuide.saveData()

legGuideData = legGuide.getGuideData()

leg = LegComponentRig()
leg.loadData(legGuideData)

builder = plugins.getBuilder()
builder.build(leg)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(leg)