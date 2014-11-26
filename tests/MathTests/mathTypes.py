from kraken.core.maths import *
from kraken.core.objects.kraken_loader import KrakenLoader 
import json

if __name__ == "__main__":
    tr = Vec3(32,35,234)
    print "tr:" + str(tr)
    sc = Vec3(2.3,2.3,2.3)
    print "sc:" + str(sc)
    xfo = Xfo(tr=tr, sc=sc)
    print "xfo:" + str(xfo)

    euler = Euler()
    print "euler:" + str(euler)
