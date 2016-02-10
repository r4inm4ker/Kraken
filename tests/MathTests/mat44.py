import json

from kraken.core.maths import *


mat44 = Xfo(Vec3(1,2,3), Quat(Euler(.6,.7,.8))).toMat44()
print "mat44:" + str(mat44)
print "clone:" + str(mat44.clone())

otherMat44 = Mat44()
otherMat44.row0 = Vec4(0, 1, 0, 1)

print "equal:" + str(mat44 == otherMat44)
print "not equal:" + str(mat44 != otherMat44)

print "add:" + str(mat44 + otherMat44)
print "subtract:" + str(mat44 - otherMat44)
print "multiply:" + str(mat44 * otherMat44)