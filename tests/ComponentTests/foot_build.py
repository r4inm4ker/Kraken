
from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat
from kraken.core.profiler import Profiler
from kraken.examples.foot_component import FootComponentGuide, FootComponent
from kraken.helpers.utility_methods import logHierarchy
import json


Profiler.getInstance().push("foot_build")

footGuide = FootComponentGuide("foot")
footGuide.loadData({
                    "name": "L_Foot",
                    "location": "L",
                    "footXfo": Xfo(tr=Vec3(0.1322, 15.403, -0.5723),
                                   ori=Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190))
                   })

# Save the foot guid data for persistence.
saveData = footGuide.saveData()

footGuideData = footGuide.getGuideData()

foot = FootComponent()
foot.loadData(footGuideData)

builder = plugins.getBuilder()
builder.build(foot)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(foot)