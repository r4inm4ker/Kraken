"""Kraken - maths.rot module.

Classes:
Euler -- Euler rotation.
Quat -- Quaternion rotation.
"""

import math

from kraken.core.maths import vec
from kraken.core.maths import matrix
from kraken.core.maths import mathUtils


class Euler(object):
    """Euler rotation object."""

    roMap = {
                0:"xyz",
                1:"xzy",
                2:"yxz",
                3:"yzx",
                4:"zxy",
                5:"zyx",
            }

    def __init__(self, x=None, y=None, z=None, ro=None):
        """Initialize values for x,y,z, and rotation order values."""

        super(Euler, self).__init__()

        self.x = None
        self.y = None
        self.z = None
        self.ro = None

        self.set(mathUtils.degToRad(x), mathUtils.degToRad(y), mathUtils.degToRad(z), ro)


    def __str__(self):
        """String representation of Euler object."""

        return "Euler(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" + " Order: " + self.roMap[self.ro]


    def set(self, x=None, y=None, z=None, ro=None):
        """Sets values for Euler."""

        if isinstance(x, (int,float)) and isinstance(y, (int,float)) and isinstance(z, (int,float)):
            self.x = x
            self.y = y
            self.z = z
        elif not x and not y and not z:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
        else:
            raise TypeError("Euler: Invalid 'x,y,z' argument.")

        if ro is None:
            self.ro = 0
        elif isinstance(ro, int):
            if ro not in range(0,6):
                raise ValueError("Euler: 'ro' argument out of range 0-5.")

            self.ro = ro
        else:
            raise ValueError("Euler: Invalid 'ro' argument.")

        return self


    def toMatrix33(self):
        """Convert this Euler rotation into a Matrix33.

        Return:
        New Matrix33 object representing this Euler rotation.

        """

        # Kraken Euler rotation order
        # 0:"xyz",
        # 1:"xzy",
        # 2:"yxz",
        # 3:"yzx",
        # 4:"zxy",
        # 5:"zyx",

        cx = math.cos(self.x)
        sx = math.sin(self.x)
        cy = math.cos(self.y)
        sy = math.sin(self.y)
        cz = math.cos(self.z)
        sz = math.sin(self.z)

        """
        rx = matrix.Matrix33(vec.Vec3(1.0, 0.0, 0.0),
                            vec.Vec3(0.0, cx, -sx),
                            vec.Vec3(0.0, sx, cx))

        ry = matrix.Matrix33(vec.Vec3(cy, 0.0, sy),
                            vec.Vec3(0.0, 1.0, 0.0),
                            vec.Vec3(-sy, 0.0, cy))

        rz = matrix.Matrix33(vec.Vec3(cz, -sz, 0.0),
                            vec.Vec3(sz, cz, 0.0),
                            vec.Vec3(0.0, 0.0, 1.0))
        """
        # =========================================
        rx = matrix.Matrix33(vec.Vec3(1.0, 0.0, 0.0),
                            vec.Vec3(0.0, cx, sx),
                            vec.Vec3(0.0, -sx, cx))

        ry = matrix.Matrix33(vec.Vec3(cy, 0.0, -sy),
                            vec.Vec3(0.0, 1.0, 0.0),
                            vec.Vec3(sy, 0.0, cy))

        rz = matrix.Matrix33(vec.Vec3(cz, sz, 0.0),
                            vec.Vec3(-sz, cz, 0.0),
                            vec.Vec3(0.0, 0.0, 1.0))

        if self.ro == 0:
            return rx.multiply(ry.multiply(rz))
        elif self.ro == 1:
            return rx.multiply(rz.multiply(ry))
        elif self.ro == 2:
            return ry.multiply(rx.multiply(rz))
        elif self.ro == 3:
            return ry.multiply(rz.multiply(rx))
        elif self.ro == 4:
            return rz.multiply(rx.multiply(ry))
        elif self.ro == 5:
            return rz.multiply(ry.multiply(rx))
        else:
            raise ValueError("Euler: 'ro' attribute value is not within 0-5.")


    def clone(self):
        """Clone the Euler into a new Euler.

        Return:
        New Euler with same values as this Euler.

        """

        return Euler(x=self.x, y=self.y, z=self.z, ro=self.ro)


    def equal(self, other):
        """Check if this Euler is equal to other Euler.

        Return:
        True if equal, false if not.

        """

        if not isinstance(other, Euler):
            raise TypeError("Euler: Invalid type for 'other' argument. Must be a Euler.")

        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z


    def almostEqual(self, other, precision=10e-12):
        """Check if this Euler is almost equal to other Euler.

        Return:
        True if equal, false if not.

        """

        if not isinstance(other, Euler):
            raise TypeError("Euler: Invalid type for 'other' argument. Must be a Euler.")

        return abs(self.x - other.x) < precision and \
               abs(self.y - other.y) < precision and \
               abs(self.z - other.z) < precision


    def jsonEncode(self):
        """Encodes object to JSON.

        Return:
        JSON string.

        """

        d = {
                "__class__":self.__class__.__name__,
            }

        attrs = {}
        for eachItem in self.__dict__.items():

            if hasattr(eachItem[1], "jsonEncode"):
                attrs[eachItem[0]] = eachItem[1].jsonEncode()
            else:
                attrs[eachItem[0]] = eachItem[1]

        d.update(attrs)

        return d


