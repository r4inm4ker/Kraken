from kraken.core.maths import *
from kraken.core.objects.kraken_saver import KrakenSaver
from kraken.core.objects.kraken_loader import KrakenLoader

from kraken.tests.arm_component import ArmComponent

import json
# import sys
# import difflib
# from pprint import pprint

if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    
    saver = KrakenSaver()
    jsonData1 = armLeft.jsonEncode(saver)

    loader = KrakenLoader()
    armLeft2 = loader.construct(jsonData1)

    saver = KrakenSaver()
    jsonData2 = armLeft.jsonEncode(saver)

    jsonText1 = json.dumps(jsonData1, indent=2)
    jsonText2 = json.dumps(jsonData2, indent=2)
    # print(jsonText2)
    # print "==="
    # differ = difflib.Differ()
    # result = list(differ.compare(jsonText1, jsonText1))
    # # pprint(result)
    # sys.stdout.writelines(result)
    print jsonText1 == jsonText2