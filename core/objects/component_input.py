"""Kraken - objects.component input module.

Classes:
ComponentInput -- Component input representation.

"""

class ComponentInput(object):
    """docstring for ComponentInput"""

    def __init__(self, name, dataType):
        super(ComponentInput, self).__init__()
        self.name = name
        self.dataType = dataType
        self.connection = None


    # ===================
    # Connection Methods
    # ===================
    def setConnection(self, componentOutput):
        self.connection = componentOutput
        componentOutput.addConnection(self)

        return True


    def removeConnection(self):

        if self.connection is None:
            return True

        self.connection.removeConnection(self)
        self.setConnection(None)

        return True


    def getConnection(self):
        return self.connection