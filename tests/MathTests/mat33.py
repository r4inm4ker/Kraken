from kraken.core.maths import *
import json

if __name__ == "__main__":
    mat33 = Euler().toMat33()
    print "mat33:" + str(mat33)
    print "clone:" + str(mat33.clone())
