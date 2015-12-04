"""Kraken - maths.vec4 module.

Classes:
Vec4 -- Vector 4 object.
"""

import math
from kraken.core.kraken_system import ks
from math_object import MathObject


class Vec4(MathObject):
    """Vector 4 object."""

    def __init__(self, x=0.0, y=0.0, z=0.0, t=0.0):
        """Initializes x, y z and t values for Vec4 object."""

        super(Vec4, self).__init__()
        if ks.getRTValTypeName(x) == 'Vec4':
            self._rtval = x
        else:
            self._rtval = ks.rtVal('Vec4')
            if isinstance(x, Vec4):
                self.set(x=x.x, y=x.y, z=x.z, t=x.z)
            else:
                self.set(x=x, y=y, z=z, t=t)


    def __str__(self):
        """String representation of the Vec4 object.

        Returns:
            str: String representation of the Vec4 object."""

        stringRep = "Vec4("
        stringRep += str(self.x) + ","
        stringRep += str(self.y) + ","
        stringRep += str(self.z) + ","
        stringRep += str(self.t) + ")"

        return stringRep


    @property
    def x(self):
        """Gets x value of this vector.

        Returns:
            float: x value of this vector.

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
            float: y value of this vector.

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

        return True


    @property
    def z(self):
        """Gets z value of this vector.

        Returns:
            float: z value of this vector.

        """

        return self._rtval.z.getSimpleType()


    @z.setter
    def z(self, value):
        """Sets z value from the input value.

        Args:
            value (float): Value to set the z property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.z = ks.rtVal('Scalar', value)

        return True


    @property
    def t(self):
        """Gets t value of this vector.

        Returns:
            float: t value of this vector.

        """

        return self._rtval.t.getSimpleType()


    @t.setter
    def t(self, value):
        """Sets t value from the input value.

        Args:
            value (float): Value to set the t property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.t = ks.rtVal('Scalar', value)


    def clone(self):
        """Returns a clone of the Vec4.

        Returns:
            Vec4: The cloned Vec4

        """

        vec4 = Vec4();
        vec4.x = self.x;
        vec4.y = self.y;
        vec4.z = self.z;
        vec4.t = self.t;
        return vec4


    def set(self, x, y, z, t):
        """Sets the x, y, z, and t value from the input values.

        Args:
            x (float): Value to set the x property as.
            y (float): Value to set the y property as.
            z (float): Value to set the z property as.
            t (float): Value to set the t property as.

        Returns:
            bool: True if successful.

        """

        self._rtval.set('', ks.rtVal('Scalar', x), ks.rtVal('Scalar', y),
                        ks.rtVal('Scalar', z), ks.rtVal('Scalar', t))

        return True


    def setNull():
        """Setting all components of the vec4 to 0.0.

        Returns:
            bool: True if successful.

        """

        self._rtval.setNull('')

        return True


    def equal(self, other):
        """Checks equality of this vec4 with another.

        Args:
            other (Vec4): other vector to check equality with.

        Returns:
            bool: True if equal.

        """

        return self._rtval.set('Boolean', other._rtval).getSimpleType()


    def almostEqual(self, other, precision):
        """Checks almost equality of this Vec4 with another.

        Args:
            other (Vec4): other value to check equality with.
            precision (float): Precision value.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', other._rtval,
                                       ks.rtVal('Scalar', precision)).getSimpleType()


    def almostEqual(self, other):
        """Checks almost equality of this Vec4 with another
        (using a default precision).

        Args:
            other (Vec4): other vector to check equality with.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', other._rtval).getSimpleType()


    def component(self, i ):
        """Gets the component of this Vec4 by index.

        Args:
            i (int): index of the component to return.

        Returns:
            float: component of this Vec4.

        """

        return self._rtval.component('Scalar', ks.rtVal('Size', i)).getSimpleType()


    def setComponent(self, i, v ):
        """Sets the component of this Vec4 by index.

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
            other (Vec4): other vector to add to this one.

        Returns:
            Vec4: New Vec4 of the sum of the two Vec4's.

        """

        return Vec4(self._rtval.add('Vec4', other._rtval))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Args:
            other (Vec4): other vector to subtract from this one.

        Returns:
            Vec4: New Vec4 of the difference of the two Vec4's.

        """

        return Vec4(self._rtval.subtract('Vec4', other._rtval))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Args:
            other (Vec4): other vector to multiply from this one.

        Returns:
            Vec4: New Vec4 of the product of the two Vec4's.

        """

        return Vec4(self._rtval.multiply('Vec4', other._rtval))


    def divide(self, other):
        """Divides this vector and an other.

        Args:
            other (Vec4): other vector to divide by.

        Returns:
            Vec4: Quotient of the division of this vector by the other.

        """

        return Vec4(self._rtval.divide('Vec4', other._rtval))


    def multiplyScalar(self, other):
        """Product of this vector and a scalar.

        Args:
            other (float): Scalar value to multiply this vector by.

        Returns:
            Vec4: Product of the multiplication of the scalar and this vector.

        """

        return Vec4(self._rtval.multiplyScalar('Vec4', ks.rtVal('Scalar', other)))


    def divideScalar(self, other):
        """Divides this vector and a scalar.

        Args:
            other (float): Value to divide this vector by.

        Returns:
            Vec4: Quotient of the division of the vector by the scalar.

        """

        return Vec4(self._rtval.divideScalar('Vec4', ks.rtVal('Scalar', other)))


    def negate(self):
        """Gets the negated version of this vector.

        Returns:
            Vec4: Negation of this vector.

        """

        return Vec4(self._rtval.negate('Vec4'))


    def inverse(self):
        """Get the inverse vector of this vector.

        Returns:
            Vec4: Inverse of this vector.

        """

        return Vec4(self._rtval.inverse('Vec4'))


    def dot(self, other):
        """Gets the dot product of this vector and another.

        Args:
            other (Vec4): other vector.

        Returns:
            float: dot product.

        """

        return self._rtval.dot('Scalar', other._rtval).getSimpleType()


    def cross(self, other):
        """Gets the cross product of this vector and another.

        Args:
            other (Vec4): other vector.

        Returns:
            Vec4: Dot product.

        """

        return Vec4(self._rtval.cross('Vec4', other._rtval))


    def lengthSquared(self):
        """Get the squared length of this vector.

        Returns:
            float: squared length oft his vector.

        """

        return self._rtval.lengthSquared('Scalar').getSimpleType()


    def length(self):
        """Gets the length of this vector.

        Returns:
            float: length of this vector.

        """

        return self._rtval.length('Scalar').getSimpleType()


    def unit(self):
        """Gets a unit vector of this one.

        Returns:
            Vec4: New unit vector from this one.

        """

        return Vec4(self._rtval.unit('Vec4'))


    def unit_safe(self):
        """Gets a unit vector of this one, no error reported if cannot be
        made unit.

        Returns:
            Vec4: New unit vector.

        """

        return Vec4(self._rtval.unit_safe('Vec4'))


    def setUnit(self):
        """Sets this vector to a unit vector and returns the previous
        length.

        Returns:
            float: this vector.

        """

        return self._rtval.setUnit('Scalar').getSimpleType()


    def normalize(self):
        """Gets a normalized vector from this vector.

        Returns:
            float: previous length.

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

        return Vec4(self._rtval.clamp('Vec4', min._rtval, max._rtval))


    def unitsAngleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one
        note expects both vectors to be units (else use angleTo)

        Args:
            other (Vec4): other vector to get angle to.

        Returns:
            float: angle.

        """

        return self._rtval.unitsAngleTo('Scalar', other._rtval).getSimpleType()


    def angleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one.

        Args:
            other (Vec4): other vector to get angle to.

        Returns:
            float: angle.

        """

        return self._rtval.angleTo('Scalar', other._rtval).getSimpleType()


    # Returns the distance of this vector to another one
    def distanceTo(self, other):
        """Doc String.

        Args:
            other (Vec4): the other vector to measure the distance to.

        Returns:
            bool: True if successful.

        """

        return self._rtval.distanceTo('Scalar', other._rtval).getSimpleType()


    def linearInterpolate(self, other, t):
        """Linearly interpolates this vector with another one based on a scalar
        blend value (0.0 to 1.0).

        Args:
            other (Vec4): vector to blend to.
            t (float): Blend value.

        Returns:
            Vec4: New vector blended between this and the input vector.

        """

        return Vec4(self._rtval.linearInterpolate('Vec4', ks.rtVal('Scalar', t)))


    def distanceToLine(self, lineP0, lineP1):
        """Returns the distance of this vector to a line defined by two points
        on the line.

        Args:
            lineP0 (Vec4): point 1 of the line.
            lineP1 (Vec4): point 2 of the line.

        Returns:
            float: distance to the line.

        """

        return self._rtval.distanceToLine('Scalar', lineP0._rtval, lineP1._rtval).getSimpleType()


    def distanceToSegment(self, segmentP0, segmentP1):
        """Returns the distance of this vector to a line segment defined by the
        start and end points of the line segment

        Args:
            segmentP0 (Vec4): point 1 of the segment.
            segmentP1 (Vec4): point 2 of the segment.

        Returns:
            float: distance to the segment.

        """

        return self._rtval.distanceToSegment('Scalar', segmentP0._rtval, segmentP1._rtval).getSimpleType()
