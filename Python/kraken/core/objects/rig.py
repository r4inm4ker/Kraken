"""Kraken - objects.rig module.

Classes:
Rig -- Rig representation.

"""

import importlib
import json
import os

from container import Container
from kraken.core.kraken_system import KrakenSystem
from kraken.core.profiler import Profiler
from kraken.core.objects.layer import Layer
from kraken.helpers.utility_methods import prepareToSave, prepareToLoad


class Rig(Container):
    """Rig object."""

    def __init__(self, name='rig'):
        super(Rig, self).__init__(name)
        self._metaData = {}


    # ====================
    # Load / Save Methods
    # ====================
    def writeRigDefinitionFile(self, filepath):
        """Load a rig definition from a file on disk.

        Args:
            filepath (str): The file path of the rig definition file.

        Returns:
            bool: True if successful.

        """

        Profiler.getInstance().push("writeRigDefinitionFile:" + filepath)

        jsonData = self.getData()

        # now preprocess the data ready for saving to disk.
        pureJSON = prepareToSave(jsonData)

        with open(filepath,'w') as rigFile:
            rigFile.write(json.dumps(pureJSON, indent=2))

        Profiler.getInstance().pop()


    def loadRigDefinitionFile(self, filepath):
        """Load a rig definition from a file on disk.

        Args:
            filepath (str): The file path of the rig definition file.

        Returns:
            bool: True if successful.

        """

        Profiler.getInstance().push("LoadRigDefinitionFile:" + filepath)

        if not os.path.exists(filepath):
            raise Exception("File not found:" + filepath)

        with open(filepath) as rigFile:
            jsonData = json.load(rigFile)

        # now preprocess the data ready for loading.
        jsonData = prepareToLoad(jsonData)

        self.loadRigDefinition(jsonData)
        Profiler.getInstance().pop()


    def _loadComponents(self, componentsJson):
        """Loads components from a JSON dict.

        Args:
            componentsJson (dict): Dictionary of components to load.

        """


        Profiler.getInstance().push("__loadComponents")

        krakenSystem = KrakenSystem.getInstance()

        for componentData in componentsJson:
            # trim off the class name to get the module path.
            modulePath = '.'.join(componentData['class'].split('.')[:-1])
            if modulePath is not "":
                importlib.import_module(modulePath)

            componentClass = krakenSystem.getComponentClass(componentData['class'])
            if 'name' in componentData:
                component = componentClass(name=componentData['name'], parent=self)
            else:
                component = componentClass(parent=self)
            component.loadData(componentData)

        Profiler.getInstance().pop()


    def _makeConnections(self, connectionsJson):
        """Makes connections based on JSON dict.

        Args:
            connectionsJson (dict): Dictionary of connections to make.

        """


        Profiler.getInstance().push("__makeConnections")

        for connectionData in connectionsJson:

            sourceComponentDecoratedName, outputName = connectionData['source'].split('.')
            targetComponentDecoratedName, inputName = connectionData['target'].split('.')

            connectionFailure = False

            sourceComponent = self.getChildByDecoratedName(sourceComponentDecoratedName)
            if sourceComponent is None:
                print("Warning: Error making connection:" + connectionData['source'] + " -> " + \
                    connectionData['target']+". Source component not found:" + sourceComponentDecoratedName)
                connectionFailure = True

            targetComponent = self.getChildByDecoratedName(targetComponentDecoratedName)
            if targetComponent is None:
                print("Warning: Error making connection:" + connectionData['source'] + " -> " + \
                    connectionData['target']+". Target component not found:" + targetComponentDecoratedName)
                connectionFailure = True

            outputPort = sourceComponent.getOutputByName(outputName)
            if outputPort is None:
                print("Warning: Error making connection:" + connectionData['source'] + " -> " + \
                    connectionData['target']+". Output '" + outputName + "' not found on Component:" + sourceComponent.getPath())
                connectionFailure = True

            inputPort = targetComponent.getInputByName(inputName)
            if inputPort is None:
                print("Warning: Error making connection:" + connectionData['source'] + " -> " + \
                    connectionData['target']+". Input '" + inputName + "' not found on Component:" + targetComponent.getPath())
                connectionFailure = True

            if connectionFailure is False:
                inputPort.setConnection(outputPort)
                inputPort.setIndex(connectionData.get('targetIndex', 0))

        Profiler.getInstance().pop()


    def loadRigDefinition(self, jsonData):
        """Load a rig definition from a JSON structure.

        Args:
            jsonData (dict): JSON data containing the rig definition.

        Returns:
            bool: True if successful.

        """

        Profiler.getInstance().push("loadRigDefinition:" + self.getName())

        krakenSystem = KrakenSystem.getInstance()

        if 'name' in jsonData:
            self.setName(jsonData['name'])

        if 'components' in jsonData:
            self._loadComponents(jsonData['components'])

            if 'connections' in jsonData:
                self._makeConnections(jsonData['connections'])

        if 'metaData' in jsonData:

            for k, v in jsonData['metaData'].iteritems():
                self.setMetaData(k, v)

        Profiler.getInstance().pop()


    def writeGuideDefinitionFile(self, filepath):
        """Writes a rig definition to a file on disk.

        Args:
            filepath (str): The file path of the rig definition file.

        Returns:
            bool: True if successful.

        """

        Profiler.getInstance().push("WriteGuideDefinitionFile:" + filepath)

        guideData = self.getRigBuildData()

        # now preprocess the data ready for saving to disk.
        pureJSON = prepareToSave(guideData)

        with open(filepath,'w') as rigDef:
            rigDef.write(json.dumps(pureJSON, indent=2))

        Profiler.getInstance().pop()


    def getData(self):
        """Get the graph definition of the rig. This method is used to save the state of the guide itself.

        Returns:
            dict: The JSON data struture of the rig data

        """

        guideData = {
            'name': self.getName()
        }

        componentsJson = []
        guideComponents = self.getChildrenByType('Component')
        for component in guideComponents:
            componentsJson.append(component.saveData())
        guideData['components'] = componentsJson

        connectionsJson = []
        for component in guideComponents:
            for i in range(component.getNumInputs()):
                componentInput = component.getInputByIndex(i)
                if componentInput.isConnected():
                    componentOutput = componentInput.getConnection()
                    connectionJson = {
                        'source': componentOutput.getParent().getDecoratedName() + '.' + componentOutput.getName(),
                        'target': component.getDecoratedName() + '.' + componentInput.getName(),
                        'targetIndex': componentInput.getIndex()
                    }
                    connectionsJson.append(connectionJson)

        guideData['connections'] = connectionsJson
        guideData['metaData'] = self._metaData

        return guideData


    def getRigBuildData(self):
        """Get the graph definition of the guide for building the final rig.

        Returns:
            dict: The JSON data struture of the guide rig data

        """

        guideData = {
            'name': self.getName()
        }

        componentsJson = []
        guideComponents = self.getChildrenByType('Component')
        for component in guideComponents:
            componentsJson.append(component.getRigBuildData())

        guideData['components'] = componentsJson

        connectionsJson = []
        for component in guideComponents:
            for i in xrange(component.getNumInputs()):
                componentInput = component.getInputByIndex(i)
                if componentInput.isConnected():
                    componentOutput = componentInput.getConnection()
                    connectionJson = {
                        'source': componentOutput.getParent().getDecoratedName() + '.' + componentOutput.getName(),
                        'target': component.getDecoratedName() + '.' + componentInput.getName(),
                        'targetIndex': componentInput.getIndex()
                    }
                    connectionsJson.append(connectionJson)

        guideData['connections'] = connectionsJson

        return guideData

    # ==========
    # Meta Data
    # ==========
    def getMetaData(self):
        """Gets the meta data from the rig.

        Returns:
            dict: Extra data stored on the rig.

        """

        return self._metaData

    def setMetaData(self, name, data):
        """Sets meta data on the rig.

        Args:
            data (dict): Extra data needed to persist the rig / graph.

        Returns:
            bool: True if successful.

        """

        self._metaData[name] = data

        return True
