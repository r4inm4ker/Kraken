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
        """String representation of the Vec3 object."""

        return "Vec3(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"


    @property
    def x(self):
        """Gets x value of this vector.

        Return:
        Scalar, x value of this vector.

        """

        return self._rtval.x


    @x.setter
    def x(self, value):
        """Sets x value from the input value.

        Arguments:
        value -- Scalar, value to set the x property as.

        Return:
        True if successful.

        """

        self._rtval.x = ks.rtVal('Scalar', value)

        return True


    @property
    def y(self):
        """Gets y value of this vector.

        Return:
        Scalar, y value of this vector.

        """

        return self._rtval.y


    @y.setter
    def y(self, value):
        """Sets y value from the input value.

        Arguments:
        value -- Scalar, value to set the y property as.

        Return:
        True if successful.

        """

        self._rtval.y = ks.rtVal('Scalar', value)


    @property
    def z(self):
        """Gets z value of this vector.

        Return:
        Scalar, z value of this vector.

        """

        return self._rtval.z


    @z.setter
    def z(self, value):
        """Sets y value from the input value.

        Arguments:
        value -- Scalar, value to set the y property as.

        Return:
        True if successful.

        """

        self._rtval.z = ks.rtVal('Scalar', value)

        return True


    def clone(self):
        """Returns a clone of the Vec3.

        Return:
        The cloned Vec3

        """

        vec3 = Vec3();
        vec3.x = self.x;
        vec3.y = self.y;
        vec3.z = self.z;

        return vec3


    def set(self, x, y, z):
        """Sets the x, y, and z value from the input values.

        Arguments:
        x -- Scalar, value to set the x property as.
        y -- Scalar, value to set the x property as.
        z -- Scalar, value to set the z property as.

        Return:
        True if successful.

        """

        self._rtval.set('', ks.rtVal('Scalar', x), ks.rtVal('Scalar', y), ks.rtVal('Scalar', z))

        return True


    def setNull():
        """Setting all components of the vec3 to 0.0.

        Return:
        True if successful.

        """

        self._rtval.setNull('')

        return True


    def equal(self, other):
        """Checks equality of this vec3 with another.

        Arguments:
        other -- Vec3, other vector to check equality with.

        Return:
        True if equal.

        """

        return self._rtval.set('Boolean', other._rtval)


    def almostEqual(self, other, precision):
        """Checks almost equality of this Vec3 with another.

        Arguments:
        other -- Vec3, other matrix to check equality with.
        precision -- Scalar, precision value.

        Return:
        True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', other._rtval, ks.rtVal('Scalar', precision))


    def almostEqual(self, other):
        """Checks almost equality of this Vec3 with another
        (using a default precision).

        Arguments:
        other -- Vec3, other vector to check equality with.

        Return:
        True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', other._rtval)


    def component(self, i):
        """Gets the component of this Vec3 by index.

        Arguments:
        i -- Integer, index of the component to return.

        Return:
        Scalar, component of this Vec3.

        """

        return self._rtval.component('Scalar', ks.rtVal('Size', i))


    # Sets the component of this vector by index
    def setComponent(self, i, v):
        """Sets the component of this Vec3 by index.

        Arguments:
        i -- Integer, index of the component to set.
        v -- Scalar, value to set component as.

        Return:
        True if successful.

        """

        return self._rtval.setComponent('', ks.rtVal('Size', i),
                                        ks.rtVal('Scalar', v))


    # # Equals operator
    # def Boolean == (Vec a, Vec b):

    # # Not equals operator
    # def Boolean != (Vec a, Vec b):

    # # unary -
    # def Vec -Vec():

    # # Adds to vectors
    # def Vec + (Vec a, Vec b):

    # # Adds a vector to this one
    # def  += (Vec other):

    # # Subtracts two vectors
    # def Vec - (Vec a, Vec b):

    # # Subtracts a vector from this one
    # def  -= (Vec other):

    # # Multiplies a scalar and a vector
    # def Vec * (Scalar a, Vec b):

    # # Multiplies a vector and a scalar
    # def Vec * (Vec a, Scalar b):

    # # Multiplies two vectors
    # def Vec * (Vec a, Vec b):


    # # Multiplies this vector with a scalar
    # def  *= (Scalar other):

    # # Multiplies this vector with another one
    # def  *= (Vec other):

    # # Divides two vectors
    # def Vec / (Vec a, Vec b):

    # # Divides a vector by a scalar
    # def Vec / (Vec a, Scalar b):

    # # Divides this vector with a scalar
    # def  /= (Scalar other):

    # # Divides this vector with another one
    # def  /= (Vec other):


    def add(self, other):
        """Overload method for the add operator.

        Arguments:
        other -- Vec3, other vector to add to this one.

        Return:
        Vec3, new Vec3 of the sum of the two Vec3's.

        """

        return Vec3(self._rtval.add('Vec3', other._rtval))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Arguments:
        other -- Vec3, other vector to subtract from this one.

        Return:
        Vec3, new Vec3 of the difference of the two Vec3's.

        """

        return Vec3(self._rtval.subtract('Vec3', other._rtval))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Arguments:
        other -- Vec3, other vector to multiply from this one.

        Return:
        Vec3, new Vec3 of the product of the two Vec3's.

        """

        return Vec3(self._rtval.multiply('Vec3', other._rtval))


    def divide(self, other):
        """Divides this vector and an other.

        Arguments:
        other -- Vec3, other vector to divide by.

        Return:
        Vec3, quotient of the division of this vector by the other.

        """

        return Vec3(self._rtval.divide('Vec3', other._rtval))


    def multiplyScalar(self, other):
        """Product of this vector and a scalar.

        Arguments:
        other -- Scalar, scalar value to multiply this vector by.

        Return:
        Vec3, product of the multiplication of the scalar and this vector.

        """

        return Vec3(self._rtval.multiplyScalar('Vec3', ks.rtVal('Scalar', other)))


    def divideScalar(self, other):
        """Divides this vector and a scalar.

        Arguments:
        other -- Scalar, value to divide this vector by.

        Return:
        Vec3, quotient of the division of the vector by the scalar.

        """

        return Vec3(self._rtval.divideScalar('Vec3', ks.rtVal('Scalar', other)))


    def negate(self):
        """Gets the negated version of this vector.

        Return:
        Vec3, negation of this vector.

        """

        return Vec3(self._rtval.negate('Vec3'))


    def inverse(self):
        """Get the inverse vector of this vector.

        Return:
        Vec3, inverse of this vector.

        """

        return Vec3(self._rtval.inverse('Vec3'))


    def dot(self, other):
        """Gets the dot product of this vector and another.

        Arguments:
        other -- Vec3, other vector.

        Return:
        Scalar, dot product.

        """

        return self._rtval.dot('Scalar', other._rtval)


    def cross(self, other):
        """Gets the cross product of this vector and another.

        Arguments:
        other -- Vec3, other vector.

        Return:
        Vec3, dot product.

        """

        return Vec3(self._rtval.cross('Vec3', other._rtval))


    def lengthSquared(self):
        """Get the squared length of this vector.

        Return:
        Scalar, squared length oft his vector.

        """

        return self._rtval.lengthSquared('Scalar')


    def length(self):
        """Gets the length of this vector.

        Return:
        Scalar, length of this vector.

        """

        return self._rtval.length('Scalar')


    def unit(self):
        """Gets a unit vector of this one.

        Return:
        Vec3, new unit vector from this one.

        """

        return Vec3(self._rtval.unit('Vec3'))


    def unit_safe(self):
        """Gets a unit vector of this one, no error reported if cannot be
        made unit.

        Return:
        Vec3, new unit vector.

        """

        return Vec3(self._rtval.unit_safe('Vec3'))


    def setUnit(self):
        """Sets this vector to a unit vector and returns the previous
        length.

        Return:
        Scalar, this vector.

        """

        return self._rtval.setUnit('Scalar')


    def normalize(self):
        """Gets a normalized vector from this vector.

        Return:
        Scalar, previous length.

        """

        return self._rtval.normalize('Scalar')


    def clamp(self, min, max):
        """Clamps this vector per component by a min and max vector.

        Arguments:
        min -- Scalar, minimum value.
        max -- Scalar, maximum value.

        Return:
        True if successful.

        """

        return Vec3(self._rtval.clamp('Vec3', min._rtval, max._rtval))


    def unitsAngleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one
        note expects both vectors to be units (else use angleTo)

        Arguments:
        other -- Vec3, other vector to get angle to.

        Return:
        Scalar, angle.

        """

        return self._rtval.unitsAngleTo('Scalar', other._rtval)


    def angleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one.

        Arguments:
        other -- Vec3, other vector to get angle to.

        Return:
        Scalar, angle.

        """

        return self._rtval.angleTo('Scalar', other._rtval)


    # Returns the distance of this vector to another one
    def distanceTo(self, other):
        """Doc String.

        Arguments:
        other -- Vec3, the other vector to measure the distance to.

        Return:
        True if successful.

        """

        return self._rtval.distanceTo('Scalar', other._rtval)


    def linearInterpolate(self, other, t):
        """Linearly interpolates this vector with another one based on a scalar
        blend value (0.0 to 1.0).

        Arguments:
        other -- Vec3, vector to blend to.
        t -- Scalar, blend value.

        Return:
        Vec3, new vector blended between this and the input vector.

        """

        return Vec3(self._rtval.linearInterpolate('Vec3', ks.rtVal('Scalar', t)))


    def distanceToLine(self, lineP0, lineP1):
        """Returns the distance of this vector to a line defined by two points
        on the line.

        Arguments:
        lineP0 -- Vec3, point 1 of the line.
        lineP1 -- Vec3, point 2 of the line.

        Return:
        Scalar, distance to the line.

        """

        return self._rtval.distanceToLine('Scalar', lineP0._rtval, lineP1._rtval)


    def distanceToSegment(self, segmentP0, segmentP1):
        """Returns the distance of this vector to a line segment defined by the
        start and end points of the line segment

        Arguments:
        segmentP0 -- Vec3, point 1 of the segment.
        segmentP1 -- Vec3, point 2 of the segment.

        Return:
        Scalar, distance to the segment.

        """

        return self._rtval.distanceToSegment('Scalar', segmentP0._rtval, segmentP1._rtval)