import json

from kraken.core.maths import *


color0 = Color()
color0.r = 1.0;
print "color:" + str(color0)
color1 = Color(1.0, 0.0, 0.74, 0.5);
print "color:" + str(color1)
print "lerp:" + str(color0.linearInterpolate(color1, 0.5))

print "rand:" + str(Color.randomColor())

