import json

from kraken.core.maths import *


xfo1 = Xfo()
print "xfo:" + str(xfo1)
print "mat44:" + str(xfo1.toMat44())
xfo2 = Xfo(tr=Vec3(1.0, 0.0, 2.0), ori=Quat(v=Vec3(1.0, 0.0, 2.0), w=0.5).unit())
print "xfo:" + str(xfo2)
print "mat44:" + str(xfo2.toMat44())
print "linearInterpolate:" + str(xfo1.linearInterpolate(xfo2, 0.5))
print "clone:" + str(xfo2.clone())
print "equal:" + str(xfo1 == xfo2)
print "not equal:" + str(xfo1 != xfo2)
print "multiply:" + str(xfo1 * xfo2)