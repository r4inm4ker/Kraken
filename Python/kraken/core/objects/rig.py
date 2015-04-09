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

    def __init__(self, name):
        super(Rig, self).__init__(name)


    def loadRigDefinitionFile(self, filepath):
        Profiler.getInstance().push("LoadRigDefinitionFile:" + filepath)

        if not os.path.exists(filepath):
            raise Exception("File not found:" + filepath)
        jsonData = json.load(str(open( referencefile ).read()))
        this.loadRigDefinition(jsonData)
        Profiler.getInstance().pop()

    def loadRigDefinition(self, jsonData):

        Profiler.getInstance().push("loadRigDefinition:" + self.getName())

        krakenSystem = KrakenSystem.getInstance()

        def loadLayers(layersData):
            for layerName in layersData:
                layer = Layer(layerName, parent=self)

        def loadComponents(componentsData):
            Profiler.getInstance().push("loadComponents")

            for componentData in componentsData:
                moduleName = '.'.join(componentData['class'].split('.')[:-1])
                className = componentData['class'].split('.').pop()
                if moduleName is not "":
                    importlib.import_module(moduleName)

                componentClass = krakenSystem.getComponentClass(className)
                if 'name' in componentData:
                    componentName = componentData['name']
                else:
                    componentName = str(componentClass.__name__)                    
                component = componentClass(componentName, parent=self, data=componentData)

            Profiler.getInstance().pop()

        def makeConnections(connectionsData):
            Profiler.getInstance().push("makeConnections")

            for connectionData in connectionsData:
                sourceComponentName, outputName = connectionData['source'].split('.')
                targetComponentName, inputName = connectionData['target'].split('.')

                sourceComponent = self.getChildByName(sourceComponentName)
                if sourceComponent is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Source component not found:" + sourceComponent)
                targetComponent = self.getChildByName(targetComponentName)
                if targetComponent is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Source component not found:" + targetComponent)
                outputPort = sourceComponent.getOutputByName(outputName)
                if outputPort is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Output '" + outputName + "' not found on Component:" + sourceComponent.getName())
                inputPort = targetComponent.getInputByName(inputName)
                if inputPort is None:
                    raise Exception("Error making connection:" + connectionData['source'] + " -> " + connectionData['target']+". Input '" + inputName + "' not found on Component:" + targetComponent.getName())
                inputPort.setSource(outputPort.getTarget())

            Profiler.getInstance().pop()

        if 'layers' in jsonData:
            loadLayers(jsonData['layers'])
        else:
            raise Exception("A rig must define layers.")

        if 'components' in jsonData:
            loadComponents(jsonData['components'])

            if 'connections' in jsonData:
                makeConnections(jsonData['connections'])


        Profiler.getInstance().pop()