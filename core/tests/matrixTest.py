from kraken.core.maths import vec
from kraken.core.maths import matrix
from kraken.core.maths import mathUtils
reload(vec)
reload(matrix)
reload(mathUtils)

import math

x = -45
y = 45
z = 0

cx = math.cos(mathUtils.degToRad(x))
sx = math.sin(mathUtils.degToRad(x))

cy = math.cos(mathUtils.degToRad(y))
sy = math.sin(mathUtils.degToRad(y))

cz = math.cos(mathUtils.degToRad(z))
sz = math.sin(mathUtils.degToRad(z))

rotX = matrix.Matrix33(vec.Vec3(1,0,0),vec.Vec3(0,cx,sx),vec.Vec3(0,-sx,cx))
rotY = matrix.Matrix33(vec.Vec3(cy,0,-sy),vec.Vec3(0,1,0),vec.Vec3(sy,0,cy))
rotZ = matrix.Matrix33(vec.Vec3(cz,sz,0),vec.Vec3(-sz,cz,0),vec.Vec3(0,0,1))

rotXYZ = rotZ.multiply(rotX.multiply(rotY))

print rotXYZ