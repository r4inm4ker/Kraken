"""Kraken - objects.rig module.

Classes:
Rig -- Rig representation.

"""

from container import Container
from kraken.core.kraken_system import KrakenSystem
from kraken.core.profiler import Profiler
from kraken.core.objects.layer import Layer
import importlib
import json


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

        with open(referencefile) as rigDef:
            jsonData = json.load(rigDef)

        # jsonData = json.load(str(open(referencefile).read()))
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
                moduleName = '.'.join(componentData['class'].split('.')[:-1])
                className = componentData['class'].split('.').pop()
                if moduleName is not "":
                    importlib.import_module(moduleName)

                componentClass = krakenSystem.getComponentClass(className)
                if 'name' in componentData:
                    component = componentClass(name=componentData['name'], parent=self)
                else:
                    component = componentClass(parent=self)
                component.loadData(componentData)

            Profiler.getInstance().pop()


        def __makeConnections(connectionJson):

            Profiler.getInstance().push("__makeConnections")

            for connectionData in connectionJson:
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
                inputPort.setSource(outputPort.getTarget())

            Profiler.getInstance().pop()


        if 'components' in jsonData:
            __loadComponents(jsonData['components'])

            if 'connections' in jsonData:
                __makeConnections(jsonData['connections'])

        Profiler.getInstance().pop()

    def getGuideData(self):

        jsonData = {
            'name': self.getName()
        }
        
        componentsJson = []
        guideComponents = self.getChildrenByType('Component')
        for component in guideComponents:
            componentsJson.append(component.getGuideData())
        jsonData['components'] = componentsJson

        connectionsJson = []
        for component in guideComponents:
            for i in range(component.getNumOutputs()):
                componentOutput = component.getOutputByIndex(i)
                if componentOutput.isConnected():
                    componentInput = componentOutput.getConnection()
                    connectionJson = {
                        'source': componentOutput.getFullName(),
                        'target': componentInput.getFullName()
                    }
                    connectionsJson.append(connectionJson)

        jsonData['connections'] = connectionsJson
        
        return jsonData
