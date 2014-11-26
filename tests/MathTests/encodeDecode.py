from kraken.core.maths import *
from kraken.core.objects.kraken_loader import KrakenLoader 

if __name__ == "__main__":
    tr = Vec3(32,35,234)
    scl = Vec3(2.3,2.3,2.3)
    xfo = Xfo(tr=tr, scl=scl)
    jsonData = xfo.jsonEncode()
    print "Xfo:" + str(jsonData)

    loader = KrakenLoader()
    xfo2 = Xfo()
    xfo2.jsonDecode(jsonData, loader)
    print "Xfo2:" + str(xfo2)