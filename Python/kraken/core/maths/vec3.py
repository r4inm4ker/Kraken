"""Kraken - maths.vec3 module.

Classes:
Vec3 -- Vector 3 object.
"""

import math
from kraken.core.kraken_system import ks
from math_object import MathObject


class Vec3(MathObject):
    """Vector 3 object."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initializes x, y, z values for Vec3 object."""

        super(Vec3, self).__init__()
        if ks.getRTValTypeName(x) == 'Vec3':
            self._rtval = x
        else:
            self._rtval = ks.rtVal('Vec3')
            if isinstance(x, Vec3):
                self.set(x=x.x, y=x.y, z=x.z)
            else:
                self.set(x=x, y=y, z=z)


    def __str__(self):
        """String representation of the Vec3 object.

        Returns:
            str: String representation of the Vec3 object.

        """

        return "Vec3(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"


    @property
    def x(self):
        """Gets x value of this vector.

        Returns:
            float: X value of this vector.

        """

        return self._rtval.x.getSimpleType()


    @x.setter
    def x(self, value):
        """Sets x value from the input value.

        Args:
            value (float): Value to set the x property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.x = ks.rtVal('Scalar', value)

        return True


    @property
    def y(self):
        """Gets y value of this vector.

        Returns:
            float: Y value of this vector.

        """

        return self._rtval.y.getSimpleType()


    @y.setter
    def y(self, value):
        """Sets y value from the input value.

        Args:
            value (float): Value to set the y property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.y = ks.rtVal('Scalar', value)


    @property
    def z(self):
        """Gets z value of this vector.

        Returns:
            float: Z value of this vector.

        """

        return self._rtval.z.getSimpleType()


    @z.setter
    def z(self, value):
        """Sets y value from the input value.

        Args:
            value (float): Value to set the y property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.z = ks.rtVal('Scalar', value)

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
        """Returns a clone of the Vec3.

        Returns:
            Vec3: The cloned Vec3

        """

        vec3 = Vec3()
        vec3.x = self.x
        vec3.y = self.y
        vec3.z = self.z

        return vec3


    def set(self, x, y, z):
        """Sets the x, y, and z value from the input values.

        Args:
            x (float): Value to set the x property as.
            y (float): Value to set the x property as.
            z (float): Value to set the z property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.set('', ks.rtVal('Scalar', x), ks.rtVal('Scalar', y), ks.rtVal('Scalar', z))

        return True


    def setNull():
        """Setting all components of the vec3 to 0.0.

        Returns:
            bool: True if successful.

        """

        self._rtval.setNull('')

        return True


    def equal(self, other):
        """Checks equality of this vec3 with another.

        Args:
            other (Vec3): other vector to check equality with.

        Returns:
            bool: True if equal.

        """

        return self._rtval.equal('Boolean', other._rtval).getSimpleType()


    def almostEqual(self, other, precision):
        """Checks almost equality of this Vec3 with another.

        Args:
            other (Vec3): other matrix to check equality with.
            precision (float): Precision value.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', other._rtval, ks.rtVal('Scalar', precision)).getSimpleType()


    def almostEqual(self, other):
        """Checks almost equality of this Vec3 with another
        (using a default precision).

        Args:
            other (Vec3): other vector to check equality with.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', other._rtval).getSimpleType()


    def component(self, i):
        """Gets the component of this Vec3 by index.

        Args:
            i (int): index of the component to return.

        Returns:
            float: Component of this Vec3.

        """

        return self._rtval.component('Scalar', ks.rtVal('Size', i)).getSimpleType()


    # Sets the component of this vector by index
    def setComponent(self, i, v):
        """Sets the component of this Vec3 by index.

        Args:
            i (int): index of the component to set.
            v (float): Value to set component as.

        Returns:
            bool: True if successful.

        """

        self._rtval.setComponent('', ks.rtVal('Size', i),
                                        ks.rtVal('Scalar', v))


    def add(self, other):
        """Overload method for the add operator.

        Args:
            other (Vec3): other vector to add to this one.

        Returns:
            Vec3: New Vec3 of the sum of the two Vec3's.

        """

        return Vec3(self._rtval.add('Vec3', other._rtval))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Args:
            other (Vec3): other vector to subtract from this one.

        Returns:
            Vec3: New Vec3 of the difference of the two Vec3's.

        """

        return Vec3(self._rtval.subtract('Vec3', other._rtval))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Args:
            other (Vec3): other vector to multiply from this one.

        Returns:
            Vec3: New Vec3 of the product of the two Vec3's.

        """

        return Vec3(self._rtval.multiply('Vec3', other._rtval))


    def divide(self, other):
        """Divides this vector and an other.

        Args:
            other (Vec3): other vector to divide by.

        Returns:
            Vec3: Quotient of the division of this vector by the other.

        """

        return Vec3(self._rtval.divide('Vec3', other._rtval))


    def multiplyScalar(self, other):
        """Product of this vector and a scalar.

        Args:
            other (float): Scalar value to multiply this vector by.

        Returns:
            Vec3: Product of the multiplication of the scalar and this vector.

        """

        return Vec3(self._rtval.multiplyScalar('Vec3', ks.rtVal('Scalar', other)))


    def divideScalar(self, other):
        """Divides this vector and a scalar.

        Args:
            other (float): Value to divide this vector by.

        Returns:
            Vec3: Quotient of the division of the vector by the scalar.

        """

        return Vec3(self._rtval.divideScalar('Vec3', ks.rtVal('Scalar', other)))


    def negate(self):
        """Gets the negated version of this vector.

        Returns:
            Vec3: Negation of this vector.

        """

        return Vec3(self._rtval.negate('Vec3'))


    def inverse(self):
        """Get the inverse vector of this vector.

        Returns:
            Vec3: Inverse of this vector.

        """

        return Vec3(self._rtval.inverse('Vec3'))


    def dot(self, other):
        """Gets the dot product of this vector and another.

        Args:
            other (Vec3): Other vector.

        Returns:
            float: Dot product.

        """

        return self._rtval.dot('Scalar', other._rtval).getSimpleType()


    def cross(self, other):
        """Gets the cross product of this vector and another.

        Args:
            other (Vec3): Other vector.

        Returns:
            Vec3: Dot product.

        """

        return Vec3(self._rtval.cross('Vec3', other._rtval))


    def lengthSquared(self):
        """Get the squared length of this vector.

        Returns:
            float: Squared length oft his vector.

        """

        return self._rtval.lengthSquared('Scalar').getSimpleType()


    def length(self):
        """Gets the length of this vector.

        Returns:
            float: Length of this vector.

        """

        return self._rtval.length('Scalar').getSimpleType()


    def unit(self):
        """Gets a unit vector of this one.

        Returns:
            Vec3: New unit vector from this one.

        """

        return Vec3(self._rtval.unit('Vec3'))


    def unit_safe(self):
        """Gets a unit vector of this one, no error reported if cannot be
        made unit.

        Returns:
            Vec3: New unit vector.

        """

        return Vec3(self._rtval.unit_safe('Vec3'))


    def setUnit(self):
        """Sets this vector to a unit vector and returns the previous
        length.

        Returns:
            float: This vector.

        """

        return self._rtval.setUnit('Scalar').getSimpleType()


    def normalize(self):
        """Gets a normalized vector from this vector.

        Returns:
            float: Previous length.

        """

        return self._rtval.normalize('Scalar').getSimpleType()


    def clamp(self, min, max):
        """Clamps this vector per component by a min and max vector.

        Args:
            min (float): Minimum value.
            max (float): Maximum value.

        Returns:
            bool: True if successful.

        """

        return Vec3(self._rtval.clamp('Vec3', min._rtval, max._rtval))


    def unitsAngleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one
        note expects both vectors to be units (else use angleTo)

        Args:
            other (Vec3): other vector to get angle to.

        Returns:
            float: Angle.

        """

        return self._rtval.unitsAngleTo('Scalar', other._rtval).getSimpleType()


    def angleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one.

        Args:
            other (Vec3): other vector to get angle to.

        Returns:
            float: Angle.

        """

        return self._rtval.angleTo('Scalar', other._rtval).getSimpleType()


    # Returns the distance of this vector to another one
    def distanceTo(self, other):
        """Doc String.

        Args:
            other (Vec3): the other vector to measure the distance to.

        Returns:
            bool: True if successful.

        """

        return self._rtval.distanceTo('Scalar', other._rtval).getSimpleType()


    def linearInterpolate(self, other, t):
        """Linearly interpolates this vector with another one based on a scalar
        blend value (0.0 to 1.0).

        Args:
            other (Vec3): vector to blend to.
            t (float): Blend value.

        Returns:
            Vec3: New vector blended between this and the input vector.

        """

        return Vec3(self._rtval.linearInterpolate('Vec3', ks.rtVal('Scalar', t)))


    def distanceToLine(self, lineP0, lineP1):
        """Returns the distance of this vector to a line defined by two points
        on the line.

        Args:
            lineP0 (Vec3): point 1 of the line.
            lineP1 (Vec3): point 2 of the line.

        Returns:
            float: Distance to the line.

        """

        return self._rtval.distanceToLine('Scalar', lineP0._rtval, lineP1._rtval).getSimpleType()


    def distanceToSegment(self, segmentP0, segmentP1):
        """Returns the distance of this vector to a line segment defined by the
        start and end points of the line segment

        Args:
            segmentP0 (Vec3): point 1 of the segment.
            segmentP1 (Vec3): point 2 of the segment.

        Returns:
            float: Distance to the segment.

        """

        return self._rtval.distanceToSegment('Scalar', segmentP0._rtval, segmentP1._rtval).getSimpleType()