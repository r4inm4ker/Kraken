"""Kraken SI - SI Builder module.

Classes:
Builder -- Component representation.

"""

from kraken.core.kraken_system import ks
from kraken.core.builder import Builder
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.plugins.si_plugin.utils import *

import FabricEngine.Core as core


class Builder(Builder):
    """Builder object for building Kraken objects in Softimage."""

    def __init__(self):
        super(Builder, self).__init__()


    # ========================
    # SceneItem Build Methods
    # ========================
    def buildContainer(self, kSceneItem, buildName):
        """Builds a container / namespace object.

        Args:
            kSceneItem (object): kSceneItem that represents a container to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddModel(None, buildName)
        dccSceneItem.Name = buildName

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        si.Refresh()

        return dccSceneItem


    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Args:
            kSceneItem (object): kSceneItem that represents a layer to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddModel(None, buildName)
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        si.Refresh()

        return dccSceneItem


    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Args:
            kSceneItem (object): kSceneItem that represents a group to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Name = buildName

        lockObjXfo(dccSceneItem)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        si.Refresh()

        return dccSceneItem


    def buildGroup(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Args:
            kSceneItem (object): kSceneItem that represents a group to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        si.Refresh()

        return dccSceneItem


    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Args:
            kSceneItem (object): kSceneItem that represents a joint to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: DCC Scene Item that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Parameters('primary_icon').Value = 2
        dccSceneItem.Parameters('size').Value = 0.125
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        si.Refresh()

        return dccSceneItem


    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Args:
            kSceneItem (object): kSceneItem that represents a locator / null to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        si.Refresh()

        return dccSceneItem


    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Args:
            kSceneItem (object): kSceneItem that represents a curve to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = None

        # Format points for Softimage
        curveData = kSceneItem.getCurveData()

        curvePoints = []
        for eachSubCurve in curveData:
            subCurvePoints = eachSubCurve["points"]

            formattedPoints = []
            for i in xrange(3):
                axisPositions = []
                for p, eachPnt in enumerate(subCurvePoints):
                    if p < len(subCurvePoints):
                        axisPositions.append(eachPnt[i])

                formattedPoints.append(axisPositions)

            formattedPoints.append([1.0] * len(subCurvePoints))
            curvePoints.append(formattedPoints)

        # Build the curve
        for i, eachSubCurve in enumerate(curvePoints):
            closedSubCurve = curveData[i]["closed"]

            # Create knots
            if closedSubCurve is True:
                knots = list(xrange(len(eachSubCurve[0]) + 1))
            else:
                knots = list(xrange(len(eachSubCurve[0])))

            if i == 0:
                dccSceneItem = parentDCCSceneItem.AddNurbsCurve(list(eachSubCurve), knots, closedSubCurve, 1, constants.siNonUniformParameterization, constants.siSINurbs)
                self._registerSceneItemPair(kSceneItem, dccSceneItem)
            else:
                dccSceneItem.ActivePrimitive.Geometry.AddCurve(eachSubCurve, knots, closedSubCurve, 1, constants.siNonUniformParameterization)

        dccSceneItem.Name = buildName

        si.Refresh()

        return dccSceneItem


    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Args:
            kSceneItem (object): kSceneItem that represents a control to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = None

        # Format points for Softimage
        curveData = kSceneItem.getCurveData()

        curvePoints = []
        for eachSubCurve in curveData:
            subCurvePoints = eachSubCurve["points"]

            formattedPoints = []
            for i in xrange(3):
                axisPositions = []
                for p, eachPnt in enumerate(subCurvePoints):
                    if p < len(subCurvePoints):
                        axisPositions.append(eachPnt[i])

                formattedPoints.append(axisPositions)

            formattedPoints.append([1.0] * len(subCurvePoints))
            curvePoints.append(formattedPoints)

        # Build the curve
        for i, eachSubCurve in enumerate(curvePoints):
            closedSubCurve = curveData[i]["closed"]

            # Create knots
            if closedSubCurve is True:
                knots = list(xrange(len(eachSubCurve[0]) + 1))
            else:
                knots = list(xrange(len(eachSubCurve[0])))

            if i == 0:
                dccSceneItem = parentDCCSceneItem.AddNurbsCurve(list(eachSubCurve), knots, closedSubCurve, 1, constants.siNonUniformParameterization, constants.siSINurbs)
                self._registerSceneItemPair(kSceneItem, dccSceneItem)
            else:
                dccSceneItem.ActivePrimitive.Geometry.AddCurve(eachSubCurve, knots, closedSubCurve, 1, constants.siNonUniformParameterization)

        dccSceneItem.Name = buildName

        si.Refresh()

        return dccSceneItem


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kAttribute):
        """Builds a Bool attribute.

        Args:
            kAttribute (object): kAttribute that represents a boolean attribute to be built.

        Returns:
            bool: True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siBool, kAttribute.getValue(), "", "", "", "", constants.siClassifUnknown, 2053, kAttribute.getName())
        dccSceneItem.Animatable = kAttribute.getAnimatable()
        dccSceneItem.Keyable = kAttribute.getKeyable()
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (object): kAttribute that represents a float attribute to be built.

        Returns:
            bool: True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siDouble, kAttribute.getValue(), kAttribute.getMin(), kAttribute.getMax(), kAttribute.getUIMin(), kAttribute.getUIMax(), constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (object): kAttribute that represents a integer attribute to be built.

        Returns:
            bool: True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siInt4, kAttribute.getValue(), kAttribute.getMin(), kAttribute.getMax(), kAttribute.getUIMin(), kAttribute.getUIMax(), constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (object): kAttribute that represents a string attribute to be built.

        Returns:
            bool: True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siString, kAttribute.getValue(), "", "", "", "", constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Args:
            kAttributeGroup (object): Kraken object to build the attribute group on.

        Returns:
            bool: True if successful.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kAttributeGroup.getParent())

        groupName = kAttributeGroup.getName()
        dccSceneItem = parentDCCSceneItem.AddProperty("CustomParameterSet", False, groupName)
        self._registerSceneItemPair(kAttributeGroup, dccSceneItem)

        # Create Attributes on this Attribute Group
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
            kAttribute (object): Attribute to connect.

        Returns:
            bool: True if successful.

        """

        if kAttribute.isConnected() is True:
            driver = self.getDCCSceneItem(kAttribute.getConnection())
            driven = self.getDCCSceneItem(kAttribute)
            driven.AddExpression(driver.FullName)

        return True


    # =========================
    # Constraint Build Methods
    # =========================
    def buildOrientationConstraint(self, kConstraint):
        """Builds an orientation constraint represented by the kConstraint.

        Args:
            kConstraint (object): Kraken constraint object to build.

        Returns:
            object: dccSceneItem that was created.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())

        constrainers = getCollection()
        for eachConstrainer in kConstraint.getConstrainers():
            constrainers.AddItems(self.getDCCSceneItem(eachConstrainer))

        dccSceneItem = constraineeDCCSceneItem.Kinematics.AddConstraint("Orientation", constrainers, kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPoseConstraint(self, kConstraint):
        """Builds an pose constraint represented by the kConstraint.

        Args:
            kConstraint (object): kraken constraint object to build.

        Returns:
            bool: True if successful.

        """


        useXSIConstraint = True
        if useXSIConstraint:

            constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
            if kConstraint.getMaintainOffset():
                constraineeTransform = constraineeDCCSceneItem.Kinematics.Global.Transform

            constrainingObjs = getCollection()
            for eachConstrainer in kConstraint.getConstrainers():
                constrainer = self.getDCCSceneItem(eachConstrainer)

                if kConstraint.getMaintainOffset():
                    constrainerTransform = constrainer.Kinematics.Global.Transform

                # si.LogMessage( "%s,%s,%s" % (constrainer.posx.Value, constrainer.posy.Value, constrainer.posz.Value) )

                constrainingObjs.AddItems(constrainer)

            dccSceneItem = constraineeDCCSceneItem.Kinematics.AddConstraint("Pose", constrainingObjs, kConstraint.getMaintainOffset())
            self._registerSceneItemPair(kConstraint, dccSceneItem)

        else:

            # Load the Fabric Engine client and construct the RTVal for the Solver
            ks.loadCoreClient()
            ks.loadExtension('Kraken')
            solverTypeName = 'PoseConstraintSolver'
            target = constraineeDCCSceneItem.FullName# + ".kine.global"
            canvasOpPath = target + ".kine.global.CanvasOp"

            # si.fabricSplice('newSplice', "{\"targets\":\"" + target + "\", \"portName\":\"constrainee\", \"portMode\":\"out\"}", "", "")
            si.FabricCanvasOpApply(target, "", True, "", "")


            # si.FabricCanvasAddFunc("polymsh.kine.global.CanvasOp", "", "func", "dfgEntry {\n  // result = a + b;\n}\n", "-4", "27")

            # Add the private/non-mayaAttr port that stores the Solver object
            # si.fabricSplice("addInternalPort", canvasOpPath, "{\"portName\":\"solver\", \"dataType\":\"" + solverTypeName + "\", \"extension\":\"Kraken\", \"portMode\":\"io\"}", "")
            # si.fabricSplice("addInternalPort", canvasOpPath, "{\"portName\":\"debug\", \"dataType\":\"Boolean\", \"extension\":\"Kraken\", \"portMode\":\"io\"}", "")
            # si.fabricSplice("addInternalPort", canvasOpPath, "{\"portName\":\"rightSide\", \"dataType\":\"Boolean\", \"extension\":\"Kraken\", \"portMode\":\"io\"}", "")

            si.FabricCanvasAddPort(canvasOpPath, "", "solver", "In", solverTypeName, "Kraken")
            si.FabricCanvasAddPort(canvasOpPath, "", "debug", "In", "Boolean", "")
            si.FabricCanvasAddPort(canvasOpPath, "", "rightSide", "In", "Boolean", "")

            connectionTargets = ""
            connectionSuffix = ".kine.global"
            for eachConstrainer in kConstraint.getConstrainers():

                if eachConstrainer is None:
                    raise Exception("Constraint '"+kConstraint.getPath()+"' has invalid connection.");

                dccSceneItem = self.getDCCSceneItem(eachConstrainer)

                if dccSceneItem is None:
                    raise Exception("Constraint '"+kConstraint.getPath()+"' of type '"+solverTypeName+"' is connected to object without corresponding SceneItem:" + eachConstrainer.getPath());

                connectionTargets = dccSceneItem.FullName + connectionSuffix
                break

            si.FabricCanvasAddPort(canvasOpPath, "", "constrainer", "In", "Mat44", "")
            # si.fabricSplice("addInputPort", canvasOpPath, "{\"portName\":\"constrainer\", \"dataType\":\"Mat44\", \"extension\":\"\", \"targets\":\"" + connectionTargets + "\"}", "")

            # Generate the operator source code.
            opSourceCode = ""
            opSourceCode += "require Kraken;\n"
            opSourceCode += "operator poseConstraint(\n"
            opSourceCode += "    io " + solverTypeName + " solver,\n"
            opSourceCode += "    in Boolean debug,\n"
            opSourceCode += "    in Boolean rightSide,\n"
            opSourceCode += "    io Mat44 constrainee,\n"
            opSourceCode += "    in Mat44 constrainer\n"
            opSourceCode += "    )\n"
            opSourceCode += "{\n"
            opSourceCode += "    solver.solve(debug, rightSide, constrainer, constrainee);"
            opSourceCode += "}\n"

            si.fabricSplice('addKLOperator', canvasOpPath, '{"opName": "poseConstraint"}', opSourceCode)

        return dccSceneItem


    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Args:
            kConstraint (object): kraken constraint object to build.

        Returns:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())

        constrainers = getCollection()
        for eachConstrainer in kConstraint.getConstrainers():
            constrainers.AddItems(self.getDCCSceneItem(eachConstrainer))

        dccSceneItem = constraineeDCCSceneItem.Kinematics.AddConstraint("Position", constrainers, kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildScaleConstraint(self, kConstraint):
        """Builds an scale constraint represented by the kConstraint.

        Args:
            kConstraint (object): kraken constraint object to build.

        Returns:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())

        constrainers = getCollection()
        for eachConstrainer in kConstraint.getConstrainers():
            constrainers.AddItems(self.getDCCSceneItem(eachConstrainer))

        dccSceneItem = constraineeDCCSceneItem.Kinematics.AddConstraint("Scaling", constrainers, kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    # ========================
    # Component Build Methods
    # ========================
    def buildAttributeConnection(self, connectionInput):
        """Builds the link between the target and connection target.

        Args:
            connectionInput (object): kraken component input to build connections for.

        Returns:
            bool: True if successful.

        """

        if connectionInput.isConnected() is False:
            return False

        connection = connectionInput.getConnection()
        connectionTarget = connection.getTarget()
        inputTarget = connectionInput.getTarget()

        if connection.getDataType().endswith('[]'):
            connectionTarget = connection.getTarget()[connectionInput.getIndex()]
        else:
            connectionTarget = connection.getTarget()

        connectionTargetDCCSceneItem = self.getDCCSceneItem(connectionTarget)
        targetDCCSceneItem = self.getDCCSceneItem(inputTarget)
        targetDCCSceneItem.AddExpression(connectionTargetDCCSceneItem.FullName)

        return True


    # =========================
    # Operator Builder Methods
    # =========================
    def buildSpliceOperators(self, kOperator):
        """Builds Splice Operators on the components.

        Args:
            kOperator (object): kraken operator that represents a Splice operator.

        Returns:
            bool: True if successful.

        """
        try:
            solverTypeName = kOperator.getSolverTypeName()
            args = kOperator.getSolverArgs()


            def findPortOfType(connectionType, dataType):
                for i in xrange(len(args)):
                    arg = args[i]
                    argName = arg.name.getSimpleType()
                    argDataType = arg.dataType.getSimpleType()
                    argConnectionType = arg.connectionType.getSimpleType()

                    if argConnectionType == connectionType and argDataType == dataType:
                        return argName

                return None


            # Find operatorOwner to attach Splice Operator to.
            operatorOwner = None
            operatorOwnerKine = None
            operatorOwnerArg = None

            ownerOutPort = findPortOfType('Mat44', 'out')
            if ownerOutPort is None:
                ownerOutPort = findPortOfType('Mat44', 'io')
            if ownerOutPort is None:
                ownerOutPort = findPortOfType('Mat44[]', 'io')
            if ownerOutPort is None:
                raise Exception("Solver '" + kOperator.getName() + "' has no Mat44 outputs!")

            # Create Splice Operator
            canvasOpPath = si.FabricCanvasOpApply(operatorOwner.FullName, "", True, "", "")
            print canvasOpPath
            canvasOp = si.Dictionary.GetObject(canvasOpPath, False)
            si.FabricCanvasSetExtDeps(canvasOpPath, "", "Kraken" )

            si.FabricCanvasAddFunc(canvasOpPath, "", kOperator.getName(), "dfgEntry {}", "100", "100")
            si.FabricCanvasAddPort(canvasOpPath, kOperator.getName(), "solver", "IO", solverTypeName, "", "Kraken")
            si.FabricCanvasAddPort(canvasOpPath, "", "solver", "IO", solverTypeName, "", "Kraken" )
            si.FabricCanvasConnect(canvasOpPath, "", "solver", kOperator.getName()+".solver")
            si.FabricCanvasConnect(canvasOpPath, "", kOperator.getName()+".solver", "solver")

            # print canvasOp.GetNumPortGroups()
            # print canvasOp.PortGroups
            # print canvasOp.PortGroups.Item
            # print canvasOp.PortGroups[canvasOp.GetNumPortGroups()]
            # print canvasOp.PortGroups.Item[canvasOp.GetNumPortGroups()-1]
            # portGroupIndex = canvasOp.PortGroups.Item[canvasOp.GetNumPortGroups()-1].Index;
            # print portGroupIndex

            # connect the operator to the objects in the DCC
            for i in xrange(len(args)):
                arg = args[i]
                argName = arg.name.getSimpleType()
                argDataType = arg.dataType.getSimpleType()
                argConnectionType = arg.connectionType.getSimpleType()

                # Skip arg if it's the target arg
                # if argName == operatorOwnerArg:
                #     continue

                print "FabricCanvasAddPort: " + str(canvasOpPath) + " " + argName + " " + argDataType + " " + argConnectionType

                if argConnectionType == 'in':
                    si.FabricCanvasAddPort(canvasOpPath, "", argName, "In", argDataType, "")
                    si.FabricCanvasAddPort(canvasOpPath, kOperator.getName(), argName, "In", argDataType, "")
                    si.FabricCanvasConnect(canvasOpPath, "", argName, kOperator.getName()+"."+argName)
                elif argConnectionType in ['io', 'out']:
                    si.FabricCanvasAddPort(canvasOpPath, "", argName, "Out", argDataType, "")
                    si.FabricCanvasAddPort(canvasOpPath, kOperator.getName(), argName, "Out", argDataType, "")
                    si.FabricCanvasConnect(canvasOpPath, "", kOperator.getName()+"."+argName, argName)

                if argDataType == 'EvalContext':
                    continue

                portGroupIndex = -1
                # Append the suffix based on the argument type, Softimage Only
                if argDataType == 'Mat44' or argDataType == 'Mat44[]':
                    connectionSuffix = ".kine.global"

                    print "FabricCanvasOpPortMapDefine:" + portmapDefinition
                    portmapDefinition = argName+"|XSI Port"

                    canvasOpPath2 = str(canvasOpPath) + ":"
                    si.FabricCanvasOpPortMapDefine(canvasOpPath, portmapDefinition)
                    canvasOpPath = str(canvasOpPath2)[:-1]

                    canvasOp = si.Dictionary.GetObject(canvasOpPath, False)
                    print canvasOp.GetNumPortGroups()
                    print canvasOp.PortGroups
                    print canvasOp.PortGroups.Item
                    # print canvasOp.PortGroups.Item[canvasOp.GetNumPortGroups()-1]
                    portGroupIndex = canvasOp.GetNumPortGroups()-1;

                elif argDataType in ['Scalar', 'Boolean']:
                    connectionSuffix = ""

                    portmapDefinition = argName+"|XSI Parameter"
                    print "FabricCanvasOpPortMapDefine:" + portmapDefinition

                    canvasOpPath2 = str(canvasOpPath) + ":"
                    si.FabricCanvasOpPortMapDefine(canvasOpPath, portmapDefinition)
                    canvasOpPath = str(canvasOpPath2)[:-1]

                    canvasOp = si.Dictionary.GetObject(canvasOpPath, False)
                    print canvasOp.GetNumPortGroups()
                    # print canvasOp.PortGroups
                    # print canvasOp.PortGroups.Item
                    # print canvasOp.PortGroups[canvasOp.GetNumPortGroups()]
                    # print canvasOp.PortGroups.Item[canvasOp.GetNumPortGroups()-1]
                    # portGroupIndex = canvasOp.PortGroups.Item[canvasOp.GetNumPortGroups()-1].Index

                    if argName == 'time':
                        timeParameter = canvasOp.Parameters("time")
                        if timeParameter is not None:
                            timeParameter.AddExpression("T")
                        continue
                    if argName == 'frame':
                        frameParameter = canvasOp.Parameters("frame")
                        if frameParameter is not None:
                            frameParameter.AddExpression("Fc")
                        continue

                else:
                    connectionSuffix = ""


                # Get the argument's input from the DCC
                # Note: this used to be a try/catch statement, which seemed quite strange to me.
                # I've replaced with a proper test with an exception if the item is not found.
                if argConnectionType == 'in':
                    connectedObjects = kOperator.getInput(argName)
                elif argConnectionType in ['io', 'out']:
                    connectedObjects = kOperator.getOutput(argName)

                if argDataType.endswith('[]'):

                    if len(connectedObjects) == 0:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' not connected.");

                    connectionTargets = ""
                    for i in range(len(connectedObjects)):
                        dccSceneItem = self.getDCCSceneItem(connectedObjects[i])

                        if dccSceneItem is None:
                            raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' dcc item not found for item:" + connectedObjects[i].getPath());

                        if i==0:
                            connectionTargets = dccSceneItem.FullName + connectionSuffix
                        else:
                            connectionTargets = connectionTargets + "," + dccSceneItem.FullName + connectionSuffix
                else:
                    if connectedObjects is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' not connected.");

                    dccSceneItem = self.getDCCSceneItem(connectedObjects)

                    if dccSceneItem is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' dcc item not found for item:" + connectedObjects.getPath());

                    if argName == operatorOwnerArg:
                        canvasOp.ConnectToGroup(portGroupIndex, operatorOwnerKine)
                    else:
                        if argDataType == 'Mat44':
                            canvasOp.ConnectToGroup(portGroupIndex, dccSceneItem)

                    #     if argDataType in ['Scalar', 'Boolean']:
                    #         parameter = canvasOp.Parameters(argName)
                    #         canvasOp.ConnectToGroup(parameter, dccSceneItem)


            # Generate the operator source code.
            opSourceCode = kOperator.generateSourceCode()
            print opSourceCode
            si.FabricCanvasSetCode(canvasOpPath, kOperator.getName(), opSourceCode)


        finally:
            pass

        return True


    # ==================
    # Parameter Methods
    # ==================
    def lockParameters(self, kSceneItem):
        """Locks flagged SRT parameters.

        Args:
            kSceneItem (object): kraken object to lock the SRT parameters on.

        Returns:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        # Lock Rotation
        if kSceneItem.testFlag("lockXRotation") is True:
            dccSceneItem.Kinematics.Local.Parameters('rotx').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('rotx').SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockYRotation") is True:
            dccSceneItem.Kinematics.Local.Parameters('roty').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('roty').SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockZRotation") is True:
            dccSceneItem.Kinematics.Local.Parameters('rotz').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('rotz').SetCapabilityFlag(constants.siKeyable, False)

        # Lock Scale
        if kSceneItem.testFlag("lockXScale") is True:
            dccSceneItem.Kinematics.Local.Parameters('sclx').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('sclx').SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockYScale") is True:
            dccSceneItem.Kinematics.Local.Parameters('scly').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('scly').SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockZScale") is True:
            dccSceneItem.Kinematics.Local.Parameters('sclz').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('sclz').SetCapabilityFlag(constants.siKeyable, False)

        # Lock Translation
        if kSceneItem.testFlag("lockXTranslation") is True:
            dccSceneItem.Kinematics.Local.Parameters('posx').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('posx').SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockYTranslation") is True:
            dccSceneItem.Kinematics.Local.Parameters('posy').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('posy').SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockZTranslation") is True:
            dccSceneItem.Kinematics.Local.Parameters('posz').SetLock(constants.siLockLevelManipulation)
            dccSceneItem.Kinematics.Local.Parameters('posz').SetCapabilityFlag(constants.siKeyable, False)

        return True


    # ===================
    # Visibility Methods
    # ===================
    def setVisibility(self, kSceneItem):
        """Sets the visibility of the object after its been created.

        Args:
            kSceneItem (object): kraken object to set the visibility on.

        Returns:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        if kSceneItem.getShapeVisibility() is False:
            dccSceneItem.Properties("Visibility").Parameters("viewvis").Value = False

        return True


    # ================
    # Display Methods
    # ================
    def setObjectColor(self, kSceneItem):
        """Sets the color on the dccSceneItem.

        Args:
            kSceneItem (object): kraken object to set the color on.

        Returns:
            bool: True if successful.

        """

        colors = self.config.getColors()
        dccSceneItem = self.getDCCSceneItem(kSceneItem)
        buildColor = self.getBuildColor(kSceneItem)

        if buildColor is not None:
            displayProperty = dccSceneItem.AddProperty("Display Property")
            displayProperty.Parameters("wirecolorr").Value = colors[buildColor][1][0]
            displayProperty.Parameters("wirecolorg").Value = colors[buildColor][1][1]
            displayProperty.Parameters("wirecolorb").Value = colors[buildColor][1][2]

        return True


    # ==================
    # Transform Methods
    # ==================
    def setTransform(self, kSceneItem):
        """Translates the transform to Softimage transform.

        Args:
            kSceneItem (object): object to set the transform on.

        Returns:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        xfo = XSIMath.CreateTransform()
        sc = XSIMath.CreateVector3(kSceneItem.xfo.sc.x, kSceneItem.xfo.sc.y, kSceneItem.xfo.sc.z)

        quat = XSIMath.CreateQuaternion(kSceneItem.xfo.ori.w, kSceneItem.xfo.ori.v.x, kSceneItem.xfo.ori.v.y, kSceneItem.xfo.ori.v.z)
        tr = XSIMath.CreateVector3(kSceneItem.xfo.tr.x, kSceneItem.xfo.tr.y, kSceneItem.xfo.tr.z)

        xfo.SetScaling(sc)
        xfo.SetRotationFromQuaternion(quat)
        xfo.SetTranslation(tr)

        dccSceneItem.Kinematics.Global.PutTransform2(None, xfo)

        dccSceneItem.Kinematics.Local.Parameters('rotorder').Value = kSceneItem.ro.order

        return True


    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Pre-Build commands.

        Args:
            kSceneItem (object): kraken kSceneItem object to build.

        Returns:
            bool: True if successful.

        """

        si.SetValue("preferences.scripting.cmdlog", False, "")

        return True


    def _postBuild(self):
        """Post-Build commands.

        Returns:
            bool: True if successful.

        """

        return True
