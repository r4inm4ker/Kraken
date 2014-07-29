from kraken.core.maths import *
from kraken.core.objects.kraken_factory import KrakenFactory 

if __name__ == "__main__":
    tr = Vec3(32,35,234)
    scl = Vec3(2.3,2.3,2.3)
    xfo = Xfo(tr=tr, scl=scl)
    jsonData = xfo.jsonEncode()
    print "Xfo:" + str(jsonData)

    loader = KrakenFactory()
    xfo2 = Xfo()
    xfo2.jsonDecode(jsonData, loader)
    print "Xfo2:" + str(xfo2)