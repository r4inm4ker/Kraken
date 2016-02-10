import json

from kraken.core.maths import *


mat33 = Euler().toMat33()
print "mat33:" + str(mat33)
print "clone:" + str(mat33.clone())

otherMat33 = Mat33()
otherMat33.row0 = Vec3(0, 1, 0)

print "equal:" + str(mat33 == otherMat33)
print "not equal:" + str(mat33 != otherMat33)

print "add:" + str(mat33 + otherMat33)
print "subtract:" + str(mat33 - otherMat33)
print "multiply:" + str(mat33 * otherMat33)
