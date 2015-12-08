from kraken.core.maths.math_object import MathObject
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.quat import Quat

from kraken.core.maths import decodeValue


def logHierarchy(kObject):
    """Traverses the given Kraken hierarchy and logs the names of all the objects.

    Args:
        Object: The object to start logging on.

    """

    print kObject.getDecoratedPath()
    for i in xrange(kObject.getNumChildren()):
        child = kObject.getChildByIndex(i)
        logHierarchy(child)


def __convertFromJSON(jsonData):

    if type(jsonData) is list:
        newList = []
        for item in jsonData:
            newList.append(__convertFromJSON(item))
        return newList
    elif type(jsonData) is dict:
        if '__mathObjectClass__' in jsonData.keys():
            return decodeValue(jsonData)
        for key, value in jsonData.iteritems():
            jsonData[key] = __convertFromJSON(value)
    return jsonData


def prepareToLoad(jsonData):
    """Prepares the json data for loading into kraken.

    Args:
        jsonData (dict): The JSON data to be prepared.

    Returns:
        dict: The prepared JSON hierarchy.

    """

    return __convertFromJSON(jsonData)


def __convertToJSON(jsonData):

    if isinstance(jsonData, MathObject):
        return jsonData.jsonEncode()
    elif type(jsonData) is list:
        newList = []
        for item in jsonData:
            newList.append(__convertToJSON(item))
        return newList
    elif type(jsonData) is dict:
        newDict = {}
        for key, value in jsonData.iteritems():
            newDict[key] = __convertToJSON(value)
        return newDict
    return jsonData


def prepareToSave(jsonData):
    """Prepares the json data for serialization.

    Args:
        jsonData (dict): The JSON data to be prepared.

    Returns:
        dict: The prepared JSON hierarchy.

    """

    return __convertToJSON(jsonData)


def __mirrorData(jsonData, plane):

    if isinstance(jsonData, Vec3):
        return jsonData

    if isinstance(jsonData, Quat):
        newQuat = Quat(jsonData)
        newQuat.mirror(plane)
        return newQuat

    elif isinstance(jsonData, Xfo):
        newXfo = Xfo(jsonData)
        if plane == 0:
            newXfo.tr.x = -newXfo.tr.x
        elif plane == 1:
            newXfo.tr.y = -newXfo.tr.y
        elif plane == 2:
            newXfo.tr.z = -newXfo.tr.z

        newXfo.ori.mirror(plane)
        return newXfo

    elif type(jsonData) is list:
        newList = []
        for item in jsonData:
            newList.append(__mirrorData(item, plane))
        return newList

    elif type(jsonData) is dict:
        newDict = {}
        for key, value in jsonData.iteritems():
            newDict[key] = __mirrorData(value, plane)
        return newDict

    return jsonData


def mirrorData(jsonData, plane):
    """Prepares the json data for serialization.

    Args:
        jsonData (dict): The JSON data to be prepared.

    Returns:
        dict: The prepared JSON hierarchy.

    """

    return __mirrorData(jsonData, plane)

