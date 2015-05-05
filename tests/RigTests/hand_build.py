from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat

from kraken.examples.hand_component import HandComponentGuide, HandComponent

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("hand_build")

handGuide = HandComponentGuide("hand")
handGuide.loadData({
                    "name": "L_Hand",
                    "location": "L",
                    "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                                   ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331))
                   })

# Save the hand guide data for persistence.
saveData = handGuide.saveData()

handGuideData = handGuide.getGuideData()

hand = HandComponent()
hand.loadData(handGuideData)

builder = plugins.getBuilder()
builder.build(hand)

Profiler.getInstance().pop()


if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(hand)