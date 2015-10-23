"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

import json

from kraken.core.kraken_system import ks
from kraken.core.builder import Builder
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.plugins.maya_plugin.utils import *

import FabricEngine.Core as core

import maya.cmds as cmds


class Builder(Builder):
    """Builder object for building Kraken objects in Maya."""

    def __init__(self):
        super(Builder, self).__init__()


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

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        pm.refresh()

        return dccSceneItem


    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Args:
            kSceneItem (Object): kSceneItem that represents a layer to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        pm.refresh()

        return dccSceneItem


    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Args:
            kSceneItem (Object): kSceneItem that represents a group to be built.
            buildName (str): The name to use on the built object.

        Return:
            object: DCC Scene Item that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        pm.refresh()

        return dccSceneItem


    def buildGroup(self, kSceneItem, buildName):
        """Builds a group object.

        Args:
            kSceneItem (Object): kSceneItem that represents a group to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        pm.refresh()

        return dccSceneItem


    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Args:
            kSceneItem (Object): kSceneItem that represents a joint to be built.
            buildName (str): The name to use on the built object.

        Return:
            object: DCC Scene Item that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.joint(name="joint")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        pm.refresh()

        return dccSceneItem


    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Args:
            kSceneItem (Object): locator / null object to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.spaceLocator(name="locator")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        pm.refresh()

        return dccSceneItem


    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Args:
            kSceneItem (Object): kSceneItem that represents a curve to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

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

        pm.refresh()

        return dccSceneItem


    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Args:
            kSceneItem (Object): kSceneItem that represents a control to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

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

        pm.refresh()

        return dccSceneItem


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

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="bool", defaultValue=kAttribute.getValue(), keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (Object): kAttribute that represents a float attribute to be built.

        Return:
            bool: True if successful.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="float", defaultValue=kAttribute.getValue(), keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        if kAttribute.getMin() is not None:
            dccSceneItem.setMin(kAttribute.getMin())

        if kAttribute.getMax() is not None:
            dccSceneItem.setMax(kAttribute.getMax())

        if kAttribute.getUIMin() is not None:
            dccSceneItem.setSoftMin(kAttribute.getUIMin())

        if kAttribute.getUIMax() is not None:
            dccSceneItem.setSoftMax(kAttribute.getUIMax())

        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (Object): kAttribute that represents a integer attribute to be built.

        Return:
            bool: True if successful.

        """

        mininum = kAttribute.getMin()
        if mininum == None:
            mininum = 0

        maximum = kAttribute.getMax()
        if maximum == None:
            maximum = kAttribute.getValue() * 2

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="long", defaultValue=kAttribute.getValue(), minValue=mininum, maxValue=maximum, keyable=True)
        parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        if kAttribute.getMin() is not None:
            dccSceneItem.setMin(kAttribute.getMin())

        if kAttribute.getMax() is not None:
            dccSceneItem.setMax(kAttribute.getMax())

        if kAttribute.getUIMin() is not None:
            dccSceneItem.setSoftMin(kAttribute.getUIMin())

        if kAttribute.getUIMax() is not None:
            dccSceneItem.setSoftMax(kAttribute.getUIMax())

        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (Object): kAttribute that represents a string attribute to be built.

        Return:
            bool: True if successful.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), dataType="string")
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem.set(kAttribute.getValue())
        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True


    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Args:
            kAttributeGroup (object): Kraken object to build the attribute group on.

        Return:
            bool: True if successful.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kAttributeGroup.getParent())

        groupName = kAttributeGroup.getName()
        parentDCCSceneItem.addAttr(groupName, niceName=groupName, attributeType="enum", enumName="-----", keyable=True)
        dccSceneItem = parentDCCSceneItem.attr(groupName)
        pm.setAttr(parentDCCSceneItem + "." + groupName, lock=True)

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
            kAttribute (Object): Attribute to connect.

        Return:
            bool: True if successful.

        """

        if kAttribute.isConnected() is True:

            driver = self.getDCCSceneItem(kAttribute.getConnection())
            driven = self.getDCCSceneItem(kAttribute)

            pm.connectAttr(driver, driven, force=True)

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

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.orientConstraint([self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_ori_cns", maintainOffset=kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPoseConstraint(self, kConstraint):
        """Builds an pose constraint represented by the kConstraint.

        Args:
            kConstraint (Object): kraken constraint object to build.

        Return:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.parentConstraint([self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_par_cns", maintainOffset=kConstraint.getMaintainOffset())
        pm.scaleConstraint([self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_scl_cns", maintainOffset=kConstraint.getMaintainOffset())

        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.pointConstraint([self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_pos_cns", maintainOffset=kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


    def buildScaleConstraint(self, kConstraint):
        """Builds an scale constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.scaleConstraint([self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()], constraineeDCCSceneItem, name=kConstraint.getName() + "_scl_cns", maintainOffset=kConstraint.getMaintainOffset())
        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem


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

        pm.connectAttr(connectionTargetDCCSceneItem, targetDCCSceneItem, force=True)

        return True


    # =========================
    # Operator Builder Methods
    # =========================
    def buildSpliceOperators(self, kOperator):
        """Builds Splice Operators on the components.

        Args:
            kOperator (Object): Kraken operator that represents a Splice operator.

        Return:
            bool: True if successful.

        """

        try:
            solverTypeName = kOperator.getSolverTypeName()

            # Create Splice Operator
            spliceNode = cmds.createNode('dfgMayaNode', name=kOperator.getName())
            cmds.FabricCanvasSetExtDeps(mayaNode=spliceNode, execPath="", extDep="Kraken" )

            cmds.FabricCanvasAddFunc(mayaNode=spliceNode, execPath="", title=kOperator.getName(), code="dfgEntry {}", xPos="100", yPos="100")
            cmds.FabricCanvasAddPort(mayaNode=spliceNode, execPath=kOperator.getName(), desiredPortName="solver", portType="IO", typeSpec=solverTypeName, connectToPortPath="", extDep="Kraken")
            cmds.FabricCanvasAddPort(mayaNode=spliceNode, execPath="", desiredPortName="solver", portType="IO", typeSpec=solverTypeName, connectToPortPath="", extDep="Kraken" )
            cmds.FabricCanvasConnect(mayaNode=spliceNode, execPath="", srcPortPath="solver", dstPortPath=kOperator.getName()+".solver")
            cmds.FabricCanvasConnect(mayaNode=spliceNode, execPath="", srcPortPath=kOperator.getName()+".solver", dstPortPath="solver")

            arraySizes = {}
            # connect the operator to the objects in the DCC
            args = kOperator.getSolverArgs()
            for i in xrange(len(args)):
                arg = args[i]
                argName = arg.name.getSimpleType()
                argDataType = arg.dataType.getSimpleType()
                argConnectionType = arg.connectionType.getSimpleType()

                if argConnectionType == 'in':
                    cmds.FabricCanvasAddPort(mayaNode=spliceNode, execPath="", desiredPortName=argName, portType="In", typeSpec=argDataType, connectToPortPath="")
                    cmds.FabricCanvasAddPort(mayaNode=spliceNode, execPath=kOperator.getName(), desiredPortName=argName, portType="In", typeSpec=argDataType, connectToPortPath="")
                    cmds.FabricCanvasConnect(mayaNode=spliceNode, execPath="", srcPortPath=argName, dstPortPath=kOperator.getName()+"."+argName)
                elif argConnectionType in ['io', 'out']:
                    cmds.FabricCanvasAddPort(mayaNode=spliceNode, execPath="", desiredPortName=argName, portType="Out", typeSpec=argDataType, connectToPortPath="")
                    cmds.FabricCanvasAddPort(mayaNode=spliceNode, execPath=kOperator.getName(), desiredPortName=argName, portType="Out", typeSpec=argDataType, connectToPortPath="")
                    cmds.FabricCanvasConnect(mayaNode=spliceNode, execPath="", srcPortPath=kOperator.getName()+"."+argName, dstPortPath=argName)

                if argDataType == 'EvalContext':
                    continue
                if argName == 'time':
                    cmds.expression( o=spliceNode + '.time', s=spliceNode + '.time = time;' )
                    continue
                if argName == 'frame':
                    cmds.expression( o=spliceNode + '.frame', s=spliceNode + '.frame = frame;' )
                    continue

                # Get the argument's input from the DCC
                if argConnectionType == 'in':
                    connectedObjects = kOperator.getInput(argName)
                elif argConnectionType in ['io', 'out']:
                    connectedObjects = kOperator.getOutput(argName)

                if argDataType.endswith('[]'):

                    # In SpliceMaya, output arrays are not resized by the system prior to calling into Splice, so we
                    # explicily resize the arrays in the generated operator stub code.
                    if argConnectionType in ['io', 'out']:
                        arraySizes[argName] = len(connectedObjects)

                    if len(connectedObjects) == 0:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' not connected.");

                    connectionTargets = []
                    for i in range(len(connectedObjects)):
                        opObject = connectedObjects[i]
                        dccSceneItem = self.getDCCSceneItem(opObject)

                        if dccSceneItem is None:
                            raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' dcc item not found for item:" + opObject.getPath());
                        connectionTargets.append( { 'opObject': opObject, 'dccSceneItem': dccSceneItem} )
                else:
                    if connectedObjects is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' not connected.");

                    opObject = connectedObjects
                    dccSceneItem = self.getDCCSceneItem(opObject)

                    if dccSceneItem is None:
                        raise Exception("Operator '"+kOperator.getName()+"' of type '"+solverTypeName+"' arg '"+argName+"' dcc item not found for item:" + connectedObjects.getPath());

                    connectionTargets = { 'opObject': opObject, 'dccSceneItem': dccSceneItem }

                # Add the splice Port for each arg.
                if argConnectionType == 'in':

                    def connectInput(tgt, opObject, dccSceneItem):
                        if isinstance(opObject, Attribute):
                            cmds.connectAttr(str(dccSceneItem), tgt)
                        elif isinstance(opObject, Object3D):
                            cmds.connectAttr(str(dccSceneItem.attr('worldMatrix')), tgt)
                        else:
                            raise Exception(opObject.getPath() + " with type '" + opObject.getTypeName() + " is not implemented!")

                    if argDataType.endswith('[]'):
                        for i in range(len(connectionTargets)):
                            connectInput( spliceNode + "." + argName+'['+str(i)+']', connectionTargets[i]['opObject'], connectionTargets[i]['dccSceneItem'])
                    else:
                        connectInput( spliceNode + "." + argName, connectionTargets['opObject'], connectionTargets['dccSceneItem'])

                elif argConnectionType in ['io', 'out']:

                    def connectOutput(src, opObject, dccSceneItem):
                        if isinstance(opObject, Attribute):
                            cmds.connectAttr(src, str(dccSceneItem))

                        elif isinstance(opObject, Object3D):
                            decomposeNode = pm.createNode('decomposeMatrix')
                            cmds.connectAttr(src, str(decomposeNode.attr("inputMatrix")))

                            decomposeNode.attr("outputRotate").connect(dccSceneItem.attr("rotate"))
                            decomposeNode.attr("outputScale").connect(dccSceneItem.attr("scale"))
                            decomposeNode.attr("outputTranslate").connect(dccSceneItem.attr("translate"))

                    if argDataType.endswith('[]'):
                        for i in range(len(connectionTargets)):
                            connectOutput(str(spliceNode + "." + argName)+'['+str(i)+']', connectionTargets[i]['opObject'], connectionTargets[i]['dccSceneItem'])
                    else:
                        connectOutput(str(spliceNode + "." + argName), connectionTargets['opObject'], connectionTargets['dccSceneItem'])


            opSourceCode = kOperator.generateSourceCode(arraySizes=arraySizes)
            cmds.FabricCanvasSetCode(mayaNode=spliceNode, execPath=kOperator.getName(), code=opSourceCode)

        finally:
            pass

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

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

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

        Args:
            kSceneItem (Object): The scene item to set the visibility on.

        Return:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

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

        Args:
            kSceneItem (Object): kraken object to set the color on.

        Return:
            bool: True if successful.

        """

        colors = self.config.getColors()
        dccSceneItem = self.getDCCSceneItem(kSceneItem)
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

        Args:
            kSceneItem -- Object: object to set the transform on.

        Return:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        quat = dt.Quaternion(kSceneItem.xfo.ori.v.x, kSceneItem.xfo.ori.v.y, kSceneItem.xfo.ori.v.z, kSceneItem.xfo.ori.w)
        dccSceneItem.setScale(dt.Vector(kSceneItem.xfo.sc.x, kSceneItem.xfo.sc.y, kSceneItem.xfo.sc.z))
        dccSceneItem.setTranslation(dt.Vector(kSceneItem.xfo.tr.x, kSceneItem.xfo.tr.y, kSceneItem.xfo.tr.z), "world")
        dccSceneItem.setRotation(quat, "world")

        dccSceneItem.setRotationOrder(kSceneItem.ro.order + 1, False)

        pm.select(clear=True)

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

        return True


    def _postBuild(self):
        """Post-Build commands.

        Return:
            bool: True if successful.

        """

        return True
