from kraken.core.maths import *
from kraken.core.objects.kraken_loader import KrakenLoader 
import json

if __name__ == "__main__":
    mat44 = Xfo(Vec3(1,2,3), Quat(Euler(.6,.7,.8))).toMat44()
    print "mat44:" + str(mat44)
    print "clone:" + str(mat44.clone())
