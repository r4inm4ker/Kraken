import json

from kraken.core.maths import *


quat = Quat()
print "quat:" + str(quat)
print "mat33:" + str(quat.toMat33())
quat = Quat(v=Vec3(1.0, 0.0, 2.0), w=0.5)
print "quat:" + str(quat)
print "mat33:" + str(quat.toMat33())

quat2 = Quat(Vec3(0, 1, 0), 1.34)

print "equal:" + str(quat == quat2)
print "not equal:" + str(quat != quat2)

print "add:" + str(quat + quat2)
print "subtract:" + str(quat - quat2)
print "multiply:" + str(quat * quat2)
print "divide:" + str(quat / quat2)