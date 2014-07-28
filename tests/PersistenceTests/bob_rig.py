from kraken.core.maths import *
from kraken.core.objects.kraken_saver import KrakenSaver
from kraken.core.objects.kraken_loader import KrakenLoader

from kraken.tests.bob_rig import Rig

import json
# import sys
# import difflib
# from pprint import pprint

if __name__ == "__main__":
    bob = Rig("Bob")
    
    saver = KrakenSaver()
    jsonData1 = bob.jsonEncode(saver)

    loader = KrakenLoader()
    bob2 = loader.construct(jsonData1)

    saver = KrakenSaver()
    jsonData2 = bob.jsonEncode(saver)

    jsonText1 = json.dumps(jsonData1, indent=2)
    jsonText2 = json.dumps(jsonData2, indent=2)

    # differ = difflib.Differ()
    # result = list(differ.compare(jsonText1, jsonText1))
    # # pprint(result)
    # sys.stdout.writelines(result)
    print jsonText1 == jsonText2