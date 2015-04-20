"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""
from kraken.core.kraken_system import ks
from kraken.core.builders.builder import Builder
from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.plugins.maya_plugin.utils import *

import FabricEngine.Core as core
import json
from maya import cmds

class Builder(Builder):
    """Builder object for building Kraken objects in Maya."""

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

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

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

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

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

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildGroup(self, kSceneItem, buildName):
        """Builds a group object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a group to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

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

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.joint(name="joint")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem


    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Arguments:
        kSceneItem -- Object, locator / null object to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.spaceLocator(name="locator")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

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

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        # Format points for Maya
        curveData = kSceneItem.getCurveData()

        # Scale, rotate, translation shape
        curvePoints = []
        for eachSubCurve in curveData:
            formattedPoints = eachSubCurve["points"]
            curvePoints.append(formattedPoints)

        mainCurve = None
        for i, eachSubCurve in enumerate(curvePoints):
            closedSubCurve = curveData[i]["closed"]
            degreeSubCurve = curveData[i]["degree"]

            currentSubCurve = pm.curve(per=False, point=curvePoints[i], degree=degreeSubCurve)

            if closedSubCurve:
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


    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Arguments:
        kSceneItem -- Object, kSceneItem that represents a control to be built.
        buildName -- String, The name to use on the built object.

        Return:
        Node that is created.

        """

        parentNode = self._getDCCSceneItem(kSceneItem.getParent())

        # Format points for Maya
        curveData = kSceneItem.getCurveData()

        # Scale, rotate, translation shape
        curvePoints = []
        for eachSubCurve in curveData:
            formattedPoints = eachSubCurve["points"]
            curvePoints.append(formattedPoints)

        mainCurve = None
        for i, eachSubCurve in enumerate(curvePoints):
            closedSubCurve = curveData[i]["closed"]
            degreeSubCurve = curveData[i]["degree"]

            currentSubCurve = pm.curve(per=False, point=curvePoints[i], degree=degreeSubCurve)

            if closedSubCurve:
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
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="float", defaultValue=kAttribute.getValue(), keyable=True)

        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        if kAttribute.min is not None:
            dccSceneItem.setMin(kAttribute.min)

        if kAttribute.max is not None:
            dccSceneItem.setMax(kAttribute.max)

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
            solverTypeName = kOperator.getSolverTypeName()

            # Create Splice Operator
            spliceNode = pm.createNode('spliceMayaNode', name=kOperator.getName() + "_SpliceOp")

            # Add the private/non-mayaAttr port that stores the Solver object
            cmds.fabricSplice("addIOPort", spliceNode, "{\"portName\":\"solver\", \"dataType\":\"" + solverTypeName + "\", \"extension\":\"" + kOperator.getExtension() + "\", \"addMayaAttr\": false}")

            arraySizes = {}
            # connect the operator to the objects in the DCC
            args = kOperator.getSolverArgs()
            for i in xrange(len(args)):
                arg = args[i]

                portArgs = {"portName": arg.name, "dataType": arg.dataType, "extension":"", "addMayaAttr": True }

                # Get the argument's input from the DCC
                # Note: this used to be a try/catch statement, which seemed quite strange to me.
                # I've replaced with a proper test with an exception if the item is not found.
                if arg.connectionType == 'in':
                    connectedObjects = kOperator.getInput(arg.name)
                elif arg.connectionType in ['io', 'out']:
                    connectedObjects = kOperator.getOutput(arg.name)

                if arg.dataType.endswith('[]'):
                    portArgs['arrayType'] = "Array (Multi)"

                    # In SpliceMaya, output arrays are not resized by the system prior to calling into Splice, so we
                    # explicily resize the arrays in the generated operator stub code.
                    if arg.connectionType in ['io', 'out']:
                        arraySizes[arg.name] = len(connectedObjects)

                    if len(connectedObjects) == 0:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' not connected.");

                    connectionTargets = []
                    for i in range(len(connectedObjects)):
                        opObject = connectedObjects[i]
                        dccSceneItem = self._getDCCSceneItem(opObject)

                        if dccSceneItem is None:
                            raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' dcc item not found for item:" + opObject.getFullName());
                        connectionTargets.append( { 'opObject': opObject, 'dccSceneItem': dccSceneItem} )
                else:
                    if connectedObjects is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' not connected.");

                    opObject = connectedObjects
                    dccSceneItem = self._getDCCSceneItem(opObject)

                    if dccSceneItem is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+arg.name+"' dcc item not found for item:" + connectedObjects.getFullName());

                    connectionTargets = { 'opObject': opObject, 'dccSceneItem': dccSceneItem }

                # Add the splice Port for each arg.
                if arg.connectionType == 'in':
                    cmds.fabricSplice("addInputPort", spliceNode, json.dumps(portArgs), "")

                    def connectInput(tgt, opObject, dccSceneItem):
                        if isinstance(opObject, Attribute):
                            cmds.connectAttr(str(dccSceneItem), tgt)
                        elif isinstance(opObject, SceneItem):
                            cmds.connectAttr(str(dccSceneItem.attr('worldMatrix')), tgt)
                        else:
                            raise Exception(opObject.getFullName() + " with type '" + opObject.getTypeName() + " is not implemented!")

                    if arg.dataType.endswith('[]'):
                        for i in range(len(connectionTargets)):
                            connectInput(str(spliceNode.attr(arg.name))+'['+str(i)+']', connectionTargets[i]['opObject'], connectionTargets[i]['dccSceneItem'])
                    else:
                        connectInput(str(spliceNode.attr(arg.name)), connectionTargets['opObject'], connectionTargets['dccSceneItem'])

                elif arg.connectionType in ['io', 'out']:
                    cmds.fabricSplice("addOutputPort", spliceNode, json.dumps(portArgs), "")

                    def connectOutput(src, opObject, dccSceneItem):
                        if isinstance(opObject, Attribute):
                            cmds.connectAttr(src, str(dccSceneItem))

                        elif isinstance(opObject, SceneItem):
                            decomposeNode = pm.createNode('decomposeMatrix')
                            cmds.connectAttr(src, str(decomposeNode.attr("inputMatrix")))

                            decomposeNode.attr("outputRotate").connect(dccSceneItem.attr("rotate"))
                            decomposeNode.attr("outputScale").connect(dccSceneItem.attr("scale"))
                            decomposeNode.attr("outputTranslate").connect(dccSceneItem.attr("translate"))


                    if arg.dataType.endswith('[]'):
                        for i in range(len(connectionTargets)):
                            connectOutput(str(spliceNode.attr(arg.name))+'['+str(i)+']', connectionTargets[i]['opObject'], connectionTargets[i]['dccSceneItem'])
                    else:
                        connectOutput(str(spliceNode.attr(arg.name)), connectionTargets['opObject'], connectionTargets['dccSceneItem'])

            # Generate the operator source code.
            opSourceCode = kOperator.generateSourceCode(arraySizes=arraySizes)

            cmds.fabricSplice('addKLOperator', spliceNode, '{"opName": "' + kOperator.getName() + '"}', opSourceCode)

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
            pm.setAttr(dccSceneItem.longName() + "." + 'rx', lock=True, keyable=False, channelBox=False)

        if kSceneItem.testFlag("lockYRotation") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'ry', lock=True, keyable=False, channelBox=False)

        if kSceneItem.testFlag("lockZRotation") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'rz', lock=True, keyable=False, channelBox=False)


        # Lock Scale
        if kSceneItem.testFlag("lockXScale") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'sx', lock=True, keyable=False, channelBox=False)

        if kSceneItem.testFlag("lockYScale") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'sy', lock=True, keyable=False, channelBox=False)

        if kSceneItem.testFlag("lockZScale") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'sz', lock=True, keyable=False, channelBox=False)


        # Lock Translation
        if kSceneItem.testFlag("lockXTranslation") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'tx', lock=True, keyable=False, channelBox=False)

        if kSceneItem.testFlag("lockYTranslation") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'ty', lock=True, keyable=False, channelBox=False)

        if kSceneItem.testFlag("lockZTranslation") is True:
            pm.setAttr(dccSceneItem.longName() + "." + 'tz', lock=True, keyable=False, channelBox=False)

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

        colors = self.config.getColors()
        dccSceneItem = self._getDCCSceneItem(kSceneItem)
        buildColor = self.getBuildColor(kSceneItem)

        if buildColor is not None:
            dccSceneItem.overrideEnabled.set(True)
            dccSceneItem.overrideColor.set(colors[buildColor][0])

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

        quat = dt.Quaternion(kSceneItem.xfo.ori.v.x, kSceneItem.xfo.ori.v.y, kSceneItem.xfo.ori.v.z, kSceneItem.xfo.ori.w)
        dccSceneItem.setScale(dt.Vector(kSceneItem.xfo.sc.x, kSceneItem.xfo.sc.y, kSceneItem.xfo.sc.z))
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
