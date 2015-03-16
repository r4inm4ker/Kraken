from kraken.core.maths import *
from kraken.core.io.kraken_saver import KrakenSaver
from kraken.core.io.kraken_loader import KrakenLoader

from kraken.examples.arm_component import ArmComponent

from kraken.helpers.utility_methods import logHierarchy

import json

# Only run this test from the Python command line.
if __name__ == "__main__":
    armLeft = ArmComponent("myArm", location='L')
    print "==armLeft=="
    logHierarchy(armLeft)

    saver = KrakenSaver()
    jsonData1 = armLeft.jsonEncode(saver)
    jsonText1 = json.dumps(jsonData1, indent=2)

    loader = KrakenLoader()
    armLeft2 = loader.construct(jsonData1)
    print "==armLeft2=="
    logHierarchy(armLeft2)

