

def logHierarchy(kObject):
    """Traverses the given Kraken hierarchy and logs the names of all the objects.

    Return:
    None

    """

    print kObject.getFullName()
    for i in xrange(kObject.getNumChildren()):
        child = kObject.getChildByIndex(i)
        logHierarchy(child)
