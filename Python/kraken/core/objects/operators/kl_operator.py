"""Kraken - objects.operators.kl_operator module.

Classes:
KLOperator - Splice operator object.

"""

import pprint

from kraken.core.maths import Mat44, Xfo
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.operators.operator import Operator
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.kraken_system import ks


class KLOperator(Operator):
    """Splice Operator representation."""

    # TODO: Look in to expanding the Splice operator to be able to handle more
    # than one extension / operator. Need to change extension to extensions and
    # figure out how to differentiate the solver types per operator. Maybe have
    # an attirbute array called 'klOperators' that contains sets of what we
    # currently have setup.

    def __init__(self, name, solverTypeName, extension):
        super(KLOperator, self).__init__(name)

        self.solverTypeName = solverTypeName
        self.extension = extension

        # Load the Fabric Engine client and construct the RTVal for the Solver
        ks.loadCoreClient()
        ks.loadExtension('Kraken')
        if self.extension != 'Kraken':
            ks.loadExtension(self.extension)
        self.solverRTVal = ks.constructRTVal(self.solverTypeName)
        self.args = self.solverRTVal.getArguments('KrakenSolverArg[]')

        # Initialize the inputs and outputs based on the given args.
        for i in xrange(len(self.args)):
            arg = self.args[i]
            argName = arg.name.getSimpleType()
            argDataType = arg.dataType.getSimpleType()
            argConnectionType = arg.connectionType.getSimpleType()

            if argConnectionType == 'In':
                if argDataType.endswith('[]'):
                    self.inputs[argName] = []
                else:
                    self.inputs[argName] = None
            else:
                if argDataType.endswith('[]'):
                    self.outputs[argName] = []
                else:
                    self.outputs[argName] = None


    def getSolverTypeName(self):
        """Returns the solver type name for this operator.

        Returns:
            str: Name of the solver type this operator uses.

        """

        return self.solverTypeName


    def getExtension(self):
        """Returns the extention this operator uses.

        Returns:
            str: Name of the extension this solver uses.

        """

        return self.extension


    def getSolverArgs(self):
        """Returns the args array defined by the KL Operator.

        Returns:
            RTValArray: Args array defined by the KL Operator.

        """

        return self.args


    def generateSourceCode(self, arraySizes={}):
        """Returns the source code for a stub operator that will invoke the KL operator

        Returns:
            str: The source code for the stub operator.

        """

        # Start constructing the source code.
        opSourceCode = "dfgEntry {\n"

        # In SpliceMaya, output arrays are not resized by the system prior to calling into Splice, so we
        # explicily resize the arrays in the generated operator stub code.
        for argName, arraySize in arraySizes.iteritems():
            opSourceCode += "  "+argName+".resize("+str(arraySize)+");\n"

        opSourceCode += "  if(solver == null)\n"
        opSourceCode += "    solver = " + self.solverTypeName + "();\n"
        opSourceCode += "  solver.solve(\n"
        for i in xrange(len(self.args)):
            argName = self.args[i].name.getSimpleType()
            if i == len(self.args) - 1:
                opSourceCode += "    " + argName + "\n"
            else:
                opSourceCode += "    " + argName + ",\n"

        opSourceCode += "  );\n"
        opSourceCode += "}\n"

        return opSourceCode


    def evaluate(self):
        """invokes the Splice operator causing the output values to be computed.

        Returns:
            bool: True if successful.

        """

        def getRTVal(obj):
            if isinstance(obj, Object3D):
                return obj.xfo.getRTVal().toMat44('Mat44')
            elif isinstance(obj, Xfo):
                return obj.getRTVal().toMat44('Mat44')
            elif isinstance(obj, Attribute):
                return obj.getRTVal()
            elif type(obj) in (int, float, bool, str):
                return obj

        def validateArg(rtVal, argName, argDataType):
            """Validate argument types when passing built in Python types.

            Args:
                rtVal (RTVal): rtValue object.
                argName (str): Name of the argument being validated.
                argDataType (str): Type of the argument being validated.

            """

            # Validate types when passing a built in Python type
            if type(rtVal) in (bool, str, int, float):
                if argDataType in ('Scalar', 'Float32', 'UInt32'):
                    if type(rtVal) not in (float, int):
                        raise TypeError(self.getName() + ".evaluate(): Invalid Argument Value: " + str(rtVal) + " (" + type(rtVal).__name__ + "), for Argument: " + argName + " (" + argDataType + ")")

                elif argDataType == 'Boolean':
                    if type(rtVal) != bool:
                        raise TypeError(self.getName() + ".evaluate(): Invalid Argument Value: " + str(rtVal) + " (" + type(rtVal).__name__ + "), for Argument: " + argName + " (" + argDataType + ")")

                elif argDataType == 'String':
                    if type(rtVal) != str:
                        raise TypeError(self.getName() + ".evaluate(): Invalid Argument Value: " + str(rtVal) + " (" + type(rtVal).__name__ + "), for Argument: " + argName + " (" + argDataType + ")")


        argVals = []
        debug = []
        for i in xrange(len(self.args)):
            arg = self.args[i]
            argName = arg.name.getSimpleType()
            argDataType = arg.dataType.getSimpleType()
            argConnectionType = arg.connectionType.getSimpleType()

            if argDataType == 'EvalContext':
                argVals.append(ks.constructRTVal(argDataType))
                continue
            if argName == 'time':
                argVals.append(ks.constructRTVal(argDataType))
                continue
            if argName == 'frame':
                argVals.append(ks.constructRTVal(argDataType))
                continue

            if argConnectionType == 'In':
                if str(argDataType).endswith('[]'):
                    rtValArray = ks.rtVal(argDataType)
                    rtValArray.resize(len(self.inputs[argName]))
                    for j in xrange(len(self.inputs[argName])):
                        rtVal = getRTVal(self.inputs[argName][j])

                        validateArg(rtVal, argName, argDataType[:-2])

                        rtValArray[j] = rtVal

                    argVals.append(rtValArray)
                else:
                    rtVal = getRTVal(self.inputs[argName])

                    validateArg(rtVal, argName, argDataType)

                    argVals.append(rtVal)
            else:
                if str(argDataType).endswith('[]'):
                    rtValArray = ks.rtVal(argDataType)
                    rtValArray.resize(len(self.outputs[argName]))
                    for j in xrange(len(self.outputs[argName])):
                        rtVal = getRTVal(self.outputs[argName][j])

                        validateArg(rtVal, argName, argDataType[:-2])

                        rtValArray[j] = rtVal

                    argVals.append(rtValArray)
                else:
                    rtVal = getRTVal(self.outputs[argName])

                    validateArg(rtVal, argName, argDataType)

                    argVals.append(rtVal)

            debug.append({argName : [{"dataType": argDataType, "connectionType": argConnectionType}, argVals[-1]]})

        try:
            self.solverRTVal.solve('', *argVals)
        except:
            errorMsg = "Possible problem with KL operator '" + self.getName() + "' arguments:"
            print errorMsg
            pprint.pprint(debug, width=800)

            raise Exception(errorMsg)

        # Now put the computed values out to the connected output objects.
        def setRTVal(obj, rtval):
            if isinstance(obj, Object3D):
                obj.xfo.setFromMat44(Mat44(rtval))
            elif isinstance(obj, Xfo):
                obj.setFromMat44(Mat44(rtval))
            elif isinstance(obj, Mat44):
                obj.setFromMat44(rtval)
            elif isinstance(obj, Attribute):
                obj.setValue(rtval)
            else:
                print "Warning: Not setting rtval " + str(rtval) + " for object " + str(obj)

        for i in xrange(len(argVals)):
            arg = self.args[i]
            argName = arg.name.getSimpleType()
            argDataType = arg.dataType.getSimpleType()
            argConnectionType = arg.connectionType.getSimpleType()

            if argConnectionType != 'In':
                if argDataType.endswith('[]'):
                    for j in xrange(len(argVals[i])):
                        setRTVal(self.outputs[argName][j], argVals[i][j])
                else:
                    setRTVal(self.outputs[argName], argVals[i])

        return True