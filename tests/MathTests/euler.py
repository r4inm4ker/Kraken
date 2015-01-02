from kraken.core.maths import *
from kraken.core.objects.kraken_loader import KrakenLoader 
import json

if __name__ == "__main__":
    euler = Euler()
    print "euler:" + str(euler)
    print "mat33:" + str(euler.toMat33())
    euler = Euler(1.0, 0.0, 2.0, 'ZYX');
    print "euler:" + str(euler)
    print "mat33:" + str(euler.toMat33())