class Quat(object):
    """Quaternion Rotation object."""

    def __init__(self, v=None, w=None):
        super(Quat, self).__init__()

        if v is not None and not isinstance(v, vec.Vec3):
            raise TypeError("Quat: Invalid type for 'v' argument. Must be a Vec3.")

        if w is not None and not isinstance(w, (int, float)):
            raise TypeError("Quat: Invalid type for 'w' argument. Must be a int or float.")

        self.v = vec.Vec3()
        self.w = 1.0

        self.set(v,w)


    def __str__(self):
        """Return string version of the Quat object."""

        return "Quat(" + str(self.v) + "," + str(self.w) + ")"


    def set(self, v=None, w=None):
        """Sets the quaternion values."""

        if v is None:
            v = vec.Vec3()

        if w is None:
            w = 1.0
        elif type(w) is int:
            w = float(w)

        self.v.set(v.x, v.y, v.z)
        self.w = w


    def setIdentity(self):
        """Set quaternion to identity."""

        return self.set()


    def setUnit(self):
        """Sets quaternion length to 1.0"""

        length = self.length()

        if mathUtils.checkDivisor(length):
            raise ValueError("Quat: setFromMat33: Invalid divisor!")

        invLen = 1.0 / length
        self.w *= invLen
        self.v = self.v.multiplyByScalar(invLen)

        return length


    def setFromEuler(self, e):
        """Set quaternion from a euler rotation."""

        # Barrowed from Creation Platform

        # Kraken Euler rotation order
        # 0:"xyz",
        # 1:"xzy",
        # 2:"yxz",
        # 3:"yzx",
        # 4:"zxy",
        # 5:"zyx",

        if not isinstance(e, Euler):
            raise TypeError("Quat: Invalid type for 'e' argument. Must be Euler.")


        ordered = vec.Vec3()

        if e.ro == 0:
          ordered.set(e.x, -e.y, e.z)
        elif e.ro == 1:
          ordered.set(e.x, e.z, e.y)
        elif e.ro == 2:
          ordered.set(e.y, e.x, e.z)
        elif e.ro == 3:
          ordered.set(e.y, -e.z, e.x)
        elif e.ro == 4:
          ordered.set(e.z, -e.x, e.y)
        elif e.ro == 5:
          ordered.set(e.z, e.y, e.x)

        ti = ordered.x * 0.5
        tj = ordered.y * 0.5
        tk = ordered.z * 0.5
        ci = math.cos(ti)
        cj = math.cos(tj)
        ck = math.cos(tk)
        si = math.sin(ti)
        sj = math.sin(tj)
        sk = math.sin(tk)
        cc = ci * ck
        cs = ci * sk
        sc = si * ck
        ss = si * sk
        ai = cj * sc - sj * cs
        aj = cj * ss + sj * cc
        ak = cj * cs - sj * sc
        self.w = cj * cc + sj * ss

        if e.ro == 0:
            self.v.x = ai
            self.v.y = -aj
            self.v.z = ak
        elif e.ro == 1:
            self.v.x = ai
            self.v.y = ak
            self.v.z = aj
        elif e.ro == 2:
            self.v.x = aj
            self.v.y = ai
            self.v.z = ak
        elif e.ro == 3:
            self.v.x = ak
            self.v.y = ai
            self.v.z = -aj
        elif e.ro == 4:
            self.v.x = -aj
            self.v.y = ak
            self.v.z = ai
        elif e.ro == 5:
            self.v.x = ak
            self.v.y = aj
            self.v.z = ai

        #self.setFromMatrix33(e.toMatrix33())

        return self


    def setFromAxisAndAngle(self, inVec, radians):
        """Set quaternion from an axis Vec3 and an angle in radians."""

        if not isinstance(inVec, vec.Vec3):
            raise TypeError("Quat: Invalid type for 'inVec' argument. Must be Vec3.")

        if not isinstance(radians, (int, float)):
            raise TypeError("Quat: Invalid type for 'radians' argument. Must be int or float.")

        halfAngle = radians * 0.5
        self.w = math.cos(halfAngle)
        self.v = inVec.unit().multiplyByScalar(math.sin(halfAngle))

        return self


    def setFromMatrix33(self, inMatrix):
        """set this quat based on a mat33"""

        trace = inMatrix.row0.x + inMatrix.row1.y + inMatrix.row2.z

        if trace > 0:
          s = 2.0 * math.sqrt(trace + 1.0)
          self.w = 0.25 * s
          mathUtils.checkDivisor(s)
          invS = 1.0 / s
          self.v.x = (inMatrix.row2.y - inMatrix.row1.z) * invS
          self.v.y = (inMatrix.row0.z - inMatrix.row2.x) * invS
          self.v.z = (inMatrix.row1.x - inMatrix.row0.y) * invS
        elif inMatrix.row0.x > inMatrix.row1.y and inMatrix.row0.x > inMatrix.row2.z:
          s = 2.0 * math.sqrt(1.0 + inMatrix.row0.x - inMatrix.row1.y - inMatrix.row2.z)
          mathUtils.checkDivisor(s)
          invS = 1.0 / s
          self.w = (inMatrix.row2.y - inMatrix.row1.z) * invS
          self.v.x = 0.25 * s
          self.v.y = (inMatrix.row0.y + inMatrix.row1.x) * invS
          self.v.z = (inMatrix.row0.z + inMatrix.row2.x) * invS
        elif inMatrix.row1.y > inMatrix.row2.z:
          s = 2.0 * math.sqrt(1.0 + inMatrix.row1.y - inMatrix.row0.x - inMatrix.row2.z)
          mathUtils.checkDivisor(s)
          invS = 1.0 / s
          self.w = (inMatrix.row0.z - inMatrix.row2.x) * invS
          self.v.x = (inMatrix.row0.y + inMatrix.row1.x) * invS
          self.v.y = 0.25 * s
          self.v.z = (inMatrix.row1.z + inMatrix.row2.y) * invS
        else:
          s = 2.0 * math.sqrt(1.0 + inMatrix.row2.z - inMatrix.row0.x - inMatrix.row1.y)
          mathUtils.checkDivisor(s)
          invS = 1.0 / s
          self.w = (inMatrix.row1.x - inMatrix.row0.y) * invS
          self.v.x = (inMatrix.row0.z + inMatrix.row2.x) * invS
          self.v.y = (inMatrix.row1.z + inMatrix.row2.y) * invS
          self.v.z = 0.25 * s

        self.setUnit()
        return self


    # def setFromMatrix33(self, inMatrix):
    #     """Set quaternion from a Matrix33"""

    #     fourWSquaredMinus1 = inMatrix.row0.x + inMatrix.row1.y + inMatrix.row2.z
    #     fourXSquaredMinus1 = inMatrix.row0.x - inMatrix.row1.y - inMatrix.row2.z
    #     fourYSquaredMinus1 = inMatrix.row1.y - inMatrix.row0.x - inMatrix.row2.z
    #     fourZSquaredMinus1 = inMatrix.row2.z - inMatrix.row0.x - inMatrix.row2.z
    #     fourBiggestSquaredMinus1 = fourWSquaredMinus1
    #     biggestIndex = 0

    #     if fourXSquaredMinus1 > fourBiggestSquaredMinus1:
    #         biggestIndex = 1
    #     elif fourYSquaredMinus1 > fourBiggestSquaredMinus1:
    #         biggestIndex = 2
    #     elif fourZSquaredMinus1 > fourBiggestSquaredMinus1:
    #         biggestIndex = 3


    #     biggestValue = math.sqrt(fourBiggestSquaredMinus1 + 1) * 0.5
    #     mult = 0.25 / biggestValue

    #     if biggestIndex == 0:
    #         self.w = biggestValue
    #         self.v.x = (inMatrix.row1.z - inMatrix.row2.y) * mult
    #         self.v.y = (inMatrix.row2.x - inMatrix.row0.z) * mult
    #         self.v.z = (inMatrix.row0.y - inMatrix.row1.x) * mult
    #         # raise Exception("w: " + str(self.w) + ", x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z))
    #     elif biggestIndex == 1:
    #         self.w = (inMatrix.row1.z - inMatrix.row2.y) * mult
    #         self.v.x = biggestValue
    #         self.v.y = (inMatrix.row0.y + inMatrix.row1.x) * mult
    #         self.v.z = (inMatrix.row2.x + inMatrix.row0.z) * mult
    #     elif biggestIndex == 2:
    #         self.w = (inMatrix.row2.x - inMatrix.row0.z) * mult
    #         self.v.x = (inMatrix.row0.y + inMatrix.row1.x) * mult
    #         self.v.y = biggestValue
    #         self.v.z = (inMatrix.row1.z + inMatrix.row2.y) * mult
    #     elif biggestIndex == 3:
    #         self.w = (inMatrix.row0.y - inMatrix.row1.x) * mult
    #         self.v.x = (inMatrix.row0.y - inMatrix.row1.x) * mult
    #         self.v.y = (inMatrix.row1.z + inMatrix.row2.y) * mult
    #         self.v.z = biggestValue

    #     self.setUnit()

    #     return self


    def setFromDirectionAndUpvector(self, direction, upvector):
        """Set quaternion from a direction Vec3 and upvector Vec3"""

        zaxis = direction.unit()
        yaxis = zaxis.cross(upvector.unit()).cross(zaxis).unit()
        xaxis = yaxis.cross(zaxis).unit()
        mat = matrix.Matrix33(xaxis, yaxis, zaxis).transpose()
        self.setFromMatrix33(mat)

        return self


    def toMatrix33(self):
        """Get a Matrix33 from on this quaternion."""

        mat3 = matrix.Matrix33()

        xx = self.v.x * self.v.x
        xy = self.v.x * self.v.y
        xz = self.v.x * self.v.z
        xw = self.v.x * self.w
        yy = self.v.y * self.v.y
        yz = self.v.y * self.v.z
        yw = self.v.y * self.w
        zz = self.v.z * self.v.z
        zw = self.v.z * self.w

        mat3.row0.x = 1.0 - (2.0 * yy) - (2 * zz)
        mat3.row1.x = (2.0 * xy) - (2 * zw)
        mat3.row2.x = (2.0 * xz) + (2*yw)

        mat3.row0.y = (2.0 * xy) +  (2 * zw)
        mat3.row1.y = 1.0 - (2.0 * xx) - (2 * zz)
        mat3.row2.y = (2.0 * yz) - (2 * xw)

        mat3.row0.z = (2.0 * xz) - (2 * yw)
        mat3.row1.z = (2.0 * yz) + (2 * xw)
        mat3.row2.z = 1.0 - (2.0 * xx) - (2 * yy)

        return mat3


    def toEuler(self, rotationOrder):
        """Get a Euler from this quaternion."""


        # Kraken Euler rotation order
        # 0:"xyz",
        # 1:"xzy",
        # 2:"yxz",
        # 3:"yzx",
        # 4:"zxy",
        # 5:"zyx",

        self.setUnit()

        ordered = vec.Vec3()
        if rotationOrder is 5:
            ordered.set(self.v.x, -self.v.z, self.v.y)
        elif rotationOrder is 1:
            ordered.set(self.v.y, -self.v.x, self.v.z)
        elif rotationOrder is 2:
            ordered.set(self.v.z, -self.v.y, self.v.x)
        elif rotationOrder is 3:
            ordered.set(self.v.x, self.v.y, self.v.z)
        elif rotationOrder is 0:
            ordered.set(self.v.z, self.v.x, self.v.y)
        elif rotationOrder is 4:
            ordered.set(self.v.y, self.v.z, self.v.x)

        euler = vec.Vec3()
        test = ordered.x*ordered.y + ordered.z*self.w
        if test > 0.49999: # singularity at north pole
            euler.y = 2.0 * math.atan2(ordered.x, self.w)
            euler.z = Math.PI/2.0
            euler.x = 0.0
        elif test < -0.49999: # singularity at south pole
            euler.y = -2.0 * math.atan2(ordered.x, self.w)
            euler.z = - Math.PI/2.0
            euler.x = 0.0
        else:
            sqx = ordered.x*ordered.x
            sqy = ordered.y*ordered.y
            sqz = ordered.z*ordered.z
            euler.y = math.atan2(2*ordered.y*self.w-2.0*ordered.x*ordered.z, 1.0 - 2.0*sqy - 2.0*sqz)
            euler.z = math.asin(2*test)
            euler.x = math.atan2(2*ordered.x*self.w-2.0*ordered.y*ordered.z, 1.0 - 2.0*sqx - 2.0*sqz)

        if rotationOrder is 5:
            return Euler(euler.x, euler.z, -euler.y, rotationOrder)
        elif rotationOrder is 1:
            return Euler(-euler.y, euler.x, euler.z, rotationOrder)
        elif rotationOrder is 2:
            return Euler(euler.z, -euler.y, euler.x, rotationOrder)
        elif rotationOrder is 3:
            return Euler(euler.x, euler.y, euler.z, rotationOrder)
        elif rotationOrder is 0:
            return Euler(euler.y, euler.z, euler.x, rotationOrder)
        elif rotationOrder is 4:
            return Euler(euler.z, euler.x, euler.y, rotationOrder)


    def add(self, q):
        """Sum of this quaternion and another quaternion."""

        return Quat(self.v.add(q.v), self.w + q.w)


    def subtract(self, q):
        """returns the subtraction of this quaternion and another quaternion."""

        return Quat(self.v.subtract(q.v), self.w - q.w)


    def multiply(self, q):
        """returns the product of this quaternion and another quaternion."""

        return Quat(q.v.multiplyByScalar(self.w).add(self.v.multiplyByScalar(q.w)).add(self.v.cross(q.v)), self.w * q.w - self.v.dotProduct(q.v))


    def multiplyByScalar(self, s):
        """returns the product of this quaternion and a scalar."""

        return Quat(self.v.multiplyByScalar(s), self.w * s)


    def divide(self, q):
        """returns the quotient of this quaternion and a quaternion divident"""

        return Quat(self.v.multiplyByScalar(q.w).subtract(q.v.multiplyByScalar(self.w)).subtract(self.v.cross(q.v)), self.w * q.w + self.v.dotProduct(q.v))


    def divideByScalar(self, s):
        """Quotient of this quaternion and a scalar divisor."""

        if mathUtils.checkDivisor(s):
            raise ValueError("Quat: setFromMat33: Invalid divisor!")

        return self.multiplyByScalar(1.0 / s)


    def rotateVector(self, v):
        """Rotate Vec3 rotated by this quaternion."""

        return self.multiply(Quat(v, 0.0)).multiply(self.conjugate()).v


    def dotProduct(self, q):
        """Dot product of this and another quaternion."""

        return self.w * q.w + self.v.dotProduct(q.v)


    def conjugate(self):
        """returns the conjugate of this quat"""

        return Quat(self.v.negate(), self.w)


    def inverse(self):
        """returns the inverse of this quat"""

        return self.unit().conjugate()


    def lengthSquared(self):
        """Get squared length of this quaternion."""

        return self.w * self.w + self.v.lengthSquared()


    def length(self):
        """Get length of this quaternion."""

        return math.sqrt(self.lengthSquared())


    def unit(self):
        """Set length of this quaternion to length of 1.0"""

        length = self.length()

        if mathUtils.checkDivisor(length):
                raise ValueError("Quat: setFromMat33: Invalid divisor!")

        return self.divideByScalar(length)


    def clone(self):
        """Creates a copy of this quaternion."""

        return Quat(self.v.clone(), self.w)


    def equal(self, other):
        """Checks if this Quat is equal to other Quat.

        Return:
        True if equal, false if not.

        """

        return self.v.equal(other.v) and self.w == other.w


    def almostEqual(self, other, precision=10e-12):
        """Checks if this Quat is almost equal to other Quat.

        Return:
        True if almost equal, false if not.

        """

        if not isinstance(other, Quat):
            raise TypeError("Quat: Invalid type for 'other' argument. Must be a Quat.")

        return self.v.almostEqual(other.v, precision) and \
               abs(self.w - other.w) < precision


    def jsonEncode(self):
        """Encodes object to JSON.

        Return:
        JSON string.

        """

        d = {
                "__class__":self.__class__.__name__,
            }

        attrs = {}
        for eachItem in self.__dict__.items():

            if hasattr(eachItem[1], "jsonEncode"):
                attrs[eachItem[0]] = eachItem[1].jsonEncode()
            else:
                attrs[eachItem[0]] = eachItem[1]

        d.update(attrs)

        return d