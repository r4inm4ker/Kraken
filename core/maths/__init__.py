"""Kraken - math module."""


from vec2 import Vec2
from vec3 import Vec3
from vec4 import Vec4
from quat import Quat
from euler import Euler
from xfo import Xfo


PI = 3.141592653589793
DEG_TO_RAD = 0.017453292519943295
RAD_TO_DEG = 57.29577951308232


def Math_radToDeg(val):
    """Converts radians to degrees.

    Arguments:
    val -- Scalar, value to convert to degrees.

    Return:
    Scalar, value in degrees.

    """

    return val * RAD_TO_DEG


def Math_degToRad(val):
    """Converts degrees to radians.

    Arguments:
    val -- Scalar, value to convert to radians.

    Return:
    Scalar, value in radians.

    """

    return val * DEG_TO_RAD