"""Kraken - maths.xfo module.

Classes:
Xfo -- Transform.
"""

from math_object import MathObject
from kraken.core.kraken_system import KrakenSystem as KS
from vec3 import Vec3
from quat import Quat
from mat33 import Mat33
from mat44 import Mat44


class Xfo(MathObject):
    """Transform object."""

    def __init__(self, tr=None, ori=None, sc=None):
        """Initializes tr, ori and sc values for Xfo object."""

        super(Xfo, self).__init__()
        if tr is not None and self.getTypeName(tr) == 'Xfo':
            self.rtval = tr
        else:
            self.rtval = KS.inst().rtVal('Xfo')
            if tr is not None:
                self.tr = tr
            if ori is not None:
                self.ori = ori
            if sc is not None:
                self.sc = sc


    def __str__(self):
        """String representation of Transform."""

        return "Xfo(ori=" + str(self.ori) + ", tr=" + str(self.tr) + ", sc=" + str(self.sc) + ")"


    @property
    def tr(self):
        """Gets translation property of this transform.

        Return:
        Scalar, translation property of this transform.

        """

        return Vec3(self.rtval.tr)


    @tr.setter
    def tr(self, value):
        """Sets translation of this transform.

        Arguments:
        value -- Vec3, vector to set the translation by.

        Return:
        True if successful.

        """

        self.rtval.tr = KS.inst().rtVal('Vec3', value)

        return True


    @property
    def ori(self):
        """Gets orientation property of this transform.

        Return:
        Scalar, orientation property of this transform.

        """

        return Quat(self.rtval.ori)


    @ori.setter
    def ori(self, value):
        """Sets orientation of this transform.

        Arguments:
        value -- Quat, quaternion to set the orientation by.

        Return:
        True if successful.

        """

        self.rtval.ori = KS.inst().rtVal('Quat', value)

        return True


    @property
    def sc(self):
        """Gets scaling property of this transform.

        Return:
        Scalar, scaling property of this transform.

        """

        return Vec3(self.rtval.sc)


    @sc.setter
    def sc(self, value):
        """Sets scaling of this transform.

        Arguments:
        value -- Vec3, quaternion to set the scaling by.

        Return:
        True if successful.

        """

        self.rtval.sc = KS.inst().rtVal('Vec3', value)

        return True


    def clone(self):
        """Returns a clone of the Xfo.

        Return:
        The cloned Xfo

        """

        xfo = Xfo();
        xfo.tr = self.tr.clone();
        xfo.ori = self.ori.clone();
        xfo.sc = self.sc.clone();

        return xfo


    def set(self, tr, ori, sc):
        """Setter from the translation, rotation and scaling.

        Arguments:
        tr -- Vec3, vector to set the translation by.
        ori -- Quat, quaternion to set the orientation by.
        sc -- Vec3, vector to set the scaling by.

        Return:
        True if successful.

        """

        self.rtval.set('', KS.inst().rtVal('Vec3', tr), KS.inst().rtVal('Quat', ori), KS.inst().rtVal('Vec3', sc))

        return True


    def setIdentity(self):
        """Sets this transform to the identity.

        Return:
        True if successful.

        """

        self.rtval.setIdentity('')

        return True


    def setFromMat44(self, m):
        """Sets this transform from the supplied matrix.

        Arguments:
        m -- Mat44, 4x4 matrix to set the transform from.

        Return:
        Xfo, new transform set from input Mat44.

        """

        return Xfo(self.rtval.setFromMat44('Xfo', KS.inst().rtVal('Mat44', m)))


    def toMat44(self):
        """Gets a Mat44 from this xfo.

        Return:
        Mat44, matrix from this transform.

        """

        return Mat44(self.rtval.toMat44('Mat44'))

    # # Equals operator
    # def Boolean self, == (Xfo a, Xfo b):


    # # Not equals operator
    # def Boolean self, != (Xfo a, Xfo b):



    # # Multiplies two transforms
    # def Xfo self, * (in Xfo local, in Xfo global):


    # # Multiplies this transform with another one
    # def  *= self, (in Xfo global):


    def multiply(self, xfo):
        """Overload method for the multiply operator.

        Arguments:
        xfo -- Xfo, other transform to multiply this one by.

        Return:
        Xfo, new Xfo of the product of the two Xfo's.

        """

        return Xfo(self.rtval.multiply('Xfo', KS.inst().rtVal('Xfo', xfo)))


    def transformVector(self, v):
        """Transforms a vector by this transform.

        Arguments:
        v -- Vec3, vector to transform.

        Return:
        Vec3, new vector transformed by this transform.

        """

        return Vec3(self.rtval.transformVector('Vec3', KS.inst().rtVal('Vec3', v)))


    def transformRay(self, ray):
        """Transforms a ray vector by this transform.

        Arguments:
        ray -- Vec3, ray vector to transform.

        Return:
        Ray, new ray vector transformed by this transform.

        """

        return Ray(self.rtval.transformRay('Ray', KS.inst().rtVal('Ray', ray)))


    def inverse(self):
        """Get the inverse transform of this transform.

        Return:
        Xfo, inverse of this transform.

        """

        return Xfo(self.rtval.inverse('Xfo'))


    def inverseTransformVector(self, vec):
        """Transforms a vector with this xfo inversely

        Note: We have 'inverseTransformVector' because Xfos with non-uniform
        scaling cannot be inverted as Xfos.

        Arguments:
        vec -- Vec3, vector to be inversely transformed.

        Return:
        Vec3, inversely transformed vector.

        """

        return Vec3(self.rtval.inverseTransformVector('Vec3', KS.inst().rtVal('Vec3', vec)))


    def linearInterpolate(self, other, t):
        """Linearly interpolates this transform with another one based on a scalar
        blend value (0.0 to 1.0).

        Arguments:
        other -- Xfo, transform to blend to.
        t -- Scalar, blend value.

        Return:
        Xfo, new transform blended between this and the input transform.

        """

        return Xfo(self.rtval.linearInterpolate('Xfo', KS.inst().rtVal('Xfo', other), KS.inst().rtVal('Scalar', t)))


    def setFromVectors(self, inVec1, inVec2, inVec3, translation):
        """Set Xfo values from 3 axis vectors and a translation vector.

        Arguments:
        inVec1 -- Vec3, x axis vector.
        inVec2 -- Vec3, y axis vector.
        inVec3 -- Vec3, z axis vector.
        translation -- Vec3, translation vector.

        Return:
        True if successful.

        """

        mat33 = Mat33()
        mat33.setRows(inVec1, inVec2, inVec3)
        self.ori.setFromMat33(mat33.transpose())
        self.tr = translation

        return True


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

