import json

from kraken.core.maths import *


color0 = Color()
color0.r = 1.0;
print "color0:" + str(color0)
color1 = Color(1.0, 0.0, 0.74, 0.5);
print "color1:" + str(color1)
print "lerp:" + str(color0.linearInterpolate(color1, 0.5))

# Random color will never pass
# print "rand:" + str(Color.randomColor(0.5))

