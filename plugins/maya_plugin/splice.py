"""Splice Utilities, Maya.

DCC agnostic python modules for loading Splice Nodes and adding connections.

Author: Eric Thivierge

"""


from kraken.kraken_maya.utils import *
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
        self.connectOpData = {}

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

            if connection["portName"] not in pm.listAttr(self.spliceNode):
                raise AttributeError(connection["portName"] + " not an attribute on the Splice Node:" + self.spliceNode)

            connection["srcNode"].attr("worldMatrix").connect(self.spliceNode.attr(connection["portName"]))

        return


    def connectOutMatrixPorts(self):

        for connection in self.connections:
            if connection["ioType"] != "output" or connection["portType"] != "matrix":
                continue

            if connection["portName"] not in pm.listAttr(self.spliceNode):
                raise AttributeError(connection["portName"] + " not an attribute on the Splice Node:" + self.spliceNode)

            portName = connection["portName"]
            if pm.getAttr(self.spliceNode.attr(connection["portName"]), type=True) == "TdataCompound":
                portName += "[" + str(pm.getAttr(self.spliceNode.attr(connection["portName"]), size=True)) + "]"

            decomposeNode = pm.createNode('decomposeMatrix')
            self.spliceNode.attr(portName).connect(decomposeNode.attr("inputMatrix"))

            decomposeNode.attr("outputRotate").connect(connection["srcNode"].attr("rotate"))
            decomposeNode.attr("outputScale").connect(connection["srcNode"].attr("scale"))
            decomposeNode.attr("outputTranslate").connect(connection["srcNode"].attr("translate"))

        return


    def connectDirectPorts(self):
        """Finds attributes on the connectDirectNode and connects directly with those on the splice node.

        Return:
        True if successful.

        """

        if self.connectDirectNode is None:
            print "No connectDirectNode specified. Continuing."
            return True

        tgtPorts = self.getInPortsByType("parameter")
        for eachItem in tgtPorts:

            if eachItem not in pm.listAttr(self.connectDirectNode) or eachItem not in pm.listAttr(self.spliceNode):
                print eachItem + " could not be connected!"
                continue

            srcAttr = self.connectDirectNode.attr(eachItem)
            tgtAttr = self.spliceNode.attr(eachItem)

            srcAttr.connect(tgtAttr)

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

        self.spliceNode = pm.createNode('spliceMayaNode', name="armLSpliceNode")
        cmds.fabricSplice('loadSplice', self.spliceNode, '{"fileName": "' + self.spliceFilePath + '"}')

        self.buildConnections()
        self.connectDirectPorts()

        pm.dgdirty(self.spliceNode)

        return True