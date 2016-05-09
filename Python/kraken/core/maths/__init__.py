"""Kraken - math module."""

from math_object import MathObject
from vec2 import Vec2
from vec3 import Vec3
from vec4 import Vec4
from quat import Quat
from euler import Euler
from xfo import Xfo
from mat33 import Mat33
from mat44 import Mat44
from rotation_order import RotationOrder
from color import Color


PI = 3.141592653589793
DEG_TO_RAD = 0.017453292519943295
RAD_TO_DEG = 57.29577951308232

AXIS_NAME_TO_TUPLE_MAP = {
    'POSX': (1, 0, 0),
    'POSY': (0, 1, 0),
    'POSZ': (0, 0, 1),
    'NEGX': (-1, 0, 0),
    'NEGY': (0, -1, 0),
    'NEGZ': (0, 0, -1)
}

AXIS_NAME_TO_INT_MAP = {
    'POSX': 0,
    'POSY': 1,
    'POSZ': 2,
    'NEGX': 3,
    'NEGY': 4,
    'NEGZ': 5
}


def Math_radToDeg(val):
    """Converts radians to degrees.

    Args:
        val (float): value to convert to degrees.

    Returns:
        float: Value in degrees.

    """

    return val * RAD_TO_DEG

def Math_degToRad(val):
    """Converts degrees to radians.

    Args:
        val (float): value to convert to radians.

    Returns:
        float: Value in radians.

    """

    return val * DEG_TO_RAD


def decodeValue(jsonData):
    """Returns a constructed math value based on the provided json data.

    Args:
        jsondata (dict): The JSON data to use to decode into a Math value.

    Returns:
        object: The constructed math value

    """

    if type(jsonData) is not dict:
        return jsonData

    if '__mathObjectClass__' not in jsonData:
        raise Exception("Invalid JSON data for constructing value:" + str(jsonData))

    if jsonData['__mathObjectClass__'] == 'Vec2':
        val = Vec2()
        val.jsonDecode(jsonData, decodeValue)
    elif jsonData['__mathObjectClass__'] == 'Vec3':
        val = Vec3()
        val.jsonDecode(jsonData, decodeValue)
    elif jsonData['__mathObjectClass__'] == 'Vec4':
        val = Vec4()
        val.jsonDecode(jsonData, decodeValue)
    elif jsonData['__mathObjectClass__'] == 'Euler':
        val = Euler()
        val.jsonDecode(jsonData, decodeValue)
    elif jsonData['__mathObjectClass__'] == 'Quat':
        val = Quat()
        val.jsonDecode(jsonData, decodeValue)
    elif jsonData['__mathObjectClass__'] == 'Xfo':
        val = Xfo()
        val.jsonDecode(jsonData, decodeValue)
    elif jsonData['__mathObjectClass__'] == 'Mat33':
        val = Mat33()
        val.jsonDecode(jsonData, decodeValue)
    elif jsonData['__mathObjectClass__'] == 'Mat44':
        val = Mat44()
        val.jsonDecode(jsonData, decodeValue)
    else:
        raise Exception("Unsupported Math type:" + jsonData['__mathObjectClass__'])

    return val
