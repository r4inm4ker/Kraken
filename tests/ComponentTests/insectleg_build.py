from kraken import plugins
from kraken.core.maths import Vec3
from kraken_components.generic.insectleg_component import InsectLegComponentGuide, InsectLegComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("insectLeg_build")

insectLegGuide = InsectLegComponentGuide("insectLeg")
insectLegGuide.loadData({
    "name": "insectLeg",
    "location": "L",
    "numJoints": 4,
    "jointPositions": [Vec3(0.9811, 9.769, -1.237),
                       Vec3(5.4488, 8.4418, -1.237),
                       Vec3(4.0, 3.1516, -1.237),
                       Vec3(6.841, 1.0, -1.237),
                       Vec3(9.841, 0.0, -1.237)]
})

# Save the hand guide data for persistence.
saveData = insectLegGuide.saveData()

insectLegGuideData = insectLegGuide.getRigBuildData()

leg = InsectLegComponentRig()
leg.loadData(insectLegGuideData)

builder = plugins.getBuilder()
builder.build(leg)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    for each in leg.getItems().values():
        # Only log hierarchy for Layer objects as Layers in this test are added to
        # the component since there is no rig object.
        if each.isTypeOf('Layer'):
            logHierarchy(each)
