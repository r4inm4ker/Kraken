

class ComponentOutput(object):
    """docstring for ComponentOutput"""

    def __init__(self, name, dataType):
        super(ComponentOutput, self).__init__()
        self.name = name
        self.dataType = dataType
        self.connections = []


    # ===================
    # Connection Methods
    # ===================
    def addConnection(self, componentInput):
        self.connections.append(componentInput)

        return True


    def removeConnection(self, instance):
        index = self.connections.index(instance)
        del self.connections[index]

        return True


    def getNumConnections(self):
        return len(self.connections)


    def getConnection(self, index):
        return self.connections[index]