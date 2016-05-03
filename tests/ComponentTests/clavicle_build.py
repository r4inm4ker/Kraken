from kraken import plugins
from kraken.core.maths import Xfo, Vec3
from kraken.core.profiler import Profiler
from kraken_components.biped.clavicle_component import ClavicleComponentGuide, ClavicleComponentRig
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("clavicle_build")

clavicleGuide = ClavicleComponentGuide("clavicle")
clavicleGuide.loadData({
    "name": "Clavicle",
    "location": "L",
    "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
    "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
    "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
})

# Save the clavicle guid data for persistence.
saveData = clavicleGuide.saveData()

clavicleGuideData = clavicleGuide.getRigBuildData()

clavicle = ClavicleComponentRig()
clavicle.loadData(clavicleGuideData)

builder = plugins.getBuilder()
builder.build(clavicle)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    for each in clavicle.getItems().values():
        # Only log hierarchy for Layer objects as Layers in this test are added to
        # the component since there is no rig object.
        if each.isTypeOf('Layer'):
            logHierarchy(each)
