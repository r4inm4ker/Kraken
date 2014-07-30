"""Kraken - maths.xfo module.

Classes:
Xfo -- Transform.
"""

from math_object import MathObject
from vec import Vec3
from rotation import Quat
from matrix import Matrix33, Matrix44


class Xfo(MathObject):
    """Transform object."""

    def __init__(self, scl=None, rot=None, tr=None, ro=0):
        super(Xfo, self).__init__()
        self.scl = Vec3(1,1,1)
        self.rot = Quat()
        self.tr = Vec3()
        self.ro = 0

        self.set(scl=scl, rot=rot, tr=tr, ro=ro)


    def __str__(self):
        """String representation of Transform."""

        return "Xfo(scl=" + str(self.scl) + ", rot=" + str(self.rot) + ", tr=" + str(self.tr) + ")"


    def copy(self, xfo):
        """Copy the values from input Xfo.

        Arguments:
        xfo -- Xfo, Xfo to copy values from.

        Return:
        This Xfo.

        """

        self.scl.copy(xfo.scl)
        self.rot.v.copy(xfo.rot.v)
        self.rot.w = xfo.rot.w
        self.tr.copy(xfo.tr)

        return self


    def set(self, scl=None, rot=None, tr=None, ro=0):
        """Sets values of the transform.

        Return:
        self

        """

        if scl is not None and not isinstance(scl, Vec3):
            raise TypeError("Xfo: Invalid type for 'scl' argument. Must be a Vec3.")

        if rot is not None and not isinstance(rot, Quat):
            raise TypeError("Xfo: Invalid type for 'rot' argument. Must be a Quat.")

        if tr is not None and not isinstance(tr, Vec3):
            raise TypeError("Xfo: Invalid type for 'tr' argument. Must be a Vec3.")

        if scl is None:
            scl = Vec3(1,1,1)

        if rot is None:
            rot = Quat()

        if tr is None:
            tr = Vec3()

        self.scl.set(scl.x, scl.y, scl.z)
        self.rot.set(rot.v, rot.w)
        self.tr.set(tr.x, tr.y, tr.z)
        self.ro = ro

        return self


    def setFromMatrix33(self, mat33):
        """Set Xfo values from a Matrix33 object.

        Arguments:
        mat33 -- Matrix33 object.

        Return:
        True if successful.

        """

        if not isinstance(mat33, Matrix33):
            raise TypeError("Xfo: setFromMatrix33: Invalid type for 'mat33' argument. Must be a Matrix33.")

        self.rot.setFromMatrix33(mat33)

        return True


    def setFromMatrix44(self, mat44):
        """Set Xfo values from a Matrix44 object.

        Arguments:
        mat44 -- Matrix44 object.

        Return:
        True if successful.

        """

        if not isinstance(mat44, Matrix44):
            raise TypeError("Xfo: setFromMatrix44: Invalid type for 'mat44' argument. Must be a Matrix44.")

        mat44Array = mat44.toArray()

        mat33 = Matrix33()
        mat33.setFromArray([mat44Array[0],mat44Array[1],mat44Array[2],
                             mat44Array[4],mat44Array[5],mat44Array[6],
                             mat44Array[8],mat44Array[9],mat44Array[10]])

        self.setFromMatrix33(mat33)

        self.tr.x = mat44Array[12]
        self.tr.y = mat44Array[13]
        self.tr.z = mat44Array[14]

        self.scl.x = Vec3(mat44Array[0],mat44Array[1],mat44Array[2]).length()
        self.scl.y = Vec3(mat44Array[4],mat44Array[5],mat44Array[6]).length()
        self.scl.z = Vec3(mat44Array[8],mat44Array[9],mat44Array[10]).length()

        return self


    def setFromVectors(self, inVec1, inVec2, inVec3, translation):
        """Set Xfo values from  3 axis vectors and .

        Arguments:
        inVec1 -- x axis.
        inVec2 -- y axis.
        inVec3 -- z axis.
        translation -- position vector.

        Return:
        True if successful.

        """
        mat33 = Matrix33()
        mat33.set(inVec1, inVec2, inVec3)
        self.rot.setFromMatrix33(mat33.transpose())
        self.tr = translation

        return True


    def setIdentity(self):
        """Sets transform to identity.

        Return:
        self

        """

        self.set(Vec3(), Vec3(), Vec3())

        return self


    def multiply(self, xfo):
        """Multiply this transform with input transform.

        Return:
        New transform.

        """

        resultXfo = Xfo()

        resultXfo.scl = self.scl.multiply(xfo.scl)
        resultXfo.rot = self.rot.multiply(xfo.rot)
        resultXfo.tr = self.tr.add(xfo.tr)

        return resultXfo


    def transformVector(self, v):
        """Transforms a vector by this xfo.

        Arguments:
        v -- Vec3, vector to transform.

        Return:
        Vec3, transformed vector.

        """

        return self.rot.rotateVector(v.multiply(self.scl)).add(self.tr)


    def isIdentity(self):
        """Check if this Xfo is set to Identity.

        Return:
        True if identity, false if not.

        """

        return self.isEqual(Xfo())


    def isEqual(self, other):
        """Check if this Xfo is equal to another.

        Return:
        True if equal, false if not.

        """

        if not isinstance(other, Xfo):
            raise TypeError("Xfo: Invalid type for 'other' argument. Must be a Xfo.")

        return self.scl.equal(other.scl) and \
               self.rot.equal(other.rot) and \
               self.tr.equal(other.tr)


# ===============
# Helper Methods
# ===============
def xfoFromDirAndUpV(base, target, upV):
    """Creates a transform for base object pointing to target with an upvector upV..

    Arguments:
    base -- Vec3, base vec3 to use in calculation.
    target -- Vec3, target vec3 to use in calculation.
    upV -- Vec3, upV vec3 to use in calculation.

    Return:
    Xfo, output xfo.

    """

    rootToTarget = target.subtract(base).unit()
    rootToUpV = upV.subtract(base).unit()
    normal = rootToUpV.cross(rootToTarget).unit()
    zAxis = rootToTarget.cross(normal).unit()
    outXfo = Xfo()
    outXfo.setFromVectors(rootToTarget, normal, zAxis, base)

    return outXfo

