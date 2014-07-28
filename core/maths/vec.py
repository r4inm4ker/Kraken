"""Kraken - maths.vec module.

Classes:
Vec2 -- Vector 2 object.
Vec3 -- Vector 3 object.
Vec4 -- Vector 4 object.
"""

import math
from math_object import MathObject


class Vec2(MathObject):
    """Vector 2 object."""

    def __init__(self, x=0.0, y=0.0):
        """Initializes x, y values for Vec2 object."""

        super(Vec2, self).__init__()
        self.x = 0
        self.y = 0
        self.set(x=x, y=y)


    def __str__(self):
        """String representation of the Vec2 object."""

        return "Vec2(" + str(self.x) + "," + str(self.y) + ")"


    def set(self, x=0.0, y=0.0):
        """Sets values for x, y attributes of Vec2.

        Arguments:
        x -- Float / Int, X axis value.
        y -- Float / Int, Y axis value.

        Return:
        Vec2 object.

        """

        if (isinstance(x, float) or isinstance(x, int)) and \
            (isinstance(y, float) or isinstance(y, int)):
            self.x = x
            self.y = y

        else:
            raise TypeError("Vec2 arguments are not of float / int type!")

        return self


    def setFromArray(self, array):
        """Sets values for x,y attributes of Vec2 from a list.

        Arguments:
        array -- List, [x,y]

        Return:
        True if successful.

        """

        if type(array) is not list:
            raise TypeError("Kraken: Vec2: setFromArray 'array' argument must be of type 'list'!")

        self.x = array[0]
        self.y = array[1]

        return True


    def toArray(self):
        """Returns a list of x,y values for this vector.

        Return:
        List of x,y values.

        """

        return [self.x, self.y]


    def copy(self, vec):
        """Copy the values from input vector.

        Arguments:
        vec -- Vec2, vector to copy values from.

        Return:
        This vector.

        """

        self.x = vec.x
        self.y = vec.y

        return self


    def add(self, vec):
        """Add this vector with input vector.

        Arguments:
        vec -- Vec2, second term to use in summation operation.

        Return:
        New Vec2 equal to the sum of this vector and input vector.

        """

        if not isinstance(vec, Vec2):
            raise TypeError("Vec2: input vec is not of Vec2 type!")

        return Vec2(x=self.x + vec.x, y=self.y + vec.y)


    def subtract(self, vec):
        """Subtract input vector from this vector.

        Arguments:
        vec -- Vec2, second term to use in subtraction operation.

        Return:
        New Vec2 equal to difference of this vector and input vector.

        """

        if not isinstance(vec, Vec2):
            raise TypeError("Vec2: input vec is not of Vec2 type!")

        return Vec2(x=self.x - vec.x, y=self.y - vec.y)


    def multiply(self, multiplier):
        """Multiply input vector by input vector.

        Arguments:
        multiplier -- Vec2, second term to use in multiplication operation.

        Return:
        New Vec2 equal to product of this vector and input vector.

        """

        if not isinstance(multiplier, Vec2):
            raise TypeError("Vec2: multiplier is not of Vec2 type!")

        return Vec2(x=self.x * multiplier.x, y=self.y * multiplier.y)


    def multiplyByScalar(self, multiplier):
        """Multiplies this vector by multiplier.

        Arguments:
        multiplier -- Float, number to multiplier this vector by.

        Return:
        New Vec2 equal to the product of this vector and input multiplier.

        """

        if not isinstance(multiplier, float) and not isinstance(multiplier, int):
            raise TypeError("Vec2: multiplier is not of float / int type!")

        return Vec2(x=self.x * multiplier, y=self.y * multiplier)


    def divide(self, divisor):
        """Divides this vector by input vector.

        Arguments:
        divisor -- Vec2, second term to use in subtraction operation.

        Return:
        New vector with subtraction of this vector and input vector.

        """

        if not isinstance(divisor, Vec2):
            raise TypeError("Vec2: divisor is not of Vec2 type!")

        return Vec2(x=self.x / divisor.x, y=self.y / divisor.y)


    def divideByScalar(self, divisor):
        """Divides this vector by input divisor.

        Arguments:
        divisor -- Float, number to divide this vec by.

        Return:
        New vector equal to the quotient of this vector and the input divisor.

        """

        if not isinstance(divisor, float) and not isinstance(divisor, int):
            raise TypeError("Vec2: divisor is not of float / int type!")

        return Vec2(x=self.x / divisor, y=self.y / divisor)


    def negate(self):
        """Negate this vector.

        Return:
        New vector equal to the negation of this vector.

        """

        return Vec2(x=-self.x, y=-self.y)


    def inverse(self):
        """Invert this vector.

        Return:
        New vector equal to the inversion of this vector.

        """

        return Vec2(x=1.0 / self.x, y=1.0 / self.y)


    def dotProduct(self, vec):
        """Dot product this vector and input vector.

        Arguments:
        vec -- Vec2, second term to use in dot product operation.

        Return:
        Float / Int equal to the dot product of this vector.

        """

        if not isinstance(vec, Vec2):
            raise TypeError("Vec2: input vec is not of Vec2 type!")

        return self.x * vec.x + self.y * vec.y


    def cross(self, vec):
        """Cross product this vector and input vector.

        Arguments:
        vec -- Vec2, second term to use in dot product operation.

        Return:
        New vector equal to the cross product of this vector and input vector.

        """

        if not isinstance(vec, Vec2):
            raise TypeError("Vec2: input vec is not of Vec2 type!")

        return self.x * vec.y - self.y * vec.x


    def length(self):
        """Length of this vector.

        Return:
        Float / Int equal to the length of this vector.

        """

        return math.sqrt(self.dotProduct(self))


    def unit(self):
        """Creates a unit vector from this vector.

        Return:
        New unit vector.

        """

        return self.divideByScalar(self.length())


    def normalize(self):
        """Normalize this vector.

        Return:
        Length of this vector.

        """

        length = self.length()
        self.x = self.x / length
        self.y = self.y / length

        return self.length()


    def angleBetween(self, vec):
        """Angle between this vector and input vector.

        Arguments:
        vec -- Vec2, second vector used to get the angle between.

        Return:
        New vector equal to the cross product of this vector and input vector.

        """

        if not isinstance(vec, Vec2):
            raise TypeError("Vec2: input vec is not of Vec2 type!")

        return math.acos(self.dotProduct(vec.unit()))


    def distanceBetween(self, vec):
        """Get the distance between this vector and input vector.

        Arguments:
        vec -- Vec2, second vector used to get the distance between.

        Return:
        Float / Int of the distance between this vector and the input vector.

        """

        if not isinstance(vec, Vec2):
            raise TypeError("Vec2: input vec is not of Vec2 type!")

        return self.subtract(vec).length()


    def linearInterpolate(self, vec, blend):
        """Linear interpolate between this vector and input vector.

        Arguments:
        vec -- Vec2, second vector used to get the distance between.

        Return:
        New vector linearly interpolated between this vector and input vector.

        """

        if not isinstance(vec, Vec2):
            raise TypeError("Vec2: input vec is not of Vec2 type!")

        if not isinstance(blend, float) and not isinstance(blend, int):
            raise TypeError("Vec2: blend is not of float / int type!")

        return self.add(vec.subtract(self).multiplyByScalar(blend))


    def clone(self):
        """Clone the Vec2 into a new Vec2.

        Return:
        New Vec2 with same values as this Vec2.

        """

        return Vec2(self.x, self.y)


    def equal(self, other):
        """Check if this Vec2 is equal to other Vec2"""

        if not isinstance(other, Vec2):
            raise TypeError("Vec2: Invalid type for 'other' argument. Must be a Vec2.")

        return self.x == other.x and \
               self.y == other.y


    def almostEqual(self, other, precision=10e-12):
        """Check if this Vec4 is almost equal to other Vec4."""

        if not isinstance(other, Vec2):
            raise TypeError("Vec2: Invalid type for 'other' argument. Must be a Vec2.")

        return abs(self.x - other.x) < precision and \
               abs(self.y - other.y) < precision





