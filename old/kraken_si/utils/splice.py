"""Splice Utilities, Softimage.

DCC agnostic python modules for loading Splice Nodes and adding connections.

Author: Eric Thivierge

"""


from kraken.kraken_si.utils import *
import json


class SpliceBuilder(object):
    """Object to aggregate all port connections for a Splice Node and build the
    Splice node."""

    def __init__(self, spliceFilePath):
        """Initialize SpliceBuilder

        Arguments:
        spliceFilePath -- String, path to the splice file you wish to laod.

        """

        super(SpliceBuilder, self).__init__()
        self.spliceFilePath = spliceFilePath
        self.spliceData = None
        self.spliceNode = None
        self.connectDirectNode = None
        self.connections = []
        self.connectOpData = {
                                "fileName": self.spliceFilePath,
                                "skipPicking":True,
                                "hideUI": True
                             }

        with open(self.spliceFilePath) as spliceFile:
            self.spliceData = json.load(spliceFile)


    # ========
    # Adders
    # ========
    def addConnection(self, ioType, portType, srcNode, portName):
        """Adds a connection from a source node to the spliceNode.

        Arguments:
        ioType -- String, input or output connection.
        portType -- String, data type of the connection to create.
        srcNode -- Node, node from which to make the connection.
        portName -- String, name of the port to connect to.

        """

        ioTypes = ["input", "output"]
        portTypes = ["matrix"]

        if ioType not in ioTypes:
            raise ValueError(ioType + " is not a valid io type: " + ioTypes)

        if portType not in portTypes:
            raise ValueError(portType + " is not a valid connection type: " + portTypes)

        connectionData = {
                            "ioType":ioType,
                            "portType":portType,
                            "srcNode":srcNode,
                            "portName":portName
                         }

        self.connections.append(connectionData)

        return True


    # ========
    # Getters
    # ========
    def getInPortsByType(self, paramType):
        """Returns a list of input ports on the Splice node.

        Arguments:
        paramType -- String, parameter type to query.

        Return:
        List of parameter ports.

        """

        paramTypes = {
                       "parameter":"addParameter",
                       "input":"addInputPort"
                     }

        if paramType not in paramTypes.keys():
            raise ValueError(paramType + " is not in " + paramTypes.keys())

        portInfo = self.spliceData["ports"]
        inPorts = []
        for eachPort in portInfo:
            if eachPort["mode"] != "in":
                continue

            if "action" not in eachPort["options"].keys():
                continue

            if eachPort["options"]["action"] != paramTypes[paramType]:
                continue

            inPorts.append(eachPort["name"])

        return inPorts


    def getOutPorts(self):
        """Get output ports on the Splice node.

        Return:
        List of output ports.

        """

        portInfo = self.spliceData["ports"]
        outPorts = []
        for eachPort in portInfo:
            if eachPort["mode"] != "io" or not eachPort["type"].startswith("Mat44"):
                continue

            outPorts.append(eachPort["name"])

        return outPorts


    # ===========
    # Connecters
    # ===========
    def connectInMatrixPorts(self):

        for connection in self.connections:
            if connection["ioType"] != "input" or connection["portType"] != "matrix":
                continue

            if connection["portName"] not in self.getInPortsByType("input"):
                raise AttributeError(connection["portName"] + " not an attribute on the Splice Node")

            if connection["portName"] not in self.connectOpData.keys():
                self.connectOpData[connection["portName"]] = connection["srcNode"].FullName + ".kine.global"
            else:
                self.connectOpData[connection["portName"]] += "," + connection["srcNode"].FullName + ".kine.global"

        return


    def connectOutMatrixPorts(self):

        for connection in self.connections:
            if connection["ioType"] != "output" or connection["portType"] != "matrix":
                continue

            if connection["portName"] not in self.getOutPorts():
                raise AttributeError(connection["portName"] + " not an attribute on the Splice Node")

            if connection["portName"] not in self.connectOpData.keys():
                self.connectOpData[connection["portName"]] = connection["srcNode"].FullName + ".kine.global"
            else:
                self.connectOpData[connection["portName"]] += "," + connection["srcNode"].FullName + ".kine.global"

        return


    def connectDirectPorts(self):
        """Finds attributes on the connectDirectNode and connects directly with those on the splice node.

        Return:
        True if successful.

        """

        if self.connectDirectNode is None:
            log("No connectDirectNode specified. Continuing.", 8)
            return True

        tgtPorts = self.getInPortsByType("parameter")
        for eachItem in tgtPorts:

            if eachItem not in [x.Name for x in self.connectDirectNode.Parameters] or eachItem not in [x.Name for x in self.spliceNode.Parameters]:
                log(eachItem + " could not be connected!", 4)
                continue

            self.spliceNode.Parameters(eachItem).AddExpression(self.connectDirectNode.Parameters(eachItem).FullName)

        return True


    # =========
    # Builders
    # =========
    def buildConnections(self):
        """Builds all connections on the Splice node."""

        self.connectInMatrixPorts()
        self.connectOutMatrixPorts()

        return True


    def build(self):
        """Creates the Splice node and makes connections.

        Return:
        True if successful.

        """

        self.buildConnections()
        spliceOpPath = si.fabricSplice("loadSplice", json.dumps(self.connectOpData), "", "")
        self.spliceNode = si.Dictionary.GetObject(spliceOpPath, False)
        self.connectDirectPorts()

        return True