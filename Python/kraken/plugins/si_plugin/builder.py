"""Kraken SI - SI Builder module.

Classes:
Builder -- Component representation.

"""

from kraken.core.kraken_system import ks
from kraken.core.builders.builder import Builder
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

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created..

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddModel(None, buildName)
        dccSceneItem.Name = buildName

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a layer to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created..

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddModel(None, buildName)
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Name = buildName

        lockObjXfo(dccSceneItem)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildGroup(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a joint to be built.
        buildName -- String, The name to use on the built object.

        Return:
        DCC Scene Item that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a locator / null to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kSceneItem.getParent())

        if parentDCCSceneItem is None:
            parentDCCSceneItem = si.ActiveProject3.ActiveScene.Root

        dccSceneItem = parentDCCSceneItem.AddNull()
        dccSceneItem.Name = buildName
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a curve to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created.

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

        return dccSceneItem


    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a control to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created.

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

        return dccSceneItem


    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kAttribute):
        """Builds a Bool attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a boolean attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siBool, kAttribute.getValue(), "", "", "", "", constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildFloatAttribute(self, kAttribute):
        """Builds a Float attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a float attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siDouble, kAttribute.getValue(), kAttribute.getMin(), kAttribute.getMax(), kAttribute.getMin(), kAttribute.getMax(), constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a integer attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siInt4, kAttribute.getValue(), kAttribute.min, kAttribute.max, kAttribute.min, kAttribute.max, constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a string attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = Dispatch(self.getDCCSceneItem(kAttribute.getParent()))
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siString, kAttribute.getValue(), "", "", "", "", constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Arguments:
        kAttributeGroup -- SceneItem, kraken object to build the attribute group on.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kAttributeGroup.getParent())

        groupName = kAttributeGroup.getName()
        if groupName == "" and kAttributeGroup.getNumAttributes() < 1:
            return False

        if groupName == "":
            groupName = "Settings"

        dccSceneItem = parentDCCSceneItem.AddProperty("CustomParameterSet", False, groupName)
        self._registerSceneItemPair(kAttributeGroup, dccSceneItem)

        # Create Attributes on this Attribute Group
        for i in xrange(kAttributeGroup.getNumAttributes()):
            kAttribute = kAttributeGroup.getAttributeByIndex(i)

            if kAttribute.isTypeOf("BoolAttribute"):
                self.buildBoolAttribute(kAttribute)

            elif kAttribute.isTypeOf("FloatAttribute"):
                self.buildFloatAttribute(kAttribute)

            elif kAttribute.isTypeOf("IntegerAttribute"):
                self.buildIntegerAttribute(kAttribute)

            elif kAttribute.isTypeOf("StringAttribute"):
                self.buildStringAttribute(kAttribute)

            else:
                raise NotImplementedError(kAttribute.getName() + ' has an unsupported type: ' + str(type(kAttribute)))

        return True


    def connectAttribute(self, kAttribute):
        """Connects the driver attribute to this one.

        Arguments:
        kAttribute -- Object, attribute to connect.

        Return:
        True if successful.

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

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        dccSceneItem that was created.

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

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        True if successful.

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
            target = constraineeDCCSceneItem.FullName + ".kine.global"
            spliceOpPath = target + ".SpliceOp"

            si.fabricSplice('newSplice', "{\"targets\":\"" + target + "\", \"portName\":\"constrainee\", \"portMode\":\"out\"}", "", "")

            # Add the private/non-mayaAttr port that stores the Solver object
            si.fabricSplice("addInternalPort", spliceOpPath, "{\"portName\":\"solver\", \"dataType\":\"" + solverTypeName + "\", \"extension\":\"Kraken\", \"portMode\":\"io\"}", "")
            si.fabricSplice("addInternalPort", spliceOpPath, "{\"portName\":\"debug\", \"dataType\":\"Boolean\", \"extension\":\"Kraken\", \"portMode\":\"io\"}", "")
            si.fabricSplice("addInternalPort", spliceOpPath, "{\"portName\":\"rightSide\", \"dataType\":\"Boolean\", \"extension\":\"Kraken\", \"portMode\":\"io\"}", "")

            connectionTargets = ""
            connectionSuffix = ".kine.global"
            for eachConstrainer in kConstraint.getConstrainers():

                if eachConstrainer is None:
                    raise Exception("Constraint '"+kConstraint.getFullName()+"' has invalid connection.");

                dccSceneItem = self.getDCCSceneItem(eachConstrainer)

                if dccSceneItem is None:
                    raise Exception("Constraint '"+kConstraint.getFullName()+"' of type '"+solverTypeName+"' is connected to object without corresponding SceneItem:" + eachConstrainer.getFullName());

                connectionTargets = dccSceneItem.FullName + connectionSuffix
                break

            si.fabricSplice("addInputPort", spliceOpPath, "{\"portName\":\"constrainer\", \"dataType\":\"Mat44\", \"extension\":\"\", \"targets\":\"" + connectionTargets + "\"}", "")

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

            si.fabricSplice('addKLOperator', spliceOpPath, '{"opName": "poseConstraint"}', opSourceCode)

        return dccSceneItem


    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        True if successful.

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

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        True if successful.

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
    def buildAttributeConnection(self, componentIO):
        """Builds the link between the target and connection target.

        Arguments:
        componentIO -- Object, kraken connection to build.

        Return:
        True if successful.

        """

        connection = componentIO.getConnection()
        connectionTarget = connection.getTarget()
        target = componentIO.getTarget()

        if componentIO.getDataType().endswith('[]'):
            # TODO: Implement array handling.
            pass
        else:

            connectionTargetDCCSceneItem = self.getDCCSceneItem(connectionTarget)
            targetDCCSceneItem = self.getDCCSceneItem(target)

            targetDCCSceneItem.AddExpression(connectionTargetDCCSceneItem.FullName)

        return True


    # =========================
    # Operator Builder Methods
    # =========================
    def buildSpliceOperators(self, kOperator):
        """Builds Splice Operators on the components.

        Arguments:
        kOperator -- Object, kraken operator that represents a Splice operator.

        Return:
        True if successful.

        """
        try:
            solverTypeName = kOperator.getSolverTypeName()
            args = kOperator.getSolverArgs()

            # Find operatorOwner to attach Splice Operator to.
            operatorOwner = None
            targets = None
            operatorOwnerArg = None
            for i in xrange(len(args)):
                arg = args[i]

                if arg.connectionType == 'io' or arg.connectionType == 'out':
                    if arg.dataType == 'Mat44':

                        target = kOperator.getOutput(arg.name)
                        if target is None:
                            raise Exception("Solver '" + kOperator.getFullName() + "' output :'" + arg.name + "' not connected.")

                        operatorOwner = self.getDCCSceneItem(target)

                        if operatorOwner is None:
                            raise Exception("Solver '" + kOperator.getFullName() + "' output :'" + arg.name + "' dcc item not found for item:" + target.getFullName())

                        targets = operatorOwner.FullName + ".kine.global"
                        operatorOwnerArg = arg.name
                        break
                    elif arg.dataType == 'Mat44[]':
                        targets = ""
                        for target in kOperator.getOutput(arg.name):

                            if target is None:
                                raise Exception("Solver '" + kOperator.getFullName() + "' output :'" + arg.name + "' not connected.")

                            dccSceneItem = self.getDCCSceneItem(target)

                            if dccSceneItem is None:
                                raise Exception("Solver '" + kOperator.getFullName() + "' output :'" + arg.name + "' dcc item not found for item:" + target.getFullName())

                            if targets == "":
                                operatorOwner = dccSceneItem
                                targets = dccSceneItem.FullName + ".kine.global"
                            else:
                                targets = targets + "," + dccSceneItem.FullName + ".kine.global"
                        operatorOwnerArg = arg.name
                        break

            if operatorOwner is None:
                raise Exception("Solver '" + kOperator.getName() + "' has no Mat44 outputs!")

            spliceOpPath = operatorOwner.FullName + ".kine.global.SpliceOp"

            # Create Splice Operator
            si.fabricSplice('newSplice', "{\"targets\":\"" + targets + "\", \"portName\":\"" + arg.name + "\", \"portMode\":\"out\"}", "", "")

            # Add the private/non-mayaAttr port that stores the Solver object
            si.fabricSplice("addInternalPort", spliceOpPath, "{\"portName\":\"solver\", \"dataType\":\"" + solverTypeName + "\", \"extension\":\"" + kOperator.getExtension() + "\", \"portMode\":\"io\"}", "")

            # connect the operator to the objects in the DCC
            for i in xrange(len(args)):
                arg = args[i]

                # Skip arg if it's the target arg
                if arg.name == operatorOwnerArg:
                    continue

                # Append the suffix based on the argument type, Softimage Only
                if arg.dataType == 'Mat44' or arg.dataType == 'Mat44[]':
                    connectionSuffix = ".kine.global"
                elif arg.dataType in ['Scalar', 'Boolean']:
                    connectionSuffix = ""
                else:
                    connectionSuffix = ""


                # Get the argument's input from the DCC
                # Note: this used to be a try/catch statement, which seemed quite strange to me.
                # I've replaced with a proper test with an exception if the item is not found.
                if arg.connectionType == 'in':
                    connectedObjects = kOperator.getInput(arg.name)
                elif arg.connectionType in ['io', 'out']:
                    connectedObjects = kOperator.getOutput(arg.name)

                if arg.dataType.endswith('[]'):

                    if len(connectedObjects) == 0:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' not connected.");

                    connectionTargets = ""
                    for i in range(len(connectedObjects)):
                        dccSceneItem = self.getDCCSceneItem(connectedObjects[i])

                        if dccSceneItem is None:
                            raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' dcc item not found for item:" + connectedObjects[i].getFullName());

                        if i==0:
                            connectionTargets = dccSceneItem.FullName + connectionSuffix
                        else:
                            connectionTargets = connectionTargets + "," + dccSceneItem.FullName + connectionSuffix
                else:
                    if connectedObjects is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' not connected.");

                    dccSceneItem = self.getDCCSceneItem(connectedObjects)

                    if dccSceneItem is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' dcc item not found for item:" + connectedObjects.getFullName());

                    connectionTargets = dccSceneItem.FullName + connectionSuffix

                connectionArgs = "{\"portName\":\"" + arg.name + "\", \"dataType\":\"" + arg.dataType + "\", \"extension\":\"\", \"targets\":\"" + connectionTargets + "\"}"

                # Add the splice Port for each arg.
                if arg.connectionType == 'in':
                    si.fabricSplice("addInputPort", spliceOpPath, connectionArgs, "")

                elif arg.connectionType in ['io', 'out']:
                    si.fabricSplice("addOutputPort", spliceOpPath, connectionArgs, "")

            # Generate the operator source code.
            opSourceCode = kOperator.generateSourceCode()

            si.fabricSplice('addKLOperator', spliceOpPath, '{"opName": "' + kOperator.getName() + '"}', opSourceCode)

        finally:
            pass

        return True


    # ==================
    # Parameter Methods
    # ==================
    def lockParameters(self, kSceneItem):
        """Locks flagged SRT parameters.

        Arguments:
        kSceneItem -- Object, kraken object to lock the SRT parameters on.

        Return:
        True if successful.

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

        Arguments:
        kSceneItem -- Object, kraken object to set the visibility on.

        Return:
        True if successful.

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

        Arguments:
        kSceneItem -- Object, kraken object to set the color on.

        Return:
        True if successful.

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

        Arguments:
        kSceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

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

        return True


    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Pre-Build commands.

        Arguments:
        kSceneItem -- Object, kraken kSceneItem object to build.

        Return:
        True if successful.

        """

        si.SetValue("preferences.scripting.cmdlog", False, "")
        si.BeginUndo("Kraken SI Build: " + kSceneItem.name)

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
        True if successful.

        """

        si.EndUndo()

        return True