class Vec3(MathObject):
    """Vector 3 object."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initializes x, y, z values for Vec3 object."""

        super(Vec3, self).__init__()
        self.x = 0
        self.y = 0
        self.z = 0
        self.set(x=x, y=y, z=z)


    def __str__(self):
        """String representation of the Vec3 object."""

        return "Vec3(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"


    def set(self, x=0.0, y=0.0, z=0.0):
        """Sets values for x, y, z attributes of Vec3.

        Arguments:
        x -- Float / Int, X axis value.
        y -- Float / Int, Y axis value.
        z -- Float / Int, Z axis value.

        Return:
        Vec3 object.

        """

        if (isinstance(x, float) or isinstance(x, int)) and \
            (isinstance(y, float) or isinstance(y, int)) and \
            (isinstance(z, float) or isinstance(z, int)):
            self.x = x
            self.y = y
            self.z = z

        else:
            raise TypeError("Vec3 arguments are not of float / int type!")

        return self


    def setFromArray(self, array):
        """Sets values for x,y,z attributes of Vec3 from a list.

        Arguments:
        array -- List, [x,y,z]

        Return:
        True if successful.

        """

        if type(array) is not list:
            raise TypeError("Kraken: Vec3: setFromArray 'array' argument must be of type 'list'!")

        self.x = array[0]
        self.y = array[1]
        self.z = array[2]

        return True


    def toArray(self):
        """Returns a list of x,y,z values for this vector.

        Return:
        List of x,y,z values.

        """

        return [self.x, self.y, self.z]


    def copy(self, vec):
        """Copy the values from input vector.

        Arguments:
        vec -- Vec3, vector to copy values from.

        Return:
        This vector.

        """

        self.x = vec.x
        self.y = vec.y
        self.z = vec.z

        return self


    def add(self, vec):
        """Add this vector with input vector.

        Arguments:
        vec -- Vec3, second term to use in summation operation.

        Return:
        New Vec3 equal to the sum of this vector and input vector.

        """

        if not isinstance(vec, Vec3):
            raise TypeError("Vec3: input vec is not of Vec3 type!")

        return Vec3(x=self.x + vec.x, y=self.y + vec.y, z=self.z + vec.z)


    def subtract(self, vec):
        """Subtract input vector from this vector.

        Arguments:
        vec -- Vec3, second term to use in subtraction operation.

        Return:
        New Vec3 equal to difference of this vector and input vector.

        """

        if not isinstance(vec, Vec3):
            raise TypeError("Vec3: input vec is not of Vec3 type!")

        return Vec3(x=self.x - vec.x, y=self.y - vec.y, z=self.z - vec.z)


    def multiply(self, multiplier):
        """Multiply input vector by input vector.

        Arguments:
        multiplier -- Vec3, second term to use in multiplication operation.

        Return:
        New Vec3 equal to product of this vector and input vector.

        """

        if not isinstance(multiplier, Vec3):
            raise TypeError("Vec3: multiplier is not of Vec3 type!")

        return Vec3(x=self.x * multiplier.x, y=self.y * multiplier.y, z=self.z * multiplier.z)


    def multiplyByScalar(self, multiplier):
        """Multiplies this vector by multiplier.

        Arguments:
        multiplier -- Float, number to multiplier this vector by.

        Return:
        New Vec3 equal to the product of this vector and input multiplier.

        """

        if not isinstance(multiplier, float) and not isinstance(multiplier, int):
            raise TypeError("Vec3: multiplier is not of float / int type!")

        return Vec3(x=self.x * multiplier, y=self.y * multiplier, z=self.z * multiplier)


    def divide(self, divisor):
        """Divides this vector by input vector.

        Arguments:
        divisor -- Vec3, second term to use in subtraction operation.

        Return:
        New vector with subtraction of this vector and input vector.

        """

        if not isinstance(divisor, Vec3):
            raise TypeError("Vec3: divisor is not of Vec3 type!")

        return Vec3(x=self.x / divisor.x, y=self.y / divisor.y, z=self.z / divisor.z)


    def divideByScalar(self, divisor):
        """Divides this vector by input divisor.

        Arguments:
        divisor -- Float, number to divide this vec by.

        Return:
        New vector equal to the quotient of this vector and the input divisor.

        """

        if not isinstance(divisor, float) and not isinstance(divisor, int):
            raise TypeError("Vec3: divisor is not of float / int type!")

        return Vec3(x=self.x / divisor, y=self.y / divisor, z=self.z / divisor)


    def negate(self):
        """Negate this vector.

        Return:
        New vector equal to the negation of this vector.

        """

        return Vec3(x=-self.x, y=-self.y, z=-self.z)


    def inverse(self):
        """Invert this vector.

        Return:
        New vector equal to the inversion of this vector.

        """

        return Vec3(x=1.0 / self.x, y=1.0 / self.y, z=1.0 / self.z)


    def dotProduct(self, vec):
        """Dot product this vector and input vector.

        Arguments:
        vec -- Vec3, second term to use in dot product operation.

        Return:
        Float / Int equal to the dot product of this vector.

        """

        if not isinstance(vec, Vec3):
            raise TypeError("Vec3: input vec is not of Vec3 type!")

        return self.x * vec.x + self.y * vec.y + self.z * vec.z


    def cross(self, vec):
        """Cross product this vector and input vector.

        Arguments:
        vec -- Vec3, second term to use in dot product operation.

        Return:
        New vector equal to the cross product of this vector and input vector.

        """

        if not isinstance(vec, Vec3):
            raise TypeError("Vec3: input vec is not of Vec3 type!")

        return Vec3(self.y * vec.z - self.z * vec.y, self.z * vec.x - self.x * vec.z, self.x * vec.y - self.y * vec.x)


    def length(self):
        """Length of this vector.

        Return:
        Float / Int equal to the length of this vector.

        """

        return math.sqrt(self.dotProduct(self))


    def lengthSquared(self):
        """Get squared length of vector."""

        return self.dotProduct(self)


    def unit(self):
        """Creates a unit vector from this vector.

        Return:
        New unit vector.

        """

        return self.divideByScalar(self.length())


    def normalize(self):
        """Normalize this vector.

        Return:
        Length of this vector.

        """

        length = self.length()
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length

        return self.length()


    def angleBetween(self, vec):
        """Angle between this vector and input vector.

        Arguments:
        vec -- Vec3, second vector used to get the angle between.

        Return:
        New vector equal to the cross product of this vector and input vector.

        """

        if not isinstance(vec, Vec3):
            raise TypeError("Vec3: input vec is not of Vec3 type!")

        return math.acos(self.dotProduct(vec.unit()))


    def distanceBetween(self, vec):
        """Get the distance between this vector and input vector.

        Arguments:
        vec -- Vec3, second vector used to get the distance between.

        Return:
        Float / Int of the distance between this vector and the input vector.

        """

        if not isinstance(vec, Vec3):
            raise TypeError("Vec3: input vec is not of Vec3 type!")

        return self.subtract(vec).length()


    def linearInterpolate(self, vec, blend):
        """Linear interpolate between this vector and input vector.

        Arguments:
        vec -- Vec3, second vector used to get the distance between.

        Return:
        New vector linearly interpolated between this vector and input vector.

        """

        if not isinstance(vec, Vec3):
            raise TypeError("Vec3: input vec is not of Vec3 type!")

        if not isinstance(blend, float) and not isinstance(blend, int):
            raise TypeError("Vec3: blend is not of float / int type!")

        return self.add(vec.subtract(self).multiplyByScalar(blend))


    def clone(self):
        """Clone the Vec3 into a new Vec3.

        Return:
        New Vec3 with same values as this Vec3.

        """

        return Vec3(self.x, self.y, self.z)


    def equal(self, other):
        """Check if this Vec3 is equal to other Vec3"""

        if not isinstance(other, Vec3):
            raise TypeError("Vec3: Invalid type for 'other' argument. Must be a Vec3.")

        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z


    def almostEqual(self, other, precision=10e-12):
        """Check if this Vec4 is almost equal to other Vec4."""

        if not isinstance(other, Vec3):
            raise TypeError("Vec3: Invalid type for 'other' argument. Must be a Vec3.")

        return abs(self.x - other.x) < precision and \
               abs(self.y - other.y) < precision and \
               abs(self.z - other.z) < precision




