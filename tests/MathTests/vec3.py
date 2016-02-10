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

vec1 = Vec3()
vec2 = Vec3(0, 1, 0)

print "equal:" + str(vec1 == vec2)
print "not equal:" + str(vec1 != vec2)

print "add:" + str(vec1 + vec2)
print "subtract:" + str(vec1 - vec2)
print "multiply:" + str(vec1 * vec2)
print "divide:" + str(vec1 / vec2)