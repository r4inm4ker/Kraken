"""Kraken - objects.containers module.

Classes:
Container -- Component container representation.

"""

from collections import OrderedDict


class Container(object):
    """docstring for Container"""

    def __init__(self, name):
        super(Container, self).__init__()
        self.name = name
        self.components = OrderedDict()
        self.definition = {
                           "name":self.name,
                           "components":{}
                          }


    def addComponent(self, component):
        """Adds a component to the container.

        Arguments:
        component -- Component to add to this container.

        Return:
        Component that was added to the container.
        """

        if component.name in self.components.keys():
            raise KeyError("Component is already part of the container: " + component.name)
            return False

        self.components[component.name] = component
        component.container = self

        return component


    def removeComponent(self, componentName):
        """Removes a component from this container.

        Arguments:
        componentName -- String, name of the component to remove from the container.

        Return:
        True if successful.
        """

        if componentName not in self.components.keys():
            raise KeyError("Component not found in this container: " + componentName)
            return False

        targetComponent = self.components[componentName]
        targetComponent.container = None

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

        for eachComponent in self.components:
            self.definition["components"][eachComponent] = component.buildDefinition()

        return self.definition