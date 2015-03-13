"""Kraken - maths.quat module.

Classes:
Quat -- Quaternion rotation.
"""

import math
from kraken.core.kraken_system import ks
from math_object import MathObject

from vec3 import Vec3
from euler import Euler
from mat33 import Mat33


class Quat(MathObject):
    """Quaternion Rotation object."""

    def __init__(self, v=None, w=None):
        """Initializes the Quaternion."""

        super(Quat, self).__init__()

        if ks.getRTValTypeName(v) == 'Quat':
            self._rtval = v
        else:
            if v is not None and not isinstance(v, Vec3) and  not isinstance(v, Euler):
                raise TypeError("Quat: Invalid type for 'v' argument. Must be a Vec3.")

            if w is not None and not isinstance(w, (int, float)):
                raise TypeError("Quat: Invalid type for 'w' argument. Must be a int or float.")

            self._rtval = ks.rtVal('Quat')
            if v is not None and isinstance(v, Euler):
                self.setFromEuler(v)
            if v is not None and w is not None:
                self.set(v=v, w=w)


    def __str__(self):
        """Return string version of the Quat object."""

        return "Quat(" + str(self.v) + "," + str(self.w) + ")"


    @property
    def v(self):
        """Gets vector of this quaternion.

        Return:
        Vec3, vector of the quaternion.

        """

        return Vec3(self._rtval.v)


    @v.setter
    def v(self, value):
        """Sets vector property from the input vector.

        Arguments:
        value -- Vec3, vector to set quaternion vector as.

        Return:
        True if successful.

        """

        self._rtval.v = ks.rtVal('Vec3', value)

        return True


    @property
    def w(self):
        """Gets scalar of this quaternion.

        Return:
        Scalar, scalar value of the quaternion.

        """

        return self._rtval.w


    @w.setter
    def w(self, value):
        """Sets scalar property from the input scalar.

        Arguments:
        value -- Scalar, value to set quaternion scalar as.

        Return:
        True if successful.

        """

        self._rtval.w = ks.rtVal('Scalar', value)

        return True

    def clone(self):
        """Returns a clone of the Quat.

        Return:
        The cloned Quat

        """

        quat = Quat();
        quat.w = self.w;
        quat.v = self.v.clone();

        return quat


    def set(self, v, w):
        """Sets the quaternion from vector and scalar values.

        Arguments:
        v -- Vec3, vector value.
        w -- Scalar, scalar value.

        Return:
        True if successful.

        """

        self._rtval.set('', ks.rtVal('Vec3', v), ks.rtVal('Scalar', w))

        return True


    def setIdentity():
        """Sets this quaternion to the identity.

        Return:
        True if successful.

        """

        self._rtval.setIdentity('')

        return True


    # Set this quat from a euler rotation
    def setFromEuler(self, e):
        """Sets the quaternion from a euler rotation.

        Arguments:
        e -- Euler, euler rotation used to set the quaternion.

        Return:
        Quat, new quaternion set from the euler argument.

        """

        return Quat(self._rtval.setFromEuler('Quat', ks.rtVal('Euler', e)))


    def setFromEulerAngles(self, angles, ro):
        """Sets this quat to a given angles vector (in radians) and a rotation order.

        Arguments:
        angles -- Vec3, angle vector.
        ro -- RotationOrder, roation order to use.

        Return:
        Quat, new quaternion set from angles vector and rotation order.

        """

        return Quat(self._rtval.setFromEuler('Quat', ks.rtVal('Vec3', angles), ks.rtVal('RotationOrder', ro)))


    def setFromEulerAngles(self, angles):
        """Sets this quat to a given angles vector (in radians) using
        the default XYZ rotation order.

        Arguments:
        angles -- Vec3, angle vector.

        Return:
        Quat, new quaternion set from angles vector.

        """

        return Quat(self._rtval.setFromEuler('Quat', ks.rtVal('Vec3', angles)))


    def setFromAxisAndAngle(self, axis, angle):
        """Set this quat to a rotation defined by an axis and an angle
        (in radians).

        Arguments:
        axis -- Vec3, vector axis.
        angle -- Scalar, angle value.

        Return:
        Quat, set from axis and angle values.

        """

        return Quat(self._rtval.setFromAxisAndAngle('Quat', ks.rtVal('Vec3', axis), ks.rtVal('Scalar', angle)))


    def setFromMat33(self, mat):
        """Set this quat to the rotation described by a 3x3 rotation matrix.

        Arguments:
        mat -- Mat33, 3 x 3 matrix to set the quaternion from.

        Return:
        Quat, new quaternion set from input Mat33.

        """

        return Quat(self._rtval.setFromMat33('Quat', ks.rtVal('Mat33', mat)))


    def setFrom2Vectors(sourceDirVec, destDirVec, arbitraryIfAmbiguous=True):
        """Set the quaternion to the rotation required to rotate the source
        vector to the destination vector.

        Function taken from the 'Game Programming Gems' article
        'The Shortest Arc Quat' by Stan Melax, both vectors must be units.

        Arguments:
        sourceDirVec -- Vec3, source vector.
        destDirVec -- Vec3, destination vector.
        arbitraryIfAmbiguous -- Bool, arbitrary if ambiguous.

        Return:
        Quat, new quaternion set from 2 vectors.

        """

        return Quat(self._rtval.setFrom2Vectors('Quat', ks.rtVal('Vec3', sourceDirVec), ks.rtVal('Vec3', destDirVec), ks.rtVal('Boolean', arbitraryIfAmbiguous)))


    def setFromDirectionAndUpvector(self, direction, upvector):
        """Set the quat to represent the direction as the Z axis and the
        upvector pointing along the XY plane.

        Arguments:
        direction -- Vec3, direction vector.
        upvector -- Vec3, up direction vector.

        Return:
        Quat, new quaternion set from direction and up vector.

        """

        return Quat(self._rtval.setFromDirectionAndUpvector('Quat', ks.rtVal('Vec3', direction), ks.rtVal('Vec3', upvector)))


    def equal(self, other):
        """Checks equality of this Quat with another.

        Arguments:
        other -- Mat33, other matrix to check equality with.

        Return:
        True if equal.

        """

        return self._rtval.equal('Boolean', ks.rtVal('Quat', other))


    def almostEqual(self, other, precision):
        """Checks almost equality of this Quat with another.

        Arguments:
        other -- Mat33, other matrix to check equality with.
        precision -- Scalar, precision value.

        Return:
        True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', ks.rtVal('Quat', other), ks.rtVal('Scalar', precision))


    def almostEqual(self, other):
        """Checks almost equality of this Quat with another
        (using a default precision).

        Arguments:
        other -- Mat33, other matrix to check equality with.

        Return:
        True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', ks.rtVal('Quat', other))


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


    def add(self, other):
        """Overload method for the add operator.

        Arguments:
        other -- Quat, other quaternion to add to this one.

        Return:
        Quat, new Quat of the sum of the two Quat's.

        """

        return self._rtval.add('Quat', ks.rtVal('Quat', other))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Arguments:
        other -- Quat, other quaternion to subtract from this one.

        Return:
        Quat, new Quat of the difference of the two Quat's.

        """

        return Quat(self._rtval.subtract('Quat', ks.rtVal('Quat', other)))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Arguments:
        other -- Quat, other quaternion to multiply this one by.

        Return:
        Quat, new Quat of the product of the two Quat's.

        """

        return Quat(self._rtval.multiply('Quat', ks.rtVal('Quat', other)))


    def divide(self, other):
        """Divides this quaternion by another.

        Arguments:
        other -- Quat, quaternion to divide this quaternion by.

        Return:
        Quat, quotient of the division of the quaternion by the other quaternion.

        """

        return Quat(self._rtval.divide('Quat', ks.rtVal('Quat', other)))


    def multiplyScalar(self, other):
        """Product of this quaternion and a scalar.

        Arguments:
        other -- Scalar, scalar value to multiply this quaternion by.

        Return:
        Quat, product of the multiplication of the scalar and this quaternion.

        """

        return Quat(self._rtval.multiplyScalar('Quat', ks.rtVal('Scalar', other)))


    def divideScalar(self, other):
        """Divides this quaternion and a scalar.

        Arguments:
        other -- Scalar, value to divide this quaternion by.

        Return:
        Quat, quotient of the division of the quaternion by the scalar.

        """

        return Quat(self._rtval.divideScalar('Quat', ks.rtVal('Scalar', other)))


    def rotateVector(self, v):
        """Rotates a vector by this quaterion.
        Don't forget to normalize the quaternion unless you want axial
        translation as well as rotation..

        Arguments:
        v -- Vec3, vector to rotate.

        Return:
        Vec3, new vector rotated by this quaternion.

        """

        return Vec3(self._rtval.rotateVector('Vec3', ks.rtVal('Vec3', v)))


    def dot(self, other):
        """Gets the dot product of this quaternion and another.

        Arguments:
        other -- Quat, other quaternion.

        Return:
        Scalar, dot product.

        """

        return self._rtval.dot('Scalar', ks.rtVal('Quat', other))


    def conjugate(self):
        """Get the conjugate of this quaternion.

        Return:
        Quat, conjugate of this quaternion.

        """

        return self._rtval.conjugate('Quat')


    def lengthSquared(self):
        """Get the squared lenght of this quaternion.

        Return:
        Scalar, squared length oft his quaternion.

        """

        return self._rtval.lengthSquared('Scalar')


    def length(self):
        """Gets the length of this quaternion.

        Return:
        Scalar, length of this quaternion.

        """

        return self._rtval.length('Scalar')


    def unit(self):
        """Gets a unit quaternion of this one.

        Return:
        Quat, new unit quaternion from this one.

        """

        return Quat(self._rtval.unit('Quat'))


    def unit_safe(self):
        """Gets a unit quaternion of this one, no error reported if cannot be
        made unit.

        Return:
        Quat, new unit quaternion.

        """

        return Quat(self._rtval.unit_safe('Quat'))


    def setUnit(self):
        """Sets this quaternion to a unit quaternion and returns the previous
        length.

        Return:
        Quat, this quaternion.

        """

        return self._rtval.setUnit('Scalar')


    def inverse(self):
        """Gets an inverse quaternion of this one.

        Return:
        Quat, inverse quaternion to this one.

        """

        return Quat(self._rtval.inverse('Quat'))


    def alignWith(self, other):
        """Aligns this quaternion with another one ensuring that the delta
        between the Quat values is the shortest path over the hypersphere.

        Arguments:
        other -- Quat, quaternion to align this one with.

        Return:
        Quat, new quaternion aligned to the other.

        """

        return Quat(self._rtval.alignWith('Quat', ks.rtVal('Quat', other)))


    def getAngle(self):
        """Gets the angle of this quaternion (in radians).

        Return:
        Scalar, angle of this quaternion (in radians).

        """

        return self._rtval.getAngle('Scalar')


    def getXaxis(self):
        """Gets the X axis of this quaternion.

        Return:
        Vec3, x axis of this quaternion.

        """

        return Vec3(self._rtval.getXaxis('Vec3'))


    def getYaxis(self):
        """Gets the Y axis of this quaternion.

        Return:
        Vec3, y axis of this quaternion.

        """

        return Vec3(self._rtval.getYaxis('Vec3'))


    def getZaxis(self):
        """Gets the Z axis of this quaternion.

        Return:
        Vec3, z axis of this quaternion.

        """

        return Vec3(self._rtval.getZaxis('Vec3'))


    def mirror(self, axisIndex):
        """Reflects this Quaternion according to the axis provided.

        Arguments:
        axisIndex -- Integer, 0 for the X axis, 1 for the Y axis, and 2 for the Z axis.

        Return:
        Quat, mirrored quaternion.

        """

        return Quat(self._rtval.mirror('Quat', ks.rtVal('Integer', axisIndex)))


    def toMat33(self):
        """Gets this quaternion as a 3x3 matrix.

        Return:
        Mat33, matrix derived from this quaternion.

        """

        return Mat33(self._rtval.toMat33('Mat33'))


    def toEuler(self, rotationOrder):
        """Returns this quaternion as a Euler rotation giving a rotation order.

        Arguments:
        rotationOrder -- RotationOrder, rotation order to use to derive the
        euler by.

        Return:
        Euler, euler rotation derived from this quaternion.

        """

        return Euler(self._rtval.toEuler('Euler', ks.rtVal('RotationOrder', rotationOrder)))


    def toEulerAngles(self, order):
        """Gets this quaternion as a Euler angles using the rotationorder XYZ.

        Arguments:
        order -- RotationOrder, rotation order used to derive the euler angles.

        Return:
        Vec3, euler angles derived from this quaternion.

        """

        return Vec3(self._rtval.toEulerAngles('Vec3', ks.rtVal('RotationOrder', rotationOrder)))


    def toEulerAngles():
        """Gets this quaternion as a Euler angles using the rotationorder XYZ.

        Return:
        Vec3, euler angles derived from this quaternion.

        """

        return Vec3(self._rtval.toEulerAngles('Vec3'))


    def sphericalLinearInterpolate(self, q2, t):
        """Interpolates two quaternions spherically (slerp) given a scalar blend
        value (0.0 to 1.0).

        Note: This and q2 should be unit Quaternions.

        Arguments:
        q2 -- Quat, quaternion to blend to.
        t -- Scalar, blend value.

        Return:
        Quat, new quaternion blended between this and the input quaternion.

        """

        return Quat(self._rtval.sphericalLinearInterpolate('Quat', ks.rtVal('Quat', q2), ks.rtVal('Scalar', t)))


    def linearInterpolate(self, other, t):
        """Interpolates two quaternions lineally (lerp) with a given blend value
        (0.0 to 1.0).

        Note: The interpolation of the 2 quaternions will result acceleration and deceleration. Use :kl-ref:`sphericalLinearInterpolate` for an interpolation that does not introduce acceleration..

        Arguments:
        other -- Quat, quaternion to blend to.
        t -- Scalar, blend value.

        Return:
        Quat, new quaternion blended between this and the input quaternion.

        """

        return Quat(self._rtval.sphericalLinearInterpolate('Quat', ks.rtVal('Quat', q2), ks.rtVal('Scalar', t)))