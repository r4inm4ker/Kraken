from kraken import plugins

from kraken_components.biped.neck_component import NeckComponentGuide, NeckComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("neck_build")

neckGuide = NeckComponentGuide("neck")
neckGuide.loadData(neckGuide.default_data)


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
    for each in neck.getItems().values():
        # Only log hierarchy for Layer objects as Layers in this test are added to
        # the component since there is no rig object.
        if each.isTypeOf('Layer'):
            logHierarchy(each)
