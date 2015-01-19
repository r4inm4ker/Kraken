"""Kraken - maths.vec4 module.

Classes:
Vec4 -- Vector 4 object.
"""

import math
from kraken.core.kraken_system import KrakenSystem as KS
from math_object import MathObject


class Vec4(MathObject):
    """Vector 4 object."""

    def __init__(self, x=0.0, y=0.0, z=0.0, t=0.0):
        """Initializes x, y z and t values for Vec4 object."""

        super(Vec4, self).__init__()
        if self.getTypeName(x) == 'Vec4':
            self.rtval = x
        else:
            self.rtval = KS.inst().rtVal('Vec4')
            self.set(x=x, y=y, z=z, t=t)


    def __str__(self):
        """String representation of the Vec4 object."""

        return "Vec4(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + "," + str(self.t) + ")"


    @property
    def x(self):
        """Gets x value of this vector.

        Return:
        Scalar, x value of this vector.

        """

        return self.rtval.x


    @x.setter
    def x(self, value):
        """Sets x value from the input value.

        Arguments:
        value -- Scalar, value to set the x property as.

        Return:
        True if successful.

        """

        self.rtval.x = KS.inst().rtVal('Scalar', value)

        return True


    @property
    def y(self):
        """Gets y value of this vector.

        Return:
        Scalar, y value of this vector.

        """

        return self.rtval.y


    @y.setter
    def y(self, value):
        """Sets y value from the input value.

        Arguments:
        value -- Scalar, value to set the y property as.

        Return:
        True if successful.

        """

        self.rtval.y = KS.inst().rtVal('Scalar', value)

        return True


    @property
    def z(self):
        """Gets z value of this vector.

        Return:
        Scalar, z value of this vector.

        """

        return self.rtval.z


    @y.setter
    def z(self, value):
        """Sets y value from the input value.

        Arguments:
        value -- Scalar, value to set the y property as.

        Return:
        True if successful.

        """

        self.rtval.z = KS.inst().rtVal('Scalar', value)

        return True


    @property
    def t(self):
        """Gets t value of this vector.

        Return:
        Scalar, t value of this vector.

        """

        return self.rtval.t


    @y.setter
    def t(self, value):
        """Sets t value from the input value.

        Arguments:
        value -- Scalar, value to set the t property as.

        Return:
        True if successful.

        """

        self.rtval.t = KS.inst().rtVal('Scalar', value)


    def clone(self):
        """Returns a clone of the Vec4.

        Return:
        The cloned Vec4

        """

        vec4 = Vec4();
        vec4.x = self.x;
        vec4.y = self.y;
        vec4.z = self.z;
        return vec4


    def set(self, x, y, z, t):
        """Sets the x, y, z, and t value from the input values.

        Arguments:
        x -- Scalar, value to set the x property as.
        y -- Scalar, value to set the x property as.
        z -- Scalar, value to set the z property as.
        t -- Scalar, value to set the t property as.

        Return:
        True if successful.

        """

        self.rtval.set('', KS.inst().rtVal('Scalar', x), KS.inst().rtVal('Scalar', y), KS.inst().rtVal('Scalar', z), KS.inst().rtVal('Scalar', t))

        return True


    def setNull():
        """Setting all components of the vec3 to 0.0.

        Return:
        True if successful.

        """

        self.rtval.setNull('')

        return True


    def equal(self, other):
        """Checks equality of this vec3 with another.

        Arguments:
        other -- Vec4, other vector to check equality with.

        Return:
        True if equal.

        """

        return self.rtval.set('Boolean', other.rtval)


    def almostEqual(self, other, precision):
        """Checks almost equality of this Vec4 with another.

        Arguments:
        other -- Vec4, other matrix to check equality with.
        precision -- Scalar, precision value.

        Return:
        True if almost equal.

        """

        return self.rtval.almostEqual('Boolean', other.rtval, KS.inst().rtVal('Scalar', precision))


    def almostEqual(self, other):
        """Checks almost equality of this Vec4 with another
        (using a default precision).

        Arguments:
        other -- Vec4, other vector to check equality with.

        Return:
        True if almost equal.

        """

        return self.rtval.almostEqual('Boolean', other.rtval)


    def component(self, i ):
        """Gets the component of this Vec4 by index.

        Arguments:
        i -- Integer, index of the component to return.

        Return:
        Scalar, component of this Vec4.

        """

        return self.rtval.component('Scalar', KS.inst().rtVal('Size', i))


    def setComponent(self, i, v ):
        """Sets the component of this Vec4 by index.

        Arguments:
        i -- Integer, index of the component to set.
        v -- Scalar, value to set component as.

        Return:
        True if successful.

        """

        return self.rtval.setComponent('', KS.inst().rtVal('Size', i), KS.inst().rtVal('Scalar', v))


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
        other -- Vec4, other vector to add to this one.

        Return:
        Vec4, new Vec4 of the sum of the two Vec4's.

        """

        return Vec4(self.rtval.add('Vec4', other.rtval))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Arguments:
        other -- Vec4, other vector to subtract from this one.

        Return:
        Vec4, new Vec4 of the difference of the two Vec4's.

        """

        return Vec4(self.rtval.subtract('Vec4', other.rtval))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Arguments:
        other -- Vec4, other vector to multiply from this one.

        Return:
        Vec4, new Vec4 of the product of the two Vec4's.

        """

        return Vec4(self.rtval.multiply('Vec4', other.rtval))


    def divide(self, other):
        """Divides this vector and an other.

        Arguments:
        other -- Vec4, other vector to divide by.

        Return:
        Vec4, quotient of the division of this vector by the other.

        """

        return Vec4(self.rtval.divide('Vec4', other.rtval))


    def multiplyScalar(self, other):
        """Product of this vector and a scalar.

        Arguments:
        other -- Scalar, scalar value to multiply this vector by.

        Return:
        Vec4, product of the multiplication of the scalar and this vector.

        """

        return Vec4(self.rtval.multiplyScalar('Vec4', KS.inst().rtVal('Scalar', other)))


    def divideScalar(self, other):
        """Divides this vector and a scalar.

        Arguments:
        other -- Scalar, value to divide this vector by.

        Return:
        Vec4, quotient of the division of the vector by the scalar.

        """

        return Vec4(self.rtval.divideScalar('Vec4', KS.inst().rtVal('Scalar', other)))


    def negate(self):
        """Gets the negated version of this vector.

        Return:
        Vec4, negation of this vector.

        """

        return Vec4(self.rtval.negate('Vec4'))


    def inverse(self):
        """Get the inverse vector of this vector.

        Return:
        Vec4, inverse of this vector.

        """

        return Vec4(self.rtval.inverse('Vec4'))


    def dot(self, other):
        """Gets the dot product of this vector and another.

        Arguments:
        other -- Vec4, other vector.

        Return:
        Scalar, dot product.

        """

        return self.rtval.dot('Scalar', other.rtval)


    def cross(self, other):
        """Gets the cross product of this vector and another.

        Arguments:
        other -- Vec4, other vector.

        Return:
        Vec4, dot product.

        """

        return Vec4(self.rtval.cross('Vec4', other.rtval))


    def lengthSquared(self):
        """Get the squared length of this vector.

        Return:
        Scalar, squared length oft his vector.

        """

        return self.rtval.lengthSquared('Scalar')


    def length(self):
        """Gets the length of this vector.

        Return:
        Scalar, length of this vector.

        """

        return self.rtval.length('Scalar')


    def unit(self):
        """Gets a unit vector of this one.

        Return:
        Vec4, new unit vector from this one.

        """

        return Vec4(self.rtval.unit('Vec4'))


    def unit_safe(self):
        """Gets a unit vector of this one, no error reported if cannot be
        made unit.

        Return:
        Vec4, new unit vector.

        """

        return Vec4(self.rtval.unit_safe('Vec4'))


    def setUnit(self):
        """Sets this vector to a unit vector and returns the previous
        length.

        Return:
        Scalar, this vector.

        """

        return self.rtval.setUnit('Scalar')


    def normalize(self):
        """Gets a normalized vector from this vector.

        Return:
        Scalar, previous length.

        """

        return self.rtval.normalize('Scalar')


    def clamp(self, min, max):
        """Clamps this vector per component by a min and max vector.

        Arguments:
        min -- Scalar, minimum value.
        max -- Scalar, maximum value.

        Return:
        True if successful.

        """

        return Vec4(self.rtval.clamp('Vec4', min.rtval, max.rtval))


    def unitsAngleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one
        note expects both vectors to be units (else use angleTo)

        Arguments:
        other -- Vec4, other vector to get angle to.

        Return:
        Scalar, angle.

        """

        return self.rtval.unitsAngleTo('Scalar', other.rtval)


    def angleTo(self, other):
        """Gets the angle (self, in radians) of this vector to another one.

        Arguments:
        other -- Vec4, other vector to get angle to.

        Return:
        Scalar, angle.

        """

        return self.rtval.angleTo('Scalar', other.rtval)


    # Returns the distance of this vector to another one
    def distanceTo(self, other):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.distanceTo('Scalar', other.rtval)


    def linearInterpolate(self, other, t):
        """Linearly interpolates this vector with another one based on a scalar
        blend value (0.0 to 1.0).

        Arguments:
        other -- Vec4, vector to blend to.
        t -- Scalar, blend value.

        Return:
        Vec4, new vector blended between this and the input vector.

        """

        return Vec4(self.rtval.linearInterpolate('Vec4', KS.inst().rtVal('Scalar', t)))


    def distanceToLine(self, lineP0, lineP1):
        """Returns the distance of this vector to a line defined by two points
        on the line.

        Arguments:
        lineP0 -- Vec4, point 1 of the line.
        lineP1 -- Vec4, point 2 of the line.

        Return:
        Scalar, distance to the line.

        """

        return self.rtval.distanceToLine('Scalar', lineP0.rtval, lineP1.rtval)


    def distanceToSegment(self, segmentP0, segmentP1):
        """Returns the distance of this vector to a line segment defined by the
        start and end points of the line segment

        Arguments:
        segmentP0 -- Vec4, point 1 of the segment.
        segmentP1 -- Vec4, point 2 of the segment.

        Return:
        Scalar, distance to the segment.

        """

        return self.rtval.distanceToSegment('Scalar', segmentP0.rtval, segmentP1.rtval)