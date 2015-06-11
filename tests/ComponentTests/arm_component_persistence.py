import json

from kraken.core.maths import Xfo, Vec3

from kraken.examples.arm_component import ArmComponentGuide, ArmComponent

from kraken.core.io.kraken_saver import KrakenSaver
from kraken.core.io.kraken_loader import KrakenLoader
from kraken.helpers.utility_methods import logHierarchy


armGuide = ArmComponentGuide("arm")
armGuide.loadData({
        "name": "Arm",
        "location": "L",
        "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
        "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
        "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
        "bicepFKCtrlSize": 1.75,
        "forearmFKCtrlSize": 1.5
    })

# Save the arm guid data for persistence.
saveData = armGuide.saveData()

armGuideData = armGuide.getRigBuildData()

armLeft = ArmComponent()
armLeft.loadData(armGuideData)

print "==armLeft=="
logHierarchy(armLeft)

saver = KrakenSaver()
jsonData1 = armLeft.jsonEncode(saver)
jsonText1 = json.dumps(jsonData1, indent=2)

loader = KrakenLoader()
armLeft2 = loader.construct(jsonData1)
print "==armLeft2=="
logHierarchy(armLeft2)
