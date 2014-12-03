"""Kraken - maths.matrix module.

Classes:
Mat33 -- Matrix 3 transform object.
"""

from math_object import MathObject
from kraken.core.objects.kraken_core import KrakenCore as KC
from vec3 import Vec3

class Mat33(MathObject):
    """3x3 Matrix object."""

    def __init__(self, row0=None, row1=None, row2=None):
        """Initialize and set values in the 3x3 matrix."""

        super(Mat33, self).__init__()

        if row0 is not None and self.getTypeName(row0) == 'Mat33':
            self.rtval = row0
        else:
            self.rtval = KC.inst().rtVal('Mat33')
            self.setRows(row0, row1, row2)


    def __str__(self):
        """Return a string representation of the 3x3 matrix."""
        return "Mat33(" + str(self.row0) + "," + str(self.row1) + "," + str(self.row2) + ")"

    @property
    def row0(self):
        """I'm the 'row0' property."""
        return Vec3(self.rtval.row0)

    @row0.setter
    def row0(self, value):
        self.rtval.row0 = KC.inst().rtVal('Scalar', value)

    @property
    def row1(self):
        """I'm the 'row1' property."""
        return Vec3(self.rtval.row1)

    @row1.setter
    def row1(self, value):
        self.rtval.row1 = KC.inst().rtVal('Scalar', value)

    @property
    def row2(self):
        """I'm the 'row2' property."""
        return Vec3(self.rtval.row2)

    @row2.setter
    def row2(self, value):
        self.rtval.row2 = KC.inst().rtVal('Scalar', value)


    # Setter from vectors, row-wise
    def setRows(self, row0, row1, row2):
        self.rtval.setRows('', KC.inst().rtVal('Vec3', row0), KC.inst().rtVal('Vec3', row0), KC.inst().rtVal('Vec3', row2))

    # Setter from vectors, column-wise
    def setColumns(self, col0, col1, col2):
        self.rtval.setColumns('', KC.inst().rtVal('Vec3', col0), KC.inst().rtVal('Vec3', col0), KC.inst().rtVal('Vec3', col2))

    # setting all components of the matrix to 0.0
    def setNull(self):
        self.rtval.setNull('')

    # setting this matrix to the identity matrix
    def setIdentity(self):
        self.rtval.setIdentity('')

    # setting the diagonal components of 
    # this matrix to a scalar
    def setDiagonal(self, v):
        self.rtval.setDiagonal('', KC.inst().rtVal('Scalar', v))

    # setting the diagonal components of this
    # matrix to the components of a vector
    def setDiagonal(self, v):
        self.rtval.setDiagonal('', KC.inst().rtVal('Vec3', v))

    # Returns true if this matrix is the same as another one
    def equal(self, other):
        return self.rtval.add('Boolean', KC.inst().rtVal('Mat33', other))

    # Returns true if this matrix is almost equal to the given matrix within the provided precision range
    def almostEqual(self, other, precision):
        return self.rtval.add('Boolean', KC.inst().rtVal('Mat33', other), KC.inst().rtVal('Scalar', precision))

    # Returns true if this matrix is almost the same as another one
    # (using a default precision)
    def almostEqual(self, other):
        return self.rtval.add('Boolean', KC.inst().rtVal('Mat33', other))

    # # Equals operator
    # def Boolean == (Mat33 a, Mat33 b):

    # # Not equals operator
    # def Boolean != (Mat33 a, Mat33 b):

    # # Returns the addition of two matrices
    # def Mat33 + (Mat33 a, Mat33 b):

    # # Adds another matrix to this one
    # def  += (Mat33 other):

    # # Returns the subtraction of two matrices
    # def Mat33 - (Mat33 a, Mat33 b):

    # # Subtracts another matrix from this one
    # def  -= (Mat33 other):

    # # Returns the product of two matrices
    # function Mat33 * (Mat33 left, Mat33 right):

    # # Returns the product of a matrix and a Vec3
    # def Vec3 * (Mat33 mat33, Vec3 vec3):

    # # Returns the product of a matrix and a scalar
    # def Mat33 * (Mat33 mat33, Scalar s):

    # # Returns the product of a scalar and a matrix
    # def Mat33 * (Scalar s, Mat33 mat33):

    # # Multiplies this matrix with another one
    # def  *= (Mat33 other):

    # # Multiplies this matrix with a scalar
    # def  *= (Scalar other):

    # # Returns the division of a matrix and a scalar
    # def Mat33 / (Mat33 mat33, Scalar s):

    # # Divides this matrix by a scalar
    # def  /= (Scalar other):

    # Overload method for the add operator
    def add(self, other):
        return Mat33(self.rtval.add('Mat33', KC.inst().rtVal('Mat33', other)))

    # Overload method for the subtract operator
    def subtract(self, other):
        return Mat33(self.rtval.subtract('Mat33', KC.inst().rtVal('Mat33', other)))

    # Overload method for the multiply operator
    def multiply(self, other):
        return Mat33(self.rtval.multiply('Mat33', KC.inst().rtVal('Mat33', other)))

    # Returns the product of this matrix and a scalar
    def multiplyScalar(self, other):
        return Mat33(self.rtval.multiplyScalar('Mat33', KC.inst().rtVal('Scalar', other)))

    # Returns the product of this matrix and a vector
    def multiplyVector(self, other):
        return Vec3(self.rtval.multiplyVector('Vec3', KC.inst().rtVal('Vec3', other)))

    # Returns the division of this matrix and a scalar
    def divideScalar(self, other):
        return Mat33(self.rtval.divideScalar('Mat33', other))

    # Returns the determinant of this matrix
    def determinant(self):
        return self.rtval.determinant('Scalar')

    # Returns the adjoint matrix of this matrix
    def adjoint(self):
        return Mat33(self.rtval.adjoint('Mat33'))

    # Returns the inverse matrix of this matrix
    def inverse(self):
        return Mat33(self.rtval.inverse('Mat33'))

    def inverse_safe(self):
        return Mat33(self.rtval.inverse_safe('Mat33'))

    # Returns the transposed matrix of this matrix
    def transpose(self):
        return Mat33(self.rtval.transpose('Mat33'))



