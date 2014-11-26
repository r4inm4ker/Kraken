"""Kraken - maths.matrix module.

Classes:
Mat44 -- Matrix 3 transform object.
"""

from math_object import MathObject
from vec import Vec3, Vec4

class Mat44(MathObject):
    """3x3 Matrix object."""

    def __init__(self, row0=None, row1=None, row2=None):
        """Initialize and set values in the 3x3 matrix."""

        super(Mat44, self).__init__()

        if self.getTypeName(row0) == 'Mat44':
            self.rtval = x
        else:
            self.rtval = KC.inst().rtVal('Mat44')
            self.setRows(row0, row1, row2)


    def __str__(self):
        """Return a string representation of the 3x3 matrix."""
        return "Mat44(" + str(self.row0) + "," + str(self.row1) + "," + str(self.row2) + "," + str(self.row3) + ")"

    # Setter from vectors, row-wise
    def setRows(self, row0, row1, row2):
        self.rtval.setRows('', KC.inst().rtVal('Vec3', row0), KC.inst().rtVal('Vec3', row0), KC.inst().rtVal('Vec3', row2), KC.inst().rtVal('Vec3', row3))

    # Setter from vectors, column-wise
    def setColumns(self, col0, col1, col2, col3):
        self.rtval.setColumns('', KC.inst().rtVal('Vec3', col0), KC.inst().rtVal('Vec3', col0), KC.inst().rtVal('Vec3', col2), KC.inst().rtVal('Vec3', col3))

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
        return self.rtval.add('Boolean', KC.inst().rtVal('Mat44', other))

    # Returns true if this matrix is almost equal to the given matrix within the provided precision range
    def almostEqual(self, other, precision):
        return self.rtval.add('Boolean', KC.inst().rtVal('Mat44', other), KC.inst().rtVal('Scalar', precision))

    # Returns true if this matrix is almost the same as another one
    # (using a default precision)
    def almostEqual(self, other):
        return self.rtval.add('Boolean', KC.inst().rtVal('Mat44', other))

    # # Equals operator
    # def Boolean == (Mat44 a, Mat44 b) {
    #   return a.equal(b);
    # }

    # # Not equals operator
    # def Boolean != (Mat44 a, Mat44 b) {
    #   return !a.equal(b);
    # }

    # # Returns the addition of two matrices
    # def Mat44 + (Mat44 a, Mat44 b) {
    #   return Mat44( a.row0 + b.row0, a.row1 + b.row1, a.row2 + b.row2 );
    # }

    # # Adds another matrix to this one
    # def  += (Mat44 other) {
    #   this = this + other;
    # }

    # # Returns the subtraction of two matrices
    # def Mat44 - (Mat44 a, Mat44 b) {
    #   return Mat44( a.row0 - b.row0, a.row1 - b.row1, a.row2 - b.row2 );
    # }

    # # Subtracts another matrix from this one
    # def  -= (Mat44 other) {
    #   this = this - other;
    # }

    # # Returns the product of two matrices
    # function Mat44 * (Mat44 left, Mat44 right) {
    #   Mat44 result;

    #   result.row0.x = left.row0.x * right.row0.x + left.row0.y * right.row1.x + left.row0.z * right.row2.x;
    #   result.row0.y = left.row0.x * right.row0.y + left.row0.y * right.row1.y + left.row0.z * right.row2.y;
    #   result.row0.z = left.row0.x * right.row0.z + left.row0.y * right.row1.z + left.row0.z * right.row2.z;

    #   result.row1.x = left.row1.x * right.row0.x + left.row1.y * right.row1.x + left.row1.z * right.row2.x;
    #   result.row1.y = left.row1.x * right.row0.y + left.row1.y * right.row1.y + left.row1.z * right.row2.y;
    #   result.row1.z = left.row1.x * right.row0.z + left.row1.y * right.row1.z + left.row1.z * right.row2.z;

    #   result.row2.x = left.row2.x * right.row0.x + left.row2.y * right.row1.x + left.row2.z * right.row2.x;
    #   result.row2.y = left.row2.x * right.row0.y + left.row2.y * right.row1.y + left.row2.z * right.row2.y;
    #   result.row2.z = left.row2.x * right.row0.z + left.row2.y * right.row1.z + left.row2.z * right.row2.z;

    #   return result;
    # }

    # # Returns the product of a matrix and a Vec3
    # def Vec3 * (Mat44 mat44, Vec3 vec3) {
    #   return Vec3(
    #     row0.self, x * vec3.x + row0.self, y * vec3.y + row0.self, z * vec3.z,
    #     row1.self, x * vec3.x + row1.self, y * vec3.y + row1.self, z * vec3.z,
    #     row2.self, x * vec3.x + row2.self, y * vec3.y + row2.self, z * vec3.z
    #   );
    # }

    # # Returns the product of a matrix and a scalar
    # def Mat44 * (Mat44 mat44, Scalar s) {
    #   return Mat44( row0 self, * s, row1 self, * s, row2 self, * s );
    # }

    # # Returns the product of a scalar and a matrix
    # def Mat44 * (Scalar s, Mat44 mat44) {
    #   return Mat44( row0 self, * s, row1 self, * s, row2 self, * s );
    # }

    # # Multiplies this matrix with another one
    # def  *= (Mat44 other) {
    #   this = this * other;
    # }

    # # Multiplies this matrix with a scalar
    # def  *= (Scalar other) {
    #   this = this * other;
    # }

    # # Returns the division of a matrix and a scalar
    # def Mat44 / (Mat44 mat44, Scalar s) {
    #   if( Boolean(Fabric_Guarded) && Math_badDivisor( s ) )//Perf: check first to avoid building the report string
    #     Math_reportBadDivisor( s, "divide"self,  );
    #   return mat44 * (1.0 / s);
    # }

    # # Divides this matrix by a scalar
    # def  /= (Scalar other) {
    #   this = this / other;
    # }

    # Overload method for the add operator
    def add(self, other):
        return self.rtval.add('Mat44', KC.inst().rtVal('Mat44', other))

    # Overload method for the subtract operator
    def subtract(self, other):
        return self.rtval.subtract('Mat44', KC.inst().rtVal('Mat44', other))

    # Overload method for the multiply operator
    def multiply(self, other):
        return self.rtval.multiply('Mat44', KC.inst().rtVal('Mat44', other))

    # Returns the product of this matrix and a scalar
    def multiplyScalar(self, other):
        return self.rtval.multiplyScalar('Mat44', KC.inst().rtVal('Scalar', other))

    # Returns the product of this matrix and a vector
    def multiplyVector(self, other):
        return self.rtval.multiplyVector('Vec3', KC.inst().rtVal('Vec3', other))

    # Returns the division of this matrix and a scalar
    def divideScalar(self, other):
        return self.rtval.divideScalar('Mat44', other)

    # Returns the determinant of this matrix
    def determinant(self):
        return self.rtval.determinant('Scalar')

    # Returns the adjoint matrix of this matrix
    def adjoint(self):
        return self.rtval.adjoint('Mat44')

    # Returns the inverse matrix of this matrix
    def inverse(self):
        return self.rtval.inverse('Mat44')

    def inverse_safe(self):
        return self.rtval.inverse_safe('Mat44')

    # Returns the transposed matrix of this matrix
    def transpose(self):
        return self.rtval.transpose('Mat44')



