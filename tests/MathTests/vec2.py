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
