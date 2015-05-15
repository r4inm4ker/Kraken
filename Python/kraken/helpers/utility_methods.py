import os


def logHierarchy(kObject):
    """Traverses the given Kraken hierarchy and logs the names of all the objects.

    Return:
    None

    """

    print kObject.getFullName()
    for i in xrange(kObject.getNumChildren()):
        child = kObject.getChildByIndex(i)
        logHierarchy(child)


def reloadModule(name="kraken"):

    module = __import__(name, globals(), locals(), ["*"], -1)

    path = module.__path__[0]

    __reloadRecursive(path, name)


def __reloadRecursive(path, parentName):

    for root, dirs, files in os.walk(path, True, None):

        # parse all the files of given path and reload python modules
        for sfile in files:
            if sfile.endswith(".py"):
                if sfile == "__init__.py":
                    name = parentName
                else:
                    name = parentName+"."+sfile[:-3]

                print "reload : %s"%name
                try:
                    module = __import__(name, globals(), locals(), ["*"], -1)
                    reload(module)
                except ImportError, e:
                    for arg in e.args:
                        print arg
                except Exception, e:
                    for arg in e.args:
                        print arg

        # Now reload sub modules
        for dirName in dirs:
            __reloadRecursive(path+"/"+dirName, parentName+"."+dirName)
        break