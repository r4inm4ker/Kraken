"""Kraken - maths.quat module.

Classes:
Quat -- Quaternion rotation.
"""

import math
from kraken.core.objects.kraken_system import KrakenSystem as KS
from math_object import MathObject

from vec3 import Vec3


class Quat(MathObject):
    """Quaternion Rotation object."""

    def __init__(self, v=None, w=None):
        super(Quat, self).__init__()

        if v is not None and self.getTypeName(v) == 'Quat':
            self.rtval = v
        else:
            if v is not None and not isinstance(v, Vec3):
                raise TypeError("Quat: Invalid type for 'v' argument. Must be a Vec3.")

            if w is not None and not isinstance(w, (int, float)):
                raise TypeError("Quat: Invalid type for 'w' argument. Must be a int or float.")

            client = KS.getInstance().getCoreClient()
            self.rtval = client.RT.types.Quat()
            self.set(v=v, w=w)


    def __str__(self):
        """Return string version of the Quat object."""
        return "Quat(" + str(self.v) + "," + str(self.w) + ")"

    @property
    def v(self):
        """I'm the 'v' property."""
        return Vec3(self.rtval.v)

    @v.setter
    def v(self, value):
        self.rtval.v = KS.inst().rtVal('Vec3', value)

    @property
    def w(self):
        """I'm the 'w' property."""
        return self.rtval.w

    @w.setter
    def w(self, value):
        self.rtval.w = KS.inst().rtVal('Scalar', value)


    # Setter from scalar components
    def set(self, v, w):
        self.rtval.set('', KS.inst().rtVal('Vec3', v), KS.inst().rtVal('Scalar', w))


    # Set this quat to the identity
    def setIdentity():
        self.rtval.setIdentity('')

    # Set this quat from a euler rotation
    def setFromEuler(self, e):
        return Quat(self.rtval.setFromEuler('Quat', KS.inst().rtVal('Euler', e)))

    # Set this quat to a given angles vector (in radians) and a rotation order
    def setFromEulerAngles(self, angles, ro):
        return Quat(self.rtval.setFromEuler('Quat', KS.inst().rtVal('Vec3', angles), KS.inst().rtVal('RotationOrder', ro)))

    # Set this quat to a given angles vector (in radians) using
    # the default XYZ rotation order
    def setFromEulerAngles(self, angles):
        return Quat(self.rtval.setFromEuler('Quat', KS.inst().rtVal('Vec3', angles)))

    # Set this quat to a rotation defined by an axis and an angle (in radians)
    def setFromAxisAndAngle(self, axis, angle):
        return Quat(self.rtval.setFromAxisAndAngle('Quat', KS.inst().rtVal('Vec3', axis), KS.inst().rtVal('Scalar', angle)))

    # Set this quat to the rotation described by a
    # 3x3 rotation matrix
    def setFromMat33(self, mat):
        return Quat(self.rtval.setFromMat33('Quat', KS.inst().rtVal('Mat33', mat)))

    # Set the quaternion to the rotation required to rotate the source
    # vector to the destination vector
    # Function taken from the 'Game Programming Gems' article 'The Shortest Arc Quat' by Stan Melax
    # Both vectors must be units.
    def setFrom2Vectors( sourceDirVec, destDirVec, arbitraryIfAmbiguous=True):
        return Quat(self.rtval.setFrom2Vectors('Quat', KS.inst().rtVal('Vec3', sourceDirVec), KS.inst().rtVal('Vec3', destDirVec), KS.inst().rtVal('Boolean', arbitraryIfAmbiguous)))

    # Set the quat to represent the direction as the Z axis
    # and the upvector pointing along the XY plane.
    def setFromDirectionAndUpvector(self, direction, upvector):
        return Quat(self.rtval.setFromDirectionAndUpvector('Quat', KS.inst().rtVal('Vec3', direction), KS.inst().rtVal('Vec3', upvector)))

    # Returns true if this quaternion is equal
    # to another one
    def equal(self, other):
        return self.rtval.equal('Boolean', KS.inst().rtVal('Quat', other))

    # Returns true if this quaternion is
    # almost equal to another one (given a precision)
    def almostEqual(self, other, precision):
        return self.rtval.almostEqual('Boolean', KS.inst().rtVal('Quat', other), KS.inst().rtVal('Scalar', precision))

    # Returns true if this quaternion is
    # almost equal to another one (using a default precision)
    def almostEqual(self, other):
        return self.rtval.almostEqual('Boolean', KS.inst().rtVal('Quat', other))

    # # Equals operator
    # def Boolean == (Quat a, Quat b):
    #   return a.v == b.v && a.w == b.w;
    # }

    # # Not equals operator
    # def Boolean != (Quat a, Quat b):
    #   return a.v != b.v || a.w != b.w;
    # }

    # # Adds two quaternions
    # def Quat + (in Quat a, in Quat b):
    #   return Quat(a.w + b.w, a.v + b.v);
    # }

    # # Adds another quaternion to this one
    # def  += (in Quat b):
    #   this = this + b;
    # }

    # # Subtracts two quaternions
    # def Quat - (in Quat a, in Quat b):
    #   return Quat(a.w - b.w, a.v - b.v);
    # }

    # # Subtracts another quaternion from this one
    # def  -= (in Quat b):
    #   this = this - b;
    # }

    # # Multiplies two quaternions
    # def Quat * (in Quat a, in Quat b):
    #   return Quat(a.w * b.w - a.v.dot(b.v), a.v.cross(b.v) + (a.w * b.v) + (a.v * b.w));
    # }

    # # Multiplies this quaternion with another one
    # def  *= (in Quat b):
    #   this = this * b;
    # }

    # # Multiplies a scalar with a quaternion
    # def Quat * (in Scalar a, in Quat b):
    #   return Quat(a * b.w, a * b.v);
    # }

    # # Multiplies a quaternion with a scalar
    # def Quat * (in Quat a, in Scalar b):
    #   return Quat(a.w * b, a.v * b);
    # }

    # # Multiplies this quaternion with a scalar
    # def  *= (in Scalar b):
    #   this = this * b;
    # }

    # # Returns the division of two quaternions
    # def Quat / (in Quat a, in Quat b):
    #   return Quat(a.w * b.w + a.v.dot(b.v), (a.v * b.w) - (a.w * b.v) - a.v.cross(b.v));
    # }

    # # Divides this quaternion by another one
    # def  /= (in Quat b):
    #   this = this / b;
    # }

    # # Returns the division of a quaternion and a scalar
    # def Quat / (Quat a, Scalar b):
    #   if( Boolean(Fabric_Guarded) && Math_badDivisor( b ) )
    #     Math_reportBadDivisor( b, "divide" );
    #   return a * (1.0 / b);
    # }

    # # Divides this quaternion by a scalar
    # def  /= (in Scalar b):
    #   this = this / b;
    # }

    # Overload method for the add operator
    def add(self, other):
        return self.rtval.add('Quat', KS.inst().rtVal('Quat', other))

    # Overload method for the subtract operator
    def subtract(self, other):
        return Quat(self.rtval.subtract('Quat', KS.inst().rtVal('Quat', other)))

    # Overload method for the multiply operator
    def multiply(self, other):
        return Quat(self.rtval.multiply('Quat', KS.inst().rtVal('Quat', other)))

    # Overload method for the divide operator
    def divide(self, other):
        return Quat(self.rtval.divide('Quat', KS.inst().rtVal('Quat', other)))

    # Returns the product of this quaternion and a scalar
    def multiplyScalar(self, other):
        return Quat(self.rtval.multiplyScalar('Quat', KS.inst().rtVal('Scalar', other)))

    # Returns the division of this quaternion and a scalar
    def divideScalar(self, other):
        return Quat(self.rtval.divideScalar('Quat', KS.inst().rtVal('Scalar', other)))

    # Rotates a vector by this quaterion.
    # Don't forget to normalize the quaternion unless
    # you want axial translation as well as rotation.
    def rotateVector(self, v):
        return Vec3(self.rtval.rotateVector('Vec3', KS.inst().rtVal('Vec3', v)))

    # Returns the dot product of this quaternion and another one
    def dot(self, other):
        return self.rtval.dot('Scalar', KS.inst().rtVal('Quat', other))

    # Returns the conjugate of this quaternion
    def conjugate(self):
        return self.rtval.conjugate('Quat')

    # Returns the squared length of this quaternion
    def lengthSquared(self):
        return self.rtval.lengthSquared('Scalar')

    # Returns the length of this quaternion
    def length(self):
        return self.rtval.length('Scalar')

    # Returns a unit quaternion of this one
    def unit(self):
        return Quat(self.rtval.unit('Quat'))

    # Returns a unit quaternion of this one, no error reported if cannot be made unit
    def unit_safe(self):
        return Quat(self.rtval.unit_safe('Quat'))

    # Sets this quaternion to a unit quaternion and returns
    # the previous length
    def setUnit(self):
        return self.rtval.setUnit('Scalar')

    # Returns a inverse quaternion of this one
    def inverse(self):
        return Quat(self.rtval.inverse('Quat'))

    # Aligns this quaternion with another one ensuring that the delta between
    # the Quat values is the shortest path over the hypersphere.
    def alignWith(self, other):
        return Quat(self.rtval.alignWith('Quat'))

    # Returns the angle of this quaternion (in radians)
    def getAngle(self):
        return self.rtval.getAngle('Scalar')

    # Returns the X axis of this quaternion
    def getXaxis(self):
        return Vec3(self.rtval.getXaxis('Vec3'))

    # Returns the Y axis of this quaternion
    def getYaxis(self):
        return Vec3(self.rtval.getYaxis('Vec3'))

    # Returns the Z axis of this quaternion
    def getZaxis(self):
        return Vec3(self.rtval.getZaxis('Vec3'))

    # Reflects this Quaternion according to the axis provided.
    # \param axisIndex An integer with value of 0 for the X axis, 1 for the Y axis, and 2 for the Z axis.
    def mirror(self, axisIndex):
        return Vec3(self.rtval.mirror('Vec3', KS.inst().rtVal('Integer', axisIndex)))

    # Returns this quaternion as a 3x3 rotation matrix
    def toMat33(self):
        return Mat33(self.rtval.toMat33('Mat33'))

    # Returns this quaternion as a Euler rotation
    # giving a rotation order
    def toEuler(self, rotationOrder ):
        return Euler(self.rtval.toEuler('Euler', KS.inst().rtVal('RotationOrder', rotationOrder)))

    # Returns this quaternion as a Euler angles using the rotationorder XYZ
    def toEulerAngles(self, order):
        return Vec3(self.rtval.toEulerAngles('Vec3', KS.inst().rtVal('RotationOrder', rotationOrder)))

    # Returns this quaternion as a Euler angles using the rotationorder XYZ
    def toEulerAngles():
        return Vec3(self.rtval.toEulerAngles('Vec3'))

    # interpolates two quaternions spherically (slerp)
    # given a scalar blend value (0.0 to 1.0).
    # \note this and q2 should be unit Quaternions
    def sphericalLinearInterpolate(self, q2, t):
        return Quat(self.rtval.sphericalLinearInterpolate('Quat', KS.inst().rtVal('Quat', q2), KS.inst().rtVal('Scalar', t)))

    # Interpolates two quaternions lineally (lerp)
    # with a given blend value (0.0 to 1.0).
    # \note The interpolation of the 2 quaternions will result acceleration and deceleration. Use :kl-ref:`sphericalLinearInterpolate` for an interpolation that does not introduce acceleration.
    def linearInterpolate(self, other, t):
        return Quat(self.rtval.sphericalLinearInterpolate('Quat', KS.inst().rtVal('Quat', q2), KS.inst().rtVal('Scalar', t)))