class Vec4(MathObject):
    """Vector 4 object."""

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        """Initializes x, y, z values for Vec4 object."""

        super(Vec4, self).__init__()
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0
        self.set(x=x, y=y, z=z, w=w)


    def __str__(self):
        """String representation of the Vec4 object."""

        return "Vec4(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + "," + str(self.w) + ")"


    def set(self, x=0.0, y=0.0, z=0.0, w=0.0):
        """Sets values for x, y, z attributes of Vec4.

        Arguments:
        x -- Float / Int, X axis value.
        y -- Float / Int, Y axis value.
        z -- Float / Int, Z axis value.
        w -- Float / Int, W axis value.

        Return:
        Vec4 object.

        """

        if (isinstance(x, float) or isinstance(x, int)) and \
            (isinstance(y, float) or isinstance(y, int)) and \
            (isinstance(z, float) or isinstance(z, int)) and \
            (isinstance(w, float) or isinstance(w, int)):
            self.x = x
            self.y = y
            self.z = z
            self.w = w

        else:
            raise TypeError("Vec4 arguments are not of float / int type!")

        return self


    def setFromArray(self, array):
        """Sets values for x,y,z,w attributes of Vec4 from a list.

        Arguments:
        array -- List, [x,y,z,w]

        Return:
        True if successful.

        """

        if type(array) is not list:
            raise TypeError("Kraken: Vec4: setFromArray 'array' argument must be of type 'list'!")

        self.x = array[0]
        self.y = array[1]
        self.z = array[2]
        self.w = array[3]

        return True


    def toArray(self):
        """Returns a list of x,y,z values for this vector.

        Return:
        List of x,y,z values.

        """

        return [self.x, self.y, self.z]


    def copy(self, vec):
        """Copy the values from input vector.

        Arguments:
        vec -- Vec4, vector to copy values from.

        Return:
        This vector.

        """

        self.x = vec.x
        self.y = vec.y
        self.z = vec.z
        self.w = vec.w

        return self


    def add(self, vec):
        """Add this vector with input vector.

        Arguments:
        vec -- Vec4, second term to use in summation operation.

        Return:
        New Vec4 equal to the sum of this vector and input vector.

        """

        if not isinstance(vec, Vec4):
            raise TypeError("Vec4: input vec is not of Vec4 type!")

        return Vec4(x=self.x + vec.x, y=self.y + vec.y, z=self.z + vec.z, w=self.w + vec.w)


    def subtract(self, vec):
        """Subtract input vector from this vector.

        Arguments:
        vec -- Vec4, second term to use in subtraction operation.

        Return:
        New Vec4 equal to difference of this vector and input vector.

        """

        if not isinstance(vec, Vec4):
            raise TypeError("Vec4: input vec is not of Vec4 type!")

        return Vec4(x=self.x - vec.x, y=self.y - vec.y, z=self.z - vec.z, w=self.w - vec.w)


    def multiply(self, multiplier):
        """Multiply this vector by input vector.

        Arguments:
        multiplier -- Vec4, second term to use in multiplication operation.

        Return:
        New Vec4 equal to product of this vector and input vector.

        """

        if not isinstance(multiplier, Vec4):
            raise TypeError("Vec4: multiplier is not of Vec4 type!")

        return Vec4(x=self.x * multiplier.x, y=self.y * multiplier.y, z=self.z * multiplier.z, w=self.w * multiplier.w)


    def multiplyByScalar(self, multiplier):
        """Multiplies this vector by multiplier.

        Arguments:
        multiplier -- Float, number to multiplier this vector by.

        Return:
        New Vec4 equal to the product of this vector and input multiplier.

        """

        if not isinstance(multiplier, float) and not isinstance(multiplier, int):
            raise TypeError("Vec4: multiplier is not of float / int type!")

        return Vec4(x=self.x * multiplier, y=self.y * multiplier, z=self.z * multiplier, w=self.w * multiplier)


    def divide(self, divisor):
        """Divides this vector by input vector.

        Arguments:
        divisor -- Vec4, second term to use in subtraction operation.

        Return:
        New vector with subtraction of this vector and input vector.

        """

        if not isinstance(divisor, Vec4):
            raise TypeError("Vec4: divisor is not of Vec4 type!")

        return Vec4(x=self.x / divisor.x, y=self.y / divisor.y, z=self.z / divisor.z, w=self.w / divisor.w)


    def divideByScalar(self, divisor):
        """Divides this vector by input divisor.

        Arguments:
        divisor -- Float, number to divide this vec by.

        Return:
        New vector equal to the quotient of this vector and the input divisor.

        """

        if not isinstance(divisor, float) and not isinstance(divisor, int):
            raise TypeError("Vec4: divisor is not of float / int type!")

        return Vec4(x=self.x / divisor, y=self.y / divisor, z=self.z / divisor, w=self.w / divisor)


    def negate(self):
        """Negate this vector.

        Return:
        New vector equal to the negation of this vector.

        """

        return Vec4(x=-self.x, y=-self.y, z=-self.z, w=-self.w)


    def inverse(self):
        """Invert this vector.

        Return:
        New vector equal to the inversion of this vector.

        """

        return Vec4(x=1.0 / self.x, y=1.0 / self.y, z=1.0 / self.z, w=1.0 / self.w)


    def dotProduct(self, vec):
        """Dot product this vector and input vector.

        Arguments:
        vec -- Vec4, second term to use in dot product operation.

        Return:
        Float / Int equal to the dot product of this vector.

        """

        if not isinstance(vec, Vec4):
            raise TypeError("Vec4: input vec is not of Vec4 type!")

        return self.x * vec.x + self.y * vec.y + self.z * vec.z + self.w * vec.w


    def length(self):
        """Length of this vector.

        Return:
        Float / Int equal to the length of this vector.

        """

        return math.sqrt(self.dotProduct(self))


    def unit(self):
        """Creates a unit vector from this vector.

        Return:
        New unit vector.

        """

        return self.divideByScalar(self.length())


    def normalize(self):
        """Normalize this vector.

        Return:
        Length of this vector.

        """

        length = self.length()
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length
        self.w = self.w / length

        return self.length()


    def angleBetween(self, vec):
        """Angle between this vector and input vector.

        Arguments:
        vec -- Vec4, second vector used to get the angle between.

        Return:
        New vector equal to the cross product of this vector and input vector.

        """

        if not isinstance(vec, Vec4):
            raise TypeError("Vec4: input vec is not of Vec4 type!")

        return math.acos(self.dotProduct(vec.unit()))


    def distanceBetween(self, vec):
        """Get the distance between this vector and input vector.

        Arguments:
        vec -- Vec4, second vector used to get the distance between.

        Return:
        Float / Int of the distance between this vector and the input vector.

        """

        if not isinstance(vec, Vec4):
            raise TypeError("Vec4: input vec is not of Vec4 type!")

        return self.subtract(vec).length()


    def linearInterpolate(self, vec, blend):
        """Linear interpolate between this vector and input vector.

        Arguments:
        vec -- Vec4, second vector used to get the distance between.

        Return:
        New vector linearly interpolated between this vector and input vector.

        """

        if not isinstance(vec, Vec4):
            raise TypeError("Vec4: input vec is not of Vec4 type!")

        if not isinstance(blend, float) and not isinstance(blend, int):
            raise TypeError("Vec4: blend is not of float / int type!")

        return self.add(vec.subtract(self).multiplyByScalar(blend))


    def clone(self):
        """Clone the Vec4 into a new Vec4.

        Return:
        New Vec4 with same values as this Vec4.

        """

        return Vec4(self.x, self.y, self.z, self.w)


    def equal(self, other):
        """Check if this Vec4 is equal to other Vec4."""

        if not isinstance(other, Vec4):
            raise TypeError("Vec4: Invalid type for 'other' argument. Must be a Vec4.")

        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z and \
               self.w == other.w


    def almostEqual(self, other, precision=10e-12):
        """Check if this Vec4 is almost equal to other Vec4."""

        if not isinstance(other, Vec4):
            raise TypeError("Vec4: Invalid type for 'other' argument. Must be a Vec4.")

        return abs(self.x - other.x) < precision and \
               abs(self.y - other.y) < precision and \
               abs(self.z - other.z) < precision and \
               abs(self.w - other.w) < precision

