"""Kraken Canvas - Canvas Graph Manager module.

Classes:
GraphManager -- Node management.

"""

import json

from kraken.core.kraken_system import ks
import FabricEngine.Core as core

class GraphManager(object):
    """Manager object for taking care of all low level Canvas tasks"""

    __dfgHost = None
    __dfgBinding = None
    __dfgArgs = None
    __dfgExec = None
    __dfgNodes = None
    __dfgNodeAndPortMap = None
    __dfgConnections = None
    __dfgGroups = None
    __dfgGroupNames = None
    __dfgCurrentGroup = None

    def __init__(self):
        super(GraphManager, self).__init__()

        client = ks.getCoreClient()
        ks.loadExtension('KrakenForCanvas')

        self.__dfgHost = client.getDFGHost()
        self.__dfgBinding = self.__dfgHost.createBindingToNewGraph()
        self.__dfgExec = self.__dfgBinding.getExec()
        self.__dfgArgs = {}
        self.__dfgNodes = {}
        self.__dfgNodeAndPortMap = {}
        self.__dfgConnections = {}
        self.__dfgGroups = {}
        self.__dfgGroupNames = []
        self.__dfgCurrentGroup = None


    # ===============
    # Canvas Methods
    # ===============
    def setTitle(self, title):
        self.__dfgExec.setTitle(title)

    def getUniqueTitle(self, path, title):
        titleSuffix = 1
        uniqueTitle = title
        lookup = '%s|%s' % (path, uniqueTitle)
        while self.__dfgNodes.has_key(lookup):
            titleSuffix = titleSuffix + 1
            uniqueTitle = '%s_%d' % (title, titleSuffix)
            lookup = '%s|%s' % (path, uniqueTitle)

        return uniqueTitle

    def addExtDep(self, extDep):
        self.__dfgExec.addExtDep(extDep)

    def hasNode(self, path, title=None):
        lookup = path
        if not title is None:
            lookup = "%s|%s" % (path, title)

        return self.__dfgNodes.has_key(lookup)

    def hasNodeSI(self, kSceneItem, title=None):
        return self.hasNode(kSceneItem.getPath(), title=title)

    def getNode(self, path, title=None):
        lookup = path
        if not title is None:
            lookup = "%s|%s" % (path, title)

        return self.__dfgNodes.get(lookup, None)

    def getNodeSI(self, kSceneItem, title=None):
        return self.getNode(kSceneItem.getPath(), title=title)

    def getNodeAndPort(self, path, asInput=True):
        if not self.__dfgNodeAndPortMap.has_key(path):
            return None

        nodeAndPort = self.__dfgNodeAndPortMap[path]
        if asInput:
            return nodeAndPort[0]

        return nodeAndPort[1]

    def getNodeAndPortSI(self, kSceneItem, asInput=True):
        return self.getNodeAndPort(kSceneItem.getPath(), asInput=asInput)

    def setNodeAndPort(self, path, node, port, asInput=False):
        nodeAndPort = self.__dfgNodeAndPortMap.get(path, [(node, port), (node, port)])

        if asInput:
            nodeAndPort[0] = (node, port)
        else:
            nodeAndPort[1] = (node, port)

        self.__dfgNodeAndPortMap[path] = nodeAndPort

    def setNodeAndPortSI(self, kSceneItem, node, port, asInput=False):
        self.setNodeAndPort(kSceneItem.getPath(), node, port, asInput=asInput)

    def getExec(self):
        return self.__dfgExec

    def getSubExec(self, node):
        return self.__dfgExec.getSubExec(node)

    def hasArgument(self, name):
        return self.__dfgArgs.has_key(name)

    def getOrCreateArgument(self, name, dataType=None, defaultValue=None, portType="In"):
        if self.__dfgArgs.has_key(name):
            return self.__dfgArgs[name]

        client = ks.getCoreClient()
        dfgPortType = client.DFG.PortTypes.In
        if portType.lower() == 'out':
            dfgPortType = client.DFG.PortTypes.Out
        elif portType.lower() == 'io':
            dfgPortType = client.DFG.PortTypes.IO

        self.__dfgArgs[name] = self.__dfgExec.addExecPort(name, dfgPortType)
        if dataType:
            self.__dfgBinding.setArgValue(self.__dfgArgs[name], ks.rtVal(dataType, defaultValue))

        return self.__dfgArgs[name]

    def removeArgument(self, name):
        if not self.__dfgArgs.has_key(name):
            return False
        self.__dfgExec.removeExecPort(self.__dfgArgs[name])
        del self.__dfgArgs[name]

        return True

    def createNodeFromPreset(self, path, preset, title=None, **metaData):
        lookup = path
        if not title is None:
            lookup = "%s|%s" % (path, title)

        if self.__dfgNodes.has_key(lookup):
            raise Exception("Node for %s already exists." % lookup)

        node = self.__dfgExec.addInstFromPreset(preset)
        self.__dfgNodes[lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData)
        self.__addNodeToGroup(node)

        return node

    def createNodeFromPresetSI(self, kSceneItem, preset, title=None, **metaData):
        node = self.createNodeFromPreset(kSceneItem.getPath(), preset, title=title, **metaData)
        self.setNodeMetaDataSI(kSceneItem, 'uiComment', kSceneItem.getPath(), title=title)

        return node

    def createFunctionNode(self, path, title, **metaData):
        lookup = path
        if not title is None:
            lookup = "%s|%s" % (path, title)

        if self.__dfgNodes.has_key(lookup):
            raise Exception("Node for %s already exists." % lookup)

        node = self.__dfgExec.addInstWithNewFunc(title)
        self.__dfgNodes[lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData)
        self.__addNodeToGroup(node)

        return node

    def createFunctionNodeSI(self, kSceneItem, title, **metaData):
        return self.createFunctionNode(kSceneItem.getPath(), title, **metaData)

    def createVariableNode(self, path, title, dataType, extension="", **metaData):
        lookup = path
        if not title is None:
            lookup = "%s|%s" % (path, title)

        if self.__dfgNodes.has_key(lookup):
            raise Exception("Node for %s already exists." % lookup)

        node = self.__dfgExec.addVar(title, dataType, extension)
        self.__dfgNodes[lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData)
        self.__addNodeToGroup(node)

        return node

    def createVariableNodeSI(self, kSceneItem, title, dataType, extension="", **metaData):
        return self.createVariableNode(kSceneItem.getPath(), title, dataType, extension=extension, **metaData)

    def removeNode(self, path, title=None):
        lookup = path
        if not title is None:
            lookup = "%s|%s" % (path, title)

        if not self.__dfgNodes.has_key(lookup):
            raise Exception("Node for %s does not exist." % lookup)

        node = self.__dfgNodes[lookup]
        self.__dfgExec.removeNode(node)
        del self.__dfgNodes[lookup]

        # clean up groups
        for group in self.__dfgGroups:
            for i in range(len(self.__dfgGroups[group])):
                if self.__dfgGroups[group][i] == node:
                    del self.__dfgGroups[group][i]
                    break

        # clean up connections
        if self.__dfgConnections.has_key(node):
            del self.__dfgConnections[node]
        for nodeName in self.__dfgConnections:
            ports = self.__dfgConnections[nodeName]
            for portName in ports:
                connections = ports[portName]
                newConnections = []
                for c in connections:
                    if c[0] == node:
                      continue
                    newConnections += [c]
                self.__dfgConnections[nodeName][portName] = newConnections

        return True

    def removeNodeSI(self, kSceneItem, title=None):
        return self.removeNode(kSceneItem.getPath(), title=title)

    def connectNodes(self, nodeA, portA, nodeB, portB):

        self.removeConnection(nodeB, portB)

        typeA = self.getNodePortResolvedType(nodeA, portA)
        typeB = self.getNodePortResolvedType(nodeB, portB)

        if typeA != typeB and typeA != None and typeB != None:
            if typeA == 'Xfo' and typeB == 'Mat44':
                preset = "Fabric.Exts.Math.Xfo.ToMat44"
                title = self.getUniqueTitle(nodeA, 'Convert')
                convertNode = self.createNodeFromPreset(nodeA, preset, title=title)
                self.connectNodes(nodeA, portA, convertNode, "this")
                nodeA = convertNode
                portA = "result"
            elif typeA == 'Mat44' and typeB == 'Xfo':
                preset = "Fabric.Exts.Math.Xfo.SetFromMat44"
                title = self.getUniqueTitle(nodeA, 'Convert')
                convertNode = self.createNodeFromPreset(nodeA, preset, title=title)
                self.connectNodes(nodeA, portA, convertNode, "m")
                nodeA = convertNode
                portA = "this"
            else:
                raise Exception('Cannot connect - incompatible type specs %s and %s.' % (typeA, typeB))

        self.__dfgExec.connectTo(nodeA+'.'+portA, nodeB+'.'+portB)

        if not self.__dfgConnections.has_key(nodeA):
          self.__dfgConnections[nodeA] = {}
        if not self.__dfgConnections[nodeA].has_key(portA):
          self.__dfgConnections[nodeA][portA] = []
        self.__dfgConnections[nodeA][portA].append((nodeB, portB))

        return True

    def connectArg(self, argA, argB, argC):
        if self.__dfgArgs.has_key(argA):
            self.__dfgExec.connectTo(argA, argB+'.'+argC)
            return True
        elif self.__dfgArgs.has_key(argC):
            self.__dfgExec.connectTo(argA+'.'+argB, argC)
            return True

        return False

    def replaceConnections(self, oldNode, oldPort, newNode, newPort):
        prevConnections = []
        prevConnections = self.getConnections(oldNode, oldPort)
        for c in prevConnections:
            if c[0] == newNode:
              continue
            self.removeConnection(c[0], c[1])
            self.connectNodes(newNode, newPort, c[0], c[1])

    def removeConnection(self, node, port):
        result = False
        for nodeName in self.__dfgConnections:
            ports = self.__dfgConnections[nodeName]
            for portName in ports:
                connections = ports[portName]
                newConnections = []
                for i in range(len(connections)):
                    if '.'.join(connections[i]) == node+'.'+port:
                        self.__dfgExec.disconnectFrom(nodeName+'.'+portName, node+'.'+port)
                        result = True
                        break
                    else:
                        newConnections += [connections[i]]
                self.__dfgConnections[nodeName][portName] = newConnections
                if result:
                    return result

        return result

    def getConnections(self, node, port, targets=True):
        result = []
        for nodeName in self.__dfgConnections:
            ports = self.__dfgConnections[nodeName]
            for portName in ports:
                connections = ports[portName]
                if targets:
                    if node+'.'+port == nodeName+'.'+portName:
                        result += connections
                    else:
                        continue
                else:
                    for c in connections:
                        if '.'.join(c) == node+'.'+port:
                            result += [(nodeName, portName)]

        return result

    def getNodeMetaData(self, path, key, defaultValue=None, title=None):
        lookup = path
        if not title is None:
            lookup = "%s|%s" % (path, title)
        if not self.__dfgNodes.has_key(lookup):
            return defaultValue
        node = self.__dfgNodes[lookup]

        return self.__dfgExec.getNodeMetadata(node, key)

    def getNodeMetaDataSI(self, kSceneItem, key, defaultValue=None, title=None):
        return self.getNodeMetaData(kSceneItem.getPath(), key, defaultValue=defaultValue, title=title)

    def setNodeMetaData(self, path, key, value, title=None):
        lookup = path
        node = path
        if not title is None:
            lookup = "%s|%s" % (path, title)
        if self.__dfgNodes.has_key(lookup):
            node = self.__dfgNodes[lookup]
        self.__dfgExec.setNodeMetadata(node, key, str(value))
        if key == 'uiComment':
            self.__dfgExec.setNodeMetadata(node, 'uiCommentExpanded', 'true')

        return True

    def setNodeMetaDataSI(self, kSceneItem, key, value, title=None):
        return self.setNodeMetaData(kSceneItem.getPath(), key, value, title=title)

    def setNodeMetaDataFromDict(self, node, metaData):
        for key in metaData:
            self.setNodeMetaData(node, key, value, metaData[key])

    def computeCurrentPortValue(self, node, port):
        client = ks.getCoreClient()
        tempPort = self.getOrCreateArgument("temp", portType="Out")
        self.connectArg(node, port, tempPort)

        errors = json.loads(self.__dfgBinding.getErrors(True))
        if errors and len(errors) > 0:
            raise Exception(str(errors))

        self.__dfgBinding.execute()

        value = self.__dfgBinding.getArgValue(tempPort)

        self.removeArgument(tempPort)

        return value

    def computeCurrentPortValueSI(self, kSceneItem):
        nodeAndPort = self.getNodeAndPortSI(kSceneItem, asInput=True)
        if not nodeAndPort:
            return None
        (node, port) = nodeAndPort

        return self.computeCurrentPortValue(node, port)

    def setPortDefaultValue(self, node, port, value):
        portPath = "%s.%s" % (node, port)

        subExec = self.__dfgExec.getSubExec(node)
        dataType = subExec.getExecPortTypeSpec(port)

        rtVal = value
        if str(type(rtVal)) != '<type \'PyRTValObject\'>':
          rtVal = ks.rtVal(dataType, value)

        self.__dfgExec.setPortDefaultValue(portPath, rtVal)

        return True

    def getNodePortResolvedType(self, node, port):
        result = self.__dfgExec.getNodePortResolvedType(node+'.'+port)
        return result

    def getCurrentGroup(self):
        return self.__dfgCurrentGroup

    def getAllGroupNames(self):
        return self.__dfgGroupNames + []

    def getNodesInGroup(self, group):
        return self.__dfgGroups.get(group, []) + []

    def setCurrentGroup(self, group):

        if group is None:
            self.__dfgCurrentGroup = None
            return None

        if not self.__dfgGroups.has_key(group):
            self.__dfgGroups[group] = []
            self.__dfgGroupNames.append(group)

        if group != self.__dfgCurrentGroup:
            self.__dfgCurrentGroup = group

        return self.__dfgGroups[self.__dfgCurrentGroup]

    def __addNodeToGroup(self, node):
        if(not self.__dfgCurrentGroup):
            return
        self.__dfgGroups[self.__dfgCurrentGroup].append(node)

    def getAllNodeNames(self):
        return self.__dfgNodes.values()

    def getNodeConnections(self, nodeName):
        keys = {}
        result = []
        node = self.__dfgConnections.get(nodeName, {})
        for portName in node:
            port = node[portName]
            for (otherNode, otherPort) in port:
                key = '%s - %s' % (nodeName, otherNode)
                if keys.has_key(key):
                    continue
                keys[key] = True
                result += [otherNode]

        return result

    def getAllNodeConnections(self):
        keys = {}
        result = {}
        for nodeName in self.__dfgConnections:
            node = self.__dfgConnections[nodeName]
            for portName in node:
                port = node[portName]
                for (otherNode, otherPort) in port:
                    key = '%s - %s' % (nodeName, otherNode)
                    if keys.has_key(key):
                        continue
                    keys[key] = True
                    if not result.has_key(nodeName):
                        result[nodeName] = []
                    result[nodeName] += [otherNode]

        return result

    def getNumPorts(self, node):
        nodeType = self.__dfgExec.getNodeType(node)
        if nodeType == 3: # var
            return 1
        elif nodeType == 0: # inst
            subExec = self.getSubExec(node)
            return subExec.getExecPortCount()

        return 0

    def hasInputConnections(self, node):
        for nodeName in self.__dfgConnections:
            ports = self.__dfgConnections[nodeName]
            for portName in ports:
                connections = ports[portName]
                for c in connections:
                    if c[0] == node:
                        return True

        return False

    def hasOutputConnections(self, node):
        ports = self.__dfgConnections.get(node, {})
        for port in ports:
            if len(ports) > 0:
                return True

        return False

    def getPortIndex(self, node, port):
        nodeType = self.__dfgExec.getNodeType(node)
        if nodeType == 3: # var
            return 0
        elif nodeType == 0: # inst
            subExec = self.getSubExec(node)
            for i in range(subExec.getExecPortCount()):
                portName = subExec.getExecPortName(i)
                if portName == port:
                    return i

        return 0

    def getMinConnectionPortIndex(self, sourceNode, targetNode):
        minIndex = 10000
        node = self.__dfgConnections.get(sourceNode, {})
        for portName in node:
            port = node[portName]
            for (otherNode, otherPort) in port:
                if not otherNode == targetNode:
                    continue
                index = self.getPortIndex(otherNode, otherPort)
                if index < minIndex:
                    minIndex = index

        if minIndex == 10000:
            return 0

        return minIndex

    def getAllNodePortIndices(self):
        result = {}
        nodes = self.getAllNodeNames()
        for n in nodes:
            result[n] = {}
            nodeType = self.__dfgExec.getNodeType(n)
            if nodeType == 3: # var
                result[n]['value'] = 0
            elif nodeType == 0: # inst
                subExec = self.getSubExec(n)
                for i in range(subExec.getExecPortCount()):
                    port = subExec.getExecPortName(i)
                    result[n][port] = i

        return result

    def getAllInputConnections(self):
        nodes = self.getAllNodeNames()
        connections = {}
        for n in nodes:
            connections[n] = []

    def implodeNodesByGroup(self):
        for group in self.__dfgGroupNames:
            nodes = self.__dfgGroups[group]

            implodedName = self.__dfgExec.implodeNodes(group, nodes)
            break # todo... right now this doesn't work properly

            # todo
            # # rename the ports based on their source metadata
            # subExec = self.__dfgTopLevelGraph.getSubExec(implodedName)
            # for i in range(subExec.getExecPortCount()):
            #     if subExec.getExecPortType(i) == client.DFG.PortTypes.In:
            #         continue
            #     arg = subExec.getExecPortName(i)
            #     shouldBreak = False
            #     for j in range(subExec.getNodeCount()):
            #         if shouldBreak:
            #             break
            #         node = subExec.getNodeName(j)
            #         if subExec.getNodeType(node) > 1:
            #             continue
            #         nodeExec = subExec.getSubExec(node)
            #         for k in range(nodeExec.getExecPortCount()):
            #             port = nodeExec.getExecPortName(k)
            #             if subExec.isConnectedTo(node+'.'+port, arg):
            #                 metaData = subExec.getNodeMetadata(node, 'uiComment')
            #                 if not metaData:
            #                     continue
            #                 name = metaData.rpartition('.')[2]
            #                 subExec.renameExecPort(arg, name)
            #                 shouldBreak = True
            #                 break

    def saveToFile(self, filePath):
        content = self.__dfgBinding.exportJSON()
        open(filePath, "w").write(content)
        print 'Canvas Builder: Saved file '+str(filePath)
