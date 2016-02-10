import json

from kraken.core.maths import *


vec4 = Vec4()
vec4.x = 3.0
print "vec4:" + str(vec4)
print "length:" + str(vec4.length())
vec4 = Vec4(1.0, 0.0, 2.0, 0.0)
print "vec4:" + str(vec4)
print "length:" + str(vec4.length())
print "clone:" + str(vec4.clone())

vec1 = Vec4(0, 2, 0, 0)
vec2 = Vec4(0, 1, 0, 0)

print "equal:" + str(vec1 == vec2)
print "not equal:" + str(vec1 != vec2)

print "add:" + str(vec1 + vec2)
print "subtract:" + str(vec1 - vec2)
print "multiply:" + str(vec1 * vec2)
print "divide:" + str(vec1 / vec2)