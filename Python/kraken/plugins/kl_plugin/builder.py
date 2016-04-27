"""Kraken KL - KL Builder module.

Classes:
Builder -- Component representation.

"""

import os
import json

from kraken.core.kraken_system import ks
from kraken.core.builder import Builder
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.control import Control
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.joint import Joint
from kraken.core.objects.rig import Rig
from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.components.component_input import ComponentInput
from kraken.core.objects.components.component_output import ComponentOutput
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.objects.operators.operator import Operator
from kraken.core.objects.operators.kl_operator import KLOperator
from kraken.core.objects.operators.canvas_operator import CanvasOperator
from kraken.core.objects.constraints.constraint import Constraint
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.color import Color
from kraken.core.maths.xfo import Xfo

from kraken.plugins.canvas_plugin.graph_manager import GraphManager

import FabricEngine.Core as core

def Boolean(b):
  return str(b).lower()

class Builder(Builder):
    """Builder object for building Kraken objects in KL."""

    __debugMode = None
    __outputFolder = None
    __rigTitle = None
    __canvasGraph = None
    __names = None
    __pathToName = None
    __klMembers = None
    __klObjects = None
    __klAttributes = None
    __klConstraints = None
    __klSolvers = None
    __klCanvasOps = None
    __klPreCode = None
    __klExtExecuted = None
    __krkItems = None
    __krkAttributes = None
    __krkDeformers = None
    __krkVisitedObjects = None

    def __init__(self):
        super(Builder, self).__init__()

    def report(self, message):
        print "KL Builder: %s" % str(message)

    def reportError(self, error):
        self.report("Error: "+str(error))

    def hasOption(self, option):
        return self.getConfig().getMetaData(option, False)

    # ========================
    # IO Methods
    # ========================
    def setOutputFolder(self, folder):
        self.__outputFolder = folder

    # ========================
    # KL related Methods
    # ========================

    def getUniqueName(self, item, earlyExit = False):
        if self.__pathToName.has_key(item.getDecoratedPath()):
            return self.__pathToName[item.getDecoratedPath()]
        name = None
        if isinstance(item, AttributeGroup):
            name = self.getUniqueName(item.getParent(), earlyExit = True) + '_' + item.getName()
        elif isinstance(item, Attribute):
            name = self.getUniqueName(item.getParent(), earlyExit = True) + '_' + item.getName()
        elif hasattr(item, 'getBuildName'):
            name = item.getBuildName()
        else:
            name = item.getName()

        component = ''
        layer = ''
        if hasattr(item, 'getComponent'):
            if item.getComponent():
                component = item.getComponent().getBuildName().replace('_', '') + '_'
        if hasattr(item, 'getLayer'):
            if item.getLayer():
                layer = item.getLayer().getName().replace('_', '') + '_'

        if isinstance(item, CtrlSpace) and not name.lower().endswith('space'):
            name = name + 'Space'
        elif isinstance(item, ComponentInput) and not name.lower().endswith('in'):
            name = name + 'In'
        elif isinstance(item, ComponentOutput) and not name.lower().endswith('out'):
            name = name + 'Out'

        if layer == '' and component == '':
            name = item.getDecoratedPath()
            if name.find('.') > -1:
                name = name.partition('.')[2]
            name = name.replace('.', '_').replace(':', '_')
        else:
          name = layer + component + name

        if earlyExit:
            return name

        namePrefix = name
        nameSuffix = 1
        while self.__names.has_key(name):
            nameSuffix = nameSuffix + 1
            name = namePrefix + str(nameSuffix)

        self.__names[name] = item.getDecoratedPath()
        self.__pathToName[item.getDecoratedPath()] = name

        return name

    def __getXfoAsStr(self, xfo):
        valueStr = "Xfo(Vec3(%.4f, %.4f, %.4f), Quat(%.4f, %.4f, %.4f, %.4f), Vec3(%.4f, %.4f, %.4f))" % (
            round(xfo.tr.x, 4),
            round(xfo.tr.y, 4),
            round(xfo.tr.z, 4),
            round(xfo.ori.v.x, 4),
            round(xfo.ori.v.y, 4),
            round(xfo.ori.v.z, 4),
            round(xfo.ori.w, 4),
            round(xfo.sc.x, 4),
            round(xfo.sc.y, 4),
            round(xfo.sc.z, 4)
          )
        return valueStr

    def getKLExtensionName(self):
        return "KRK_" + self.__rigTitle.replace(' ', '')

    def __visitKLObject(self, item):
        
        kl = []
        if item['visited']:
            return kl
        item['visited'] = True

        member = item['member']
        driver = item['driver']

        if driver is None:
            kl += ["", "  // solving global transform %s" % member]
            kl += ["  this.%s.globalXfo = this.%s.xfo;" % (member, member)]
            self.__krkVisitedObjects.append(item);
            return kl

        driverObj = self.findKLObjectForSI(driver)
        if driverObj:
            kl += self.__visitKLObject(driverObj)
            kl += ["", "  // solving parent child constraint %s" % member]
            if self.__debugMode:
                kl += ["  report(\"solving parent child constraint %s\");" % member]
            kl += ["  this.%s.globalXfo = this.%s.globalXfo * this.%s.xfo;" % (member, driverObj['member'], member)]
            self.__krkVisitedObjects.append(item);
            return kl

        driverConstraint = self.findKLConstraint(driver)
        if driverConstraint:
            driverMember = driverConstraint['member']
            constraint = driverConstraint['sceneItem']
            for i in range(len(constraint.getConstrainers())):
                constrainer = constraint.getConstrainers()[i]
                constrainerObj = self.findKLObjectForSI(constrainer)
                kl += self.__visitKLObject(constrainerObj)

            kl += ["", "  // solving %s constraint %s" % (driverConstraint['sceneItem'].__class__.__name__, driverMember)]
            if self.__debugMode:
                kl += ["  report(\"solving %s constraint %s\");" % (driverConstraint['sceneItem'].__class__.__name__, driverMember)]
            for i in range(len(constraint.getConstrainers())):
                constrainer = constraint.getConstrainers()[i]
                constrainerObj = self.findKLObjectForSI(constrainer)
                kl += ['  this.%s.constrainers[%d] = this.%s.globalXfo;' % (driverMember, i, constrainerObj['member'])]

            constrainee = constraint.getConstrainee()
            constraineeObj = self.findKLObjectForSI(constrainee)

            kl += ['  this.%s.globalXfo = this.%s.compute(this.%s.globalXfo);' % (constraineeObj['member'], driverMember, constraineeObj['member'])]
            self.__krkVisitedObjects.append(driverConstraint);
            self.__krkVisitedObjects.append(item);
            return kl

        driverSolver = self.findKLSolver(driver)
        if driverSolver:
            driverMember = driverSolver['member']
            kOperator = driverSolver['sceneItem']
            args = kOperator.getSolverArgs()

            if not driverSolver.get('visited', False):
                driverSolver['visited'] = True

                kl += ["", "  // solving KLSolver %s" % (driverMember)]
                if self.__debugMode:
                    kl += ["  report(\"solving KLSolver %s\");" % (driverMember)]

                # first let's find all args which are arrays and prepare storage
                for i in xrange(len(args)):
                    arg = args[i]
                    argName = arg.name.getSimpleType()
                    argDataType = arg.dataType.getSimpleType()
                    argConnectionType = arg.connectionType.getSimpleType()
                    connectedObjects = None
                    argVarName = "%s_%s" % (driverMember, argName)
                    isArray = argDataType.endswith('[]')

                    if argConnectionType == 'In':
                        connectedObjects = kOperator.getInput(argName)
                    elif argConnectionType in ['IO', 'Out']:
                        connectedObjects = kOperator.getOutput(argName)

                    if isArray:
                        kl += ["  %s %s[](%d);" % (argDataType[:-2], argVarName, len(connectedObjects))]
                        if argConnectionType == 'Out':
                            continue
                        for j in xrange(len(connectedObjects)):
                            connected = connectedObjects[j]

                            if isinstance(connected, Attribute):
                                connectedObj = self.findKLAttribute(connected)
                                kl += ["  %s[%d] = this.%s.value;" % (argVarName, j, connectedObj['member'])]
                                continue
                            elif isinstance(connected, SceneItem):
                                connectedObj = self.findKLObjectForSI(connected)
                                kl += self.__visitKLObject(connectedObj)
                                if argDataType == "Mat44[]":
                                    kl += ["  %s[%d] = this.%s.globalXfo.toMat44();" % (argVarName, j, connectedObj['member'])]
                                else:
                                    kl += ["  %s[%d] = this.%s.globalXfo;" % (argVarName, j, connectedObj['member'])]
                            elif isinstance(connected, Xfo):
                                if argDataType == "Mat44[]":
                                    kl += ["  %s[%d] = %s.toMat44();" % (argVarName, j, self.__getXfoAsStr(connected))]
                                else:
                                    kl += ["  %s[%d] = %s;" % (argVarName, j, self.__getXfoAsStr(connected))]
                            elif isinstance(connected, str):
                                kl += ["  %s[%d] = \"%s\";" % (argVarName, j, connected)]
                            else:
                                kl += ["  %s[%d] = %s;" % (argVarName, j, str(connected))]
  
                        continue

                    if argConnectionType == 'Out':
                        kl += ["  %s %s;" % (argDataType, argVarName)]
                        continue

                    connected = connectedObjects
                    if isinstance(connected, Attribute):
                        connectedObj = self.findKLAttribute(connected)
                        kl += ["  %s %s = this.%s.value;" % (argDataType, argVarName, connectedObj['member'])]
                        continue

                    if isinstance(connected, SceneItem):
                        connectedObj = self.findKLObjectForSI(connected)
                        kl += self.__visitKLObject(connectedObj)

                        if argDataType == "Mat44":
                            kl += ["  %s %s = this.%s.globalXfo.toMat44();" % (argDataType, argVarName, connectedObj['member'])]
                        else:
                            kl += ["  %s %s = this.%s.globalXfo;" % (argDataType, argVarName, connectedObj['member'])]

                    elif isinstance(connected, Xfo):
                        if argDataType == "Mat44":
                            kl += ["  %s %s = %s.toMat44();" % (argDataType, argVarName, self.__getXfoAsStr(connected))]
                        else:
                            kl += ["  %s %s = %s;" % (argDataType, argVarName, self.__getXfoAsStr(connected))]
                    elif isinstance(connected, str):
                        kl += ["  %s %s = \"%s\";" % (argDataType, argVarName, connected)]
                    else:
                        kl += ["  %s %s = %s;" % (argDataType, argVarName, str(connected))]

                # perform the solve
                if self.__debugMode:
                    for i in xrange(len(args)):
                        arg = args[i]
                        argName = arg.name.getSimpleType()
                        argDataType = arg.dataType.getSimpleType()
                        argConnectionType = arg.connectionType.getSimpleType()
                        if argConnectionType != 'In':
                            continue
                        kl += ["  report(\"arg %s \" + %s_%s);" % (argName, driverMember, argName)]

                kl += ["  this.%s.solve(" % driverMember]
                for i in xrange(len(args)):
                    arg = args[i]
                    argName = arg.name.getSimpleType()
                    argVarName = "%s_%s" % (driverMember, argName)
                    comma = ""
                    if i < len(args) - 1:
                        comma = ","
                    kl += ["    %s%s" % (argVarName, comma)]

                kl += ["  );"]
                self.__krkVisitedObjects.append(driverSolver);

            # output to the results!
            for i in xrange(len(args)):
                arg = args[i]
                argName = arg.name.getSimpleType()
                argDataType = arg.dataType.getSimpleType()
                argConnectionType = arg.connectionType.getSimpleType()
                if argConnectionType == 'In':
                  continue
                argVarName = "%s_%s" % (driverMember, argName)
                connectedObjects = kOperator.getOutput(argName)
                if not argDataType.endswith('[]'):
                    connectedObjects = [connectedObjects]

                for j in xrange(len(connectedObjects)):
                    connected = connectedObjects[j]
                    if connected.getDecoratedPath() == item['sceneItem'].getDecoratedPath():
                        kl += ["", "  // retrieving value for %s from solver %s" % (member, driverMember)]
                        if argDataType.endswith('[]'):
                            kl += ["  this.%s.globalXfo = %s_%s[%d];" % (member, driverMember, argName, j)]
                        else:
                            kl += ["  this.%s.globalXfo = %s_%s;" % (member, driverMember, argName)]
                        self.__krkVisitedObjects.append(item);
                    else:
                        connectedObj = self.findKLObjectForSI(connected)
                        kl += self.__visitKLObject(connectedObj)

            return kl

        driverCanvasOp = self.findKLCanvasOp(driver)
        if driverCanvasOp:
            driverMember = driverCanvasOp['member']
            kOperator = driverCanvasOp['sceneItem']

            # todo...
            # if not driverCanvasOp.get('visited', False):
            #     driverCanvasOp['visited'] = True
            #     kl += ["", "  // TODO: Canvas solver %s missing!" % driverMember]
            self.__krkVisitedObjects.append(item);
            return kl

        # todo: canvas operators
        self.__krkVisitedObjects.append(item);
        return kl

    def __visitKLAttribute(self, attr):
        klCode = []
        if attr.get('visited', False):
            return klCode
        if attr.get('driver', None) is None:
            return klCode
        driverAttr = self.findKLAttribute(attr['driver'])
        klCode += self.__visitKLAttribute(driverAttr)
        klCode += ["  this.%s.value = this.%s.value;" % (attr['member'], driverAttr['member'])]
        return klCode

    def generateKLCode(self):

        controls = []
        for obj in self.__klObjects:
            if obj['sceneItem'].isTypeOf('Control'):
                controls.append(obj)

        scalarAttributes = []
        for attr in self.__klAttributes:
            if attr['sceneItem'].isTypeOf('ScalarAttribute') and attr.get('driver', None) is None:
                scalarAttributes.append(attr)

        kl = []
        kl += ["require Math;"]
        kl += ["require Geometry;"]
        kl += ["require Kraken;"]
        kl += ["require KrakenForCanvas;"]
        kl += ["require KrakenAnimation;"]
        kl += [""]
        kl += ["object %s : KrakenKLRig {" % self.getKLExtensionName()]
        kl += ["  Float64 solveTimeMs;"]
        kl += ["  KrakenClip clip; // the default clip of the rig"]
        for member in self.__klMembers:
            kl += ["  %s %s;" % (member['type'], member['name'])]
        kl += ["};"]
        kl += [""]
        kl += ["function %s() {" % self.getKLExtensionName()]
        kl += ["  this.init();"]
        kl += ["}", ""]

        kl += ["function %s.init!() {" % self.getKLExtensionName()]
        kl += ["  Float32 floatAnimation[String];"]
        kl += [""]
        if self.__debugMode:
            kl += ["  // build 3D objects"]
        for obj in self.__klObjects:
            memberName = obj['member']
            if self.__debugMode:
                kl += ["  this.%s.name = \"%s\";" % (memberName, obj['name'])]
                kl += ["  this.%s.buildName = \"%s\";" % (memberName, obj['buildName'])]
                kl += ["  this.%s.path = \"%s\";" % (memberName, obj['path'])]
                kl += ["  this.%s.layer = \"%s\";" % (memberName, obj.get('layer', ''))]
                kl += ["  this.%s.component = \"%s\";" % (memberName, obj.get('component', ''))]
                kl += ["  this.%s.visibility = %s;" % (memberName, Boolean(obj.get('visibility', False)))]
                kl += ["  this.%s.color = %s;" % (memberName, obj.get('color', 'Color(0.0, 0.0, 0.0, 1.0)'))]
        kl += ["  this.resetPose();"]

        kl += ["", "  // build constraints"]
        for constraint in self.__klConstraints:
            memberName = constraint['member']
            kl += ["  this.%s.offset = %s;" % (memberName, constraint.get('offset', 'Xfo()'))]
            kl += ["  this.%s.constrainers.resize(%d);" % (memberName, len(constraint['constrainers']))]

        kl += ["", "  // build kl solvers"]
        for solver in self.__klSolvers:
            memberName = solver['member']
            kl += ["  this.%s = %s();" % (memberName, solver['type'])]

        kl += ["", "  // build kl canvas ops"]
        for canvasOp in self.__klCanvasOps:
            memberName = canvasOp['member']
            # todo....
            kl += ["  // todo: this.%s = CanvasSolver?();" % (memberName)]

        kl += ["", "  // build attributes"]
        for attr in self.__klAttributes:
            name = attr['name']
            path = attr['path']
            if not self.__debugMode:
              name = ""
              path = ""

            if attr['cls'] == "BoolAttribute":
                kl += ["  this.%s = Kraken%s(\"%s\", \"%s\", %s, %s, %s);" % (
                    attr['member'], 
                    attr['cls'],
                    name,
                    path,
                    Boolean(attr['keyable']),
                    Boolean(attr['animatable']),
                    Boolean(attr['value'])
                )]
            elif attr['cls'] == "ColorAttribute":
                kl += ["  this.%s = Kraken%s(\"%s\", \"%s\", %s, %s, %s);" % (
                    attr['member'], 
                    attr['cls'],
                    name,
                    path,
                    Boolean(attr['keyable']),
                    Boolean(attr['animatable']),
                    "Color(%f, %f, %f, %f)" % (
                        attr['value'].r,
                        attr['value'].g,
                        attr['value'].b,
                        attr['value'].a
                    )
                )]
            elif attr['cls'] == "IntegerAttribute":
                kl += ["  this.%s = Kraken%s(\"%s\", \"%s\", %s, %s, %s, %s, %d);" % (
                    attr['member'], 
                    attr['cls'],
                    name,
                    path,
                    Boolean(attr['keyable']),
                    Boolean(attr['animatable']),
                    attr.get('min', "-SCALAR_INFINITE"),
                    attr.get('max', "SCALAR_INFINITE"),
                    attr['value']
                )]
            elif attr['cls'] == "ScalarAttribute":
                kl += ["  this.%s = Kraken%s(\"%s\", \"%s\", %s, %s, %s, %s, %f, floatAnimation);" % (
                    attr['member'], 
                    attr['cls'],
                    name,
                    path,
                    Boolean(attr['keyable']),
                    Boolean(attr['animatable']),
                    attr.get('min', "-SCALAR_INFINITE"),
                    attr.get('max', "SCALAR_INFINITE"),
                    attr['value']
                )]
            elif attr['cls'] == "StringAttribute":
                kl += ["  this.%s = Kraken%s(\"%s\", \"%s\", %s, %s, \"%s\");" % (
                    attr['member'], 
                    attr['cls'],
                    name,
                    path,
                    Boolean(attr['keyable']),
                    Boolean(attr['animatable']),
                    attr['value']
                )]

        kl += ["}", ""]

        kl += ["function %s.resetPose!() {" % self.getKLExtensionName()]
        kl += ["  // reset objects"]
        for obj in self.__klObjects:
            kl += ["  this.%s.xfo = %s;" % (obj['member'], obj.get('xfo', 'Xfo()'))]
        kl += ["  // reset attributes"]
        for attr in scalarAttributes:
            kl += ["  this.%s.value = %f;" % (attr['member'], attr['value'])]
        kl += ["}", ""]

        kl += ["function %s.solve!() {" % self.getKLExtensionName()]
        kl += ["  UInt64 timerStart = getCurrentTicks();"]
        kl += self.__klPreCode

        for obj in self.__klObjects:
            obj['visited'] = False
        for solver in self.__klSolvers:
            solver['visited'] = False
        for attr in self.__klAttributes:
            attr['visited'] = False
        for canvasOp in self.__klCanvasOps:
            canvasOp['visited'] = False

        for attr in self.__klAttributes:
            kl += self.__visitKLAttribute(attr)

        self.__krkVisitedObjects = []
        for obj in self.__klObjects:
            kl += self.__visitKLObject(obj)

        kl += ["  UInt64 timerEnd = getCurrentTicks();"]
        kl += ["  this.solveTimeMs = 1000.0 * getSecondsBetweenTicks(timerStart, timerEnd);"]
        kl += ["}", ""]

        kl += ["function %s.evaluate!(KrakenClipContext context) {" % self.getKLExtensionName()]
        kl += ["  if(this.clip != null) {"]
        kl += ["    KrakenKLRig rig = this;"]
        kl += ["    this.clip.apply(rig, context, 1.0);"]
        kl += ["  }"]
        kl += ["  this.solve();"]
        kl += ["}", ""]

        kl += ["function %s.evaluate!(KrakenClipContext context, Boolean inGlobalSpace, io Xfo joints<>) {" % self.getKLExtensionName()]
        kl += ["  if(joints.size() != %d)" % len(self.__krkDeformers)]
        kl += ["    throw(\"Expected number of joints does not match (\"+joints.size()+\" given, %d expected).\");" % len(self.__krkDeformers)]
        kl += ["  if(this.clip != null) {"]
        kl += ["    KrakenKLRig rig = this;"]
        kl += ["    this.clip.apply(rig, context, 1.0);"]
        kl += ["  }"]
        kl += ["  this.solve();"]
        kl += ["  if(inGlobalSpace) {"]
        for i in range(len(self.__krkDeformers)):
            kl += ["    joints[%d] = this.%s.globalXfo;" % (i, self.__krkDeformers[i]['member'])]
        kl += ["  } else {", ]
        for i in range(len(self.__krkDeformers)):
            parentObj = self.findKLObjectForSI(self.__krkDeformers[i]['sceneItem'].getParent())
            if parentObj:
                kl += ["    joints[%d] = this.%s.globalXfo.inverse() * this.%s.globalXfo;" % (i, parentObj['member'], self.__krkDeformers[i]['member'])]
            else:
                kl += ["    joints[%d] = this.%s.globalXfo;" % (i, self.__krkDeformers[i]['member'])]
        kl += ["  }"]
        kl += ["}", ""]

        kl += ["function Xfo[] %s.getControlXfos() {" % self.getKLExtensionName()]
        kl += ["  Xfo result[](%d);" % len(controls)]
        for i in range(len(controls)):
            kl += ["  result[%d] = this.%s.xfo;" % (i, controls[i]['member'])]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function String[] %s.getControlNames() {" % self.getKLExtensionName()]
        kl += ["  String result[](%d);" % len(controls)]
        for i in range(len(controls)):
            kl += ["  result[%d] = \"%s\";" % (i, controls[i]['sceneItem'].getBuildName())]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function Xfo[] %s.getJointXfos() {" % self.getKLExtensionName()]
        kl += ["  Xfo result[](%d);" % len(self.__krkDeformers)]
        for i in range(len(self.__krkDeformers)):
            kl += ["  result[%d] = this.%s.globalXfo;" % (i, self.__krkDeformers[i]['member'])]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function String[] %s.getJointNames() {" % self.getKLExtensionName()]
        kl += ["  String result[](%d);" % len(self.__krkDeformers)]
        for i in range(len(self.__krkDeformers)):
            kl += ["  result[%d] = \"%s\";" % (i, self.__krkDeformers[i]['sceneItem'].getBuildName())]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function Xfo[] %s.getAllXfos() {" % self.getKLExtensionName()]
        kl += ["  Xfo result[](%d);" % len(self.__klObjects)]
        for i in range(len(self.__klObjects)):
            kl += ["  result[%d] = this.%s.globalXfo;" % (i, self.__klObjects[i]['member'])]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function String[] %s.getAllNames() {" % self.getKLExtensionName()]
        kl += ["  String result[](%d);" % len(self.__klObjects)]
        for i in range(len(self.__klObjects)):
            kl += ["  result[%d] = \"%s\";" % (i, self.__klObjects[i]['sceneItem'].getBuildName())]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function Float32[] %s.getScalarAttributeValues() {" % self.getKLExtensionName()]
        kl += ["  Float32 result[](%d);" % len(scalarAttributes)]
        for i in range(len(scalarAttributes)):
            kl += ["  result[%d] = this.%s.value;" % (i, scalarAttributes[i]['member'])]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function String[] %s.getScalarAttributeNames() {" % self.getKLExtensionName()]
        kl += ["  String result[](%d);" % len(scalarAttributes)]
        for i in range(len(scalarAttributes)):
            ownerName = scalarAttributes[i]['sceneItem'].getParent().getParent().getBuildName()
            kl += ["  result[%d] = \"%s.%s\";" % (i, ownerName, scalarAttributes[i]['name'])]
        kl += ["  return result;"]
        kl += ["}", ""]

        kl += ["function %s.setControlXfos!(Xfo values<>) {" % self.getKLExtensionName()]
        kl += ["  if(values.size() != %d)" % len(controls)]
        kl += ["    throw(\"Expected number of values does not match (\"+values.size()+\" given, %d expected).\");" % len(controls)]
        for i in range(len(controls)):
            kl += ["  this.%s.xfo = values[%d];" % (controls[i]['member'], i)]
        kl += ["}", ""]        

        kl += ["function %s.setScalarAttributeValues!(Float32 values<>) {" % self.getKLExtensionName()]
        kl += ["  if(values.size() != %d)" % len(scalarAttributes)]
        kl += ["    throw(\"Expected number of values does not match (\"+values.size()+\" given, %d expected).\");" % len(scalarAttributes)]
        for i in range(len(scalarAttributes)):
            kl += ["  this.%s.value = values[%d];" % (scalarAttributes[i]['member'], i)]
        kl += ["}", ""]        

        kl += ["function %s.setClip!(KrakenClip clip) {" % self.getKLExtensionName()]
        kl += ["  this.clip = clip;"]
        kl += ["}", ""]

        kl += ["function %s.loadClipFromFile!(String filePath) {" % self.getKLExtensionName()]
        kl += ["  this.clip = KrakenClip_loadFromFile(filePath);"]
        kl += ["}", ""]

        # kl += ["function %s.evaluateClip!(KrakenClipContext context, Ref<KrakenClip> clip) {" % self.getKLExtensionName()]
        # kl += ["  if(!clip)", "    return;"]
        # kl += ["  KrakenClip mutableClip = clip;"]
        # kl += ["  for(UInt32 i=0;i<mutableClip.getChannelCount();i++) {"]
        # kl += ["    switch(mutableClip.getChannelType(i)) {"]
        # kl += ["      case KrakenClipChannel_Float32: {"]
        # kl += ["        switch(mutableClip.getChannelName(i)) {"]
        # for attr in self.__klAttributes:
        #     if attr['cls'] != "ScalarAttribute":
        #         continue
        #     kl += ["          case \"%s.%s\": {" % (attr['sceneItem'].getParent().getParent().getBuildName(), attr['sceneItem'].getName())]
        #     kl += ["            this.%s.value = mutableClip.evaluateFloat32(i, context);" % (attr['member'])]
        #     kl += ["            break;"]
        #     kl += ["          }"]
        # kl += ["        }"]
        # kl += ["        break;"]
        # kl += ["      }"]
        # kl += ["      case KrakenClipChannel_Xfo: {"]
        # kl += ["        switch(mutableClip.getChannelName(i)) {"]
        # for obj in self.__klObjects:
        #     if not obj['sceneItem'].isTypeOf('Control'):
        #         continue
        #     kl += ["          case \"%s\": {" % obj['sceneItem'].getBuildName()]
        #     kl += ["            this.%s.xfo = mutableClip.evaluateXfo(i, context);" % (obj['member'])]
        #     kl += ["            break;"]
        #     kl += ["          }"]
        # kl += ["        }"]
        # kl += ["        break;"]
        # kl += ["      }"]
        # kl += ["    }"]
        # kl += ["  }"]
        # kl += ["}", ""]

        # kl += ["function %s.evaluateJointsForUnreal!(KrakenClipContext context, io Float32 result<>) {" % self.getKLExtensionName()]
        # kl += ["  Xfo xfos[];"]
        # kl += ["  this.evaluateJoints(context, xfos);"]
        # kl += ["  if(xfos.dataSize() != result.dataSize())"]
        # kl += ["    throw(\"Provided float array has incorrect size. Should be \"+xfos.size() * 10+\" floats.\");"]
        # kl += ["  UInt32 offset = 0;"]
        # kl += ["  for(Size i=0;i<xfos.size();i++) {"]
        # kl += ["    Xfo xfo = xfos[i];"]
        # kl += ["    // todo: unreal space conversion!"]
        # kl += ["    result[offset++] = xfo.ori.v.x;"]
        # kl += ["    result[offset++] = xfo.ori.v.y;"]
        # kl += ["    result[offset++] = xfo.ori.v.z;"]
        # kl += ["    result[offset++] = xfo.ori.w;"]
        # kl += ["    result[offset++] = xfo.tr.x;"]
        # kl += ["    result[offset++] = xfo.tr.y;"]
        # kl += ["    result[offset++] = xfo.tr.z;"]
        # kl += ["    result[offset++] = xfo.sc.x;"]
        # kl += ["    result[offset++] = xfo.sc.y;"]
        # kl += ["    result[offset++] = xfo.sc.z;"]
        # kl += ["  }"]
        # kl += ["}", ""]

        return "\n".join(kl)

    def getKLTestCode(self):
        kl = []
        kl += ["require %s;" % self.getKLExtensionName()]
        kl += [""]
        kl += ["operator entry() {"]
        kl += ["  %s rig();" % self.getKLExtensionName()]
        kl += ["  rig.solve();"]
        kl += ["  report(rig.getJointXfos());"]
        kl += ["}"]
        return "\n".join(kl)

    def generateKLExtension(self):
        if not self.__outputFolder:
            raise Exception("KL Builder: OutputFolder not specified!")
            return False

        klCode = self.generateKLCode()
        extName = self.getKLExtensionName()
        return [{
            "filename": "%s.kl" % extName, 
            "sourceCode": klCode
        }]

    def loadKLExtension(self, reloadExt = False):
        ext = self.generateKLExtension()
        client = ks.getCoreClient()
        client.registerKLExtension(
            self.getKLExtensionName(),
            ext,
            version="1.0.0",
            loadExt=True,
            reloadExt=reloadExt
        )

    def reloadKLExtension(self):
        return self.loadKLExtension( reloadExt = True)

    def __ensureFolderExists(self, filePath):
        folder = os.path.split(filePath)[0]
        if not os.path.exists(folder):
            os.makedirs(folder)

    def saveKLExtension(self):
        ext = self.generateKLExtension()
        fpmFilePath = os.path.join(self.__outputFolder, "%s.fpm.json" % self.getKLExtensionName())
        klFilePath = os.path.join(self.__outputFolder, ext[0]['filename'])
        testFilePath = os.path.join(self.__outputFolder, "test.kl")
        fpm = "{\"code\": [\"%s\"], \"dfgPresets\": {\"dir\": \"DFG\", \"presetPath\": \"Kraken.KLRigs.%s\"}}" % (ext[0]['filename'], self.getKLExtensionName())
        self.__ensureFolderExists(fpmFilePath)
        self.__ensureFolderExists(klFilePath)
        self.__ensureFolderExists(testFilePath)
        open(fpmFilePath, "w").write(fpm)
        open(klFilePath, "w").write(ext[0]['sourceCode'])
        open(testFilePath, "w").write(self.getKLTestCode())
        self.saveDFGPresets()
        return True

    def saveDFGPresets(self):
        client = ks.getCoreClient()
        dfgHost = client.getDFGHost()
        rigType = str(self.getKLExtensionName())

        presetFolder = os.path.join(self.__outputFolder, 'DFG')
        if not os.path.exists(presetFolder):
          os.makedirs(presetFolder)

        # Create preset
        filePath = os.path.join(presetFolder, 'Create.canvas')
        dfgBinding = dfgHost.createBindingToNewGraph()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("Create")
        dfgExec.addExtDep(rigType)
        var = dfgExec.addVar("rig", rigType, rigType)
        varResult = dfgExec.addExecPort('result', client.DFG.PortTypes.Out)
        dfgExec.connectTo(var+'.value', varResult)
        func = dfgExec.addInstWithNewFunc("constructor")
        subExec = dfgExec.getSubExec(func)
        subExec.addExtDep(rigType)
        funcResult = subExec.addExecPort('result', client.DFG.PortTypes.Out, rigType)
        subExec.setCode("dfgEntry {\n  %s = %s();\n}\n" % (funcResult, rigType))
        dfgExec.connectTo(func+'.'+funcResult, var+'.value')
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)

        # SetClip preset
        filePath = os.path.join(presetFolder, 'SetClip.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("SetClip")
        dfgExec.addExtDep(rigType)
        funcResult = dfgExec.addExecPort('rig', client.DFG.PortTypes.IO, rigType)
        clipInput = dfgExec.addExecPort('clip', client.DFG.PortTypes.In, "KrakenClip")
        dfgExec.setCode("dfgEntry {\n  %s.setClip(%s);\n}\n" % (funcResult, clipInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

        # Solve preset
        filePath = os.path.join(presetFolder, 'Solve.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("Solve")
        dfgExec.addExtDep(rigType)
        funcResult = dfgExec.addExecPort('rig', client.DFG.PortTypes.IO, rigType)
        dfgExec.setCode("dfgEntry {\n  %s.solve();\n}\n" % (funcResult))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)   

        # Evaluate preset
        filePath = os.path.join(presetFolder, 'Evaluate.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("Evaluate")
        dfgExec.addExtDep(rigType)
        funcResult = dfgExec.addExecPort('rig', client.DFG.PortTypes.IO, rigType)
        contextInput = dfgExec.addExecPort('context', client.DFG.PortTypes.In, "KrakenClipContext")
        dfgExec.setCode("dfgEntry {\n  %s.evaluate(%s);\n}\n" % (funcResult, contextInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)   

        # ResetPose preset
        filePath = os.path.join(presetFolder, 'ResetPose.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("ResetPose")
        dfgExec.addExtDep(rigType)
        funcResult = dfgExec.addExecPort('rig', client.DFG.PortTypes.IO, rigType)
        dfgExec.setCode("dfgEntry {\n  %s.resetPose();\n}\n" % (funcResult))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

        # GetControlXfos preset
        filePath = os.path.join(presetFolder, 'GetControlXfos.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("GetControlXfos")
        dfgExec.addExtDep(rigType)
        funcInput = dfgExec.addExecPort('rig', client.DFG.PortTypes.In, rigType)
        funcResult = dfgExec.addExecPort('result', client.DFG.PortTypes.Out, 'Xfo[]')
        dfgExec.setCode("dfgEntry {\n  %s = %s.getControlXfos();\n}\n" % (funcResult, funcInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

        # GetJointXfos preset
        filePath = os.path.join(presetFolder, 'GetJointXfos.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("GetJointXfos")
        dfgExec.addExtDep(rigType)
        funcInput = dfgExec.addExecPort('rig', client.DFG.PortTypes.In, rigType)
        funcResult = dfgExec.addExecPort('result', client.DFG.PortTypes.Out, 'Xfo[]')
        dfgExec.setCode("dfgEntry {\n  %s = %s.getJointXfos();\n}\n" % (funcResult, funcInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

        # GetAllXfos preset
        filePath = os.path.join(presetFolder, 'GetAllXfos.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("GetAllXfos")
        dfgExec.addExtDep(rigType)
        funcInput = dfgExec.addExecPort('rig', client.DFG.PortTypes.In, rigType)
        funcResult = dfgExec.addExecPort('result', client.DFG.PortTypes.Out, 'Xfo[]')
        dfgExec.setCode("dfgEntry {\n  %s = %s.getAllXfos();\n}\n" % (funcResult, funcInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

        # GetControlNames preset
        filePath = os.path.join(presetFolder, 'GetControlNames.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("GetControlNames")
        dfgExec.addExtDep(rigType)
        funcInput = dfgExec.addExecPort('rig', client.DFG.PortTypes.In, rigType)
        funcResult = dfgExec.addExecPort('result', client.DFG.PortTypes.Out, 'String[]')
        dfgExec.setCode("dfgEntry {\n  %s = %s.getControlNames();\n}\n" % (funcResult, funcInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

        # GetJointNames preset
        filePath = os.path.join(presetFolder, 'GetJointNames.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("GetJointNames")
        dfgExec.addExtDep(rigType)
        funcInput = dfgExec.addExecPort('rig', client.DFG.PortTypes.In, rigType)
        funcResult = dfgExec.addExecPort('result', client.DFG.PortTypes.Out, 'String[]')
        dfgExec.setCode("dfgEntry {\n  %s = %s.getJointNames();\n}\n" % (funcResult, funcInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

        # GetAllNames preset
        filePath = os.path.join(presetFolder, 'GetAllNames.canvas')
        dfgBinding = dfgHost.createBindingToNewFunc()
        dfgExec = dfgBinding.getExec()
        dfgExec.setTitle("GetAllNames")
        dfgExec.addExtDep(rigType)
        funcInput = dfgExec.addExecPort('rig', client.DFG.PortTypes.In, rigType)
        funcResult = dfgExec.addExecPort('result', client.DFG.PortTypes.Out, 'String[]')
        dfgExec.setCode("dfgEntry {\n  %s = %s.getAllNames();\n}\n" % (funcResult, funcInput))
        content = dfgBinding.exportJSON()
        open(filePath, "w").write(content)        

    def findKLObjectForSI(self, kSceneItem):
        member = self.getUniqueName(kSceneItem)
        for obj in self.__klObjects:
            if obj['member'] == member:
                return obj
        return None

    def findKLAttribute(self, kAttribute):
        member = self.getUniqueName(kAttribute)
        for attr in self.__klAttributes:
            if attr['member'] == member:
                return attr
        return None

    def findKLConstraint(self, kConstraint):
        member = self.getUniqueName(kConstraint)
        for constraint in self.__klConstraints:
            if constraint['member'] == member:
                return constraint
        return None

    def findKLSolver(self, kOperator):
        member = self.getUniqueName(kOperator)
        for solver in self.__klSolvers:
            if solver['member'] == member:
                return solver
        return None

    def findKLCanvasOp(self, kOperator):
        member = self.getUniqueName(kOperator)
        for canvasOp in self.__klCanvasOps:
            if canvasOp['member'] == member:
                return canvasOp
        return None

    def buildKLSceneItem(self, kSceneItem, buildName):

        if isinstance(kSceneItem, Rig):
            self.__rigTitle = kSceneItem.getName()

        cls = kSceneItem.__class__.__name__

        if kSceneItem.isTypeOf('ComponentGroup'):
            cls = 'ComponentGroup'
        elif kSceneItem.isTypeOf('ComponentInput'):
            cls = 'ComponentInput'
        elif kSceneItem.isTypeOf('ComponentOutput'):
            cls = 'ComponentOutput'
        elif kSceneItem.isTypeOf('Rig'):
            cls = 'Rig'
        elif kSceneItem.isTypeOf('Layer'):
            cls = 'Layer'
        elif kSceneItem.isTypeOf('CtrlSpace'):
            cls = 'CtrlSpace'
        elif kSceneItem.isTypeOf('Curve'):
            cls = 'Curve'
        elif kSceneItem.isTypeOf('Control'):
            cls = 'Control'
        elif kSceneItem.isTypeOf('Joint'):
            cls = 'Joint'
        elif kSceneItem.isTypeOf('Locator'):
            cls = 'Locator'
        elif kSceneItem.isTypeOf('HierarchyGroup'):
            cls = 'HierarchyGroup'
        elif kSceneItem.isTypeOf('Container'):
            cls = 'Container'
        elif kSceneItem.isTypeOf('Transform'):
            cls = 'Transform'
        else:
            self.reportError("buildKLSceneItem: Unexpected class " + cls)
            return False
            
        if kSceneItem.isTypeOf('ComponentInput') or \
            kSceneItem.isTypeOf('ComponentOutput') or \
            kSceneItem.isTypeOf('Layer') or \
            kSceneItem.isTypeOf('Rig'):
            cls = 'Transform'

        obj = {
            'sceneItem': kSceneItem,
            'member': self.getUniqueName(kSceneItem),
            'name': kSceneItem.getName(),
            'buildName': buildName,
            'type': "Kraken%s" % cls,
            'path': kSceneItem.getDecoratedPath(),
            'parent': None,
            'driver': None
        }

        if kSceneItem.isTypeOf('Joint'):
          self.__krkDeformers.append(obj)

        for parentName in ['layer', 'component']:
            getMethod = 'get%s' % parentName.capitalize()
            if not hasattr(kSceneItem, getMethod):
                continue
            parent = getattr(kSceneItem, getMethod)()
            if not parent:
                continue
            obj[parentName] = parent.getDecoratedPath()

        if hasattr(kSceneItem, 'getParent'):
            parent = kSceneItem.getParent()
            if not parent is None:
                obj['parent'] = parent.getDecoratedPath()
                obj['driver'] = parent

        self.__klMembers.append({'name': self.getUniqueName(kSceneItem), 'type': obj['type']})
        self.__klObjects.append(obj)
        return True

    def buildKLAttribute(self, kAttribute):
        cls = kAttribute.__class__.__name__
        if kAttribute.isTypeOf('BoolAttribute'):
            cls = 'BoolAttribute'
        elif kAttribute.isTypeOf('ColorAttribute'):
            cls = 'ColorAttribute'
        elif kAttribute.isTypeOf('IntegerAttribute'):
            cls = 'IntegerAttribute'
        elif kAttribute.isTypeOf('ScalarAttribute'):
            cls = 'ScalarAttribute'
        elif kAttribute.isTypeOf('StringAttribute'):
            cls = 'StringAttribute'
        else:
            self.reportError("buildNodeAttribute: Unexpected class " + cls)
            return False

        attr = {
            'member': self.getUniqueName(kAttribute),
            'sceneItem': kAttribute,
            'name': kAttribute.getName(),
            'path': kAttribute.getDecoratedPath(),
            'cls': cls,
            'keyable': kAttribute.getKeyable(),
            'animatable': kAttribute.getAnimatable(),
            'value': kAttribute.getValue()
        }

        if cls in ['IntegerAttribute', 'ScalarAttribute']:
            if not kAttribute.getMin() is None:
              attr['min'] = kAttribute.getMin()
            if not kAttribute.getMax() is None:
              attr['max'] = kAttribute.getMax()

        self.__klMembers.append({'name': self.getUniqueName(kAttribute), 'type': 'Kraken'+cls})
        self.__klAttributes.append(attr)
        return kAttribute

    def buildKLConstraint(self, kConstraint):
        cls = kConstraint.__class__.__name__

        constraintObj = self.findKLConstraint(kConstraint)
        if constraintObj:
            return None

        constraint = {
            'sceneItem': kConstraint,
            'member': self.getUniqueName(kConstraint),
            'name': kConstraint.getName(),
            'buildName': kConstraint.getName(),
            'type': "Kraken%s" % cls,
            'path': kConstraint.getDecoratedPath(),
            'constrainee': kConstraint.getConstrainee(),
            'constrainers': kConstraint.getConstrainers()
        }

        constrainee = self.findKLObjectForSI(constraint['constrainee'])
        if constrainee:
            constrainee['driver'] = kConstraint

        self.__klMembers.append({'name': self.getUniqueName(kConstraint), 'type': constraint['type']})
        self.__klConstraints.append(constraint)
        return kConstraint

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

        if self.buildKLSceneItem(kSceneItem, buildName):
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

        if self.buildKLSceneItem(kSceneItem, buildName):
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

        if self.buildKLSceneItem(kSceneItem, buildName):
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

        if self.buildKLSceneItem(kSceneItem, buildName):
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

        if self.buildKLSceneItem(kSceneItem, buildName):
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
        if self.buildKLSceneItem(kSceneItem, buildName):
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
        if self.buildKLSceneItem(kSceneItem, buildName):
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
        if not self.buildKLSceneItem(kSceneItem, buildName):
            return None
        return kSceneItem

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
        return self.buildKLAttribute(kAttribute)

    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (Object): kAttribute that represents a float attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildKLAttribute(kAttribute)

    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (Object): kAttribute that represents a integer attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildKLAttribute(kAttribute)

    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (Object): kAttribute that represents a string attribute to be built.

        Return:
            bool: True if successful.

        """
        return self.buildKLAttribute(kAttribute)

    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Args:
            kAttributeGroup (object): Kraken object to build the attribute group on.

        Return:
            bool: True if successful.

        """

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

        attrA = self.findKLAttribute(connection)
        attrB = self.findKLAttribute(kAttribute)
        if attrA is None or attrB is None:
            return False

        attrB['driver'] = attrA['sceneItem']
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
        return self.buildKLConstraint(kConstraint)

    def buildPoseConstraint(self, kConstraint):
        """Builds an pose constraint represented by the kConstraint.

        Args:
            kConstraint (Object): kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildKLConstraint(kConstraint)

    def buildPositionConstraint(self, kConstraint):
        """Builds an position constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildKLConstraint(kConstraint)

    def buildScaleConstraint(self, kConstraint):
        """Builds an scale constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """
        return self.buildKLConstraint(kConstraint)

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

        attrA = self.findKLAttribute(connectionTarget)
        attrB = self.findKLAttribute(inputTarget)
        if attrA is None or attrB is None:
            return False

        attrB['driver'] = attrA['sceneItem']
        return True

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

        solverTypeName = kOperator.getSolverTypeName()

        solver = {
          "sceneItem": kOperator,
          "name": kOperator.getName(),
          "member": self.getUniqueName(kOperator),
          "path": kOperator.getDecoratedPath(),
          "type": kOperator.getSolverTypeName(),
        }

        self.__klMembers.append({'name': self.getUniqueName(kOperator), 'type': solver['type']})
        self.__klSolvers.append(solver)

        args = kOperator.getSolverArgs()
        for i in xrange(len(args)):
            arg = args[i]
            argName = arg.name.getSimpleType()
            argDataType = arg.dataType.getSimpleType()
            argConnectionType = arg.connectionType.getSimpleType()

            if argConnectionType == 'In':
                continue;
            if argDataType == 'EvalContext':
                continue

            connectedObjects = kOperator.getOutput(argName)
            if not argDataType.endswith('[]'):
                connectedObjects = [connectedObjects]

            for item in connectedObjects:
                itemObj = self.findKLObjectForSI(item)
                itemObj['driver'] = kOperator

        return True


    def buildCanvasOperator(self, kOperator):
        """Builds KL Operators on the components.

        Args:
            kOperator (Object): Kraken operator that represents a KL operator.

        Return:
            bool: True if successful.

        """

        raise Exception("The KL builder does not support Canvas Operators yet. (%s)" % kOperator.getDecoratedPath())

        # todo: we should only instaniate each preset once
        # and we should add functions to the kl code for each ONCE
        node = self.__canvasGraph.createNodeFromPresetSI(kOperator, kOperator.getPresetPath(), title='constructor')
        subExec = self.__canvasGraph.getSubExec(node)

        portTypeMap = {
            0: 'In',
            1: 'IO',
            2: 'Out'
        }

        canvasOp = {
          "sceneItem": kOperator,
          "name": kOperator.getName(),
          "node": node,
          "exec": subExec,
          "member": self.getUniqueName(kOperator),
          "path": kOperator.getDecoratedPath()
        }
        self.__klCanvasOps.append(canvasOp)

        for i in xrange(subExec.getExecPortCount()):
            portName = subExec.getExecPortName(i)
            portConnectionType = portTypeMap[subExec.getExecPortType(i)]
            portDataType = self.__canvasGraph.getNodePortResolvedType(node, portName)
            if portConnectionType == 'In':
                continue
            if portDataType == 'EvalContext':
                continue
            connectedObjects = kOperator.getOutput(portName)
            if not portDataType.endswith('[]'):
                connectedObjects = [connectedObjects]

            for item in connectedObjects:
                itemObj = self.findKLObjectForSI(item)
                itemObj['driver'] = kOperator

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

        obj = self.findKLObjectForSI(kSceneItem)
        if obj is None:
            return False

        obj['visibility'] = kSceneItem.getVisibility()
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

        obj = self.findKLObjectForSI(kSceneItem)
        if obj is None:
            return False

        value = kSceneItem.getColor()
        if value is None:
            value = self.getBuildColor(kSceneItem)
        if value:
            colors = self.config.getColors()
            c = colors[value]
            value = Color(r=c[1][0], g=c[1][1], b=c[1][2], a=1.0)

        if value is None:
          return True

        valueStr = "Color(%f, %f, %f, %f)" % (
            value.r,
            value.g,
            value.b,
            value.a
          )
        obj['color'] = valueStr

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

        obj = self.findKLObjectForSI(kSceneItem)
        if obj is None:
            return False

        valueStr = self.__getXfoAsStr(kSceneItem.xfo)
        obj['initialXfo'] = kSceneItem.xfo.getRTVal().clone('Xfo')
        obj['initialXfo'].sc.x = round(obj['initialXfo'].sc.x.getSimpleType(), 4)
        obj['initialXfo'].sc.y = round(obj['initialXfo'].sc.y.getSimpleType(), 4)
        obj['initialXfo'].sc.z = round(obj['initialXfo'].sc.z.getSimpleType(), 4)

        if obj['driver'] is None:
            obj['xfo'] = valueStr
        else:
            obj['globalXfo'] = valueStr
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

        self.__rigTitle = self.getConfig().getMetaData('RigTitle', 'Rig')
        self.__canvasGraph = GraphManager()
        self.__debugMode = False
        self.__names = {}
        self.__pathToName = {}
        self.__klMembers = []
        self.__klObjects = []
        self.__klAttributes = []
        self.__klConstraints = []
        self.__klSolvers = []
        self.__klCanvasOps = []
        self.__klExtExecuted = False
        self.__klPreCode = []
        self.__krkItems = {}
        self.__krkAttributes = {}
        self.__krkDeformers = []
        self.__krkVisitedObjects = []

        return True

    def __computeGlobalTransform(self, item, rig):
        if isinstance(item, Constraint):
            itemObj = self.findKLObjectForSI(item.getConstrainee())
            constraintObj = self.findKLConstraint(item)
            krkConstraint = getattr(rig, constraintObj['member'])

            for i in range(len(item.getConstrainers())):
                constrainer = item.getConstrainers()[i]
                globalXfo = self.__computeGlobalTransform(constrainer, rig)
                krkConstraint.constrainers[i] = globalXfo

            initialXfo = itemObj.get('initialXfo', Xfo().getRTVal())
            return krkConstraint.compute("Xfo", initialXfo)
        else:
            itemObj = self.findKLObjectForSI(item)

            driverConstraint = itemObj['driver']
            if driverConstraint and isinstance(driverConstraint, Constraint):
                if driverConstraint.getMaintainOffset() == False:
                    return self.__computeGlobalTransform(driverConstraint, rig)

            return itemObj.get('initialXfo', Xfo().getRTVal())

    def __computeOffset(self, item, rig):
        if isinstance(item['sceneItem'], Object3D):
            driver = item['driver']
            if isinstance(driver, Object3D):
                driverObj = self.findKLObjectForSI(driver)
                print 'Solving local xfo for '+item['member']
                rig.solve("")

                parentXfo = getattr(rig, driverObj['member']).globalXfo
                initialXfo = item.get('initialXfo', Xfo().getRTVal())
                localXfo = parentXfo.inverse('Xfo').multiply('Xfo', initialXfo)
                krkObj = getattr(rig, item['member'])
                krkObj.xfo = localXfo
                setattr(rig, item['member'], krkObj)
                item['xfo'] = self.__getXfoAsStr(Xfo(localXfo))

            elif isinstance(driver, Constraint):

                if not driver.getMaintainOffset():
                    return
                    
                driverObj = self.findKLConstraint(driver)
                print 'Solving offset for '+driverObj['member']
                rig.solve("")

                krkConstraint = getattr(rig, driverObj['member'])
                initialXfo = item.get('initialXfo', Xfo().getRTVal())
                offsetXfo = krkConstraint.computeOffset('Xfo', initialXfo)
                krkConstraint.offset = offsetXfo
                setattr(rig, driverObj['member'], krkConstraint)
                driverObj['offset'] = self.__getXfoAsStr(Xfo(offsetXfo))

    def _postBuild(self):
        """Post-Build commands.

        Return:
            bool: True if successful.

        """

        # self.saveKLExtension()
        self.loadKLExtension()
        client = ks.getCoreClient()

        # get the rig
        rt = client.RT.types
        rig = getattr(rt, self.getKLExtensionName()).create()

        for item in self.__krkVisitedObjects:
            self.__computeOffset(item, rig)

        return self.saveKLExtension()
