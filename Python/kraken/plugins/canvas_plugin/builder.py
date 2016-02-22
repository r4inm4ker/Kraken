"""Kraken Canvas - Canvas Builder module.

Classes:
Builder -- Component representation.

"""

import json

from kraken.core.kraken_system import ks
from kraken.core.builder import Builder
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.control import Control
from kraken.core.objects.joint import Joint
from kraken.core.objects.rig import Rig
from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.objects.operators.operator import Operator
from kraken.core.objects.constraints.constraint import Constraint
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.color import Color
from kraken.core.maths.xfo import Xfo

from kraken.plugins.canvas_plugin.hash import makeHash
from kraken.plugins.canvas_plugin.graph_manager import GraphManager

import FabricEngine.Core as core

class Builder(Builder):
    """Builder object for building Kraken objects in Canvas."""

    __outputFilePath = None
    __graph = None
    __dfgCurves = None
    __dfgLastCurveNode = None
    __dfgLastLinesNode = None

    def __init__(self):
        super(Builder, self).__init__()

    def report(self, message):
        print "Canvas Builder: %s" % str(message)

    def reportError(self, error):
        self.report("Error: "+str(error))

    def hasOption(self, option):
        return self.getConfig().getMetaData(option, False)

    @property
    def graph(self):
        return self.__graph

    # ========================
    # IO Methods
    # ========================
    def setOutputFilePath(self, filePath):
        self.__outputFilePath = filePath

    # ========================
    # Canvas related Methods
    # ========================

    def setTransformPortSI(self, kSceneItem, node, port):
        prevNode = None
        prevPort = None
        prevNodeAndPort = self.graph.getNodeAndPortSI(kSceneItem, asInput=False)
        if prevNodeAndPort:
            (prevNode, prevPort) = prevNodeAndPort

        self.graph.setNodeAndPortSI(kSceneItem, node, port, asInput=False)
        self.graph.setNodeMetaData(node, 'uiComment', kSceneItem.getPath())

        if prevNode:
          self.graph.replaceConnections(prevNode, prevPort, node, port)

    def connectCanvasOperatorPort(self, kSceneItem, node, port, dataType, portType, connectedObjects, arraySizes):
        if dataType.endswith('[]'):

            if portType == 'In':

                pushNodes = []
                for i in range(len(connectedObjects)):
                    title = 'Push_%d' % i
                    c = connectedObjects[i]
                    pushNode = self.graph.createNodeFromPresetSI(kSceneItem, "Fabric.Core.Array.Push", title=title)
                    if len(pushNodes) > 0:
                        self.graph.connectNodes(pushNodes[-1], "array", pushNode, "array")
                    pushNodes.append(pushNode)

                self.graph.connectNodes(pushNode, 'array', node, port)

                for i in range(len(connectedObjects)):
                    c = connectedObjects[i]
                    (connNode, connPort) = self.graph.getNodeAndPortSI(c, asInput=False)
                    self.graph.connectNodes(connNode, connPort, pushNodes[i], 'element')

            else:

                arraySizes[port] = len(connectedObjects)
                for i in range(len(connectedObjects)):
                    title = 'Get_%d' % i
                    c = connectedObjects[i]
                    getNode = self.graph.createNodeFromPresetSI(kSceneItem, "Fabric.Core.Array.Get", title=title)
                    self.graph.connectNodes(node, port, getNode, 'array')
                    self.graph.setPortDefaultValue(getNode, 'index', i)

                    if isinstance(c, Attribute):
                      (connNode, connPort) = self.graph.getNodeAndPortSI(c, asInput=True)
                      self.graph.connectNodes(getNode, 'element', connNode, connPort)
                    else:
                      self.setTransformPortSI(c, getNode, 'element')

        else:

            if portType == 'In':
                (connNode, connPort) = self.graph.getNodeAndPortSI(connectedObjects, asInput=False)
                self.graph.connectNodes(connNode, connPort, node, port)
            elif isinstance(connectedObjects, Attribute):
                (connNode, connPort) = self.graph.getNodeAndPortSI(connectedObjects, asInput=True)
                self.graph.connectNodes(node, port, connNode, connPort)
            else:
                self.setTransformPortSI(connectedObjects, node, port)

    def setCurrentGroupSI(self, kSceneItem):

        # todo:
        # expose all of the attributes below the created ComponentInput
        # expose all of the attributes below the created ComponentOutput
        groupName = None
        if isinstance(kSceneItem, ComponentGroup):
            groupName = kSceneItem.getName()
            # groupName = kSceneItem.getPath()
        elif isinstance(kSceneItem, Constraint):
            groupName = self.setCurrentGroupSI(kSceneItem.getConstrainee())
            if groupName:
                return groupName
        elif isinstance(kSceneItem, Operator):
            outputs = kSceneItem.getOutputNames()
            for outputName in outputs:
                connectedObjects = kSceneItem.getOutput(outputName)
                if not isinstance(connectedObjects, list):
                    connectedObjects = [connectedObjects]

                for c in connectedObjects:
                    groupName = self.setCurrentGroupSI(c)
                    if groupName:
                        return groupName
        else:
            parent = kSceneItem.getParent()
            if parent is None:
                self.__dfgCurrentComponent = None
                return None
            else:
                return self.setCurrentGroupSI(parent)

        return self.graph.setCurrentGroup(groupName)

    def buildNodeSI(self, kSceneItem, buildName):

        if isinstance(kSceneItem, Rig):
            self.graph.setTitle(kSceneItem.getName())

        cls = kSceneItem.__class__.__name__

        if cls in [
            'Layer',
            'Rig'
        ]:
            return True

        cls = kSceneItem.__class__.__name__
        if cls in [
            'ComponentInput',
            'ComponentOutput'
        ]:
            cls = 'Transform'

        if not cls in [
            'ComponentGroup',
            'Container',
            'CtrlSpace',
            'Curve',
            'Control',
            'HierarchyGroup',
            'Joint',
            'Locator',
            'Transform',
            'Layer',
            'Rig'
        ]:
            self.reportError("buildNodeSI: Unexpected class " + cls)
            return False

        self.report('Item '+kSceneItem.getPath())
        self.setCurrentGroupSI(kSceneItem)

        path = kSceneItem.getPath()
        preset = "Kraken.Constructors.Kraken%s" % cls
        node = self.graph.createNodeFromPresetSI(kSceneItem, preset, title='constructor')
        self._registerSceneItemPair(kSceneItem, node)

        # only the types which support animation
        if isinstance(kSceneItem, Control):
            preset = "Kraken.Constructors.GetXfo"
            xfoNode = self.graph.createNodeFromPresetSI(kSceneItem, preset, title='getXfo')
            self.graph.connectNodes(node, 'result', xfoNode, 'this')
            self.setTransformPortSI(kSceneItem, xfoNode, 'result')
        else:
            self.setTransformPortSI(kSceneItem, node, 'xfo')

        # set the defaults
        self.graph.setPortDefaultValue(node, "name", kSceneItem.getName())
        self.graph.setPortDefaultValue(node, "buildName", kSceneItem.getBuildName())
        self.graph.setPortDefaultValue(node, "path", kSceneItem.getPath())

        for parentName in ['layer', 'component']:
            getMethod = 'get%s' % parentName.capitalize()
            if not hasattr(kSceneItem, getMethod):
                continue
            parent = getattr(kSceneItem, getMethod)()
            if not parent:
                continue
            self.graph.setPortDefaultValue(node, parentName, parent.getName())

        if isinstance(kSceneItem, Control):
            if self.graph.hasArgument('controls'):
                self.graph.connectArg('controls', node, 'xfoAnimation')
            if self.graph.hasArgument('floats'):
                self.graph.connectArg('floats', node, 'floatAnimation')

        if self.hasOption('SetupDebugDrawing'):
            if hasattr(kSceneItem, 'getCurveData'):
                curveData = kSceneItem.getCurveData()
                self.graph.setCurrentGroup('DebugCurves')
                shapeHash = self.buildCanvasCurveShape(curveData)
                self.setCurrentGroupSI(kSceneItem)
                self.graph.setPortDefaultValue(node, "shapeHash", shapeHash)

        if self.hasOption('SetupDebugDrawing'):
            # shapeNode = self.__dfgLastCurveNode
            # if shapeNode and not shapeNode.startswith('Cache'):
            #   preset = "Fabric.Core.Data.Cache"
            #   cacheNode = self.graph.createNodeFromPreset(preset)
            #   self.graph.connectNodes(shapeNode, 'this', cacheNode, 'value')
            #   self.__dfgLastCurveNode = cacheNode

            if not self.__dfgLastLinesNode:
                self.graph.setCurrentGroup('DebugCurves')
                preset = "Fabric.Exts.Geometry.Lines.EmptyLines"
                linesNode = self.graph.createNodeFromPreset('DebugLines', preset, title='constructor')
                self.__dfgLastLinesNode = (linesNode, 'lines')
                self.setCurrentGroupSI(kSceneItem)

            if cls in [
                'Control'
                #,'Joint'
            ]:
              (prevNode, prevPort) = self.__dfgLastLinesNode
              preset = "Kraken.DebugDrawing.DrawIntoLinesObject"
              if isinstance(kSceneItem, Control):
                preset = "Kraken.DebugDrawing.DrawIntoLinesObjectForControl"
              drawNode = self.graph.createNodeFromPresetSI(kSceneItem, preset, title='drawIntoLines')
              self.graph.connectNodes(node, 'result', drawNode, 'this')
              (xfoNode, xfoPort) = self.graph.getNodeAndPortSI(kSceneItem, asInput=False)
              self.graph.connectNodes(xfoNode, xfoPort, drawNode, 'xfo')
              if isinstance(kSceneItem, Control):
                self.graph.connectNodes(self.__dfgLastCurveNode, 'this', drawNode, 'shapes')
              self.graph.connectNodes(prevNode, prevPort, drawNode, 'lines')
              self.__dfgLastLinesNode = (drawNode, 'lines')

        if hasattr(kSceneItem, 'getParent'):
            parent = kSceneItem.getParent()
            if not parent is None:
                parentNodeAndPort = self.graph.getNodeAndPortSI(parent, asInput=False)
                if parentNodeAndPort:
                    (parentNode, parentPort) = parentNodeAndPort
                    (childNode, childPort) = self.graph.getNodeAndPortSI(kSceneItem, asInput=False)
                    preset = "Fabric.Core.Math.Mul"
                    title = kSceneItem.getPath()+' x '+parent.getPath()
                    transformNode = self.graph.createNodeFromPresetSI(kSceneItem, preset, title=title)
                    self.graph.connectNodes(parentNode, parentPort, transformNode, 'lhs')
                    self.graph.connectNodes(childNode, childPort, transformNode, 'rhs')
                    self.setTransformPortSI(kSceneItem, transformNode, 'result')

        return True

    def buildNodeAttribute(self, kAttribute):
        cls = kAttribute.__class__.__name__
        if not cls in [
            'BoolAttribute',
            'ColorAttribute',
            'IntegerAttribute',
            'ScalarAttribute',
            'StringAttribute'
        ]:
            self.reportError("buildNodeAttribute: Unexpected class " + cls)
            return False

        self.setCurrentGroupSI(kAttribute)

        path = kAttribute.getPath()
        preset = "Kraken.Attributes.Kraken%s" % cls
        node = self.graph.createNodeFromPresetSI(kAttribute, preset, title='constructor')
        self.graph.setNodeAndPortSI(kAttribute, node, 'value')

        # only the types which support animation
        valueNode = None
        if isinstance(kAttribute.getParent().getParent(), Control):
            if isinstance(kAttribute, ScalarAttribute):
                if self.graph.hasArgument('floats'):
                    self.graph.connectArg('floats', node, 'floatAnimation')
                preset = "Kraken.Attributes.Get%sValue" % cls[:-9]
                valueNode = self.graph.createNodeFromPresetSI(kAttribute, preset, title="getValue")
                self.graph.connectNodes(node, 'result', valueNode, 'this')
                self.graph.setNodeAndPortSI(kAttribute, valueNode, 'result', asInput=False)

        self._registerSceneItemPair(kAttribute, node)

        # set the defaults
        self.graph.setPortDefaultValue(node, "name", kAttribute.getName())
        self.graph.setPortDefaultValue(node, "path", kAttribute.getPath())
        self.graph.setPortDefaultValue(node, "keyable", kAttribute.getKeyable())
        self.graph.setPortDefaultValue(node, "animatable", kAttribute.getAnimatable())
        self.graph.setPortDefaultValue(node, "value", kAttribute.getValue())
        for propName in ['min', 'max']:
            methodName = 'get' + propName.capitalize()
            if not hasattr(kAttribute, methodName):
                continue
            self.graph.setPortDefaultValue(node, propName, getattr(kAttribute, methodName)())

        return True

    def buildNodesFromConstraint(self, kConstraint):
        return False # todo

        cls = kConstraint.__class__.__name__
        if not cls in [
            'OrientationConstraint',
            'PoseConstraint',
            'PositionConstraint',
            'ScaleConstraint'
        ]:
            self.reportError("buildNodesFromConstraint: Unexpected class " + cls)
            return False

        self.report('Constraint '+kConstraint.getPath())
        self.setCurrentGroupSI(kConstraint)

        path = kConstraint.getPath()
        
        nodes = []

        constrainers = kConstraint.getConstrainers()
        constrainee = kConstraint.getConstrainee()
        (constraineeNode, constraineePort) = self.graph.getNodeAndPortSI(constrainee, asInput=False)

        computeNode = None

        if len(constrainers) == 1:

            (constrainerNode, constrainerPort) = self.graph.getNodeAndPortSI(constrainers[0], asInput=False)

            preset = "Kraken.Constraints.ComputeKraken%s" % cls
            computeNode = self.graph.createNodeFromPresetSI(kConstraint, preset, title='compute')
            self.graph.connectNodes(constrainerNode, constrainerPort, computeNode, 'constrainer')
            self.graph.connectNodes(constraineeNode, constraineePort, computeNode, 'constrainee')

            if kConstraint.getMaintainOffset():
                preset = "Kraken.Constraints.Kraken%s" % cls
                constructNode = self.graph.createNodeFromPresetSI(kConstraint, preset, title='constructor')
                preset = "Kraken.Constraints.ComputeOffsetSimple"
                computeOffsetNode = self.graph.createNodeFromPresetSI(kConstraint, preset, title='computeOffset')
                self.graph.connectNodes(constructNode, 'result', computeOffsetNode, 'this')
                self.graph.connectNodes(constrainerNode, constrainerPort, computeOffsetNode, 'constrainer')
                self.graph.connectNodes(constraineeNode, constraineePort, computeOffsetNode, 'constrainee')
                offset = Xfo(self.graph.computeCurrentPortValue(computeOffsetNode, 'result'))
                self.graph.removeNodeSI(kConstraint, title='computeOffset')
                self.graph.removeNodeSI(kConstraint, title='constructor')
                self.graph.setPortDefaultValue(computeNode, "offset", offset)

        else:

            preset = "Kraken.Constraints.Kraken%s" % cls
            constructNode = self.graph.createNodeFromPresetSI(kConstraint, preset, title='constructor')
            lastNode = constructNode
            lastPort = "result"

            for constrainer in constrainers:
                preset = "Kraken.Constraints.AddConstrainer"
                title = 'addConstrainer_' + constrainer.getPath()
                addNode = self.graph.createNodeFromPresetSI(kConstraint, preset, title=title)

                self.graph.connectNodes(lastNode, lastPort, addNode, 'this')

                (constrainerNode, constrainerPort) = self.graph.getNodeAndPortSI(constrainer, asInput=False)
                self.graph.connectNodes(constrainerNode, constrainerPort, addNode, 'constrainer')

                lastNode = addNode
                lastPort = 'this'

            preset = "Kraken.Constraints.Compute"
            computeNode = self.graph.createNodeFromPresetSI(kConstraint, preset, title='compute')
            self.graph.connectNodes(lastNode, lastPort, computeNode, 'this')
            self.graph.connectNodes(constraineeNode, constraineePort, computeNode, 'xfo')

            if kConstraint.getMaintainOffset():
                preset = "Kraken.Constraints.ComputeOffset"
                computeOffsetNode = self.graph.createNodeFromPresetSI(kConstraint, preset, title='computeOffset')
                self.graph.connectNodes(lastNode, lastPort, computeOffsetNode, 'this')
                self.graph.connectNodes(constraineeNode, constraineePort, computeOffsetNode, 'constrainee')
                offset = self.graph.computeCurrentPortValue(computeOffsetNode, 'result')
                self.graph.removeNodeSI(kConstraint, title='computeOffset')
                self.graph.setPortDefaultValue(constructNode, "offset", offset)

        self.setTransformPortSI(constrainee, computeNode, 'result')

        self._registerSceneItemPair(kConstraint, computeNode)

        return True

    def buildCanvasCurveShape(self, curveData):

        if self.__dfgCurves is None:
            preset = "Kraken.DebugDrawing.KrakenCurveDict"
            self.__dfgLastCurveNode = self.graph.createNodeFromPreset('drawing', preset, title='curveDict')
            self.__dfgCurves = {}

        numVertices = 0
        for subCurve in curveData:
            points = subCurve['points']
            numVertices = numVertices + len(points)

        hashSource = [curveData]
        hashSource += [len(curveData)]
        hashSource += [numVertices]

        shapeHash = str(makeHash(hashSource))
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
            curveNode = self.graph.createNodeFromPreset('drawing', preset, title=shapeHash)

            self.graph.setPortDefaultValue(curveNode, 'shapeHash', shapeHashVal)
            self.graph.setPortDefaultValue(curveNode, 'positions', positionsRTVal)
            self.graph.setPortDefaultValue(curveNode, 'indices', indicesRTVal)

            # connec the new nodes with the first port
            subExec = self.graph.getSubExec(self.__dfgLastCurveNode)
            outPort = subExec.getExecPortName(0)
            subExec = self.graph.getSubExec(curveNode)
            inPort = subExec.getExecPortName(0)
            self.graph.connectNodes(self.__dfgLastCurveNode, outPort, curveNode, inPort)

            self.graph.replaceConnections(self.__dfgLastCurveNode, outPort, curveNode, 'this')

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
        collectNode = self.graph.createFunctionNode('collectors', title='collect'+arg.capitalize())
        subExec = self.graph.getSubExec(collectNode)

        resultPort = subExec.addExecPort('result', client.DFG.PortTypes.Out)
        subExec.setExecPortTypeSpec(resultPort, '%s[String]' % dataType)

        driverMap = {}
        code = []
        for driver in drivers:
            driverName = str(driver.getName())
            driverPort = subExec.addExecPort(driverName, client.DFG.PortTypes.In)
            driverMap[driver.getPath()] = driverPort

            (node, port) = self.graph.getNodeAndPortSI(driver, asInput=False)
            resolvedType = self.graph.getNodePortResolvedType(node, port)
            if resolvedType:
                subExec.setExecPortTypeSpec(driverPort, resolvedType)

            code += ['  %s["%s"] = %s;' % (resultPort, driver.getPath(), driverPort)]

        subExec.setCode('dfgEntry {\n%s}\n' % '\n'.join(code))

        for driver in drivers:
            (node, port) = self.graph.getNodeAndPortSI(driver, asInput=False)
            self.graph.connectNodes(node, port, collectNode, driverMap[driver.getPath()])

        self.graph.connectArg(collectNode, 'result', arg)

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
        if self.buildNodeSI(kSceneItem, buildName):
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
        if self.buildNodeSI(kSceneItem, buildName):
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
        if self.buildNodeSI(kSceneItem, buildName):
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
        if self.buildNodeSI(kSceneItem, buildName):
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
        if self.buildNodeSI(kSceneItem, buildName):
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
        if self.buildNodeSI(kSceneItem, buildName):
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
        if self.buildNodeSI(kSceneItem, buildName):
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
        if self.buildNodeSI(kSceneItem, buildName):
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

        result = self.buildNodeAttribute(kAttribute)

        if self.hasOption('SetupDebugDrawing'):
            if kAttribute.getName().lower().find('debug') > -1:
                (node, port) = self.graph.getNodeAndPortSI(kAttribute, asInput=True)
                self.graph.connectArg('debugDraw', node, port)

        return result

    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (Object): kAttribute that represents a float attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildNodeAttribute(kAttribute)

    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (Object): kAttribute that represents a integer attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildNodeAttribute(kAttribute)

    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (Object): kAttribute that represents a string attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildNodeAttribute(kAttribute)

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

        (nodeA, portA) = self.graph.getNodeAndPortSI(connection, asInput=False)
        (nodeB, portB) = self.graph.getNodeAndPortSI(kAttribute, asInput=True)
        if nodeA is None or nodeB is None:
            return False

        self.graph.connectNodes(nodeA, portA, nodeB, portB)
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
        return self.buildNodesFromConstraint(kConstraint)

    def buildPoseConstraint(self, kConstraint):
        """Builds an pose constraint represented by the kConstraint.

        Args:
            kConstraint (Object): kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildNodesFromConstraint(kConstraint)

    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildNodesFromConstraint(kConstraint)

    def buildScaleConstraint(self, kConstraint):
        """Builds an scale constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildNodesFromConstraint(kConstraint)

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
        if not connectionInput.isConnected():
            return True

        connection = connectionInput.getConnection()
        connectionTarget = connection.getTarget()
        inputTarget = connectionInput.getTarget()

        if connection.getDataType().endswith('[]'):
            connectionTarget = connection.getTarget()[connectionInput.getIndex()]
        else:
            connectionTarget = connection.getTarget()

        (nodeA, portA) = self.graph.getNodeAndPortSI(inputTarget, asInput=False)
        (nodeB, portB) = self.graph.getNodeAndPortSI(connectionTarget, asInput=True)
        if nodeA is None or nodeB is None:
            return False

        self.graph.connectNodes(nodeA, portA, nodeB, portB)
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
        self.report('KLOp '+kOperator.getPath())
        self.setCurrentGroupSI(kOperator)

        solverTypeName = kOperator.getSolverTypeName()
        path = kOperator.getPath()

        client = ks.getCoreClient()

        constructNode = self.graph.createFunctionNodeSI(kOperator, solverTypeName+'Constructor')
        subExec = self.graph.getSubExec(constructNode)
        solverPort = subExec.addExecPort("solver", client.DFG.PortTypes.Out)
        subExec.setExecPortTypeSpec(solverPort, solverTypeName)
        subExec.setCode('dfgEntry { solver = %s(); }' % solverTypeName)

        varNode = self.graph.createVariableNodeSI(kOperator, 'solver', solverTypeName, extension=kOperator.getExtension())
        self.graph.connectNodes(constructNode, 'solver', varNode, "value")

        node = self.graph.createFunctionNodeSI(kOperator, solverTypeName)
        self._registerSceneItemPair(kOperator, node)

        # set dependencies
        self.graph.addExtDep(kOperator.getExtension())
        subExec = self.graph.getSubExec(node)

        solverPort = subExec.addExecPort("solver", client.DFG.PortTypes.IO)
        subExec.setExecPortTypeSpec(solverPort, solverTypeName)
        self.graph.connectNodes(varNode, 'value', node, solverPort)

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
                self.arg.connectArg("time", node, argPort)
                continue
            if argName == 'frame'and argConnectionType == 'In':
                self.arg.connectArg("frame", node, argPort)
                continue

            # Get the argument's input from the DCC
            if argConnectionType == 'In':
                connectedObjects = kOperator.getInput(argName)
            elif argConnectionType in ['IO', 'Out']:
                connectedObjects = kOperator.getOutput(argName)

            self.connectCanvasOperatorPort(kOperator, node, argPort, argDataType, argConnectionType, connectedObjects, arraySizes)

        opSourceCode = kOperator.generateSourceCode(arraySizes=arraySizes)

        funcExec = self.graph.getSubExec(node)
        funcExec.setCode(opSourceCode)

        return False


    def buildCanvasOperator(self, kOperator):
        """Builds Canvas Operators on the components.

        Args:
            kOperator (Object): Kraken operator that represents a Canvas operator.

        Return:
            bool: True if successful.

        """
        self.report('CanvasOp '+kOperator.getPath())
        self.setCurrentGroupSI(kOperator)

        node = self.graph.createNodeFromPresetSI(kOperator, kOperator.getPresetPath(), title='constructor')
        self._registerSceneItemPair(kOperator, node)
        subExec = self.graph.getSubExec(node)

        portTypeMap = {
            0: 'In',
            1: 'IO',
            2: 'Out'
        }

        arraySizes = {}

        for i in xrange(subExec.getExecPortCount()):
            portName = subExec.getExecPortName(i)
            portConnectionType = portTypeMap[subExec.getExecPortType(i)]
            portDataType = self.graph.getNodePortResolvedType(node, portName)

            if portDataType == 'EvalContext':
                continue
            if portName == 'time' and portConnectionType == 'In':
                self.arg.connectArg("time", node, portName)
                continue
            if portName == 'frame'and portConnectionType == 'In':
                self.arg.connectArg("frame", node, portName)
                continue

            # Get the port's input from the DCC
            if portConnectionType == 'In':
                connectedObjects = kOperator.getInput(portName)
            else:
                connectedObjects = kOperator.getOutput(portName)

            self.connectCanvasOperatorPort(kOperator, node, portName, portDataType, portConnectionType, connectedObjects, arraySizes)


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
        constructorNode = self.graph.getNodeSI(kSceneItem, title='constructor')
        if constructorNode:
          self.graph.setPortDefaultValue(constructorNode, "visibility", kSceneItem.getVisibility())
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

        constructorNode = self.graph.getNodeSI(kSceneItem, title='constructor')
        if not constructorNode:
          return False

        value = kSceneItem.getColor()
        if value is None:
            value = self.getBuildColor(kSceneItem)
        if value:
            colors = self.config.getColors()
            c = colors[value]
            value = Color(r=c[1][0], g=c[1][1], b=c[1][2], a=1.0)

        self.graph.setPortDefaultValue(constructorNode, "color", value)
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

        nodeAndPort = self.graph.getNodeAndPortSI(kSceneItem, asInput=False)
        if not nodeAndPort:
            return False

        (node, port) = nodeAndPort
        constructorNode = self.graph.getNodeSI(kSceneItem, title='constructor')
        if node != constructorNode:
            self.graph.setPortDefaultValue(constructorNode, "xfo", Xfo())
            parentXfo = Xfo(self.graph.computeCurrentPortValue(node, port))
            invXfo = parentXfo.inverse()
            localXfo = invXfo.multiply(kSceneItem.xfo)
            self.graph.setPortDefaultValue(constructorNode, "xfo", localXfo)
            return True
  
        self.graph.setPortDefaultValue(constructorNode, "xfo", kSceneItem.xfo)
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
        self.__graph = GraphManager()

        if self.hasOption('SetupDebugDrawing'):
            self.graph.getOrCreateArgument('debugDraw', dataType='Boolean', portType='In', defaultValue=False)
        self.graph.getOrCreateArgument('time', dataType='Float32', portType='In', defaultValue=0.0)
        self.graph.getOrCreateArgument('frame', dataType='Float32', portType='In', defaultValue=0.0)
        self.graph.getOrCreateArgument('controls', dataType='Xfo[String]', portType='In')
        self.graph.getOrCreateArgument('floats', dataType='Float32[String]', portType='In')

        if self.hasOption('AddCollectJointsNode'):
            self.graph.getOrCreateArgument('joints', dataType='Xfo[String]', portType='Out')

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
            bool: True if successful.

        """
        client = ks.getCoreClient()
        self.graph.setCurrentGroup(None)

        if self.graph.hasArgument('all'):
            self.collectResultPorts('all', Object3D, 'Xfo')
        if self.graph.hasArgument('joints'):
            self.collectResultPorts('joints', Joint, 'Xfo')

        if self.hasOption('SetupDebugDrawing'):
            client = ks.getCoreClient()
            handleArg = self.graph.getOrCreateArgument('handle', dataType='DrawingHandle', portType='Out')

            # draw the lines
            if self.__dfgLastLinesNode:
                preset = "Fabric.Exts.InlineDrawing.DrawingHandle.EmptyDrawingHandle"
                handleNode = self.graph.createNodeFromPreset('drawing', preset, title='handle')
                preset = "Fabric.Exts.InlineDrawing.DrawingHandle.DrawColoredLines"
                drawNode = self.graph.createNodeFromPreset('drawing', preset, title='drawLines')
                preset = "Fabric.Core.Control.If"
                ifNode = self.graph.createNodeFromPreset('drawing', preset, title='if')
                self.graph.connectNodes(handleNode, 'handle', drawNode, "this")
                self.graph.connectNodes(ifNode, 'result', drawNode, "lines")
                self.graph.connectArg(drawNode, "this", handleArg)
                (linesNode, linesPort) = self.__dfgLastLinesNode
                self.graph.connectNodes(linesNode, linesPort, ifNode, "if_true")
                self.graph.connectArg('debugDraw', ifNode, 'cond')

        # perform layout based on reingold tilford
        nodes = self.graph.getAllNodeNames()
        nodeConnections = self.graph.getAllNodeConnections()

        depth = {}
        height = {}
        for n in nodes:
            depth[n] = 0

        changed = True
        while changed:
            changed = False

            # forward
            for n in nodes:
                connections = nodeConnections.get(n, [])
                for c in connections:
                    if depth[c] <= depth[n]:
                        depth[c] = depth[n] + 1
                        changed = True

            # backward
            for n in nodes:
                connections = nodeConnections.get(n, [])
                minDiff = 0
                for c in connections:
                    diff = depth[c] - depth[n]
                    if diff < minDiff or minDiff == 0:
                        minDiff = diff
                if minDiff > 1:
                    depth[n] = depth[n] + minDiff - 1

        rows = []
        maxPortsPerRow = []
        for n in depth:
            while len(rows) <= depth[n]:
                rows += [[]]
                maxPortsPerRow += [0]
            rows[depth[n]] += [n]
            if self.graph.getNumPorts(n) > maxPortsPerRow[depth[n]]:
                maxPortsPerRow[depth[n]] = self.graph.getNumPorts(n)

        for j in range(len(rows)-1, -1, -1):

            row = rows[j]
            rowHeights = {}
            for i in range(len(row)):
                n = row[i]
                if j == len(rows)-1:
                    height[n] = i
                    continue

                connectedNodes = self.graph.getNodeConnections(n)
                offset = maxPortsPerRow[j+1]
                height[n] = len(rows[j+1]) *  + i
                for connectedNode in connectedNodes:
                    h = height[connectedNode] * maxPortsPerRow[j+1]
                    h = h + self.graph.getMinConnectionPortIndex(n, connectedNode)
                    if h < height[n]:
                        height[n] = h

                h = height[n]
                while rowHeights.has_key(h):
                  h = h + 1
                height[n] = h
                rowHeights[height[n]] = True

            # normalize the heights
            sortedHeights = sorted(rowHeights.keys())
            if len(sortedHeights) > 0:
                heightLookup = {}
                for i in range(len(sortedHeights)):
                    heightLookup[sortedHeights[i]] = i
                for i in range(len(row)):
                    n = row[i]
                    height[n] = heightLookup[height[n]]

        for n in nodes:
            x = float(depth[n]) * 300.0
            y = float(height[n]) * 120.0
            self.graph.setNodeMetaData(n, 'uiGraphPos', json.dumps({"x": x, "y": y}))
            self.graph.setNodeMetaData(n, 'uiCollapsedState', "1")

        if self.hasOption('CollapseComponents'):
            self.graph.implodeNodesByGroup()

        if self.__outputFilePath:
            self.graph.saveToFile(self.__outputFilePath)
            self.report('Saved filed %s' % self.__outputFilePath)

        return True
