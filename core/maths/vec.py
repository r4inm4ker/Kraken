"""Kraken - maths.vec module.

Classes:
Vec -- Base Vector object.
"""

import math
from math_object import MathObject
from kraken.core.objects.kraken_core import KrakenCore as KC

class Vec(MathObject):
    """Vector object."""

    def __init__(self):
        super(Vec, self).__init__()

    # Setter from same scalar for all components
    def set(self, value):
        self.rtval.set('', KC.inst().rtVal('Scalar', value))

    # Sets all components of this vec to 0.0
    def setNull():
        self.rtval.setNull('')

    # Returns true if this vector is the same as another one
    def equal(self, other):
        return self.rtval.set('Boolean', other.rtval)

    # Returns true if this vector is the same as another one
    # (given a precision)
    def almostEqual(self, other, precision):
        return self.rtval.almostEqual('Boolean', other.rtval, KC.inst().rtVal('Scalar', precision))

    # Returns true if this vector is the same as another one
    # (using a default precision)
    def almostEqual(self, other):
        return self.rtval.almostEqual('Boolean', other.rtval)

    # Returns the component of this vector by index
    def component(self, i ):
        return self.rtval.component('Scalar', KC.inst().rtVal('Size', i))

    # Sets the component of this vector by index
    def setComponent(self, i, v ):
        return self.rtval.setComponent('', KC.inst().rtVal('Size', i), KC.inst().rtVal('Scalar', v))

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

    # Overload method for the add operator
    def add(self, other):
        return self.rtval.add(self.typeName(), other.rtval)

    # Overload method for the subtract operator
    def subtract(self, other):
        return self.rtval.subtract(self.typeName(), other.rtval)

    # Overload method for the multiply operator
    def multiply(self, other):
        return self.rtval.multiply(self.typeName(), other.rtval)

    # Overload method for the divide operator
    def divide(self, other):
        return self.rtval.divide(self.typeName(), other.rtval)

    # Returns the product of this vector and a scalar
    def multiplyScalar(self, other):
        return self.rtval.multiplyScalar(self.typeName(), KC.inst().rtVal('Scalar', other))

    # Returns the division of this vector and a scalar
    def divideScalar(self, other):
        return self.rtval.divideScalar(self.typeName(), KC.inst().rtVal('Scalar', other))

    # Returns the negated version of this vector
    def negate(self):
        return self.rtval.negate(self.typeName())

    # Returns the inversed version of this vector
    def inverse(self):
        return self.rtval.inverse(self.typeName())

    # Returns the dot product of this vector and another one
    def dot(self, other):
        return self.rtval.dot('Scalar', other.rtval)

    # Returns the cross product of this vector and another one
    def cross(self, other):
        return Vec3(self.rtval.cross(self.typeName(), other.rtval))

    # Returns the squared length of this vector
    def lengthSquared(self):
        return self.rtval.lengthSquared('Scalar')

    # Returns the length of this vector
    def length(self):
        return self.rtval.length('Scalar')

    # Returns the unit vector of this one, throws and exception if almost zero length
    def unit(self):
        return self.rtval.unit(self.typeName())

    # Returns the unit vector of this one, with an arbitrary value if almost zero length
    def unit_safe(self):
        return self.rtval.unit_safe(self.typeName())

    # Sets this vector to its unit vector
    # and returns its previous length
    def setUnit(self):
        return self.rtval.setUnit('Scalar')

    def normalize(self):
        return self.rtval.normalize('Scalar')

    # clamps this vector per component by 
    # a min and max vector
    def clamp(self, min, max):
        return self.rtval.clamp(self.typeName(), min.rtval, max.rtval)

    # Returns the angle (self, in radians) of this vector
    # to another one
    # \note expects both vectors to be units (else use angleTo)
    def unitsAngleTo(self, other):
        return self.rtval.unitsAngleTo('Scalar', other.rtval)

    # Returns the angle (self, in radians) of this vector
    # to another one
    def angleTo(self, other):
        return self.rtval.angleTo('Scalar', other.rtval)

    # Returns the distance of this vector to another one
    def distanceTo(self, other):
        return self.rtval.distanceTo('Scalar', other.rtval)

    # Linearly interpolates this vector with another one
    # based on a scalar blend value (0.0 to 1.0)
    def linearInterpolate(self, other, t):
        return self.rtval.linearInterpolate(self.typeName(), KC.inst().rtVal('Scalar', t))

    # Returns the distance of this vector to a line defined
    # by two points on the line
    def distanceToLine(self, lineP0, lineP1):
        return self.rtval.distanceToLine('Scalar', lineP0.rtval, lineP1.rtval)

    # Returns the distance of this vector to a line segment defined
    # by the start and end points of the line segment
    def distanceToSegment(self, segmentP0, segmentP1):
        return self.rtval.distanceToSegment('Scalar', segmentP0.rtval, segmentP1.rtval)

