import json

from kraken.core.maths import *


vec2 = Vec2()
vec2.x = 2.0
print "vec2:" + str(vec2)
print "length:" + str(vec2.length())
vec2 = Vec2(1.0, 2.0)
print "vec2:" + str(vec2)
print "length:" + str(vec2.length())
print "clone:" + str(vec2.clone())

vec1 = Vec2()
vec2 = Vec2(0, 1)

print "equal:" + str(vec1 == vec2)
print "not equal:" + str(vec1 != vec2)

print "add:" + str(vec1 + vec2)
print "subtract:" + str(vec1 - vec2)
print "multiply:" + str(vec1 * vec2)
print "divide:" + str(vec1 / vec2)