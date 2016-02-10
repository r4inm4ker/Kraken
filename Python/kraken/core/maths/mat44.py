"""Kraken - maths.matrix module.

Classes:
Mat44 -- Matrix 3 transform object.
"""

from math_object import MathObject
from kraken.core.kraken_system import ks
from vec import Vec3, Vec4
from mat33 import Mat33


class Mat44(MathObject):
    """4x4 Matrix object."""

    def __init__(self, row0=None, row1=None, row2=None, row3=None):
        """Initialize and set values in the 3x3 matrix."""

        super(Mat44, self).__init__()

        if ks.getRTValTypeName(row0) == 'Mat44':
            self._rtval = row0
        else:
            self._rtval = ks.rtVal('Mat44')
            if isinstance(row0, Mat33):
                self.setRows(row0=row0.row0, row1=row0.row1, row2=row0.row2, row3=row0.row3)
            elif row0 is not None and row1 is not None and row2 is not None and row3 is not None:
                self.setRows(row0, row1, row2, row3)


    def __str__(self):
        """String representation of the 4x4 matrix.

        Returns:
            str: String representation of the 4x4 matrix.

        """

        stringRep = "Mat44("
        stringRep += str(self.row0) + ","
        stringRep += str(self.row1) + ","
        stringRep += str(self.row2) + ","
        stringRep += str(self.row3) + ")"

        return stringRep


    @property
    def row0(self):
        """Gets row 0 of this matrix.

        Returns:
            Vec4: row 0 vector.

        """

        return Vec4(self._rtval.row0)


    @row0.setter
    def row0(self, value):
        """Sets row 0 as the input vector.

        Args:
            value (Vec4): Vector to set row 0 as.

        Returns:
            bool: True if successful.

        """

        self._rtval.row0 = ks.rtVal('Vec4', value)

        return True


    @property
    def row1(self):
        """Gets row 1 of this matrix.

        Returns:
            Vec4: row 1 vector.

        """

        return Vec4(self._rtval.row1)


    @row1.setter
    def row1(self, value):
        """Sets row 1 as the input vector.

        Args:
            value (Vec4): vector to set row 1 as.

        Returns:
            bool: True if successful.

        """

        self._rtval.row1 = ks.rtVal('Vec4', value)

        return True


    @property
    def row2(self):
        """Gets row 2 of this matrix.

        Returns:
            Vec4: row 2 vector.

        """

        return Vec4(self._rtval.row2)


    @row2.setter
    def row2(self, value):
        """Sets row 2 as the input vector.

        Args:
            value (Vec4): vector to set row 2 as.

        Returns:
            bool: True if successful.

        """

        self._rtval.row2 = ks.rtVal('Vec4', value)

        return True


    @property
    def row3(self):
        """Gets row 3 of this matrix.

        Returns:
            Vec4: row 3 vector.

        """

        return Vec4(self._rtval.row3)


    @row3.setter
    def row3(self, value):
        """Sets row 3 as the input vector.

        Args:
        value (Vec4): vector to set row 3 as.

        Returns:
            bool: True if successful.

        """

        self._rtval.row3 = ks.rtVal('Vec4', value)

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


    def clone(self):
        """Returns a clone of the Mat44.

        Returns:
            Mat44: The cloned Mat44.

        """

        mat44 = Mat44()
        mat44.row0 = self.row0.clone()
        mat44.row1 = self.row1.clone()
        mat44.row2 = self.row2.clone()
        mat44.row3 = self.row3.clone()

        return mat44


    def setRows(self, row0, row1, row2, row3):
        """Set from vectors, row-wise.

        Args:
            row0 (Vec4): vector to use for row 0.
            row1 (Vec4): vector to use for row 1.
            row2 (Vec4): vector to use for row 2.
            row3 (Vec4): vector to use for row 3.

        Returns:
            bool: True if successful.

        """

        self._rtval.setRows('', ks.rtVal('Vec4', row0), ks.rtVal('Vec4', row0),
                            ks.rtVal('Vec4', row2), ks.rtVal('Vec4', row3))

        return True


    def setColumns(self, col0, col1, col2, col3):
        """Setter from vectors, column-wise.

        Args:
            col0 (Vec4): vector to use for column 0.
            col1 (Vec4): vector to use for column 1.
            col2 (Vec4): vector to use for column 2.
            col3 (Vec4): vector to use for column 3.

        Returns:
            bool: True if successful.

        """

        self._rtval.setColumns('', ks.rtVal('Vec4', col0), ks.rtVal('Vec4', col0),
                               ks.rtVal('Vec4', col2), ks.rtVal('Vec4', col3))

        return True


    def setNull(self):
        """Setting all components of the matrix to 0.0.

        Returns:
            bool: True if successful.

        """

        self._rtval.setNull('')

        return True


    def setIdentity(self):
        """Sets this matrix to the identity matrix.

        Returns:
            bool: True if successful.

        """

        self._rtval.setIdentity('')

        return True


    def setDiagonal(self, v):
        """Sets the diagonal components of this matrix to a scalar.

        Args:
            v (float): value to set diagonals to.

        Returns:
            bool: True if successful.

        """

        self._rtval.setDiagonal('', ks.rtVal('Scalar', v))

        return True


    def setDiagonal(self, v):
        """Sets the diagonal components of this matrix to the components of a
        vector.

        Args:
            v (Vec3): vector to set diagonals to.

        Returns:
            bool: True if successful.

        """

        self._rtval.setDiagonal('', ks.rtVal('Vec3', v))

        return True


    def equal(self, other):
        """Checks equality of this Matrix44 with another.

        Args:
            other (Mat44): other matrix to check equality with.

        Returns:
            bool: True if equal.

        """

        return self._rtval.equal('Boolean', ks.rtVal('Mat44', other)).getSimpleType()


    def almostEqual(self, other, precision):
        """Checks almost equality of this Matrix44 with another.

        Args:
            other (Mat44): other matrix to check equality with.
            precision (float): precision value.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', ks.rtVal('Mat44', other),
                                       ks.rtVal('Scalar', precision)).getSimpleType()


    def almostEqual(self, other):
        """Checks almost equality of this Matrix44 with another
        (using a default precision).

        Args:
            other (Mat44): other matrix to check equality with.

        Returns:
            bool: True if almost equal.

        """

        return self._rtval.almostEqual('Boolean', ks.rtVal('Mat44', other)).getSimpleType()


    def add(self, other):
        """Overload method for the add operator.

        Args:
            other (Mat44): other matrix to add to this one.

        Returns:
            Mat44: new Mat44 of the sum of the two Mat44's.

        """

        return Mat44(self._rtval.add('Mat44', ks.rtVal('Mat44', other)))


    def subtract(self, other):
        """Overload method for the subtract operator.

        Args:
            other (Mat44): other matrix to subtract from this one.

        Returns:
            Mat44: new Mat44 of the difference of the two Mat44's.

        """

        return Mat44(self._rtval.subtract('Mat44', ks.rtVal('Mat44', other)))


    def multiply(self, other):
        """Overload method for the multiply operator.

        Args:
            other (Mat44): other matrix to multiply from this one.

        Returns:
            Mat44: new Mat44 of the product of the two Mat44's.

        """

        return Mat44(self._rtval.multiply('Mat44', ks.rtVal('Mat44', other)))


    def multiplyScalar(self, other):
        """Product of this matrix and a scalar.

        Args:
            other (float): scalar value to multiply this matrix by.

        Returns:
            Mat44: product of the multiplication of the scalar and this matrix.

        """

        return Mat44(self._rtval.multiplyScalar('Mat44', ks.rtVal('Scalar', other)))


    def multiplyVector(self, other):
        """Returns the product of this matrix and a vector.

        Args:
            other (Vec3): vector to multiply this matrix by.

        Returns:
            Vec3: product of the multiplication of the Vec3 and this matrix.

        """

        return Vec3(self._rtval.multiplyVector('Vec3', ks.rtVal('Vec3', other)))


    def divideScalar(self, other):
        """Divides this matrix and a scalar.

        Args:
            other (float): Value to divide this matrix by

        Returns:
            Mat44: Quotient of the division of the matrix by the scalar.

        """

        return Mat44(self._rtval.divideScalar('Mat44', other))


    def determinant(self):
        """Gets the determinant of this matrix.

        Returns:
            float: Determinant of this matrix.

        """

        return self._rtval.determinant('Scalar').getSimpleType()


    def adjoint(self):
        """Gets the adjoint matrix of this matrix.

        Returns:
            Mat44: Adjoint of this matrix.

        """

        return Mat44(self._rtval.adjoint('Mat44'))


    def inverse(self):
        """Get the inverse matrix of this matrix.

        Returns:
            Mat44: Inverse of this matrix.

        """

        return Mat44(self._rtval.inverse('Mat44'))


    def inverse_safe(self):
        """Get the inverse matrix of this matrix, always checking the
        determinant value.

        Returns:
            Mat44: Safe inverse of this matrix.

        """

        return Mat44(self._rtval.inverse_safe('Mat44'))


    def transpose(self):
        """Get the transposed matrix of this matrix.

        Returns:
            Mat44: Transpose of this matrix.

        """

        return Mat44(self._rtval.transpose('Mat44'))
