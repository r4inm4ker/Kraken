"""Kraken - maths.matrix module.

Classes:
Matrix33 -- Matrix 3 transform object.
Matrix44 -- Matrix 4 transform object.
"""

from math_object import MathObject
from vec import Vec3, Vec4

class Matrix33(MathObject):
    """3x3 Matrix object."""

    def __init__(self, row0=None, row1=None, row2=None):
        """Initialize and set values in the 3x3 matrix."""

        super(Matrix33, self).__init__()

        self.row0 = Vec3()
        self.row1 = Vec3()
        self.row2 = Vec3()

        self.components = None
        self.set(row0, row1, row2)


    def __str__(self):
        """Return a string representation of the 3x3 matrix."""

        return "Matrix33(" + str(self.row0) + "," + str(self.row1) + "," + str(self.row2) + ")"


    def set(self, row0=None, row1=None, row2=None):
        """Sets the row values for the 3x3 matrix.

        Arguments:
        row0 -- Vec3
        row1 -- Vec3
        row2 -- Vec3

        Return:
        Self

        """

        if row0 is None:
            self.row0.set(1.0, 0.0, 0.0)
        elif not isinstance(row0, Vec3):
            raise TypeError("Matrix33: Invalid 'row0' argument.")
        else:
            self.row0 = row0.clone()

        if row1 is None:
            self.row1.set(0.0, 1.0, 0.0)
        elif not isinstance(row1, Vec3):
            raise TypeError("Matrix33: Invalid 'row1' argument.")
        else:
            self.row1 = row1.clone()

        if row2 is None:
            self.row2.set(0.0, 0.0, 1.0)
        elif not isinstance(row2, Vec3):
            raise TypeError("Matrix33: Invalid 'row2' argument.")
        else:
            self.row2 = row2.clone()

        self.components = self.toArray()

        return self


    def setFromArray(self, a):
        """Set the matrix values from input array.

        Arguments:
        a -- List of 9 matrix values.

        Return:
        True if successful.
        """

        self.row0.x = a[0]
        self.row0.y = a[1]
        self.row0.z = a[2]

        self.row1.x = a[3]
        self.row1.y = a[4]
        self.row1.z = a[5]

        self.row2.x = a[6]
        self.row2.y = a[7]
        self.row2.z = a[8]

        return True


    def toArray(self):
        """Creates a 1D array of the matrix components.

        Return:
        1D array of matrix components.

        """

        components = [x for x in xrange(9)]

        components[0] = self.row0.x
        components[1] = self.row0.y
        components[2] = self.row0.z

        components[3] = self.row1.x
        components[4] = self.row1.y
        components[5] = self.row1.z

        components[6] = self.row2.x
        components[7] = self.row2.y
        components[8] = self.row2.z

        return components


    def add(self, matrix):
        """Adds this matrix with input matrix.

        Arguments:
        matrix -- Matrix33 -- Input matrix to add to this matrix.

        Return:
        New matrix with sum of input matrix and this matrix.

        """

        if not isinstance(matrix, Matrix33):
            raise TypeError("Matrix33 Add: Invalid 'matrix' argument.")

        return Matrix33(self.row0.add(matrix.row0),
                       self.row1.add(matrix.row1),
                       self.row2.add(matrix.row2))


    def subtract(self, matrix):
        """Subtracts this input matrix from this matrix.

        Arguments:
        matrix -- Matrix33 -- Input matrix to subtract from this matrix.

        Return:
        New matrix with difference of input matrix and this matrix.

        """

        if not isinstance(matrix, Matrix33):
            raise TypeError("Matrix33 Subtract: Invalid 'matrix' argument.")

        return Matrix33(self.row0.subtract(matrix.row0),
                     self.row1.subtract(matrix.row1),
                     self.row2.subtract(matrix.row2))


    def multiply(self, other):
        """Multiply this matrix by input matrix.

        Arguments:
        other -- Matrix33, second term to use in multiplication operation.

        Return:
        New Matrix33 equal to product of this matrix and input matrix.

        """

        if not isinstance(other, Matrix33):
            raise TypeError("Matrix33 Multiply: Invalid 'matrix' argument.")

        product = Matrix33()
        product.row0.x = self.row0.x * other.row0.x + self.row0.y * other.row1.x + self.row0.z * other.row2.x
        product.row0.y = self.row0.x * other.row0.y + self.row0.y * other.row1.y + self.row0.z * other.row2.y
        product.row0.z = self.row0.x * other.row0.z + self.row0.y * other.row1.z + self.row0.z * other.row2.z

        product.row1.x = self.row1.x * other.row0.x + self.row1.y * other.row1.x + self.row1.z * other.row2.x
        product.row1.y = self.row1.x * other.row0.y + self.row1.y * other.row1.y + self.row1.z * other.row2.y
        product.row1.z = self.row1.x * other.row0.z + self.row1.y * other.row1.z + self.row1.z * other.row2.z

        product.row2.x = self.row2.x * other.row0.x + self.row2.y * other.row1.x + self.row2.z * other.row2.x
        product.row2.y = self.row2.x * other.row0.y + self.row2.y * other.row1.y + self.row2.z * other.row2.y
        product.row2.z = self.row2.x * other.row0.z + self.row2.y * other.row1.z + self.row2.z * other.row2.z

        return product


    def multiplyByScalar(self, multiplier):
        """Multiply this matrix by input multiplier.

        Arguments:
        multiplier -- Float, second term to use in multiplication operation.

        Return:
        New Matrix33 equal to product of this matrix and input multiplier.

        """

        if not isinstance(multiplier, float) and not isinstance(multiplier, int):
            raise TypeError("Matrix33 multiplyByScalar: Invalid 'multiplier' argument.")

        return Matrix33(self.row0.multiplyByScalar(multiplier),
                       self.row1.multiplyByScalar(multiplier),
                       self.row2.multiplyByScalar(multiplier))


    def divideByScalar(self, divisor):
        """Divides this matrix by input divisor.

        Arguments:
        divisor -- Float, number to divide this vec by.

        Return:
        New matrix equal to the quotient of this matrix and the input divisor.

        """

        if not isinstance(divisor, (float, int)):
            raise TypeError("Matrix33 divideByScalar: Invalid 'divisor' argument.")
        elif divisor < 0:
            raise ValueError("Matrix33 divideByScalar: 'divisor' argument is less than zero.")

        return self.multiplyByScalar(1.0 / divisor)


    def determinant(self):
        """Calculates the determinant for this matrix.

        Return:
        Determinant

        """

        det = self.row0.x * self.row1.y * self.row2.z + \
              self.row0.y * self.row1.z * self.row2.x + \
              self.row0.z * self.row1.x * self.row2.y - \
              self.row0.x * self.row1.z * self.row2.y - \
              self.row0.y * self.row1.x * self.row2.z - \
              self.row0.z * self.row1.y * self.row2.x

        return det


    def inverse(self):
        """Calculates inverse of this matrix.

        Return:
        Inverse of this matrix.

        """

        inverse = Matrix33()
        det = self.determinant()

        if det < 0:
            raise ValueError("Matrix33 inverse: determinant is less than zero.")

        return inverse.divideByScalar(det)


    def transpose(self):
        """Flip the matrix diagonally.

        Return:
        New Matrix33 with the matrix flipped diagonally.

        """

        transposition = Matrix33()
        transposition.row0.x = self.row0.x
        transposition.row0.y = self.row1.x
        transposition.row0.z = self.row2.x

        transposition.row1.x = self.row0.y
        transposition.row1.y = self.row1.y
        transposition.row1.z = self.row2.y

        transposition.row2.x = self.row0.z
        transposition.row2.y = self.row1.z
        transposition.row2.z = self.row2.z

        return transposition


    def clone(self):
        """Clone the Matrix33 into a new Matrix33.

        Return:
        New Matrix33 with same values as this Matrix33.

        """

        return Matrix33(row0=self.row0.clone(), row1=self.row1.clone(), row2=self.row2.clone())



