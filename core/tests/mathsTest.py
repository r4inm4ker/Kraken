from kraken.core.maths import mathUtils
from kraken.core.maths import vec
from kraken.core.maths import rotation
from kraken.core.maths import matrix
from kraken.core.maths import xfo
reload(mathUtils)
reload(vec)
reload(rotation)
reload(matrix)
reload(xfo)


# =================
# Create vec types
# =================
myVec2 = vec.Vec2()
myVec3 = vec.Vec3()
myVec4 = vec.Vec4()


# ======================
# Create rotation types
# ======================
myEuler = rotation.Euler()
myQuat = rotation.Quat()


# ======================
# Creation Matrix types
# ======================
myMatrix33 = matrix.Matrix33()
myMatrix44 = matrix.Matrix44()


# =================
# Create xfo types
# =================
myXfo = xfo.Xfo()


# =============
# Test Vectors
# =============
print "===============\nVec2\n==============="
myVec2.set(0, 1)
print "Set Values: " + str(myVec2)

print "\n===============\nVec3\n==============="
myVec3.set(1,0,0)
print "Set Values: " + str(myVec3)

print "\n===============\nVec4\n==============="
myVec4.set(0,1,0,0)
print "Set Values: " + str(myVec4)


# ===============
# Test Rotations
# ===============
print "\n===============\nEuler\n==============="
print "Set Values: " + str(myEuler.set(0, mathUtils.degToRad(-45), 0))

print "To Matrix3: " + str(myEuler.toMatrix33())

print "Clone: " + str(myEuler.clone())

print "\n===============\nQuat\n==============="
myQuat.set(None,5)
print "Set Values: " + str(myQuat)

myQuat.setIdentity()
print "Set Identity: " + str(myQuat)

myQuat.setUnit()
print "Set Unit: " + str(myQuat)

myQuat.setFromEuler(myEuler)
print "Set from Euler: " + str(myQuat)

myQuat.setFromAxisAndAngle(vec.Vec3(1,0,0), mathUtils.degToRad(45))
print "Set from Axis and Angle: " + str(myQuat)

myQuat.setFromMatrix33(myEuler.toMatrix33())
print "Set from Matrix33: " + str(myQuat)

myQuat.setFromDirectionAndUpvector(vec.Vec3(0,0,0).subtract(vec.Vec3(0,0,1)).unit(), vec.Vec3(0,0,0).subtract(vec.Vec3(0,1,0)).unit())
print "Set from Direction and UpVec: " + str(myQuat)

myQuat.setIdentity()
print "To Matrix33: " + str(myQuat.toMatrix33())

print "To Euler: " + str(myQuat.toEuler(0))

tmpQuat = rotation.Quat().setFromAxisAndAngle(myVec3, mathUtils.degToRad(90))
print "Add: " + str(myQuat.add(tmpQuat))

print "Subtract: " + str(myQuat.subtract(tmpQuat))

print "Multiply: " + str(myQuat.multiply(tmpQuat))

print "Multiply By Scalar: " + str(myQuat.multiplyByScalar(5))

print "Divide: " + str(myQuat.divide(tmpQuat))

print "Divide By Scalar: " + str(myQuat.divideByScalar(2))

print "Rotate Vector: " + str(tmpQuat.rotateVector(vec.Vec3(0, 0, 1)))

print "Dot Product: " + str(myQuat.dotProduct(tmpQuat))

print "Conjugate: " + str(myQuat.conjugate())

print "Inverse: " + str(myQuat.inverse())

print "Length Squared: " + str(myQuat.lengthSquared())

print "Length: " + str(myQuat.length())

print "Unit: " + str(tmpQuat.unit())

print "Clone: " + str(myQuat.clone())


# ==============
# Test Matrices
# ==============
print "\n===============\nMatrix3\n==============="
myMatrix33.set(vec.Vec3(0.707, 0, 0.707), vec.Vec3(0,1,0), vec.Vec3(-.5,0,-0.5))
print myMatrix33

utilMatrix3 = matrix.Matrix3(vec.Vec3(1, 0, 0), vec.Vec3(0,-0.5,0), vec.Vec3(-.5,0,-0.5))
print utilMatrix3

util2Matrix3 = matrix.Matrix3(vec.Vec3(-0.5, 0, -0.5), vec.Vec3(0,1,0), vec.Vec3(0.707,0,0.707))
print util2Matrix3

multMat33 = myMatrix33.multiply(utilMatrix3)
print multMat33

mult2Mat33 = multMat33.multiply(util2Matrix3)
print mult2Mat33
print multMat33


print "\n===============\nMatrix4\n==============="
myMatrix44.set(myVec4, myVec4, myVec4, myVec4)
print "Set Values: " + str(myMatrix44)


# =========
# Test Xfo
# =========
print "\n===============\nXfo\n==============="
myXfo.set(vec.Vec3(2,1,2), rotation.Euler(0,45,0), myVec3)
print "Set Values: " + str(myXfo)