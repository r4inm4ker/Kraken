"""Kraken SI - SI Builder module.

Classes:
Builder -- Component representation.

"""

from kraken.core.kraken_system import ks
from kraken.core.builders.base_builder import BaseBuilder
from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.plugins.si_plugin.utils import *

import FabricEngine.Core as core


class Builder(BaseBuilder):
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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kSceneItem.getParent())

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

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent())
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

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent())
        dccSceneItem = parentDCCSceneItem.AddParameter2(kAttribute.getName(), constants.siDouble, kAttribute.getValue(), kAttribute.min, kAttribute.max, kAttribute.min, kAttribute.max, constants.siClassifUnknown, 2053, kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a integer attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent())
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

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent())
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

        parentDCCSceneItem = self._getDCCSceneItem(kAttributeGroup.getParent())

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
            kType = kAttribute.getKType()

            if kType == "BoolAttribute":
                self.buildBoolAttribute(kAttribute)

            elif kType == "FloatAttribute":
                self.buildFloatAttribute(kAttribute)

            elif kType == "IntegerAttribute":
                self.buildIntegerAttribute(kAttribute)

            elif kType == "StringAttribute":
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
            driver = self._getDCCSceneItem(kAttribute.getConnection())
            driven = self._getDCCSceneItem(kAttribute)
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

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())

        constrainers = getCollection()
        for eachConstrainer in kConstraint.getConstrainers():
            constrainers.AddItems(self._getDCCSceneItem(eachConstrainer))

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

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())

        constrainingObjs = getCollection()
        for eachConstrainer in kConstraint.getConstrainers():
            constrainingObjs.AddItems(self._getDCCSceneItem(eachConstrainer))

        dccSceneItem = constraineeDCCSceneItem.Kinematics.AddConstraint("Pose", constrainingObjs, kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Arguments:
        kConstraint -- Object, kraken constraint object to build.

        Return:
        True if successful.

        """

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())

        constrainers = getCollection()
        for eachConstrainer in kConstraint.getConstrainers():
            constrainers.AddItems(self._getDCCSceneItem(eachConstrainer))

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

        constraineeDCCSceneItem = self._getDCCSceneItem(kConstraint.getConstrainee())

        constrainers = getCollection()
        for eachConstrainer in kConstraint.getConstrainers():
            constrainers.AddItems(self._getDCCSceneItem(eachConstrainer))

        dccSceneItem = constraineeDCCSceneItem.Kinematics.AddConstraint("Scaling", constrainers, kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    # ========================
    # Component Build Methods
    # ========================
    def buildAttributeConnection(self, kConnection):
        """Builds the connection between the attribute and the connection.

        Arguments:
        kConnection -- Object, kraken connection to build.

        Return:
        True if successful.

        """

        source = kConnection.getSource()
        target = kConnection.getTarget()

        sourceDCCSceneItem = self._getDCCSceneItem(kConnection.getSource())
        targetDCCSceneItem = self._getDCCSceneItem(kConnection.getTarget())

        targetDCCSceneItem.AddExpression(sourceDCCSceneItem.FullName)

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
                        operatorOwner = self._getDCCSceneItem(kOperator.getOutput(arg.name))
                        targets = operatorOwner.FullName + ".kine.global"
                        operatorOwnerArg = arg.name
                        break
                    elif arg.dataType == 'Mat44[]':
                        targets = ""
                        for target in kOperator.getOutput(arg.name):
                            dccSceneItem = self._getDCCSceneItem(target)
                            if targets == "":
                                operatorOwner = dccSceneItem
                                targets = dccSceneItem.FullName + ".kine.global"
                            else:
                                targets = targets + "," + dccSceneItem.FullName + ".kine.global"
                        operatorOwnerArg = arg.name
                        break

            if operatorOwner is None:
                raise Exception("Solver '" + kOperator.getName() + "' has no outputs!")

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
                        raise Exception("Operator '"+kOperator.getName()+"' or type '"+solverTypeName+"' arg '"+arg.name+"' not connected.");

                    connectionTargets = ""
                    for i in range(len(connectedObjects)):
                        dccSceneItem = self._getDCCSceneItem(connectedObjects[i])

                        if dccSceneItem is None:
                            raise Exception("Operator '"+kOperator.getName()+"' or type '"+solverTypeName+"' arg '"+arg.name+"' connection is invalid");

                        if i==0:
                            connectionTargets = dccSceneItem.FullName + connectionSuffix
                        else:
                            connectionTargets = connectionTargets + "," + dccSceneItem.FullName + connectionSuffix
                else:
                    if connectedObjects is None:
                        raise Exception("Operator '"+kOperator.getName()+"' or type '"+solverTypeName+"' arg '"+arg.name+"' not connected.");

                    dccSceneItem = self._getDCCSceneItem(connectedObjects)

                    if dccSceneItem is None:
                        raise Exception("Operator '"+kOperator.getName()+"' or type '"+solverTypeName+"' arg '"+arg.name+"' connection is invalid.");

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

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        # Lock Rotation
        if kSceneItem.testFlag("lockXRotation") is True:
            dccSceneItem.rotx.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.rotx.SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockYRotation") is True:
            dccSceneItem.roty.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.roty.SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockZRotation") is True:
            dccSceneItem.rotz.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.rotz.SetCapabilityFlag(constants.siKeyable, False)

        # Lock Scale
        if kSceneItem.testFlag("lockXScale") is True:
            dccSceneItem.sclx.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.sclx.SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockYScale") is True:
            dccSceneItem.scly.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.scly.SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockZScale") is True:
            dccSceneItem.sclz.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.sclz.SetCapabilityFlag(constants.siKeyable, False)

        # Lock Translation
        if kSceneItem.testFlag("lockXTranslation") is True:
            dccSceneItem.posx.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.posx.SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockYTranslation") is True:
            dccSceneItem.posy.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.posy.SetCapabilityFlag(constants.siKeyable, False)

        if kSceneItem.testFlag("lockZTranslation") is True:
            dccSceneItem.posz.SetLock(constants.siLockLevelManipulation)
            dccSceneItem.posz.SetCapabilityFlag(constants.siKeyable, False)

        return True


    # ===================
    # Visibility Methods
    # ===================
    def setVisibility(self, kSceneItem):
        """Sets the visibility of the object after its been created.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

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
        dccSceneItem = self._getDCCSceneItem(kSceneItem)
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

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

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