class Matrix44(MathObject):
    """4x4 Matrix object."""

    def __init__(self, row0=None, row1=None, row2=None, row3=None):
        """Initialize and set values in the 4x4 matrix."""

        super(Matrix44, self).__init__()
        self.components = None
        self.set(row0, row1, row2, row3)


    def __str__(self):
        """Return a string representation of the 4x4 matrix."""

        return "Matrix44(" + str(self.row0) + "," + str(self.row1) + "," + str(self.row2) + "," + str(self.row3) + ")"


    def set(self, row0=None, row1=None, row2=None, row3=None):
        """Sets the row values for the 4x4 matrix.

        Arguments:
        row0 -- Vec4
        row1 -- Vec4
        row2 -- Vec4
        row3 -- Vec4

        Return:
        Self

        """

        if row0 is None:
            self.row0 = Vec4(1.0, 0.0, 0.0, 0.0)
        elif not isinstance(row0, Vec4):
            raise TypeError("Matrix44: Invalid 'row0' argument.")
        else:
            self.row0 = row0.clone()

        if row1 is None:
            self.row1 = Vec4(0.0, 1.0, 0.0, 0.0)
        elif not isinstance(row1, Vec4):
            raise TypeError("Matrix44: Invalid 'row0' argument.")
        else:
            self.row1 = row1.clone()

        if row2 is None:
            self.row2 = Vec4(0.0, 0.0, 1.0, 0.0)
        elif not isinstance(row2, Vec4):
            raise TypeError("Matrix44: Invalid 'row2' argument.")
        else:
            self.row2 = row2.clone()

        if row3 is None:
            self.row3 = Vec4(0.0, 0.0, 0.0, 1.0)
        elif not isinstance(row3, Vec4):
            raise TypeError("Matrix44: Invalid 'row3' argument.")
        else:
            self.row3 = row3.clone()

        self.components = self.toArray()

        return self


    def setFromArray(self, a):
        """Set the matrix values from input array.

        Arguments:
        a -- List of 16 matrix values.

        Return:
        True if successful.
        """

        self.row0.x = a[0]
        self.row0.y = a[1]
        self.row0.z = a[2]
        self.row0.w = a[3]

        self.row1.x = a[4]
        self.row1.y = a[5]
        self.row1.z = a[6]
        self.row1.w = a[7]

        self.row2.x = a[8]
        self.row2.y = a[9]
        self.row2.z = a[10]
        self.row2.w = a[11]

        self.row3.x = a[12]
        self.row3.y = a[13]
        self.row3.z = a[14]
        self.row3.w = a[15]

        return True


    def toArray(self):
        """Creates a 1D array of the matrix components.

        Return:
        1D array of matrix components.

        """

        components = [x for x in xrange(16)]

        components[0] = self.row0.x
        components[1] = self.row0.y
        components[2] = self.row0.z
        components[3] = self.row0.w

        components[4] = self.row1.x
        components[5] = self.row1.y
        components[6] = self.row1.z
        components[7] = self.row1.w

        components[8] = self.row2.x
        components[9] = self.row2.y
        components[10] = self.row2.z
        components[11] = self.row2.w

        components[12] = self.row3.x
        components[13] = self.row3.y
        components[14] = self.row3.z
        components[15] = self.row3.w

        return components


    def add(self, matrix):
        """Adds this matrix with input matrix.

        Arguments:
        matrix -- Matrix44 -- Input matrix to add to this matrix.

        Return:
        New matrix with sum of input matrix and this matrix.

        """

        if not isinstance(matrix, Matrix44):
            raise TypeError("Matrix44 Add: Invalid 'matrix' argument.")

        return Matrix44(self.row0.add(matrix.row0),
                       self.row1.add(matrix.row1),
                       self.row2.add(matrix.row2),
                       self.row3.add(matrix.row3))


    def subtract(self, matrix):
        """Subtracts this input matrix from this matrix.

        Arguments:
        matrix -- Matrix44 -- Input matrix to subtract from this matrix.

        Return:
        New matrix with difference of input matrix and this matrix.

        """

        if not isinstance(matrix, Matrix44):
            raise TypeError("Matrix44 Subtract: Invalid 'matrix' argument.")

        return Matrix44(self.row0.subtract(matrix.row0),
                     self.row1.subtract(matrix.row1),
                     self.row2.subtract(matrix.row2),
                     self.row3.subtract(matrix.row3))


    def multiply(self, matrix):
        """Multiply this matrix by input matrix.

        Arguments:
        matrix -- Matrix44, second term to use in multiplication operation.

        Return:
        New Matrix44 equal to product of this matrix and input matrix.

        """

        if not isinstance(matrix, Matrix44):
            raise TypeError("Matrix44 Multiply: Invalid 'matrix' argument.")

        product = Matrix44()
        product.row0.x = self.row0.x * matrix.row0.x + self.row0.y * matrix.row1.x + self.row0.z * matrix.row2.x + self.row0.w * matrix.row3.x
        product.row0.y = self.row0.x * matrix.row0.y + self.row0.y * matrix.row1.y + self.row0.z * matrix.row2.y + self.row0.w * matrix.row3.y
        product.row0.z = self.row0.x * matrix.row0.z + self.row0.y * matrix.row1.z + self.row0.z * matrix.row2.z + self.row0.w * matrix.row3.z
        product.row0.w = self.row0.x * matrix.row0.w + self.row0.y * matrix.row1.w + self.row0.z * matrix.row2.w + self.row0.w * matrix.row3.w

        product.row1.x = self.row1.x * matrix.row0.x + self.row1.y * matrix.row1.x + self.row1.z * matrix.row2.x + self.row1.w * matrix.row3.x
        product.row1.y = self.row1.x * matrix.row0.y + self.row1.y * matrix.row1.y + self.row1.z * matrix.row2.y + self.row1.w * matrix.row3.y
        product.row1.z = self.row1.x * matrix.row0.z + self.row1.y * matrix.row1.z + self.row1.z * matrix.row2.z + self.row1.w * matrix.row3.z
        product.row1.w = self.row1.x * matrix.row0.w + self.row1.y * matrix.row1.w + self.row1.z * matrix.row2.w + self.row1.w * matrix.row3.w

        product.row2.x = self.row2.x * matrix.row0.x + self.row2.y * matrix.row1.x + self.row2.z * matrix.row2.x + self.row2.w * matrix.row3.x
        product.row2.y = self.row2.x * matrix.row0.y + self.row2.y * matrix.row1.y + self.row2.z * matrix.row2.y + self.row2.w * matrix.row3.y
        product.row2.z = self.row2.x * matrix.row0.z + self.row2.y * matrix.row1.z + self.row2.z * matrix.row2.z + self.row2.w * matrix.row3.z
        product.row2.w = self.row2.x * matrix.row0.w + self.row2.y * matrix.row1.w + self.row2.z * matrix.row2.w + self.row2.w * matrix.row3.w

        product.row3.x = self.row3.x * matrix.row0.x + self.row3.y * matrix.row1.x + self.row3.z * matrix.row2.x + self.row3.w * matrix.row3.x
        product.row3.y = self.row3.x * matrix.row0.y + self.row3.y * matrix.row1.y + self.row3.z * matrix.row2.y + self.row3.w * matrix.row3.y
        product.row3.z = self.row3.x * matrix.row0.z + self.row3.y * matrix.row1.z + self.row3.z * matrix.row2.z + self.row3.w * matrix.row3.z
        product.row3.w = self.row3.x * matrix.row0.w + self.row3.y * matrix.row1.w + self.row3.z * matrix.row2.w + self.row3.w * matrix.row3.w
        return product


    def multiplyByScalar(self, multiplier):
        """Multiply this matrix by input multiplier.

        Arguments:
        multiplier -- Float, second term to use in multiplication operation.

        Return:
        New Matrix44 equal to product of this matrix and input multiplier.

        """

        if not isinstance(multiplier, float) and not isinstance(multiplier, int):
            raise TypeError("Matrix44 multiplyByScalar: Invalid 'multiplier' argument.")

        return Matrix44(self.row0.multiplyByScalar(multiplier),
                       self.row1.multiplyByScalar(multiplier),
                       self.row2.multiplyByScalar(multiplier),
                       self.row3.multiplyByScalar(multiplier))


    def divideByScalar(self, divisor):
        """Divides this matrix by input divisor.

        Arguments:
        divisor -- Float, number to divide this vec by.

        Return:
        New matrix equal to the quotient of this matrix and the input divisor.

        """

        if not isinstance(divisor, (float, int)):
            raise TypeError("Matrix44 divideByScalar: Invalid 'divisor' argument.")
        elif divisor < 0:
            raise ValueError("Matrix44 divideByScalar: 'divisor' argument is less than zero.")

        return self.multiplyByScalar(1.0 / divisor)


    def determinant(self):
        """Calculates the determinant for this matrix.

        Return:
        Determinant

        """

        a0 = self.row0.x * self.row1.y - self.row0.y * self.row1.x
        a1 = self.row0.x * self.row1.z - self.row0.z * self.row1.x
        a2 = self.row0.x * self.row1.t - self.row0.t * self.row1.x
        a3 = self.row0.y * self.row1.z - self.row0.z * self.row1.y
        a4 = self.row0.y * self.row1.t - self.row0.t * self.row1.y
        a5 = self.row0.z * self.row1.t - self.row0.t * self.row1.z
        b0 = self.row2.x * self.row3.y - self.row2.y * self.row3.x
        b1 = self.row2.x * self.row3.z - self.row2.z * self.row3.x
        b2 = self.row2.x * self.row3.t - self.row2.t * self.row3.x
        b3 = self.row2.y * self.row3.z - self.row2.z * self.row3.y
        b4 = self.row2.y * self.row3.t - self.row2.t * self.row3.y
        b5 = self.row2.z * self.row3.t - self.row2.t * self.row3.z

        det = a0 * b5 - a1 * b4 + a2 * b3 + a3 * b2 - a4 * b1 + a5 * b0

        return det


    def inverse(self):
        """Calculates inverse of this matrix.

        Return:
        Inverse of this matrix.

        """

        inverse = Matrix44()
        det = self.determinant()

        if det < 0:
            raise ValueError("Matrix44 inverse: determinant is less than zero.")

        return inverse.divideByScalar(det)


    def transpose(self):
        """Flip the matrix diagonally.

        Return:
        New Matrix44 with the matrix flipped diagonally.

        """

        transposition = Matrix44()
        transposition.row0.x = self.row0.x
        transposition.row0.y = self.row1.x
        transposition.row0.z = self.row2.x
        transposition.row0.w = self.row3.x

        transposition.row1.x = self.row0.y
        transposition.row1.y = self.row1.y
        transposition.row1.z = self.row2.y
        transposition.row1.w = self.row3.y

        transposition.row2.x = self.row0.z
        transposition.row2.y = self.row1.z
        transposition.row2.z = self.row2.z
        transposition.row2.w = self.row3.z

        transposition.row3.x = self.row0.w
        transposition.row3.y = self.row1.w
        transposition.row3.z = self.row2.w
        transposition.row3.w = self.row3.w

        return transposition


    def clone(self):
        """Clone the Matrix44 into a new Matrix44.

        Return:
        New Matrix44 with same values as this Matrix44.

        """

        return Matrix44(row0=self.row0.clone(), row1=self.row1.clone(), row2=self.row2.clone(), row3=self.row3.clone())

