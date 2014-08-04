"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

from kraken.core.builders.base_builder import BaseBuilder
from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.attributes.base_attribute import BaseAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.plugins.maya_plugin.utils import *

import FabricEngine.Core as core


class Builder(BaseBuilder):
    """Builder object for building Kraken objects in Maya."""

    def __init__(self):
        super(Builder, self).__init__()


    # ========================
    # SceneItem Build Methods
    # ========================
    def buildContainer(self, kSceneItem):
        """Builds a container / namespace object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a container to be built.

        Return:
        Node that is created..

        """

        buildName = kSceneItem.getBuildName()

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLayer(self, kSceneItem):
        """Builds a layer object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a layer to be built.

        Return:
        Node that is created..

        """

        buildName = kSceneItem.getBuildName()

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildHierarchyGroup(self, kSceneItem):
        """Builds a hierarchy group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.

        Return:
        DCC Scene Item that is created.

        """

        buildName = kSceneItem.getBuildName()

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        lockObjXfo(dccSceneItem)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildGroup(self, kSceneItem):
        """Builds a group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.

        Return:
        Node that is created.

        """

        buildName = kSceneItem.getBuildName()

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildJoint(self, kSceneItem):
        """Builds a joint object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a joint to be built.

        Return:
        DCC Scene Item that is created.

        """

        buildName = kSceneItem.getBuildName()

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.joint(name="joint")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLocator(self, kSceneItem):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, locator / null object to be built.

        Return:
        Node that is created.

        """

        buildName = kSceneItem.getBuildName()

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.spaceLocator(name="locator")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildCurve(self, kSceneItem):
        """Builds a Curve object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a curve to be built.

        Return:
        Node that is created.

        """

        buildName = kSceneItem.getBuildName()

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        # Format points for Maya
        points = kSceneItem.getControlPoints()

        # Scale, rotate, translation shape
        curvePoints = []
        for eachSubCurve in points:
            formattedPoints = [x.toArray() for x in eachSubCurve]
            curvePoints.append(formattedPoints)

        mainCurve = None
        for i, eachSubCurve in enumerate(curvePoints):
            currentSubCurve = pm.curve(per=False, point=curvePoints[i], degree=1) #, knot=[x for x in xrange(len(curvePoints[i]))])

            if kSceneItem.getCurveSectionClosed(i):
                pm.closeCurve(currentSubCurve, preserveShape=True, replaceOriginal=True)

            if mainCurve is None:
                mainCurve = currentSubCurve

            if i > 0:
                pm.parent(currentSubCurve.getShape(), mainCurve, relative=True, shape=True)
                pm.delete(currentSubCurve)

        dccSceneItem = mainCurve
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

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

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="bool", defaultValue=kAttribute.getValue(), keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        print dccSceneItem

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildFloatAttribute(self, kAttribute):
        """Builds a Float attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a float attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="float", defaultValue=kAttribute.getValue(), minValue=kAttribute.min, maxValue=kAttribute.max, keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a integer attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="long", defaultValue=kAttribute.getValue(), minValue=kAttribute.min, maxValue=kAttribute.max, keyable=True)
        parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Arguments:
        kAttribute -- Object, kAttribute that represents a string attribute to be built.

        Return:
        True if successful.

        """

        parentDCCSceneItem = self._getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), dataType="string")
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem.set(kAttribute.getValue())

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
        if groupName == "":
            groupName = "Settings"

        parentDCCSceneItem.addAttr(groupName, niceName=groupName, attributeType="enum", enumName="-----", keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(groupName)
        pm.setAttr(parentDCCSceneItem + "." + groupName, lock=True)

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
            print kAttribute.getFullName()
            print self._getDCCSceneItem(kAttribute.getConnection())
            print self._getDCCSceneItem(kAttribute)

            driver = self._getDCCSceneItem(kAttribute.getConnection())
            driven = self._getDCCSceneItem(kAttribute)

            pm.connectAttr(driver, driven, force=True)

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
        dccSceneItem = pm.orientConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_ori_cns", maintainOffset=kConstraint.getMaintainOffset())
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
        dccSceneItem = pm.parentConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_par_cns", maintainOffset=kConstraint.getMaintainOffset())
        pm.scaleConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_scl_cns", maintainOffset=kConstraint.getMaintainOffset())

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
        dccSceneItem = pm.pointConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_pos_cns", maintainOffset=kConstraint.getMaintainOffset())
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
        dccSceneItem = pm.scaleConstraint([self._getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_scl_cns", maintainOffset=kConstraint.getMaintainOffset())
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

        sourceDCCSceneItem = self._getDCCSceneItem(kConnection.getSource())
        targetDCCSceneItem = self._getDCCSceneItem(kConnection.getTarget())

        pm.connectAttr(sourceDCCSceneItem, targetDCCSceneItem, force=True)

        return None


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
            # Get or construct a Fabric Engine client
            contextID = cmds.fabricSplice('getClientContextID')
            if contextID == '':
                cmds.fabricSplice('constructClient')
                contextID = cmds.fabricSplice('getClientContextID')

            # Connect the Python client to the Softimage client.
            client = core.createClient({"contextID": contextID})

            # Get the extension to load and create an instance of the object.
            extension = kOperator.getExtension()
            client.loadExtension(extension)

            client.loadExtension('KrakenSolver')
            client.loadExtension('KrakenSolverArg')

            solverTypeName = kOperator.getSolverTypeName()
            klType = getattr(client.RT.types, solverTypeName)

            try:
                # Test if object
                solver = klType.create()
            except:
                # Else is struct
                solver = klType()

            # Create Splice Operator
            spliceNode = pm.createNode('spliceMayaNode', name=kOperator.getName() + "_SpliceOp")

            # Add the private/non-mayaAttr port that stores the Solver object
            cmds.fabricSplice("addIOPort", spliceNode, "{\"portName\":\"solver\", \"dataType\":\"" + solverTypeName + "\", \"extension\":\"" + kOperator.getExtension() + "\", \"addMayaAttr\": false}")

            # Start constructing the source code.
            opSourceCode = ""
            opSourceCode += "require KrakenSolver;\n"
            opSourceCode += "require KrakenSolverArg;\n"
            opSourceCode += "require " + kOperator.getExtension() + ";\n\n"
            opSourceCode += "operator " + kOperator.getName() + "(\n"

            opSourceCode += "    io " + solverTypeName + " solver,\n"

            # Get the args from the solver KL object.
            args = solver.getArguments('KrakenSolverArg[]')

            functionCall = "    solver.solve("
            for i in range(len(args)):
                arg = args[i]

                # Get the argument's input from the DCC
                try:
                    opObject = kOperator.getInput(arg.name)
                    targetObject = self._getDCCSceneItem(kOperator.getInput(arg.name))
                except:
                    opObject = kOperator.getOutput(arg.name)
                    targetObject = self._getDCCSceneItem(kOperator.getOutput(arg.name))

                # Add the splice Port for each arg.
                if arg.connectionType == 'in':
                    cmds.fabricSplice("addInputPort", spliceNode, "{\"portName\":\"" + arg.name + "\", \"dataType\":\"" + arg.dataType + "\", \"extension\":\"\", \"addMayaAttr\": true}", "")

                    if isinstance(opObject, BaseAttribute):
                        targetObject.connect(spliceNode.attr(arg.name))
                    elif isinstance(opObject, SceneItem):
                        targetObject.attr('worldMatrix').connect(spliceNode.attr(arg.name))
                    else:
                        raise Exception(opObject.getFullName() + " with type '" + opObject.getKType() + " is not implemented!")


                elif arg.connectionType in ['io', 'out']:
                    cmds.fabricSplice("addOutputPort", spliceNode, "{\"portName\":\"" + arg.name + "\", \"dataType\":\"" + arg.dataType + "\", \"extension\":\"\", \"addMayaAttr\": true}", "")

                    if opObject.getKType().endswith('Attribute'):
                        spliceNode.attr(arg.name).connect(targetObject)

                    elif opObject.getKType().endswith('Locator'): # Change to isinstance() check
                        decomposeNode = pm.createNode('decomposeMatrix')
                        spliceNode.attr(arg.name).connect(decomposeNode.attr("inputMatrix"))

                        decomposeNode.attr("outputRotate").connect(targetObject.attr("rotate"))
                        decomposeNode.attr("outputScale").connect(targetObject.attr("scale"))
                        decomposeNode.attr("outputTranslate").connect(targetObject.attr("translate"))


                # Connect the ports to the inputs/outputs in the rig.
                opSourceCode += "    " + arg.connectionType + " " + arg.dataType + " " + arg.name
                if i == len(args) - 1:
                    opSourceCode += "\n"
                else:
                    opSourceCode += ",\n"

                if i == len(args) - 1:
                    functionCall += arg.name
                else:
                    functionCall += arg.name + ", "

            opSourceCode += "    )\n"
            opSourceCode += "{\n"
            opSourceCode += functionCall + ");\n"
            opSourceCode += "}\n"

            cmds.fabricSplice('addKLOperator', spliceNode, '{"opName": "' + kOperator.getName() + '"}', opSourceCode)

        finally:
            cmds.fabricSplice('destroyClient')

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

            # Get shape node, if it exists, hide it.
            shape = dccSceneItem.getShape()
            if shape is not None:
                shape.visibility.set(False)

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

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        objectColor = kSceneItem.getColor()
        if objectColor not in self.VALID_COLORS.keys():
            return False

        dccSceneItem.overrideEnabled.set(True)
        dccSceneItem.overrideColor.set(self.VALID_COLORS[objectColor][0])

        return True


    # ==================
    # Transform Methods
    # ==================
    def setTransform(self, kSceneItem):
        """Translates the transform to Maya transform.

        Arguments:
        kSceneItem -- Object: object to set the transform on.

        Return:
        True if successful.

        """

        dccSceneItem = self._getDCCSceneItem(kSceneItem)

        quat = dt.Quaternion(kSceneItem.xfo.rot.v.x, kSceneItem.xfo.rot.v.y, kSceneItem.xfo.rot.v.z, kSceneItem.xfo.rot.w)
        dccSceneItem.setScale(dt.Vector(kSceneItem.xfo.scl.x, kSceneItem.xfo.scl.y, kSceneItem.xfo.scl.z))
        dccSceneItem.setTranslation(dt.Vector(kSceneItem.xfo.tr.x, kSceneItem.xfo.tr.y, kSceneItem.xfo.tr.z), "world")
        dccSceneItem.setRotation(quat, "world")

        pm.select(clear=True)

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

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
        True if successful.

        """

        return True