from kraken.core.maths import *
import json

quat = Quat()
print "quat:" + str(quat)
print "mat33:" + str(quat.toMat33())
quat = Quat(v=Vec3(1.0, 0.0, 2.0), w=0.5);
print "quat:" + str(quat)
print "mat33:" + str(quat.toMat33())
