import json

from kraken.core.maths import *


mat33 = Euler().toMat33()
print "mat33:" + str(mat33)
print "clone:" + str(mat33.clone())
