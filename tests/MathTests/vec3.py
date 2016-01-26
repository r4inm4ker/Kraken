import json

from kraken.core.maths import *


vec3 = Vec3()
vec3.x = 3.0
print "vec3:" + str(vec3)
print "length:" + str(vec3.length())
vec3 = Vec3(1.0, 0.0, 2.0)
print "vec3:" + str(vec3)
print "length:" + str(vec3.length())
print "clone:" + str(vec3.clone())
