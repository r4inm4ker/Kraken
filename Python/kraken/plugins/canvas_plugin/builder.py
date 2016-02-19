"""Kraken Canvas - Canvas Builder module.

Classes:
Builder -- Component representation.

"""

import json
import copy

from kraken.core.kraken_system import ks
from kraken.core.builder import Builder
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.control import Control
from kraken.core.objects.joint import Joint
from kraken.core.objects.rig import Rig
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.color import Color
from kraken.core.maths.xfo import Xfo
from kraken.plugins.canvas_plugin.layout import SpringLayout

import FabricEngine.Core as core

class Builder(Builder):
    """Builder object for building Kraken objects in Canvas."""

    __outputFilePath = None
    __dfgBinding = None
    __dfgArguments = None
    __dfgTopLevelGraph = None
    __dfgNodes = None
    __dfgConstructors = None
    __dfgCurves = None
    __dfgLastCurveNode = None
    __dfgAttributes = None
    __dfgConstraints = None
    __dfgComponentPortMap = None
    __dfgTransforms = None
    __dfgConnections = None
    __dfgLastLinesNode = None
    __layoutG = None
    __layoutFunc = None

    def __init__(self):
        super(Builder, self).__init__()

    def report(self, message):
        print "Canvas Builder: %s" % str(message)

    def reportError(self, error):
        self.report("Error: "+str(error))

    def makeHash(self, o):
        """
        Makes a hash from a dictionary, list, tuple or set to any level, that contains
        only other hashable types (including any lists, tuples, sets, and
        dictionaries).
        """

        if isinstance(o, (set, tuple, list)):
          new_o = copy.deepcopy(o)
          for i in range(len(new_o)):
              new_o[i] = self.makeHash(new_o[i])
          return hash(tuple(frozenset(sorted(new_o))))        

        elif not isinstance(o, dict):
            return hash(o)

        new_o = copy.deepcopy(o)
        for k, v in new_o.items():
            new_o[k] = self.makeHash(v)
        return hash(tuple(frozenset(sorted(new_o.items()))))  

    # ========================
    # IO Methods
    # ========================
    def setOutputFilePath(self, filePath):
        self.__outputFilePath = filePath

    # ========================
    # Canvas Preset Methods
    # ========================

    def hasSceneItemNode(self, kSceneItem):
        return self.__dfgNodes.has_key(kSceneItem.getPath())

    def getAttributeNodeAndPort(self, kAttribute, asInput = True):
        path = kAttribute.getPath()
        if self.__dfgAttributes.has_key(path):
            (constructNode, valueNode) = self.__dfgAttributes[path]
            if asInput or valueNode is None:
                return (constructNode, 'value')
            else:
                return (valueNode, 'result')

        objPath = path.rpartition('.')[0].rpartition('.')[0]
        return (self.__dfgNodes[objPath], kAttribute.getName())

    def getSceneItemNodeAndPort(self, kSceneItem, asInput = True):
        if isinstance(kSceneItem, Attribute):
            return self.getAttributeNodeAndPort(kSceneItem, asInput)

        path = kSceneItem.getPath()
        return self.__dfgTransforms[path]

    def setSceneItemTransformPort(self, kSceneItem, node, port):

        # we might want to replace connections!
        prevConnections = []
        prevNode = None
        prevPort = None
        if self.__dfgTransforms.has_key(kSceneItem.getPath()):
            (prevNode, prevPort) = self.__dfgTransforms[kSceneItem.getPath()]
            prevConnections = self.getConnections(prevNode, prevPort)

        self.__dfgTransforms[kSceneItem.getPath()] = (node, port)
        # self.report('%s is now driven by %s.%s' % (kSceneItem.getPath(), node, port))

        for c in prevConnections:
            if c[0] == node:
              continue
            self.removeConnection(c[0], c[1])
            self.connectCanvasNodes(node, port, c[0], c[1])

    def createTopLevelArguments(self):
        # todo: we might want to add options here
        client = ks.getCoreClient()
        if self.getConfig().getMetaData('DebugDrawingSupport', False):
            self.__dfgArguments['debugDraw'] = self.__dfgTopLevelGraph.addExecPort("debugDraw", client.DFG.PortTypes.In)
            self.__dfgBinding.setArgValue(self.__dfgArguments['debugDraw'], ks.rtVal('Boolean', False))
        self.__dfgArguments['time'] = self.__dfgTopLevelGraph.addExecPort("time", client.DFG.PortTypes.In)
        self.__dfgBinding.setArgValue(self.__dfgArguments['time'], ks.rtVal('Float32', 0.0))
        self.__dfgArguments['frame'] = self.__dfgTopLevelGraph.addExecPort("frame", client.DFG.PortTypes.In)
        self.__dfgBinding.setArgValue(self.__dfgArguments['frame'], ks.rtVal('Float32', 0.0))

        self.__dfgArguments['controls'] = self.__dfgTopLevelGraph.addExecPort("controls", client.DFG.PortTypes.In)
        self.__dfgBinding.setArgValue(self.__dfgArguments['controls'], ks.rtVal('Xfo[String]'))
        self.__dfgArguments['floats'] = self.__dfgTopLevelGraph.addExecPort("floats", client.DFG.PortTypes.In)
        self.__dfgBinding.setArgValue(self.__dfgArguments['floats'], ks.rtVal('Float32[String]'))
        # self.__dfgArguments['all'] = self.__dfgTopLevelGraph.addExecPort("all", client.DFG.PortTypes.Out)
        # self.__dfgBinding.setArgValue(self.__dfgArguments['all'], ks.rtVal('Xfo[String]'))
        self.__dfgArguments['joints'] = self.__dfgTopLevelGraph.addExecPort("joints", client.DFG.PortTypes.Out)
        self.__dfgBinding.setArgValue(self.__dfgArguments['joints'], ks.rtVal('Xfo[String]'))

    def decorateCanvasNode(self, node, metaData):
        for key in metaData:
            self.__dfgTopLevelGraph.setNodeMetadata(node, 'ui'+key.capitalize(), str(metaData[key]))
            if key == 'comment':
                self.__dfgTopLevelGraph.setNodeMetadata(node, 'uiCommentExpanded', 'true')

    def createCanvasNodeFromPreset(self, preset, addToLayout = True, **metaData):
        path = self.__dfgTopLevelGraph.addInstFromPreset(preset)
        if not self.__layoutG is None and addToLayout:
            self.__layoutG.addNode(path)
        self.decorateCanvasNode(path, metaData)
        self.report('Created node '+path)
        return path

    def createCanvasNodeFromFunction(self, name, addToLayout = True, **metaData):
        path = self.__dfgTopLevelGraph.addInstWithNewFunc(name)
        if not self.__layoutG is None and addToLayout:
            self.__layoutG.addNode(path)
        self.decorateCanvasNode(path, metaData)
        self.report('Created KL function '+path)
        return path

    def removeCanvasNode(self, node):
        self.__dfgTopLevelGraph.removeNode(node)
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

    def connectCanvasNodes(self, nodeA, portA, nodeB, portB, addToLayout = True):

        self.removeConnection(nodeB, portB)

        typeA = self.__dfgTopLevelGraph.getNodePortResolvedType("%s.%s" % (nodeA, portA))
        typeB = self.__dfgTopLevelGraph.getNodePortResolvedType("%s.%s" % (nodeB, portB))

        if typeA != typeB and typeA != None and typeB != None:
            if typeA == 'Xfo' and typeB == 'Mat44':
                preset = "Fabric.Exts.Math.Xfo.ToMat44"
                convertNode = self.createCanvasNodeFromPreset(preset)
                self.connectCanvasNodes(nodeA, portA, convertNode, "this")
                nodeA = convertNode
                portA = "result"
            elif typeA == 'Mat44' and typeB == 'Xfo':
                preset = "Fabric.Exts.Math.Xfo.SetFromMat44"
                convertNode = self.createCanvasNodeFromPreset(preset)
                self.connectCanvasNodes(nodeA, portA, convertNode, "m")
                nodeA = convertNode
                portA = "this"
            else:
                self.reportError('Cannot connect - incompatible type specs %s and %s.' % (typeA, typeB))

        result = self.__dfgTopLevelGraph.connectTo(nodeA+'.'+portA, nodeB+'.'+portB)
        # self.report('Connected %s.%s to %s.%s' % (nodeA, portA, nodeB, portB))

        if not self.__dfgConnections.has_key(nodeA):
          self.__dfgConnections[nodeA] = {}
        if not self.__dfgConnections[nodeA].has_key(portA):
          self.__dfgConnections[nodeA][portA] = []
        self.__dfgConnections[nodeA][portA].append((nodeB, portB))

        if not self.__layoutG is None and addToLayout:
            self.__layoutG.addEdge(nodeA, nodeB)

        return result

    def connectCanvasArg(self, argA, argB, argC, argIsInput = True):
        if argIsInput:
            self.__dfgTopLevelGraph.connectTo(argA, argB+'.'+argC)
            # self.report('Connected %s to %s.%s' % (argA, argB, argC))
        else:
            self.__dfgTopLevelGraph.connectTo(argA+'.'+argB, argC)
            # self.report('Connected %s.%s to %s' % (argA, argB, argC))

    def removeConnection(self, node, port):
        result = False
        for nodeName in self.__dfgConnections:
            ports = self.__dfgConnections[nodeName]
            for portName in ports:
                connections = ports[portName]
                newConnections = []
                for i in range(len(connections)):
                    if '.'.join(connections[i]) == node+'.'+port:
                        self.__dfgTopLevelGraph.disconnectFrom(nodeName+'.'+portName, node+'.'+port)
                        result = True
                    else:
                        newConnections += [connections[i]]
                self.__dfgConnections[nodeName][portName] = newConnections
        return result

    def getConnections(self, node, port, targets = True):
        result = []
        if targets:
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

    def connectCanvasOperatorPort(self, node, port, dataType, portType, connectedObjects, arraySizes):
        if dataType.endswith('[]'):

            if portType == 'In':

                pushNodes = []
                for c in connectedObjects:
                    pushNode = self.createCanvasNodeFromPreset("Fabric.Core.Array.Push", comment = c.getPath())
                    if len(pushNodes) > 0:
                        self.connectCanvasNodes(pushNodes[-1], "array", pushNode, "array")
                    pushNodes.append(pushNode)

                self.connectCanvasNodes(pushNode, 'array', node, port)

                for i in range(len(connectedObjects)):
                    c = connectedObjects[i]
                    (connNode, connPort) = self.getSceneItemNodeAndPort(c, asInput = False)
                    self.connectCanvasNodes(connNode, connPort, pushNodes[i], 'element')

            else:

                arraySizes[port] = len(connectedObjects)
                getNodes = []
                for i in range(len(connectedObjects)):
                    c = connectedObjects[i]
                    getNode = self.createCanvasNodeFromPreset("Fabric.Core.Array.Get", comment = c.getPath())
                    self.connectCanvasNodes(node, port, getNode, 'array')
                    indexVal = ks.rtVal("UInt32", i)
                    self.__dfgTopLevelGraph.setPortDefaultValue(getNode+'.index', indexVal)
                    getNodes.append(getNode)

                for i in range(len(connectedObjects)):
                    c = connectedObjects[i]
                    (connNode, connPort) = self.getSceneItemNodeAndPort(c, asInput = True)
                    if isinstance(c, Attribute):
                      self.connectCanvasNodes(getNodes[i], 'element', connNode, connPort)
                    else:
                      self.setSceneItemTransformPort(c, getNodes[i], 'element')

        else:

            if portType == 'In':
                (connNode, connPort) = self.getSceneItemNodeAndPort(connectedObjects, asInput = False)
                self.connectCanvasNodes(connNode, connPort, node, port)
            elif isinstance(connectedObjects, Attribute):
                (connNode, connPort) = self.getSceneItemNodeAndPort(connectedObjects, asInput = True)
                self.connectCanvasNodes(node, port, connNode, connPort)
            else:
                self.setSceneItemTransformPort(connectedObjects, node, port)

    def getIntermediateValue(self, node, port, prefix = ""):
        client = ks.getCoreClient()
        intermediatePort = self.__dfgTopLevelGraph.addExecPort("intermediateValue", client.DFG.PortTypes.Out)
        self.connectCanvasArg(node, port, intermediatePort, argIsInput = False)

        errors = json.loads(self.__dfgBinding.getErrors(True))
        if errors and len(errors) > 0:
            raise Exception(str(errors))

        # self.report(prefix+"Computing intermediate value "+port)
        self.__dfgBinding.execute()

        value = self.__dfgBinding.getArgValue(intermediatePort)
        self.__dfgTopLevelGraph.removeExecPort(intermediatePort)
        return value

    def setPortDefaultValue(self, kObj, port, value):
        path = kObj.getPath()

        if self.__dfgComponentPortMap.has_key(path):
            return True

        if not self.__dfgNodes.has_key(path):
            self.reportError('No DFG node has been created for path '+path)
            return False

        nodePath = self.__dfgNodes[path]
        portPath = "%s.%s" % (nodePath, port)

        subExec = self.__dfgTopLevelGraph.getSubExec(nodePath)
        dataType = subExec.getExecPortTypeSpec(port)

        if dataType == 'Color':
            if value is None:
                value = self.getBuildColor(kObj)
            if value:
                colors = self.config.getColors()
                c = colors[value]
                value = Color(r=c[1][0], g=c[1][1], b=c[1][2], a=1.0)

        rtVal = ks.rtVal(dataType, value)
        self.__dfgTopLevelGraph.setPortDefaultValue(portPath, rtVal)
        return True

    def buildCanvasNodeFromSceneItem(self, kSceneItem, buildName):

        cls = kSceneItem.__class__.__name__
        if cls in [
            'ComponentInput',
            'ComponentOutput'
        ]:
            cls = 'Transform'

        # todo: collect all nodes being created within a 
        # ComponentGroup
        # then expose all of hte attributes below the created ComponentInput
        # then expose all of hte attributes below the created ComponentOutput

        if cls in [
            'Layer',
            'Rig'
        ]:
            return True

        if not cls in [
            'ComponentGroup',
            'Container',
            'CtrlSpace',
            'Curve',
            'Control',
            'HierarchyGroup',
            'Joint',
            'Locator',
            'Transform'
        ]:
            self.reportError("buildCanvasNodeFromSceneItem: Unexpected class " + cls)
            return False

        path = kSceneItem.getPath()
        preset = "Kraken.Constructors.Kraken%s" % cls
        nodePath = self.createCanvasNodeFromPreset(preset, comment = kSceneItem.getPath())
        self.__dfgNodes[path] = nodePath
        self._registerSceneItemPair(kSceneItem, nodePath)
        self.__dfgConstructors[path] = nodePath

        # only the types which support animation
        if isinstance(kSceneItem, Control):
            preset = "Kraken.Constructors.GetXfo"
            xfoNode = self.createCanvasNodeFromPreset(preset, comment = kSceneItem.getPath())
            self.connectCanvasNodes(nodePath, 'result', xfoNode, 'this')
            self.setSceneItemTransformPort(kSceneItem, xfoNode, 'result')
        else:
            self.setSceneItemTransformPort(kSceneItem, nodePath, 'xfo')

        # set the defaults
        self.setPortDefaultValue(kSceneItem, "name", kSceneItem.getName())
        self.setPortDefaultValue(kSceneItem, "buildName", kSceneItem.getBuildName())
        self.setPortDefaultValue(kSceneItem, "path", kSceneItem.getPath())

        for parentName in ['layer', 'component']:
            getMethod = 'get%s' % parentName.capitalize()
            if not hasattr(kSceneItem, getMethod):
                continue
            parent = getattr(kSceneItem, getMethod)()
            if not parent:
                continue
            self.setPortDefaultValue(kSceneItem, parentName, parent.getName())

        if isinstance(kSceneItem, Control):
            if self.__dfgArguments.has_key('controls'):
                self.connectCanvasArg('controls', nodePath, 'xfoAnimation')
            if self.__dfgArguments.has_key('floats'):
                self.connectCanvasArg('floats', nodePath, 'floatAnimation')

        if self.getConfig().getMetaData('DebugDrawingSupport', False):
            if hasattr(kSceneItem, 'getCurveData'):
                curveData = kSceneItem.getCurveData()
                shapeHash = self.buildCanvasCurveShape(curveData)
                self.setPortDefaultValue(kSceneItem, "shapeHash", shapeHash)

        if self.getConfig().getMetaData('DebugDrawingSupport', False):
            # shapeNode = self.__dfgLastCurveNode
            # if shapeNode and not shapeNode.startswith('Cache'):
            #   preset = "Fabric.Core.Data.Cache"
            #   cacheNode = self.createCanvasNodeFromPreset(preset)
            #   self.connectCanvasNodes(shapeNode, 'this', cacheNode, 'value')
            #   self.__dfgLastCurveNode = cacheNode

            if not self.__dfgLastLinesNode:
                preset = "Fabric.Exts.Geometry.Lines.EmptyLines"
                linesNode = self.createCanvasNodeFromPreset(preset)
                self.__dfgLastLinesNode = (linesNode, 'lines')

            if cls in [
                'Control',
                'Joint'
            ]:
              (prevNode, prevPort) = self.__dfgLastLinesNode
              preset = "Kraken.DebugDrawing.DrawIntoLinesObject"
              if isinstance(kSceneItem, Control):
                preset = "Kraken.DebugDrawing.DrawIntoLinesObjectForControl"
              drawNode = self.createCanvasNodeFromPreset(preset)
              self.connectCanvasNodes(nodePath, 'result', drawNode, 'this')
              (xfoNode, xfoPort) = self.getSceneItemNodeAndPort(kSceneItem)
              self.connectCanvasNodes(xfoNode, xfoPort, drawNode, 'xfo')
              if isinstance(kSceneItem, Control):
                self.connectCanvasNodes(self.__dfgLastCurveNode, 'this', drawNode, 'shapes')
              self.connectCanvasNodes(prevNode, prevPort, drawNode, 'lines')
              self.__dfgLastLinesNode = (drawNode, 'lines')

        if hasattr(kSceneItem, 'getParent'):
            parent = kSceneItem.getParent()
            if not parent is None and self.hasSceneItemNode(parent):
                (parentNode, parentPort) = self.getSceneItemNodeAndPort(parent, asInput = False)
                (childNode, childPort) = self.getSceneItemNodeAndPort(kSceneItem, asInput = False)
                preset = "Fabric.Core.Math.Mul"
                transformNode = self.createCanvasNodeFromPreset(preset, comment = kSceneItem.getPath())
                self.connectCanvasNodes(parentNode, parentPort, transformNode, 'lhs')
                self.connectCanvasNodes(childNode, childPort, transformNode, 'rhs')
                self.setSceneItemTransformPort(kSceneItem, transformNode, 'result')

        if isinstance(kSceneItem, Rig):
            self.__dfgTopLevelGraph.setTitle(kSceneItem.getName())

        return True

    def buildCanvasNodeFromAttribute(self, kAttribute):
        cls = kAttribute.__class__.__name__
        if not cls in [
            'BoolAttribute',
            'ColorAttribute',
            'IntegerAttribute',
            'ScalarAttribute',
            'StringAttribute'
        ]:
            self.reportError("buildCanvasNodeFromAttribute: Unexpected class " + cls)
            return False

        path = kAttribute.getPath()
        preset = "Kraken.Attributes.Kraken%s" % cls
        nodePath = self.createCanvasNodeFromPreset(preset, comment = kAttribute.getPath())

        # only the types which support animation
        valueNode = None
        if isinstance(kAttribute, ScalarAttribute):
            preset = "Kraken.Attributes.Get%sValue" % cls[:-9]
            valueNode = self.createCanvasNodeFromPreset(preset, comment = kAttribute.getPath())
            self.connectCanvasNodes(nodePath, 'result', valueNode, 'this')

        self.__dfgNodes[path] = nodePath
        self._registerSceneItemPair(kAttribute, nodePath)
        self.__dfgAttributes[path] = (nodePath, valueNode)

        # set the defaults
        self.setPortDefaultValue(kAttribute, "name", kAttribute.getName())
        self.setPortDefaultValue(kAttribute, "path", kAttribute.getPath())
        self.setPortDefaultValue(kAttribute, "keyable", kAttribute.getKeyable())
        self.setPortDefaultValue(kAttribute, "animatable", kAttribute.getAnimatable())
        self.setPortDefaultValue(kAttribute, "value", kAttribute.getValue())
        for propName in ['min', 'max']:
            methodName = 'get' + propName.capitalize()
            if not hasattr(kAttribute, methodName):
                continue
            self.setPortDefaultValue(kAttribute, propName, getattr(kAttribute, methodName)())

        if isinstance(kAttribute.getParent().getParent(), Control):
            if isinstance(kAttribute, ScalarAttribute):
                if self.__dfgArguments.has_key('floats'):
                    self.connectCanvasArg('floats', nodePath, 'floatAnimation')

        return True

    def buildCanvasNodesFromConstraint(self, kConstraint):
        cls = kConstraint.__class__.__name__
        if not cls in [
            'OrientationConstraint',
            'PoseConstraint',
            'PositionConstraint',
            'ScaleConstraint'
        ]:
            self.reportError("buildCanvasNodesFromConstraint: Unexpected class " + cls)
            return False

        path = kConstraint.getPath()
        
        nodes = []
        preset = "Kraken.Constraints.Kraken%s" % cls
        constructNode = self.createCanvasNodeFromPreset(preset)
        lastNode = constructNode
        lastPort = "result"

        # todo: move this to use compute simple instead
        # we also need a compute offset simple

        constrainers = kConstraint.getConstrainers()
        for constrainer in constrainers:
            preset = "Kraken.Constraints.AddConstrainer"
            addNode = self.createCanvasNodeFromPreset(preset, comment = constrainer.getPath())

            self.connectCanvasNodes(lastNode, lastPort, addNode, 'this')

            (constrainerNode, constrainerPort) = self.getSceneItemNodeAndPort(constrainer, asInput = False)
            self.connectCanvasNodes(constrainerNode, constrainerPort, addNode, 'constrainer')

            lastNode = addNode
            lastPort = 'this'

        constrainee = kConstraint.getConstrainee()
        (constraineeNode, constraineePort) = self.getSceneItemNodeAndPort(constrainee, asInput = True)

        if kConstraint.getMaintainOffset():
            preset = "Kraken.Constraints.ComputeOffset"
            computeOffsetNode = self.createCanvasNodeFromPreset(preset, addToLayout = False)
            self.connectCanvasNodes(lastNode, lastPort, computeOffsetNode, 'this', addToLayout = False)
            self.connectCanvasNodes(constraineeNode, constraineePort, computeOffsetNode, 'constrainee', addToLayout = False)
            offset = self.getIntermediateValue(computeOffsetNode, 'result', prefix = str(cls)+": ")
            self.removeCanvasNode(computeOffsetNode)
            self.__dfgTopLevelGraph.setPortDefaultValue(constructNode+".offset", offset)

        preset = "Kraken.Constraints.Compute"
        computeNode = self.createCanvasNodeFromPreset(preset, comment = kConstraint.getConstrainee().getPath())
        self.connectCanvasNodes(lastNode, lastPort, computeNode, 'this')
        self.connectCanvasNodes(constraineeNode, constraineePort, computeNode, 'xfo')

        self.setSceneItemTransformPort(constrainee, computeNode, 'result')

        self._registerSceneItemPair(kConstraint, computeNode)

        return True

    def buildCanvasCurveShape(self, curveData):

        if self.__dfgCurves is None:
            preset = "Kraken.DebugDrawing.KrakenCurveDict"
            self.__dfgLastCurveNode = self.createCanvasNodeFromPreset(preset)
            self.__dfgCurves = {}

        numVertices = 0
        for subCurve in curveData:
            points = subCurve['points']
            numVertices = numVertices + len(points)

        hashSource = [curveData]
        hashSource += [len(curveData)]
        hashSource += [numVertices]

        shapeHash = str(self.makeHash(hashSource))
        if not self.__dfgCurves.has_key(shapeHash):
            positions = []
            indices = []
            for subCurve in curveData:
                points = subCurve['points']
                firstIndex = len(positions)
                index = firstIndex
                for i in range(len(points)):
                    positions.append(Vec3(points[i][0], points[i][1], points[i][2]))
                    if i > 0:
                        indices.append(index-1)
                        indices.append(index)
                    index = index + 1

                if subCurve.get('closed', False):
                    indices.append(index-1)
                    indices.append(firstIndex)

            shapeHashVal = ks.rtVal("String", shapeHash)
            positionsRTVal = ks.rtVal("Vec3[]")
            indicesRTVal = ks.rtVal("UInt32[]")
            positionsRTVal.resize(len(positions))
            indicesRTVal.resize(len(indices))

            for i in range(len(positions)):
                positionsRTVal[i] = ks.rtVal('Vec3', positions[i])
            for i in range(len(indices)):
                indicesRTVal[i] = ks.rtVal('UInt32', indices[i])

            preset = "Kraken.DebugDrawing.DefineCurve"
            curveNode = self.createCanvasNodeFromPreset(preset)

            self.__dfgTopLevelGraph.setPortDefaultValue(curveNode+'.shapeHash', shapeHashVal)
            self.__dfgTopLevelGraph.setPortDefaultValue(curveNode+'.positions', positionsRTVal)
            self.__dfgTopLevelGraph.setPortDefaultValue(curveNode+'.indices', indicesRTVal)

            # connec the new nodes with the first port
            subExec = self.__dfgTopLevelGraph.getSubExec(self.__dfgLastCurveNode)
            outPort = subExec.getExecPortName(0)
            subExec = self.__dfgTopLevelGraph.getSubExec(curveNode)
            inPort = subExec.getExecPortName(0)
            self.connectCanvasNodes(self.__dfgLastCurveNode, outPort, curveNode, inPort)

            self.__dfgCurves[shapeHash] = curveNode
            self.__dfgLastCurveNode = curveNode

        return shapeHash

    def collectResultPorts(self, arg, cls, dataType = 'Xfo'):

        drivers = []
        driversHit = {}
        pairs = self.getDCCSceneItemPairs()
        for pair in pairs:
            driver = pair['src']
            if driversHit.has_key(driver.getPath()):
              continue
            if not isinstance(driver, cls):
                continue
            drivers.append(driver)
            driversHit[driver.getPath()] = driver

        if len(drivers) == 0:
            return None          

        client = ks.getCoreClient()
        collectNode = self.createCanvasNodeFromFunction('collect'+arg.capitalize())
        subExec = self.__dfgTopLevelGraph.getSubExec(collectNode)

        resultPort = subExec.addExecPort('result', client.DFG.PortTypes.Out)
        subExec.setExecPortTypeSpec(resultPort, '%s[String]' % dataType)

        driverMap = {}
        code = []
        for driver in drivers:
            driverName = str(driver.getName())
            driverPort = subExec.addExecPort(driverName, client.DFG.PortTypes.In)
            driverMap[driver.getPath()] = driverPort

            (node, port) = self.getSceneItemNodeAndPort(driver, asInput = True)
            resolvedType = self.__dfgTopLevelGraph.getNodePortResolvedType(node+'.'+port)
            if resolvedType:
                subExec.setExecPortTypeSpec(driverPort, resolvedType)

            code += ['  %s["%s"] = %s;' % (resultPort, driver.getPath(), driverPort)]

        subExec.setCode('dfgEntry {\n%s}\n' % '\n'.join(code))

        for driver in drivers:
            (node, port) = self.getSceneItemNodeAndPort(driver, asInput = True)
            self.connectCanvasNodes(node, port, collectNode, driverMap[driver.getPath()])

        self.connectCanvasArg(collectNode, 'result', arg, argIsInput = False)

    # ========================
    # Object3D Build Methods
    # ========================
    def buildContainer(self, kSceneItem, buildName):
        """Builds a container / namespace object.

        Args:
            kSceneItem (Object): kSceneItem that represents a container to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None


    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Args:
            kSceneItem (Object): kSceneItem that represents a layer to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None


    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Args:
            kSceneItem (Object): kSceneItem that represents a group to be built.
            buildName (str): The name to use on the built object.

        Return:
            object: DCC Scene Item that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None


    def buildGroup(self, kSceneItem, buildName):
        """Builds a group object.

        Args:
            kSceneItem (Object): kSceneItem that represents a group to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None

    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Args:
            kSceneItem (Object): kSceneItem that represents a joint to be built.
            buildName (str): The name to use on the built object.

        Return:
            object: DCC Scene Item that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None

    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Args:
            kSceneItem (Object): locator / null object to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None

    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Args:
            kSceneItem (Object): kSceneItem that represents a curve to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None

    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Args:
            kSceneItem (Object): kSceneItem that represents a control to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """
        if self.buildCanvasNodeFromSceneItem(kSceneItem, buildName):
            return kSceneItem
        return None

    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kAttribute):
        """Builds a Bool attribute.

        Args:
            kAttribute (Object): kAttribute that represents a boolean attribute to be built.

        Return:
            bool: True if successful.

        """

        if kAttribute.getName() in ['visibility', 'shapeVisibility']:
            return True

        result = self.buildCanvasNodeFromAttribute(kAttribute)

        if self.getConfig().getMetaData('DebugDrawingSupport', False):
            if kAttribute.getName().lower().find('debug') > -1:
                (node, port) = self.getAttributeNodeAndPort(kAttribute, asInput = True)
                self.connectCanvasArg('debugDraw', node, port)

        return result

    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (Object): kAttribute that represents a float attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildCanvasNodeFromAttribute(kAttribute)

    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (Object): kAttribute that represents a integer attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildCanvasNodeFromAttribute(kAttribute)

    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (Object): kAttribute that represents a string attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildCanvasNodeFromAttribute(kAttribute)

    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Args:
            kAttributeGroup (object): Kraken object to build the attribute group on.

        Return:
            bool: True if successful.

        """
        for i in xrange(kAttributeGroup.getNumAttributes()):
            kAttribute = kAttributeGroup.getAttributeByIndex(i)

            if kAttribute.isTypeOf("BoolAttribute"):
                self.buildBoolAttribute(kAttribute)

            elif kAttribute.isTypeOf("ScalarAttribute"):
                self.buildScalarAttribute(kAttribute)

            elif kAttribute.isTypeOf("IntegerAttribute"):
                self.buildIntegerAttribute(kAttribute)

            elif kAttribute.isTypeOf("StringAttribute"):
                self.buildStringAttribute(kAttribute)

            else:
                raise NotImplementedError(kAttribute.getName() + ' has an unsupported type: ' + str(type(kAttribute)))

        return True

    def connectAttribute(self, kAttribute):
        """Connects the driver attribute to this one.

        Args:
            kAttribute (Object): Attribute to connect.

        Return:
            bool: True if successful.

        """
        if not kAttribute.isConnected():
            return True

        connection = kAttribute.getConnection()

        (nodeA, portA) = self.getAttributeNodeAndPort(connection, asInput = False)
        (nodeB, portB) = self.getAttributeNodeAndPort(kAttribute, asInput = True)
        if nodeA is None or nodeB is None:
            return False

        self.connectCanvasNodes(nodeA, portA, nodeB, portB)
        return True


    # =========================
    # Constraint Build Methods
    # =========================
    def buildOrientationConstraint(self, kConstraint):
        """Builds an orientation constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildCanvasNodesFromConstraint(kConstraint)

    def buildPoseConstraint(self, kConstraint):
        """Builds an pose constraint represented by the kConstraint.

        Args:
            kConstraint (Object): kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildCanvasNodesFromConstraint(kConstraint)

    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildCanvasNodesFromConstraint(kConstraint)

    def buildScaleConstraint(self, kConstraint):
        """Builds an scale constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildCanvasNodesFromConstraint(kConstraint)

    # ========================
    # Component Build Methods
    # ========================
    def buildAttributeConnection(self, connectionInput):
        """Builds the connection between the attribute and the connection.

        Args:
            connectionInput (Object): Kraken connection to build.

        Return:
            bool: True if successful.

        """
        # todo
        self.reportError("buildAttributeConnection not yet implemented.")
        return False

    # =========================
    # Operator Builder Methods
    # =========================
    def buildKLOperator(self, kOperator):
        """Builds Splice Operators on the components.

        Args:
            kOperator (Object): Kraken operator that represents a Splice operator.

        Return:
            bool: True if successful.

        """

        # create the node
        solverTypeName = kOperator.getSolverTypeName()
        path = kOperator.getPath()

        client = ks.getCoreClient()

        constructNode = self.createCanvasNodeFromFunction(solverTypeName)
        subExec = self.__dfgTopLevelGraph.getSubExec(constructNode)
        solverPort = subExec.addExecPort("solver", client.DFG.PortTypes.Out)
        subExec.setExecPortTypeSpec(solverPort, solverTypeName)
        subExec.setCode('dfgEntry { solver = %s(); }' % solverTypeName)

        varNode = self.__dfgTopLevelGraph.addVar('solver', solverTypeName, kOperator.getExtension())
        self.connectCanvasNodes(constructNode, 'solver', varNode, "value")

        node = self.createCanvasNodeFromFunction(solverTypeName)
        self.__dfgNodes[path] = node
        self._registerSceneItemPair(kOperator, node)

        # set dependencies
        self.__dfgTopLevelGraph.addExtDep(kOperator.getExtension())
        subExec = self.__dfgTopLevelGraph.getSubExec(node)

        solverPort = subExec.addExecPort("solver", client.DFG.PortTypes.IO)
        subExec.setExecPortTypeSpec(solverPort, solverTypeName)
        self.connectCanvasNodes(varNode, 'value', node, solverPort)

        argPorts = {}
        arraySizes = {}
        
        args = kOperator.getSolverArgs()
        for i in xrange(len(args)):
            arg = args[i]
            argName = arg.name.getSimpleType()
            argDataType = arg.dataType.getSimpleType()
            argConnectionType = arg.connectionType.getSimpleType()

            argPort = None
            if argConnectionType == 'In':
                argPort = subExec.addExecPort(argName, client.DFG.PortTypes.In)
            else:
                argPort = subExec.addExecPort(argName, client.DFG.PortTypes.Out)
            argPorts[argName] = argPort
            subExec.setExecPortTypeSpec(argPort, argDataType)

            if argDataType == 'EvalContext':
                continue
            if argName == 'time' and argConnectionType == 'In':
                self.connectCanvasArg("time", node, argPort)
                continue
            if argName == 'frame'and argConnectionType == 'In':
                self.connectCanvasArg("frame", node, argPort)
                continue

            # Get the argument's input from the DCC
            if argConnectionType == 'In':
                connectedObjects = kOperator.getInput(argName)
            elif argConnectionType in ['IO', 'Out']:
                connectedObjects = kOperator.getOutput(argName)

            self.connectCanvasOperatorPort(node, argPort, argDataType, argConnectionType, connectedObjects, arraySizes)

        opSourceCode = kOperator.generateSourceCode(arraySizes=arraySizes)

        funcExec = self.__dfgTopLevelGraph.getSubExec(node)
        funcExec.setCode(opSourceCode)

        return False


    def buildCanvasOperator(self, kOperator):
        """Builds Canvas Operators on the components.

        Args:
            kOperator (Object): Kraken operator that represents a Canvas operator.

        Return:
            bool: True if successful.

        """
        node = self.createCanvasNodeFromPreset(kOperator.getPresetPath())
        self.__dfgNodes[kOperator.getPath()] = node
        self._registerSceneItemPair(kOperator, node)
        subExec = self.__dfgTopLevelGraph.getSubExec(node)

        portTypeMap = {
            0: 'In',
            1: 'IO',
            2: 'Out'
        }

        arraySizes = {}

        for i in xrange(subExec.getExecPortCount()):
            portName = subExec.getExecPortName(i)
            portConnectionType = portTypeMap[subExec.getExecPortType(i)]
            portDataType = self.__dfgTopLevelGraph.getNodePortResolvedType(node+'.'+portName)

            if portDataType == 'EvalContext':
                continue
            if portName == 'time' and portConnectionType == 'In':
                self.connectCanvasArg("time", node, portName)
                continue
            if portName == 'frame'and portConnectionType == 'In':
                self.connectCanvasArg("frame", node, portName)
                continue

            # Get the port's input from the DCC
            if portConnectionType == 'In':
                connectedObjects = kOperator.getInput(portName)
            else:
                connectedObjects = kOperator.getOutput(portName)

            self.connectCanvasOperatorPort(node, portName, portDataType, portConnectionType, connectedObjects, arraySizes)


        return True

    # ==================
    # Parameter Methods
    # ==================
    def lockParameters(self, kSceneItem):
        """Locks flagged SRT parameters.

        Args:
            kSceneItem (Object): Kraken object to lock the SRT parameters on.

        Return:
            bool: True if successful.

        """
        return True

    # ===================
    # Visibility Methods
    # ===================
    def setVisibility(self, kSceneItem):
        """Sets the visibility of the object after its been created.

        Args:
            kSceneItem (Object): The scene item to set the visibility on.

        Return:
            bool: True if successful.

        """
        if not self.hasSceneItemNode(kSceneItem):
            return True

        self.setPortDefaultValue(kSceneItem, "visibility", kSceneItem.getVisibility())
        return True

    # ================
    # Display Methods
    # ================
    def setObjectColor(self, kSceneItem):
        """Sets the color on the dccSceneItem.

        Args:
            kSceneItem (Object): kraken object to set the color on.

        Return:
            bool: True if successful.

        """
        if not self.hasSceneItemNode(kSceneItem):
            return True

        self.setPortDefaultValue(kSceneItem, "color", kSceneItem.getColor())
        return True

    # ==================
    # Transform Methods
    # ==================
    def setTransform(self, kSceneItem):
        """Translates the transform to Maya transform.

        Args:
            kSceneItem -- Object: object to set the transform on.

        Return:
            bool: True if successful.

        """

        if not self.hasSceneItemNode(kSceneItem):
            return True

        (node, port) = self.getSceneItemNodeAndPort(kSceneItem, asInput = True)
        if node != self.__dfgNodes[kSceneItem.getPath()]:
            self.setPortDefaultValue(kSceneItem, "xfo", Xfo())
            parentXfo = Xfo(self.getIntermediateValue(node, port, kSceneItem.getPath()))
            invXfo = parentXfo.inverse()
            localXfo = invXfo.multiply(kSceneItem.xfo)
            self.setPortDefaultValue(kSceneItem, "xfo", localXfo)
            return True
  
        self.setPortDefaultValue(kSceneItem, "xfo", kSceneItem.xfo)
        return True

    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Pre-Build commands.

        Args:
            kSceneItem (Object): Kraken kSceneItem object to build.

        Return:
            bool: True if successful.

        """
        try:
            client = ks.getCoreClient()
            ks.loadExtension('KrakenForCanvas')

            host = client.getDFGHost()

            self.__dfgBinding = host.createBindingToNewGraph()
            self.__dfgArguments = {}
            self.__dfgTopLevelGraph = self.__dfgBinding.getExec()
            self.__dfgNodes = {}
            self.__dfgConstructors = {}
            self.__dfgAttributes = {}
            self.__dfgConstraints = {}
            self.__dfgComponentPortMap = {}
            self.__dfgTransforms = {}
            self.__dfgConnections = {}
            self.__dfgLastLinesNode = None
            self.__layoutG = SpringLayout()

            self.createTopLevelArguments()

        except BaseException as e:
            self.reportError(e)

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
            bool: True if successful.

        """
        if self.__dfgArguments.has_key('all'):
            self.collectResultPorts('all', Object3D, 'Xfo')
        if self.__dfgArguments.has_key('joints'):
            self.collectResultPorts('joints', Joint, 'Xfo')

        if self.getConfig().getMetaData('DebugDrawingSupport', False):
            client = ks.getCoreClient()
            self.__dfgArguments['handle'] = self.__dfgTopLevelGraph.addExecPort("handle", client.DFG.PortTypes.Out)

            # draw the lines
            if self.__dfgLastLinesNode:
                preset = "Fabric.Exts.InlineDrawing.DrawingHandle.EmptyDrawingHandle"
                handleNode = self.createCanvasNodeFromPreset(preset)
                preset = "Fabric.Exts.InlineDrawing.DrawingHandle.DrawColoredLines"
                drawNode = self.createCanvasNodeFromPreset(preset)
                preset = "Fabric.Core.Control.If"
                ifNode = self.createCanvasNodeFromPreset(preset)
                self.connectCanvasNodes(handleNode, 'handle', drawNode, "this")
                self.connectCanvasNodes(ifNode, 'result', drawNode, "lines")
                self.connectCanvasArg(drawNode, "this", 'handle', argIsInput = False)
                (linesNode, linesPort) = self.__dfgLastLinesNode
                self.connectCanvasNodes(linesNode, linesPort, ifNode, "if_true")
                self.connectCanvasArg('debugDraw', ifNode, 'cond')

        if not self.__layoutG is None:
            layout = self.__layoutG.compute()
            for key in layout:
                pos = layout[key]
                posStr = '{"x": %f, "y": %f}' % (pos[0], pos[1])
                self.__dfgTopLevelGraph.setNodeMetadata(key, "uiGraphPos", posStr)

        if self.__outputFilePath:
            content = self.__dfgBinding.exportJSON()
            try:
                open(self.__outputFilePath, "w").write(content)
                self.report("Saved %s canvas file." % self.__outputFilePath)
            except IOError as e:
                self.report(e)

        return True
