"""Kraken - maths.xfo module.

Classes:
Xfo -- Transform.
"""

from math_object import MathObject
from kraken.core.objects.kraken_core import KrakenCore as KC
from vec3 import Vec3
from quat import Quat


class Xfo(MathObject):
    """Transform object."""

    def __init__(self, tr=None, ori=None, sc=None):
        super(Xfo, self).__init__()
        client = KC.getInstance().getCoreClient()
        self.rtval = client.RT.types.Xfo()
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
        """The 'translation' property."""
        return Vec3(self.rtval.tr)

    @tr.setter
    def tr(self, value):
        self.rtval.tr = KC.inst().rtVal('Vec3', value)

    @property
    def ori(self):
        """The 'orientation' property."""
        return Quat(self.rtval.ori)

    @ori.setter
    def ori(self, value):
        self.rtval.ori = KC.inst().rtVal('Quat', value)


    @property
    def sc(self):
        """The 'scaling' property."""
        return Vec3(self.rtval.sc)

    @sc.setter
    def sc(self, value):
        self.rtval.sc = KC.inst().rtVal('Vec3', value)


    # Setter from just the rotation
    def set(self, ori):
        self.rtval.set('', KC.inst().rtVal('Quat', ori))

    # Setter from Mat33 (only setting rotation)
    def set(self, mat):
        self.rtval.set('', KC.inst().rtVal('Mat33', mat))

    # Setter from just the translation
    def set(self, tr):
        self.rtval.set('', KC.inst().rtVal('Vec3', tr))

    # Setter from the translation and rotation
    def set(self, tr, ori):
        self.rtval.set('', KC.inst().rtVal('Vec3', tr), KC.inst().rtVal('Quat', ori))

    # Setter from the translation, rotation and scaling
    def set(self, tr, ori, sc):
        self.rtval.set('', KC.inst().rtVal('Vec3', tr), KC.inst().rtVal('Quat', ori), KC.inst().rtVal('Vec3', sc))

    # Setter from the orientation, translation and scaling
    def set(self, ori, tr, sc):
        self.rtval.set('', KC.inst().rtVal('Quat', ori), KC.inst().rtVal('Vec3', tr), KC.inst().rtVal('Vec3', sc))

    # Sets this transform to the identity
    def setIdentity(self):
        self.rtval.setIdentity('')

    # Sets this transform from a given Mat44
    def setFromMat44(self):
        self.rtval.setFromMat44('', KC.inst().rtVal('Mat44', m))

    # Returns this xfo as a Mat44
    def toMat44(self):
        return self.rtval.toMat44('Mat44')

    # # Equals operator
    # def Boolean self, == (Xfo a, Xfo b):


    # # Not equals operator
    # def Boolean self, != (Xfo a, Xfo b):



    # # Multiplies two transforms
    # def Xfo self, * (in Xfo local, in Xfo global):


    # # Multiplies this transform with another one
    # def  *= self, (in Xfo global):


    # Overload method for the multiply operator
    def multiply(self, xfo):
        return self.rtval.multiply('Xfo', KC.inst().rtVal('Xfo', xfo))


    # Transforms a vector with this transform
    def transformVector(self, v):
        return self.rtval.transformVector('Vec3', KC.inst().rtVal('Vec3', v))

    # Transforms a vector with this transform
    def  transformRay(self, ray):
        return self.rtval.transformRay('Ray', KC.inst().rtVal('Ray', ray))

    # Returns the inverse transform of this one
    def  inverse(self):
        return self.rtval.inverse('Xfo')

    # Transforms a vector with this xfo inversely
    # \note we have 'inverseTransformVector' because Xfos with non-uniform scaling cannot be inverted as Xfos
    def inverseTransformVector(self, vec):
        return self.rtval.inverseTransformVector('Vec3', KC.inst().rtVal('Vec3', vec))

    # Linearly interpolates this Xfo with another one based on 
    # a scalar blend value (0.0 to 1.0)
    def linearInterpolate(self,  other, t):
        return self.rtval.inverseTransformVector('Xfo', KC.inst().rtVal('Xfo', other), KC.inst().rtVal('Scalar', t))








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
    outXfo.setFromVectors(rootToTarget.clone(), normal.clone(), zAxis.clone(), base.clone())

    return outXfo

