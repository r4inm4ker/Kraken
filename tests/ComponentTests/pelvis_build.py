from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat

from kraken.examples.pelvis_component import PelvisComponentGuide, PelvisComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("pelvis_build")

pelvisGuide = PelvisComponentGuide("pelvis")
pelvisGuide.loadData({
                      "name": "pelvis",
                      "location": "M",
                      "pelvisXfo": Xfo(tr=Vec3(0.0, 11.1351, -0.1382))
                     })

# Save the pelvis guide data for persistence.
saveData = pelvisGuide.saveData()

pelvisGuideData = pelvisGuide.getGuideData()

pelvis = PelvisComponentRig()
pelvis.loadData(pelvisGuideData)

builder = plugins.getBuilder()
builder.build(pelvis)

Profiler.getInstance().pop()


if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(pelvis)