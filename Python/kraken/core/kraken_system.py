"""KrakenSystem - objects.kraken_core module.

Classes:
KrakenSystem - Class for constructing the Fabric Engine Core client.

"""

import os
import sys
import json
import imp
import inspect
import importlib
from collections import OrderedDict
import traceback

import FabricEngine.Core

import kraken
from kraken.core.profiler import Profiler

krakenSystemModuleDir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
krakenDir=os.path.abspath(os.path.join(krakenSystemModuleDir, '..', '..', '..'))
os.environ['KRAKEN_PATH']  = krakenDir

krakenExtsDir = os.path.join(krakenDir, 'Exts')
if krakenExtsDir not in os.environ['FABRIC_EXTS_PATH']:
    os.environ['FABRIC_EXTS_PATH'] = krakenExtsDir + os.pathsep + os.environ['FABRIC_EXTS_PATH']

canvasPresetsDir = os.path.join(krakenDir, 'CanvasPresets')
if 'FABRIC_DFG_PATH' in os.environ:
    if canvasPresetsDir not in os.environ['FABRIC_DFG_PATH']:
        os.environ['FABRIC_DFG_PATH'] = canvasPresetsDir + os.pathsep + os.environ['FABRIC_DFG_PATH']
else:
    os.environ['FABRIC_DFG_PATH'] = canvasPresetsDir

