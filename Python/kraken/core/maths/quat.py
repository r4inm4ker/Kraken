"""Kraken - maths.quat module.

Classes:
Quat -- Quaternion rotation.
"""

import math

from kraken.core.kraken_system import ks
from kraken.core.maths.math_object import MathObject

from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.euler import Euler
from kraken.core.maths.mat33 import Mat33


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
            if isinstance(v, Quat):
                self.set(v=v.v, w=v.w)
            elif isinstance(v, Euler):
                self.setFromEuler(v)
            elif v is not None and w is not None:
                self.set(v=v, w=w)


    def __str__(self):
        """Return string version of the Quat object.

        Returns:
            str: String representation of the Quat.

        """

        return "Quat(" + str(self.v) + "," + str(self.w) + ")"


    @property
    def v(self):
        """Gets vector of this quaternion.

        Returns:
            Vec3: Vector of the quaternion.

        """

        return Vec3(self._rtval.v)


    @v.setter
    def v(self, value):
        """Sets vector property from the input vector.

        Args:
            value (Vec3): vector to set quaternion vector as.

        Returns:
            bool: True if successful.

        """

        self._rtval.v = ks.rtVal('Vec3', value)

        return True


    @property
    def w(self):
        """Gets scalar of this quaternion.

        Returns:
            float: Scalar value of the quaternion.

        """

        return self._rtval.w.getSimpleType()


    @w.setter
    def w(self, value):
        """Sets scalar property from the input scalar.

        Args:
            value -- Scalar, value to set quaternion scalar as.

        Returns:
            bool: True if successful.

        """

        self._rtval.w = ks.rtVal('Scalar', value)

        return True


    def __eq__(self, other):
        return self.equal(other)

    def __ne__(self, other):
        return not self.equal(other)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __div__(self, other):
        return self.divide(other)


    def clone(self):
        """Returns a clone of the Quat.

        Returns:
            Quat: The cloned Quaternion.

        """

        quat = Quat()
        quat.w = self.w
        quat.v = self.v.clone()

        return quat


    def set(self, v, w):
        """Sets the quaternion from vector and scalar values.

        Args:
            v (Vec3): vector value.
            w (float): scalar value.

        Returns:
            bool: True if successful.

        """

        self._rtval.set('', ks.rtVal('Vec3', v), ks.rtVal('Scalar', w))

        return True


    def setIdentity():
        """Sets this quaternion to the identity.

        Returns:
            bool: True if successful.

        """

        self._rtval.setIdentity('')

        return True


    # Set this quat from a euler rotation
    def setFromEuler(self, e):
        """Sets the quaternion from a euler rotation.

        Args:
            e (Euler): Euler rotation used to set the quaternion.

        Returns:
            Quat: New quaternion set from the euler argument.

        """

        return Quat(self._rtval.setFromEuler('Quat', ks.rtVal('Euler', e)))


    def setFromEulerAngles(self, angles, ro):
        """Sets this quat to a given angles vector (in radians) and a rotation
        order.

        Args:
            angles (Vec3): Angle vector.
            ro (RotationOrder): Rotation order to use.

        Returns:
            Quat: New quaternion set from angles vector and rotation order.

        """

        return Quat(self._rtval.setFromEuler('Quat', ks.rtVal('Vec3', angles),
                    ks.rtVal('RotationOrder', ro)))


    def setFromEulerAngles(self, angles):
        """Sets this quat to a given angles vector (in radians) using
        the default XYZ rotation order.

        Args:
            angles (Vec3): angle vector.

        Returns:
            Quat: New quaternion set from angles vector.

        """

        return Quat(self._rtval.setFromEuler('Quat', ks.rtVal('Vec3', angles)))


    def setFromAxisAndAngle(self, axis, angle):
        """Set this quat to a rotation defined by an axis and an angle
        (in radians).

        Args:
            axis (Vec3): vector axis.
            angle (float): angle value.

        Returns:
            Quat: Set from axis and angle values.

        """

        return Quat(self._rtval.setFromAxisAndAngle('Quat', ks.rtVal('Vec3', axis),
                    ks.rtVal('Scalar', angle)))


    def setFromMat33(self, mat):
        """Set this quat to the rotation described by a 3x3 rotation matrix.

        Args:
            mat (Mat33): 3x3 matrix to set the quaternion from.

        Returns:
            Quat: New quaternion set from input Mat33.

        """

        return Quat(self._rtval.setFromMat33('Quat', ks.rtVal('Mat33', mat)))


    def setFrom2Vectors(sourceDirVec, destDirVec, arbitraryIfAmbiguous=True):
        """Set the quaternion to the rotation required to rotate the source
        vector to the destination vector.

        Function taken from the 'Game Programming Gems' article
        'The Shortest Arc Quat' by Stan Melax, both vectors must be units.

        Args:
            sourceDirVec (Vec3): Source vector.
            destDirVec (Vec3): Destination vector.
            arbitraryIfAmbiguous (bool): Arbitrary if ambiguous.

        Returns:
            Quat: New quaternion set from 2 vectors.

        """

        return Quat(self._rtval.setFrom2Vectors('Quat', ks.rtVal('Vec3', sourceDirVec),
                    ks.rtVal('Vec3', destDirVec), ks.rtVal('Boolean', arbitraryIfAmbiguous)))


    def setFromDirectionAndUpvector(self, direction, upvector):
        """Set the quat to represent the direction as the Z axis and the
        upvector pointing along the XY plane.

        Args:
            direction (Vec3): Direction vector.
            upvector (Vec3): Up direction vector.

        Returns:
            Quat: New quaternion set from direction and up vector.

        """

        return Quat(self._rtval.setFromDirectionAndUpvector('Quat',
                    ks.rtVal('Vec3', direction), ks.rtVal('Vec3', upvector)))


    def equal(self, other):
        """Checks equality of this Quat with another.

        Args:
            other (Mat33): other matrix to check equality with.

        Returns:
            bool: True if equal.

        """

        return self._rtval.equal('Boolean', ks.rtVal('Quat', other)).getSimpleType()


    def almostEqual(self, other, precision):
        """Checks almost equality of this Quat with another.

        Args:
            other (Mat33): other matrix to check equality with.
            precision (float): precision value.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', ks.rtVal('Quat', other),
                                       ks.rtVal('Scalar', precision)).getSimpleType()


    def almostEqual(self, other):
        """Checks almost equality of this Quat with another
        (using a default precision).

        Args:
            other (Mat33): other matrix to check equality with.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', ks.rtVal('Quat', other)).getSimpleType()


    def add(self, other):
        """Overload method for the add operator.

        Args:
            other (Quat): Other quaternion to add to this one.

        Returns:
            Quat: New Quat of the sum of the two Quat's.

        """

        return Quat(self._rtval.add('Quat', ks.rtVal('Quat', other)))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Args:
            other (Quat): Other quaternion to subtract from this one.

        Returns:
            Quat: New Quat of the difference of the two Quat's.

        """

        return Quat(self._rtval.subtract('Quat', ks.rtVal('Quat', other)))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Args:
            other (Quat): Other quaternion to multiply this one by.

        Returns:
            Quat: New Quat of the product of the two Quat's.

        """

        return Quat(self._rtval.multiply('Quat', ks.rtVal('Quat', other)))


    def divide(self, other):
        """Divides this quaternion by another.

        Args:
            other (Quat): Quaternion to divide this quaternion by.

        Returns:
            Quat: Quotient of the division of the quaternion by the other quaternion.

        """

        return Quat(self._rtval.divide('Quat', ks.rtVal('Quat', other)))


    def multiplyScalar(self, other):
        """Product of this quaternion and a scalar.

        Args:
            other (float): scalar value to multiply this quaternion by.

        Returns:
            Quat: Product of the multiplication of the scalar and this quaternion.

        """

        return Quat(self._rtval.multiplyScalar('Quat', ks.rtVal('Scalar', other)))


    def divideScalar(self, other):
        """Divides this quaternion and a scalar.

        Args:
            other (float): value to divide this quaternion by.

        Returns:
            Quat: Quotient of the division of the quaternion by the scalar.

        """

        return Quat(self._rtval.divideScalar('Quat', ks.rtVal('Scalar', other)))


    def rotateVector(self, v):
        """Rotates a vector by this quaterion.
        Don't forget to normalize the quaternion unless you want axial
        translation as well as rotation..

        Args:
            v (Vec3): vector to rotate.

        Returns:
            Vec3: New vector rotated by this quaternion.

        """

        return Vec3(self._rtval.rotateVector('Vec3', ks.rtVal('Vec3', v)))


    def dot(self, other):
        """Gets the dot product of this quaternion and another.

        Args:
            other (Quat): Other quaternion.

        Returns:
            float: Dot product.

        """

        return self._rtval.dot('Scalar', ks.rtVal('Quat', other)).getSimpleType()


    def conjugate(self):
        """Get the conjugate of this quaternion.

        Returns:
            Quat: Conjugate of this quaternion.

        """

        return Quat(self._rtval.conjugate('Quat'))


    def lengthSquared(self):
        """Get the squared lenght of this quaternion.

        Returns:
            float: Squared length oft his quaternion.

        """

        return self._rtval.lengthSquared('Scalar').getSimpleType()


    def length(self):
        """Gets the length of this quaternion.

        Returns:
            float: Length of this quaternion.

        """

        return self._rtval.length('Scalar').getSimpleType()


    def unit(self):
        """Gets a unit quaternion of this one.

        Returns:
            Quat: New unit quaternion from this one.

        """

        return Quat(self._rtval.unit('Quat'))


    def unit_safe(self):
        """Gets a unit quaternion of this one, no error reported if cannot be
        made unit.

        Returns:
            Quat: New unit quaternion.

        """

        return Quat(self._rtval.unit_safe('Quat'))


    def setUnit(self):
        """Sets this quaternion to a unit quaternion and returns the previous
        length.

        Returns:
            Quat: This quaternion.

        """

        return self._rtval.setUnit('Scalar').getSimpleType()


    def inverse(self):
        """Gets an inverse quaternion of this one.

        Returns:
            Quat: Inverse quaternion to this one.

        """

        return Quat(self._rtval.inverse('Quat'))


    def alignWith(self, other):
        """Aligns this quaternion with another one ensuring that the delta
        between the Quat values is the shortest path over the hypersphere.

        Args:
            other (Quat): Quaternion to align this one with.

        Returns:
            Quat: New quaternion aligned to the other.

        """

        return Quat(self._rtval.alignWith('Quat', ks.rtVal('Quat', other)))


    def getAngle(self):
        """Gets the angle of this quaternion (in radians).

        Returns:
            float: Angle of this quaternion (in radians).

        """

        return self._rtval.getAngle('Scalar').getSimpleType()


    def getXaxis(self):
        """Gets the X axis of this quaternion.

        Returns:
            Vec3: X axis of this quaternion.

        """

        return Vec3(self._rtval.getXaxis('Vec3'))


    def getYaxis(self):
        """Gets the Y axis of this quaternion.

        Returns:
            Vec3: Y axis of this quaternion.

        """

        return Vec3(self._rtval.getYaxis('Vec3'))


    def getZaxis(self):
        """Gets the Z axis of this quaternion.

        Returns:
            Vec3: Z axis of this quaternion.

        """

        return Vec3(self._rtval.getZaxis('Vec3'))


    def mirror(self, axisIndex):
        """Reflects this Quaternion according to the axis provided.

        Args:
            axisIndex (int): 0 for the X axis, 1 for the Y axis, and 2 for the Z axis.

        Returns:
            Quat: Mirrored quaternion.

        """

        return Quat(self._rtval.mirror('Quat', ks.rtVal('Integer', axisIndex)))


    def toMat33(self):
        """Gets this quaternion as a 3x3 matrix.

        Returns:
            Mat33: Matrix derived from this quaternion.

        """

        return Mat33(self._rtval.toMat33('Mat33'))


    def toEuler(self, rotationOrder):
        """Returns this quaternion as a Euler rotation giving a rotation order.

        Args:
            rotationOrder (RotationOrder): rotation order to use to derive the euler by.

        Returns:
            Euler: Euler rotation derived from this quaternion.

        """

        return Euler(self._rtval.toEuler('Euler', ks.rtVal('RotationOrder', rotationOrder)))


    def toEulerAngles(self, order):
        """Gets this quaternion as a Euler angles using the rotationorder XYZ.

        Args:
            order (RotationOrder): rotation order used to derive the euler angles.

        Returns:
            Vec3: Euler angles derived from this quaternion.

        """

        return Vec3(self._rtval.toEulerAngles('Vec3', ks.rtVal('RotationOrder', rotationOrder)))


    def toEulerAngles():
        """Gets this quaternion as a Euler angles using the rotationorder XYZ.

        Returns:
            Vec3: Euler angles derived from this quaternion.

        """

        return Vec3(self._rtval.toEulerAngles('Vec3'))


    def sphericalLinearInterpolate(self, q2, t):
        """Interpolates two quaternions spherically (slerp) given a scalar blend
        value (0.0 to 1.0).

        Note: This and q2 should be unit Quaternions.

        Args:
            q2 (Quat): Quaternion to blend to.
            t (float): blend value.

        Returns:
            Quat: New quaternion blended between this and the input quaternion.

        """

        return Quat(self._rtval.sphericalLinearInterpolate('Quat',
                    ks.rtVal('Quat', q2), ks.rtVal('Scalar', t)))


    def linearInterpolate(self, other, t):
        """Interpolates two quaternions lineally (lerp) with a given blend value
        (0.0 to 1.0).

        Note: The interpolation of the 2 quaternions will result acceleration
        and deceleration. Use `sphericalLinearInterpolate` for an
        interpolation that does not introduce acceleration..

        Args:
            other (Quat): Quaternion to blend to.
            t (float): blend value.

        Returns:
            Quat: New quaternion blended between this and the input quaternion.

        """

        return Quat(self._rtval.sphericalLinearInterpolate('Quat', ks.rtVal('Quat', q2), ks.rtVal('Scalar', t)))
