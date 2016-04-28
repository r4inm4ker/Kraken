import json

from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat
from kraken_components.biped.leg_component import LegComponentGuide, LegComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("leg_build")

legGuide = LegComponentGuide("leg")
legGuide.loadData({
    "name": "Leg",
    "location": "L",
    "createIKHandle": False,
    "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
    "kneeXfo": Xfo(Vec3(1.408, 5.4371, -0.5043)),
    "ankleXfo": Xfo(Vec3(1.75, 1.15, -1.25))
})

# Save the arm guid data for persistence.
saveData = legGuide.saveData()

legGuideData = legGuide.getRigBuildData()

leg = LegComponentRig()
leg.loadData(legGuideData)

builder = plugins.getBuilder()
builder.buildComponent(leg)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    for each in leg.getItems().values():
        # Only log hierarchy for Layer objects as Layers in this test are added to
        # the component since there is no rig object.
        if each.isTypeOf('Layer'):
            logHierarchy(each)