class KrakenSystem(object):
    """The KrakenSystem is a singleton object used to provide an interface with
    the FabricEngine Core and RTVal system."""

    __instance = None

    def __init__(self):
        """Initializes the Kraken System object."""

        super(KrakenSystem, self).__init__()

        self.client = None
        self.typeDescs = None
        self.registeredTypes = None
        self.loadedExtensions = []

        self.registeredConfigs = OrderedDict()
        self.registeredComponents = OrderedDict()
        # self.moduleImportManager = ModuleImportManager()


    def loadCoreClient(self):
        """Loads the Fabric Engine Core Client"""

        if self.client == None:
            Profiler.getInstance().push("loadCoreClient")

            try:
                imp.find_module('cmds')
                host = 'Maya'
            except ImportError:
                try:
                    imp.find_module('sipyutils')
                    host = 'Softimage'
                except ImportError:
                    host = 'Python'

            if host == "Python":
                # self.client = FabricEngine.Core.createClient({'optimizeSynchronously': True, 'guarded': True})
                self.client = FabricEngine.Core.createClient({'guarded': True})

            elif host == "Maya":
                contextID = cmds.fabricSplice('getClientContextID')
                if contextID == '':
                    cmds.fabricSplice('constructClient')
                    contextID = cmds.fabricSplice('getClientContextID')

                # Pull out the Splice client.
                self.client = FabricEngine.Core.createClient({"contextID": contextID})

            elif host == "Softimage":
                from win32com.client.dynamic import Dispatch
                si = Dispatch("XSI.Application").Application
                contextID = si.fabricSplice('getClientContextID')
                if contextID == '':
                    si.fabricSplice('constructClient')
                    contextID = si.fabricSplice('getClientContextID')

                # Pull out the Splice client.
                self.client = FabricEngine.Core.createClient({"contextID": contextID})

            self.loadExtension('Math')

            # krakenDir = os.environ['KRAKEN_PATH']
            # self.client.DFG.host.addPresetDir('', 'Kraken', os.path.join(krakenDir, 'CanvasPresets'))

            Profiler.getInstance().pop()


    def getCoreClient(self):
        """Returns the Fabric Engine Core Client owned by the KrakenSystem

        Returns:
            object: The Fabric Engine Core Client

        """

        if self.client is None:
            self.loadCoreClient()

        return self.client


    def loadExtension(self, extension):
        """Loads the given extension and updates the registeredTypes cache.

        Args:
            extension (str): The name of the extension to load.

        """

        if extension not in self.loadedExtensions:
            Profiler.getInstance().push("loadExtension:" + extension)
            self.client.loadExtension(extension)
            self.registeredTypes = self.client.RT.types
            self.typeDescs = self.client.RT.getRegisteredTypes()
            # Cache the loaded extension so that we aviod refreshing the typeDescs cache(costly)
            self.loadedExtensions.append(extension)
            Profiler.getInstance().pop()

    # ==============
    # RTVal Methods
    # ==============

    def constructRTVal(self, dataType, defaultValue=None):
        """Constructs a new RTVal using the given name and optional devault value.

        Args:
            dataType (str): The name of the data type to construct.
            defaultValue (value): The default value to use to initialize the RTVal

        Returns:
            object: The constructed RTval.

        """

        self.loadCoreClient()
        klType = getattr(self.registeredTypes, dataType)

        if defaultValue is not None:
            if hasattr(defaultValue, '_rtval'):
                return defaultValue._rtval

            typeDesc = self.typeDescs[dataType]
            if 'members' in typeDesc:
                try:
                    value = klType.create()
                except:
                    value = klType()
                for i in range(0, len(typeDesc['members'])):
                    memberName = typeDesc['members'][i]['name']
                    memberType = typeDesc['members'][i]['type']
                    if memberName in defaultValue:
                        setattr(value, memberName, self.constructRTVal(memberType, getattr(defaultValue, memberName)))
                return value

            else:
                return klType(defaultValue)
        else:
            try:
                return klType.create()
            except:
                try:
                    return klType()
                except Exception as e:
                    raise Exception("Error constructing RTVal:" + dataType)


    def rtVal(self, dataType, defaultValue=None):
        """Constructs a new RTVal using the given name and optional devault value.

        Args:
            dataType (str): The name of the data type to construct.
            defaultValue (value): The default value to use to initialize the RTVal

        Returns:
            object: The constructed RTval.

        """

        return self.constructRTVal(dataType, defaultValue)


    def isRTVal(self, value):
        """Returns true if the given value is an RTVal.

        Args:
            value (value): value to test.

        Returns:
            bool: True if successful.

        """

        return str(type(value)) == "<type 'PyRTValObject'>"


    def getRTValTypeName(self, rtval):
        """Returns the name of the type, handling extracting the name from KL RTVals.

        Args:
            rtval (rtval): The rtval to extract the name from.

        Returns:
            bool: True if successful.

        """

        if ks.isRTVal(rtval):
            return json.loads(rtval.type("Type").jsonDesc("String").getSimpleType())['name']
        else:
            return "None"

    # ==================
    # Config Methods
    # ==================

    def registerConfig(self, configClass):
        """Registers a config Python class with the KrakenSystem so ti can be built by the rig builder.

        Args:
            configClass (str): The Python class of the config

        """

        configModulePath = configClass.__module__ + "." + configClass.__name__
        if configModulePath in self.registeredConfigs:
            # we allow reregistring of configs because as a config's class is edited
            # it will be re-imported by python(in Maya), and the classes reregistered.
            pass

        self.registeredConfigs[configModulePath] = configClass


    def getConfigClass(self, className):
        """Returns the registered Python config class with the given name

        Args:
            className (str): The name of the Python config class

        Returns:
            object: The Python config class

        """

        if className not in self.registeredConfigs:
            raise Exception("Config with that class not registered:" + className)

        return self.registeredConfigs[className]


    def getConfigClassNames(self):
        """Returns the names of the registered Python config classes

        Returns:
            list: The array of config class names.

        """

        return self.registeredConfigs.keys()

    # ==================
    # Component Methods
    # ==================

    def registerComponent(self, componentClass):
        """Registers a component Python class with the KrakenSystem so ti can be built by the rig builder.

        Args:
            componentClass (str): The Python class of the component

        """
        componentClassPath = componentClass.__module__ + "." + componentClass.__name__
        if componentClassPath in self.registeredComponents:
            # we allow reregistring of components because as a component's class is edited
            # it will be re-imported by python(in Maya), and the classes reregistered.
            pass

        self.registeredComponents[componentClassPath] = componentClass


    def getComponentClass(self, className):
        """Returns the registered Python component class with the given name

        Args:
            className (str): The name of the Python component class

        Returns:
            object: The Python component class

        """

        if className not in self.registeredComponents:
            raise Exception("Component with that class not registered:" + className)

        return self.registeredComponents[className]


    def reloadAllComponents(self):
        """Force the reload of all registered component modules

        Return:
        True if successful.

        """

        for componentClassPath in self.registeredComponents:
            componentModulePath = self.registeredComponents[componentClassPath].__module__
            if componentModulePath in sys.modules:
                del(sys.modules[componentModulePath])

        prevRegsteredComponents = self.registeredComponents.copy()
        self.registeredComponents = {}

        for componentClassPath in prevRegsteredComponents:
            componentModulePath = prevRegsteredComponents[componentClassPath].__module__
            try:
                importlib.import_module(componentModulePath)
            except Exception as e:
                stack = traceback.format_tb(sys.exc_info()[2])
                exception_list = []
                exception_list.extend(stack)
                exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

                exception_str = "Traceback (most recent call last):\n"
                exception_str += "".join(exception_list)
                # Removing the last \n
                exception_str = exception_str[:-1]
                print(exception_str)

        return True


    def getComponentClassNames(self):
        """Returns the names of the registered Python component classes

        Returns:
            list: The array of component class names.

        """

        return self.registeredComponents.keys()


    def loadComponentModules(self):
        """Loads all the component modules and configs specified in the 'KRAKEN_PATHS' environment variable.

        The kraken_examples are loaded at all times.

        """


        def __importDirRecursive(path, parentModulePath=''):
            contents = os.listdir(path)
            moduleFilefound = False
            for item in contents:
                if os.path.isfile(os.path.join(path, item)):
                    if item == "__init__.py":
                        if parentModulePath == '':
                            modulePath = os.path.basename(path)

                            moduleParentFolder = os.path.split( path )[0]
                            if moduleParentFolder not in sys.path:
                                sys.path.append(moduleParentFolder)
                        else:
                            modulePath = parentModulePath + '.' + os.path.basename(path)
                        moduleFilefound = True


            if moduleFilefound:
                for item in contents:
                    if os.path.isfile(os.path.join(path, item)):
                        # parse all the files of given path and import python modules
                        if item.endswith(".py") and item != "__init__.py":
                            module = modulePath+"."+item[:-3]
                            try:
                                importlib.import_module(module)

                            except ImportError, e:
                                print e
                                for arg in e.args:
                                    print arg

                            except Exception, e:
                                for arg in e.args:
                                    print arg


            for item in contents:
                if os.path.isdir(os.path.join(path, item)):
                    if moduleFilefound:
                        __importDirRecursive(os.path.join(path, item), modulePath)
                    else:
                        __importDirRecursive(os.path.join(path, item))


        # find the kraken examples module in the same folder as the kraken module.
        examplePaths = os.path.join(os.path.dirname(os.path.dirname(kraken.__file__)), 'kraken_examples')
        __importDirRecursive(examplePaths)

        pathsVar = os.getenv('KRAKEN_PATHS')
        if pathsVar is not None:
            pathsList = pathsVar.split(os.pathsep)
            for path in pathsList:

                if path == '':
                    continue

                if not os.path.exists(path):
                    print "Invalid Kraken Path: " + path
                    continue

                __importDirRecursive(path)


    @classmethod
    def getInstance(cls):
        """This class method returns the singleton instance for the KrakenSystem

        Returns:
            object: The singleton instance.

        """

        if cls.__instance is None:
            cls.__instance = KrakenSystem()

        return cls.__instance




ks = KrakenSystem.getInstance()
