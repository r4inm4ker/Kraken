

def logHierarchy(kObject):
    """Traverses the given Kraken hierarchy and logs the names of all the objects.

    Return:
    None

    """

    print kObject.getFullName()
    for i in xrange(kObject.getNumChildren()):
        child = kObject.getChildByIndex(i)
        logHierarchy(child)



from kraken.core.maths.math_object import MathObject
from kraken.core.maths import decodeValue

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
        for key, value in jsonData.iteritems():
            jsonData[key] = __convertToJSON(value)
    return jsonData

def prepareToSave(jsonData):
    return __convertToJSON(jsonData)