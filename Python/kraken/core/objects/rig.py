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


    def loadRigDefinitionFile(self, filepath):
        """Load a rig definition from a file on disk.

        Arguments:
        filepath -- string, the file path of the rig definition file.

        Return:
        True if successful.

        """

        Profiler.getInstance().push("LoadRigDefinitionFile:" + filepath)

        if not os.path.exists(filepath):
            raise Exception("File not found:" + filepath)

        with open(filepath) as rigDef:
            jsonData = json.load(rigDef)

        # now preprocess the data ready for loading.
        jsonData = prepareToLoad(jsonData)

        self.loadRigDefinition(jsonData)
        Profiler.getInstance().pop()


    def loadRigDefinition(self, jsonData):
        """Load a rig definition from a JSON structure.

        Arguments:
        jsonData -- dict, the JSON data containing the rig definition.

        Return:
        True if successful.

        """

        Profiler.getInstance().push("loadRigDefinition:" + self.getName())

        krakenSystem = KrakenSystem.getInstance()

        if 'name' in jsonData:
            self.setName(jsonData['name'])


        def __loadComponents(componentsJson):
            Profiler.getInstance().push("__loadComponents")

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


        def __makeConnections(connectionsJson):

            Profiler.getInstance().push("__makeConnections")

            for connectionData in connectionsJson:
                sourceComponentName, outputName = connectionData['source'].split('.')
                targetComponentName, inputName = connectionData['target'].split('.')

                sourceComponent = self.getChildByName(sourceComponentName)
                if sourceComponent is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Source component not found:" + sourceComponentName)
                targetComponent = self.getChildByName(targetComponentName)
                if targetComponent is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Target component not found:" + targetComponentName)
                outputPort = sourceComponent.getOutputByName(outputName)
                if outputPort is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Output '" + outputName + "' not found on Component:" + sourceComponent.getName())
                inputPort = targetComponent.getInputByName(inputName)
                if inputPort is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Input '" + inputName + "' not found on Component:" + targetComponent.getName())
                inputPort.setConnection(outputPort)

            Profiler.getInstance().pop()


        if 'components' in jsonData:
            __loadComponents(jsonData['components'])

            if 'connections' in jsonData:
                __makeConnections(jsonData['connections'])

        Profiler.getInstance().pop()



    def writeGuideDefinitionFile(self, filepath):
        """Writes a rig definition to a file on disk.

        Arguments:
        filepath -- string, the file path of the rig definition file.

        Return:
        True if successful.

        """

        Profiler.getInstance().push("WriteGuideDefinitionFile:" + filepath)

        guideData = self.getGuideData()

        # now preprocess the data ready for saving to disk.
        pureJSON = prepareToSave(guideData)

        with open(filepath,'w') as rigDef:
            rigDef.write(json.dumps(pureJSON, indent=2))

        Profiler.getInstance().pop()


    def getGuideData(self):
        """Get the graph definition of the guide for biulding the final rig.

        Return:
        The JSON data struture of the guide rig data

        """

        guideData = {
            'name': self.getName()
        }

        componentsJson = []
        guideComponents = self.getChildrenByType('Component')
        for component in guideComponents:
            componentsJson.append(component.getGuideData())
        guideData['components'] = componentsJson

        connectionsJson = []
        for component in guideComponents:
            for i in range(component.getNumInputs()):
                componentInput = component.getInputByIndex(i)
                if componentInput.isConnected():
                    componentOutput = componentInput.getConnection()
                    connectionJson = {
                        'source': componentOutput.getParent().getName() + '.' + componentOutput.getName(),
                        'target': component.getName() + '.' + componentInput.getName()
                    }
                    connectionsJson.append(connectionJson)

        guideData['connections'] = connectionsJson

        return guideData
