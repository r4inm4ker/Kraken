"""Kraken - maths.xfo module.

Classes:
Xfo -- Transform.
"""

from math_object import MathObject
from kraken.core.kraken_system import ks
from vec3 import Vec3
from quat import Quat
from mat33 import Mat33
from mat44 import Mat44

axisStrToTupleMapping = {
    'POSX': (1, 0, 0),
    'POSY': (0, 1, 0),
    'POSZ': (0, 0, 1),
    'NEGX': (-1, 0, 0),
    'NEGY': (0, -1, 0),
    'NEGZ': (0, 0, -1)
}

axisStrToIntMapping = {
    'POSX': 0,
    'POSY': 1,
    'POSZ': 2,
    'NEGX': 3,
    'NEGY': 4,
    'NEGZ': 5
}

class Xfo(MathObject):
    """Transform object."""

    def __init__(self, tr=None, ori=None, sc=None):
        """Initializes tr, ori and sc values for Xfo object."""

        super(Xfo, self).__init__()
        if ks.getRTValTypeName(tr) == 'Xfo':
            self._rtval = tr
        else:
            self._rtval = ks.rtVal('Xfo')
            if isinstance(tr, Xfo):
                self.set(tr=tr.tr, ori=tr.ori, sc=tr.sc)
            else:
                if tr is not None:
                    self.tr = tr
                if ori is not None:
                    self.ori = ori
                if sc is not None:
                    self.sc = sc


    def __str__(self):
        """String representation of Transform.

        Returns:
            str: String representation of Transform.

        """

        stringRep = "Xfo(ori=" + str(self.ori)
        stringRep += ", tr=" + str(self.tr)
        stringRep += ", sc=" + str(self.sc) + ")"

        return stringRep


    @property
    def tr(self):
        """Gets translation property of this transform.

        Returns:
            float: Translation property of this transform.

        """

        return Vec3(self._rtval.tr)


    @tr.setter
    def tr(self, value):
        """Sets translation of this transform.

        Args:
            value (Vec3): Vector to set the translation by.

        Returns:
            bool: True if successful.

        """

        self._rtval.tr = ks.rtVal('Vec3', value)

        return True


    @property
    def ori(self):
        """Gets orientation property of this transform.

        Returns:
            float: Orientation property of this transform.

        """

        return Quat(self._rtval.ori)


    @ori.setter
    def ori(self, value):
        """Sets orientation of this transform.

        Args:
            value (Quat): Quaternion to set the orientation by.

        Returns:
            bool: True if successful.

        """

        self._rtval.ori = ks.rtVal('Quat', value)

        return True


    @property
    def sc(self):
        """Gets scaling property of this transform.

        Returns:
            float: Scaling property of this transform.

        """

        return Vec3(self._rtval.sc)


    @sc.setter
    def sc(self, value):
        """Sets scaling of this transform.

        Args:
            value (Vec3): Quaternion to set the scaling by.

        Returns:
            bool: True if successful.

        """

        self._rtval.sc = ks.rtVal('Vec3', value)

        return True


    def __eq__(self, other):
        return self.ori.equal(other.ori) and self.tr.equal(other.tr) and self.sc.equal(other.sc)

    def __ne__(self, other):
        return not self.ori.equal(other.ori) or not self.tr.equal(other.tr) or not self.sc.equal(other.sc)

    def __mul__(self, other):
        return self.multiply(other)


    def clone(self):
        """Returns a clone of the Xfo.

        Returns:
            The cloned Xfo

        """

        xfo = Xfo()
        xfo.tr = self.tr.clone()
        xfo.ori = self.ori.clone()
        xfo.sc = self.sc.clone()

        return xfo


    def set(self, tr, ori, sc):
        """Setter from the translation, rotation and scaling.

        Args:
            tr (Vec3): Vector to set the translation by.
            ori (Quat): Quaternion to set the orientation by.
            sc (Vec3): Vector to set the scaling by.

        Returns:
            bool: True if successful.

        """

        self._rtval.set('', ks.rtVal('Vec3', tr), ks.rtVal('Quat', ori),
                        ks.rtVal('Vec3', sc))

        return True


    def setIdentity(self):
        """Sets this transform to the identity.

        Returns:
            bool: True if successful.

        """

        self._rtval.setIdentity('')

        return True


    def setFromMat44(self, m):
        """Sets this transform from the supplied matrix.

        Args:
            m (Mat44): 4x4 matrix to set the transform from.

        Returns:
            Xfo: New transform set from input Mat44.

        """

        return Xfo(self._rtval.setFromMat44('Xfo', ks.rtVal('Mat44', m)))


    def toMat44(self):
        """Gets a Mat44 from this xfo.

        Returns:
            Mat44: Matrix from this transform.

        """

        return Mat44(self._rtval.toMat44('Mat44'))


    def multiply(self, xfo):
        """Overload method for the multiply operator.

        Args:
            xfo (Xfo): Other transform to multiply this one by.

        Returns:
            Xfo: New Xfo of the product of the two Xfo's.

        """

        return Xfo(self._rtval.multiply('Xfo', ks.rtVal('Xfo', xfo)))


    def transformVector(self, v):
        """Transforms a vector by this transform.

        Args:
            v (Vec3): Vector to transform.

        Returns:
            Vec3: New vector transformed by this transform.

        """

        return Vec3(self._rtval.transformVector('Vec3', ks.rtVal('Vec3', v)))


    def transformRay(self, ray):
        """Transforms a ray vector by this transform.

        Args:
            ray (Vec3): Ray vector to transform.

        Returns:
            Ray: New ray vector transformed by this transform.

        """

        return Ray(self._rtval.transformRay('Ray', ks.rtVal('Ray', ray)))


    def inverse(self):
        """Get the inverse transform of this transform.

        Returns:
            Xfo: Inverse of this transform.

        """

        return Xfo(self._rtval.inverse('Xfo'))


    def inverseTransformVector(self, vec):
        """Transforms a vector with this xfo inversely

        Note: We have 'inverseTransformVector' because Xfos with non-uniform
        scaling cannot be inverted as Xfos.

        Args:
            vec (Vec3): Vector to be inversely transformed.

        Returns:
            Vec3: Inversely transformed vector.

        """

        return Vec3(self._rtval.inverseTransformVector('Vec3', ks.rtVal('Vec3', vec)))


    def linearInterpolate(self, other, t):
        """Linearly interpolates this transform with another one based on a
        scalar blend value (0.0 to 1.0).

        Args:
            other (Xfo): Transform to blend to.
            t (float): Blend value.

        Returns:
            Xfo: New transform blended between this and the input transform.

        """

        return Xfo(self._rtval.linearInterpolate('Xfo', ks.rtVal('Xfo', other),
                                                 ks.rtVal('Scalar', t)))


    def setFromVectors(self, inVec1, inVec2, inVec3, translation):
        """Set Xfo values from 3 axis vectors and a translation vector.

        Args:
            inVec1 (Vec3): X axis vector.
            inVec2 (Vec3): Y axis vector.
            inVec3 (Vec3): Z axis vector.
            translation (Vec3): Translation vector.

        Returns:
            bool: True if successful.

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
    """Creates a transform for base object pointing to target with an upvector
    upV.

    Args:
        base (Vec3): Base vec3 to use in calculation.
        target (Vec3): Target vec3 to use in calculation.
        upV (Vec3): UpV vec3 to use in calculation.

    Returns:
        Xfo: Output xfo.

    """

    rootToTarget = target.subtract(base).unit()
    rootToUpV = upV.subtract(base).unit()
    normal = rootToUpV.cross(rootToTarget).unit()
    zAxis = rootToTarget.cross(normal).unit()
    outXfo = Xfo()
    outXfo.setFromVectors(rootToTarget, normal, zAxis, base)

    return outXfo


def aimAt(targetXfo, aimPos=None, aimVector=None, aimAxis=(1, 0, 0), upPos=None, upVector=None, upAxis=(0, 1, 0)):
    """
    Point the xfo's aimAxis at the aimPos (or aimVector),
        while attempting to keep the xfo's upAxis pointing at the upPos (or upVector)
    Must provide
    1. aimPos or aimVector
    2. upPos or upVector

    The aim direction takes precendence over the up direction when the two are not orthoganal as input.

    Args:
        aimPos (Vec3): Aim the aimAxis of the Xform at this larget location
        upPos (Vec3):  Aim the upAxis of the xform at this location (if upVector not provided)
        upVector (Vec3): Aim the upAxis of the xform in this direction (if upPos not provided)
        aimAxis (List): Use this axis of the xform to point at aimPos (NOTE: want to make this Vec3)
        upAxis (List): Use this axis of the xform to point at upPos (or point in direction of upVector)

    Returns:
        None

    """

    if aimPos:
        aimVector = aimPos.subtract(targetXfo.tr).unit()
    elif not aimVector:
        raise ValueError("Must provide either aimPos or aimVector argument")

    if upPos:
        upVector = upPos.subtract(targetXfo.tr).unit()
    elif not upVector:
        raise ValueError("Must provide either upPos or upVector argument")


    aimAxisVector = aimVector #same as input arg always
    normalAxisVector = upVector.cross(aimAxisVector).unit()  # perpendiculuar to aim, but could be one of two directions
    upAxisVector = normalAxisVector.cross(aimAxisVector).unit() # perpendicular to aim and normal, but could be one of two directions

    # Measure the upAxisVector against the original upVector to see if it is less that 90, if not, we want the opposite side, so negate
    angle = upVector.dot(upAxisVector)
    if angle < 0:  # more than 90 degrees from the ideal upvector
        upAxisVector = upAxisVector.negate()

    #Simply negate the directions of aimAxis and upAxis if needed depending on sign of arguments
    if -1 in upAxis:
        upAxisVector = upAxisVector.negate()

    if -1 in aimAxis:
        aimAxisVector = aimAxisVector.negate()

    # Sort out which vectors are which axis
    argVectors = [None, None, None]

    for i, x in enumerate(aimAxis):
        if x:
            argVectors[i] = aimAxisVector

    for i, x in enumerate(upAxis):
        if x:
            argVectors[i] = upAxisVector

    # Now, that we have a definite aimAxisVector and upAxisVector,
    # let's find the "real" normalAxisVectortor with the guaranteed correct side.
    # Given the arguments, we know what axis the aim and up are supposed to be
    # That leaves us with a third to solve for
    # Based on the right-hand rule universe, we know the order to cross product the two known vectors

    if not aimAxis[0] and not upAxis[0]: # X is normal axis, so do Y cross Z (in that order) to get it
        normalAxisVector = argVectors[1].cross(argVectors[2]).unit()

    elif not aimAxis[1] and not upAxis[1]: # Y is normal axis, so do Z cross X (in that order) to get it
        normalAxisVector = argVectors[2].cross(argVectors[0]).unit()

    elif not aimAxis[2] and not upAxis[2]: # Z is normal axis, so do X cross Y (in that order) to get it
        normalAxisVector = argVectors[0].cross(argVectors[1]).unit()

    # add the normalAxisVector to the remaining axis
    for i, x in enumerate(argVectors):
        if x is None:
            argVectors[i] = normalAxisVector

    targetXfo.setFromVectors(argVectors[0], argVectors[1], argVectors[2], targetXfo.tr)