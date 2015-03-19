from kraken.core.maths import *
import json

mat44 = Xfo(Vec3(1,2,3), Quat(Euler(.6,.7,.8))).toMat44()
print "mat44:" + str(mat44)
print "clone:" + str(mat44.clone())
