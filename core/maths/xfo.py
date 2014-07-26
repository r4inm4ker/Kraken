"""Kraken - maths.xfo module.

Classes:
Xfo -- Transform.
"""

from kraken.core.maths import vec
from kraken.core.maths import rotation
from kraken.core.maths import matrix


class Xfo(object):
    """Transform object."""

    def __init__(self, scl=None, rot=None, tr=None, ro=0):
        super(Xfo, self).__init__()
        self.scl = vec.Vec3(1,1,1)
        self.rot = rotation.Quat()
        self.tr = vec.Vec3()
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

        if scl is not None and not isinstance(scl, vec.Vec3):
            raise TypeError("Xfo: Invalid type for 'scl' argument. Must be a Vec3.")

        if rot is not None and not isinstance(rot, rotation.Quat):
            raise TypeError("Xfo: Invalid type for 'rot' argument. Must be a Quat.")

        if tr is not None and not isinstance(tr, vec.Vec3):
            raise TypeError("Xfo: Invalid type for 'tr' argument. Must be a Vec3.")

        if scl is None:
            scl = vec.Vec3(1,1,1)

        if rot is None:
            rot = rotation.Quat()

        if tr is None:
            tr = vec.Vec3()

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

        if not isinstance(mat33, matrix.Matrix33):
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

        mat44Array = mat44.toArray()

        mat33 = matrix.Matrix33()
        mat33.setFromArray([mat44Array[0],mat44Array[1],mat44Array[2],
                             mat44Array[4],mat44Array[5],mat44Array[6],
                             mat44Array[8],mat44Array[9],mat44Array[10]])

        self.setFromMatrix33(mat33)

        self.tr.x = mat44Array[12]
        self.tr.y = mat44Array[13]
        self.tr.z = mat44Array[14]

        self.scl.x = vec.Vec3(mat44Array[0],mat44Array[1],mat44Array[2]).length()
        self.scl.y = vec.Vec3(mat44Array[4],mat44Array[5],mat44Array[6]).length()
        self.scl.z = vec.Vec3(mat44Array[8],mat44Array[9],mat44Array[10]).length()

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

        mat33 = matrix.Matrix33()
        mat33.set(inVec1, inVec2, inVec3)
        self.rot.setFromMatrix33(mat33.transpose())
        self.tr = translation

        return True


    def setIdentity(self):
        """Sets transform to identity.

        Return:
        self

        """

        self.set(vec.Vec3(), vec.Vec3(), vec.Vec3())

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


# ===============
# Helper Methods
# ===============
def xfoFromThreePoints(base, target, upV):
    """Creates a transform for base object pointing to target with an upvector upV..

    Arguments:
    base -- Vec3, base vec3 to use in calculation.
    target -- Vec3, target vec3 to use in calculation.
    upV -- Vec3, upV vec3 to use in calculation.

    Return:
    Xfo, output xfo.

    """

    vecBase = base
    vecUpV = upV
    vecTgt = target

    vecX = vecTgt.clone()
    vecY = vec.Vec3()
    vecZ = vec.Vec3()
    vecToTgt = vec.Vec3()
    vecBaseToUpV = vecUpV.clone()

    vecX = vecX.subtract(vecBase)
    vecX.normalize()

    vecZ.copy(vecX)

    vecBaseToUpV = vecBaseToUpV.subtract(vecBase)
    vecBaseToUpV.normalize()

    vecZ = vecZ.cross(vecBaseToUpV)
    vecZ.normalize()

    vecY.copy(vecZ)
    vecY = vecY.cross(vecX)
    vecY.normalize()

    print vecX
    print vecY
    print vecZ

    xformDir = Xfo()
    xformDir.setFromVectors(vecX, vecY, vecZ, vecBase)

    print xformDir
    #rotUtil = XSIMath.CreateRotation(0, XSIMath.DegreesToRadians(180), 0)
    #xformDir.AddLocalRotation(rotUtil)

    return xformDir