"""Kraken - objects.operators.splice_operator module.

Classes:
SpliceOperator - Splice operator object.

"""

from kraken.core.maths import Mat44
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.operators.operator import Operator
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.kraken_system import ks


class SpliceOperator(Operator):
    """Splice Operator representation."""

    # TODO: Look in to expanding the Splice operator to be able to handle more
    # than one extension / operator. Need to change extension to extensions and
    # figure out how to differentiate the solver types per operator. Maybe have
    # an attirbute array called 'klOperators' that contains sets of what we
    # currently have setup.

    def __init__(self, name, solverTypeName, extension, alwaysEval=False):
        super(SpliceOperator, self).__init__(name)

        self.solverTypeName = solverTypeName
        self.extension = extension
        self.alwaysEval = alwaysEval # This is for Softimage only to force eval.

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

            if argConnectionType == 'in':
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

        Return:
        String, name of the solver type this operator uses.

        """

        return self.solverTypeName


    def getExtension(self):
        """Returns the extention this operator uses.

        Return:
        String, name of the extension this solver uses.

        """

        return self.extension


    def getAlwaysEval(self):
        """Gets the value of the alwaysEval attribute.

        Returns:
            bool: Whether the operator is set to always evaluate.

        """

        return self.alwaysEval



    def getSolverArgs(self):
        """Returns the args array defined by the KL Operator.

        Return:
        RTValArray, args array defined by the KL Operator.

        """

        return self.args


    def generateSourceCode(self, arraySizes={}):
        """Returns the source code for a stub operator that will invoke the KL operator

        Return:
        String, The source code for the stub operator.

        """

        # Start constructing the source code.
        opSourceCode = "dfgEntry {\n"

        # In SpliceMaya, output arrays are not resized by the system prior to calling into Splice, so we
        # explicily resize the arrays in the generated operator stub code.
        for argName, arraySize in arraySizes.iteritems():
            opSourceCode += "  "+argName+".resize("+str(arraySize)+");\n"

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

        Return:
        Boolean, True if successful.

        """

        def getRTVal(obj):
            if isinstance(obj, Object3D):
                return obj.xfo.getRTVal().toMat44('Mat44')
            elif isinstance(obj, Attribute):
                return obj.getRTVal()

        argVals = []
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

            if argConnectionType == 'in':
                if str(argDataType).endswith('[]'):
                    rtValArray = ks.rtVal(argDataType[:-2]+'Array')
                    rtValArray.resize(len(self.inputs[argName]))
                    for j in xrange(len(self.inputs[argName])):
                        rtValArray[j] = getRTVal(self.inputs[argName][j])
                    argVals.append(rtValArray)
                else:
                    argVals.append(getRTVal(self.inputs[argName]))
            else:
                if str(argDataType).endswith('[]'):
                    rtValArray = ks.rtVal(argDataType[:-2]+'Array')
                    rtValArray.resize(len(self.outputs[argName]))
                    for j in xrange(len(self.outputs[argName])):
                        rtValArray[j] = getRTVal(self.outputs[argName][j])
                    argVals.append(rtValArray)
                else:
                    argVals.append(getRTVal(self.outputs[argName]))

        self.solverRTVal.solve('', *argVals)

        # Now put the computed values out to the connected output objects.
        def setRTVal(obj, rtval):
            if isinstance(obj, Object3D):
                obj.xfo.setFromMat44(Mat44(rtval))
            elif isinstance(obj, Attribute):
                obj.setValue(rtval)

        for i in xrange(len(argVals)):
            arg = self.args[i]
            argName = arg.name.getSimpleType()
            argDataType = arg.dataType.getSimpleType()
            argConnectionType = arg.connectionType.getSimpleType()

            if argConnectionType != 'in':
                if argDataType.endswith('[]'):
                    for j in xrange(len(argVals[i])):
                        setRTVal(self.outputs[argName][j], argVals[i][j])
                else:
                    setRTVal(self.outputs[argName], argVals[i])

        return True