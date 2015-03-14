from kraken.core.maths import *
from kraken.core.io.kraken_saver import KrakenSaver
from kraken.core.io.kraken_loader import KrakenLoader
from kraken.helpers.utility_methods import logHierarchy 

from bob_rig import Rig

import json

if __name__ == "__main__":
    bob = Rig("Bob")
    print "==bob=="
    logHierarchy(bob)
    
    saver = KrakenSaver()
    jsonData1 = bob.jsonEncode(saver)

    loader = KrakenLoader()
    bob2 = loader.construct(jsonData1)
    
    print "==bob2=="
    logHierarchy(bob2)