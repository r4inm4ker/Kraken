
from kraken import plugins
from kraken.core.maths import Vec3
from kraken_components.generic.tentacle_component import TentacleComponentGuide, TentacleComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("tentacle_build")

tentacleGuide = TentacleComponentGuide("tentacle")
tentacleGuide.loadData(
                        {
                         "name": "tentacle",
                         "location": "L",
                         "numJoints": 12,
                         "jointPositions": [
                                            Vec3(0.9811,    12, -1.237),
                                            Vec3(5.4488,    11, -1.237),
                                            Vec3(4.0,       10, -1.237),
                                            Vec3(6.841,     9, -1.237),
                                            Vec3(9.841,     8, -1.237),
                                            Vec3(9.841,     7, -1.237),
                                            Vec3(9.841,     6, -1.237),
                                            Vec3(9.841,     5, -1.237),
                                            Vec3(9.841,     4, -1.237),
                                            Vec3(9.841,     3, -1.237),
                                            Vec3(9.841,     2, -1.237),
                                            Vec3(9.841,     1, -1.237)
                                           ]
                        })

# Save the hand guide data for persistence.
saveData = tentacleGuide.saveData()

tentacleGuideData = tentacleGuide.getRigBuildData()

tentacle = TentacleComponentRig()
tentacle.loadData(tentacleGuideData)

builder = plugins.getBuilder()
builder.buildComponent(tentacle)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    for each in tentacle.getItems().values():
        # Only log hierarchy for Layer objects as Layers in this test are added to
        # the component since there is no rig object.
        if each.isTypeOf('Layer'):
            logHierarchy(each)