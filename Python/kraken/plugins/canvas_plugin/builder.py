"""Kraken Canvas - Canvas Builder module.

Classes:
Builder -- Component representation.

"""

import json
import copy

from kraken.core.kraken_system import ks
from kraken.core.builder import Builder
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.color import Color

import FabricEngine.Core as core

class Builder(Builder):
    """Builder object for building Kraken objects in Canvas."""

    __outputFilePath = None
    __dfgBinding = None
    __dfgTopLevelGraph = None
    __dfgNodes = None # todo: to be replaced by _registerSceneItemPair, getDCCSceneItem
    __dfgConstructors = None
    __dfgCurves = None
    __dfgLastCurveNode = None
    __dfgAttributes = None
    __dfgConstraints = None
    __dfgComponentPortMap = None
    __dfgTransforms = None

    def __init__(self):
        super(Builder, self).__init__()

    def reportError(self, error):
        print "====> canvas_plugin.builder.%s" % error
        # raise(Exception(error))

    def makeHash(self, o):
        """
        Makes a hash from a dictionary, list, tuple or set to any level, that contains
        only other hashable types (including any lists, tuples, sets, and
        dictionaries).
        """

        if isinstance(o, (set, tuple, list)):
          new_o = copy.deepcopy(o)
          for i in range(len(new_o)):
              new_o[i] = self.makeHash(i)
          return hash(tuple(frozenset(sorted(new_o))))        

        elif not isinstance(o, dict):
            return hash(o)

        new_o = copy.deepcopy(o)
        for k, v in new_o.items():
            new_o[k] = self.makeHash(v)
        return hash(tuple(frozenset(sorted(new_o.items()))))  

    def getAttributeNodeAndPort(self, kAttribute):
      path = kAttribute.getPath()
      if self.__dfgAttributes.has_key(path):
        return (self.__dfgAttributes[path], 'value')

      objPath = path.rpartition('.')[0].rpartition('.')[0]
      return (self.__dfgNodes[objPath], kAttribute.getName())

    # ========================
    # IO Methods
    # ========================
    def setOutputFilePath(self, filePath):
        self.__outputFilePath = filePath

    # ========================
    # Canvas Preset Methods
    # ========================

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

        rtVal = ks.constructRTVal(dataType, value)
        self.__dfgTopLevelGraph.setPortDefaultValue(portPath, rtVal)
        return True

    def buildCanvasNodeFromSceneItem(self, kSceneItem, buildName):
        cls = kSceneItem.__class__.__name__
        if cls in [
          'ComponentInput',
          'ComponentOutput'
        ]:
          cls = 'Transform'
          # todo: we need to filter these out,
          # and somehow relay connections to them
          # self.__dfgComponentPortMap[kSceneItem.getPath()] = None
          # return kSceneItem

        if not cls in [
            'ComponentGroup',
            'Container',
            'CtrlSpace',
            'Curve',
            'Control',
            'HierarchyGroup',
            'Joint',
            'Layer',
            'Locator',
            'Rig',
            'Transform'
        ]:
            self.reportError("buildCanvasNodeFromSceneItem: Unexpected class " + cls)
            return False

        path = kSceneItem.getPath()
        preset = "Kraken.Constructors.Kraken%s" % cls
        nodePath = self.__dfgTopLevelGraph.addInstFromPreset(preset)
        self.__dfgNodes[path] = nodePath
        self.__dfgConstructors[path] = nodePath
        self.__dfgTransforms[path] = (nodePath, 'xfo')

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

        for propName in ['visibility', 'color']:
            getMethod = 'get%s' % propName.capitalize()
            if not hasattr(kSceneItem, getMethod):
              continue
            self.setPortDefaultValue(kSceneItem, propName, getattr(kSceneItem, getMethod)())

        for propName in ['xfo']:
            if not hasattr(kSceneItem, propName):
              continue
            self.setPortDefaultValue(kSceneItem, propName, getattr(kSceneItem, propName))

        if hasattr(kSceneItem, 'getCurveData'):
            curveData = kSceneItem.getCurveData()
            shapeHash = self.buildCanvasCurveShape(curveData)
            self.setPortDefaultValue(kSceneItem, "shapeHash", shapeHash)

        if hasattr(kSceneItem, 'getParent'):
            parent = kSceneItem.getParent()
            if not parent is None:
              parentPath = parent.getPath()
              if self.__dfgTransforms.has_key(parentPath):
                (parentNode, parentPort) = self.__dfgTransforms[parentPath]
                (childNode, childPort) = self.__dfgTransforms[path]
                preset = "Fabric.Core.Math.Mul"
                transformNode = self.__dfgTopLevelGraph.addInstFromPreset(preset)
                self.__dfgTopLevelGraph.connectTo(parentNode+'.'+parentPort, transformNode+'.lhs')
                self.__dfgTopLevelGraph.connectTo(childNode+'.'+childPort, transformNode+'.rhs')
                self.__dfgTransforms[path] = (transformNode, 'result')

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
        nodePath = self.__dfgTopLevelGraph.addInstFromPreset(preset)
        self.__dfgNodes[path] = nodePath
        self.__dfgAttributes[path] = nodePath

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
        constructNode = self.__dfgTopLevelGraph.addInstFromPreset(preset)
        lastNode = constructNode
        lastPort = "result"

        # todo: compute the offset if the constraint is set to maintain offset!

        constrainers = kConstraint.getConstrainers()
        for constrainer in constrainers:
          preset = "Kraken.Constraints.AddConstrainer"
          addNode = self.__dfgTopLevelGraph.addInstFromPreset(preset)

          self.__dfgTopLevelGraph.connectTo(lastNode+"."+lastPort, addNode+'.this')

          constrainerPath = constrainer.getPath()
          (constrainerNode, constrainerPort) = self.__dfgTransforms[constrainerPath]
          self.__dfgTopLevelGraph.connectTo(constrainerNode+"."+constrainerPort, addNode+'.constrainer')

          lastNode = addNode
          lastPort = 'this'

        constraineePath = kConstraint.getConstrainee().getPath()
        (constraineeNode, constraineePort) = self.__dfgTransforms[constraineePath]

        preset = "Kraken.Constraints.Compute"
        computeNode = self.__dfgTopLevelGraph.addInstFromPreset(preset)
        self.__dfgTopLevelGraph.connectTo(lastNode+"."+lastPort, computeNode+'.this')
        self.__dfgTopLevelGraph.connectTo(constraineeNode+"."+constraineePort, computeNode+'.xfo')

        self.__dfgTransforms[constraineePath] = (computeNode, 'result')

        return None

    def buildCanvasCurveShape(self, curveData):

        if self.__dfgCurves is None:
            preset = "Kraken.DebugDrawing.KrakenCurveDict"
            self.__dfgLastCurveNode = self.__dfgTopLevelGraph.addInstFromPreset(preset)
            self.__dfgCurves = {}

        shapeHash = str(self.makeHash(curveData))
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

            shapeHashVal = ks.constructRTVal("String", shapeHash)
            positionsRTVal = ks.constructRTVal("Vec3[]")
            indicesRTVal = ks.constructRTVal("UInt32[]")
            positionsRTVal.resize(len(positions))
            indicesRTVal.resize(len(indices))

            for i in range(len(positions)):
               positionsRTVal[i] = ks.constructRTVal('Vec3', positions[i])
            for i in range(len(indices)):
                indicesRTVal[i] = ks.constructRTVal('UInt32', indices[i])

            preset = "Kraken.DebugDrawing.DefineCurve"
            curveNode = self.__dfgTopLevelGraph.addInstFromPreset(preset)

            self.__dfgTopLevelGraph.setPortDefaultValue(curveNode+'.shapeHash', shapeHashVal)
            self.__dfgTopLevelGraph.setPortDefaultValue(curveNode+'.positions', positionsRTVal)
            self.__dfgTopLevelGraph.setPortDefaultValue(curveNode+'.indices', indicesRTVal)

            # connec the new nodes with the first port
            subExec = self.__dfgTopLevelGraph.getSubExec(self.__dfgLastCurveNode)
            outPort = subExec.getExecPortName(0)
            subExec = self.__dfgTopLevelGraph.getSubExec(curveNode)
            inPort = subExec.getExecPortName(0)
            self.__dfgTopLevelGraph.connectTo(self.__dfgLastCurveNode+"."+outPort, curveNode+'.'+inPort)

            self.__dfgCurves[shapeHash] = curveNode
            self.__dfgLastCurveNode = curveNode

        return shapeHash

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

        return self.buildCanvasNodeFromAttribute(kAttribute)

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

        (nodeA, portA) = self.getAttributeNodeAndPort(connection)
        (nodeB, portB) = self.getAttributeNodeAndPort(kAttribute)
        if nodeA is None or nodeB is None:
          return False

        self.__dfgTopLevelGraph.connectTo(nodeA+"."+portA, nodeB+'.'+portB)
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
        self.reportError("buildKLOperator not yet implemented.")
        return False


    def buildCanvasOperator(self, kOperator):
        """Builds Canvas Operators on the components.

        Args:
            kOperator (Object): Kraken operator that represents a Canvas operator.

        Return:
            bool: True if successful.

        """
        self.reportError("buildCanvasOperator not yet implemented.")
        return False

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
            self.__dfgTopLevelGraph = self.__dfgBinding.getExec()
            self.__dfgNodes = {}
            self.__dfgConstructors = {}
            self.__dfgAttributes = {}
            self.__dfgConstraints = {}
            self.__dfgComponentPortMap = {}
            self.__dfgTransforms = {}

        except Exception as e:
            self.reportError(e)

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
            bool: True if successful.

        """

        if self.__outputFilePath:
            content = self.__dfgBinding.exportJSON()
            try:
                open(self.__outputFilePath, "w").write(content)
                print "Saved %s canvas file." % self.__outputFilePath
            except IOError as e:
                print e

        return True
