"""Kraken - maths.matrix module.

Classes:
Mat33 -- Matrix 3 transform object.
"""

from math_object import MathObject
from kraken.core.objects.kraken_system import KrakenSystem as KS
from vec3 import Vec3


class Mat33(MathObject):
    """3x3 Matrix object."""

    def __init__(self, row0=None, row1=None, row2=None):
        """Initialize and set values in the 3x3 matrix."""

        super(Mat33, self).__init__()

        if row0 is not None and self.getTypeName(row0) == 'Mat33':
            self.rtval = row0
        else:
            self.rtval = KS.inst().rtVal('Mat33')
            self.setRows(row0, row1, row2)


    def __str__(self):
        """Return a string representation of the 3x3 matrix."""
        return "Mat33(" + str(self.row0) + "," + str(self.row1) + "," + str(self.row2) + ")"

    @property
    def row0(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Vec3(self.rtval.row0)


    @row0.setter
    def row0(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.row0 = KS.inst().rtVal('Scalar', value)


    @property
    def row1(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Vec3(self.rtval.row1)


    @row1.setter
    def row1(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.row1 = KS.inst().rtVal('Scalar', value)


    @property
    def row2(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Vec3(self.rtval.row2)


    @row2.setter
    def row2(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.row2 = KS.inst().rtVal('Scalar', value)


    def setRows(self, row0, row1, row2):
        """Setter from vectors, row-wise.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.setRows('', KS.inst().rtVal('Vec3', row0), KS.inst().rtVal('Vec3', row1), KS.inst().rtVal('Vec3', row2))


    def setColumns(self, col0, col1, col2):
        """Setter from vectors, column-wise.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.setColumns('', KS.inst().rtVal('Vec3', col0), KS.inst().rtVal('Vec3', col1), KS.inst().rtVal('Vec3', col2))


    def setNull(self):
        """Setting all components of the matrix to 0.0.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.setNull('')


    def setIdentity(self):
        """Setting this matrix to the identity matrix.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.setIdentity('')


    def setDiagonal(self, v):
        """Setting the diagonal components of this matrix to a scalar.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.setDiagonal('', KS.inst().rtVal('Scalar', v))


    def setDiagonal(self, v):
        """Setting the diagonal components of this matrix to the components of a
        vector.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.setDiagonal('', KS.inst().rtVal('Vec3', v))


    def equal(self, other):
        """Returns true if this matrix is the same as another one.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.add('Boolean', KS.inst().rtVal('Mat33', other))


    def almostEqual(self, other, precision):
        """Returns true if this matrix is almost equal to the given matrix within the provided precision range.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.add('Boolean', KS.inst().rtVal('Mat33', other), KS.inst().rtVal('Scalar', precision))


    def almostEqual(self, other):
        """Returns true if this matrix is almost the same as another one
        (using a default precision).

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.add('Boolean', KS.inst().rtVal('Mat33', other))


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


    def add(self, other):
        """Overload method for the add operator.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.add('Mat33', KS.inst().rtVal('Mat33', other)))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.subtract('Mat33', KS.inst().rtVal('Mat33', other)))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.multiply('Mat33', KS.inst().rtVal('Mat33', other)))


    def multiplyScalar(self, other):
        """Returns the product of this matrix and a scalar.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.multiplyScalar('Mat33', KS.inst().rtVal('Scalar', other)))


    def multiplyVector(self, other):
        """Returns the product of this matrix and a vector.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Vec3(self.rtval.multiplyVector('Vec3', KS.inst().rtVal('Vec3', other)))


    def divideScalar(self, other):
        """Returns the division of this matrix and a scalar.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.divideScalar('Mat33', other))


    def determinant(self):
        """Returns the determinant of this matrix.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.determinant('Scalar')


    def adjoint(self):
        """Returns the adjoint matrix of this matrix.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.adjoint('Mat33'))


    def inverse(self):
        """Returns the inverse matrix of this matrix

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.inverse('Mat33'))


    def inverse_safe(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.inverse_safe('Mat33'))


    def transpose(self):
        """Returns the transposed matrix of this matrix.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return Mat33(self.rtval.transpose('Mat33'))