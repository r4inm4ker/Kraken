"""Kraken - Assembler."""

from kraken.core.objects import containers
from kraken.core import *

from collections import OrderedDict
import json


class Assembler(object):
    """Kraken Assembler."""

    def __init__(self):
        super(Assembler, self).__init__()
        self.container = None
        self.definition = {
                        "app":"Kraken",
                        "version":getVersion(),
                        "definition":{}
                      }


    def addContainer(self, container):
        """Adds a container to the Assembler.

        Arguments:
        container -- Container to add to this Assembler.

        Return:
        True if successful.
        """

        if container.name in self.containers.keys():
            raise KeyError("Container is already part of the Assembler: " + container.name)
            return False

        self.containers[container.name] = container
        container.container = self

        return container


    def removeContainer(self, containerName):
        """Removes a container from this Assembler.

        Arguments:
        containerName -- String, name of the container to remove from the Assembler.

        Return:
        True if successful.
        """

        if componentName not in self.components.keys():
            raise KeyError("Container not found in this Assembler: " + componentName)
            return False

        targetContainer = self.components[componentName]
        targetContainer.container = None

        del self.components[componentName]

        return True


    # ================
    # Build Functions
    # ================
    def buildDef(self):
        """Builds the Rig Definition and stores to rigDef attribute.

        Return:
        Dictionary of object data.
        """

        if self.container is None:
            raise AttributeError("Assembler has no container!")

        self.definition["definition"] = self.container.buildDef()

        return self.definition


from kraken.core.objects.containers import *

assembler = Assembler()
container = Container("MyContainer")
assembler.container = container
print json.dumps(assembler.buildDef())