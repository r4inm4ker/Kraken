"""Kraken - objects.operators.splice_operator module.

Classes:
SpliceOperator - Splice operator object.

"""

from kraken.core.maths import Mat44
from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.operators.base_operator import BaseOperator
from kraken.core.objects.attributes.base_attribute import BaseAttribute
from kraken.core.kraken_system import ks

class SpliceOperator(BaseOperator):
    """Base Operator representation."""

    # TODO: Look in to expanding the Splice operator to be able to handle more
    # than one extension / operator. Need to change extension to extensions and
    # figure out how to differentiate the solver types per operator. Maybe have
    # an attirbute array called 'klOperators' that contains sets of what we
    # currently have setup.

    def __init__(self, name, solverTypeName, extension):
        super(SpliceOperator, self).__init__(name)

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
            if arg.connectionType == 'in':
                if str(arg.dataType).endswith('[]'):
                    self.inputs[arg.name] = []
                else:
                    self.inputs[arg.name] = None
            else:
                if str(arg.dataType).endswith('[]'):
                    self.outputs[arg.name] = []
                else:
                    self.outputs[arg.name] = None

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

    def getSolverArgs(self):
        """Returns the args array defined by the KL Operator.

        Return:
        RTValArray, args array defined by the KL Operator.

        """

        # Get the args from the solver KL object.
        return self.args

    def generateSourceCode(self, arraySizes={}):
        """Returns the source code for a stub operator that will invoke the KL operator

        Return:
        String, The source code for the stub operator.

        """

        # Start constructing the source code.
        opSourceCode = ""
        opSourceCode += "require Kraken;\n"
        opSourceCode += "require " + self.getExtension() + ";\n\n"
        opSourceCode += "operator " + self.getName() + "(\n"

        opSourceCode += "    io " + self.solverTypeName + " solver,\n"

        # In SpliceMaya, output arrays are not resized by the system prior to calling into Splice, so we
        # explicily resize the arrays in the generated operator stub code. 
        arrayResizing = "";
        for argName, arraySize in arraySizes.iteritems():
            arrayResizing += "    "+argName+".resize("+str(arraySize)+");\n"

        functionCall = "    solver.solve("
        for i in xrange(len(self.args)):
            arg = self.args[i]
            # Connect the ports to the inputs/outputs in the rig.
            if arg.connectionType == 'out':
                outArgType = 'io' 
            else:
                outArgType = arg.connectionType
            suffix = ""
            outDataType = arg.dataType
            if outDataType.endswith('[]'):
                outDataType = outDataType[:-2]
                suffix = "[]"
            opSourceCode += "    " + outArgType + " " + outDataType + " " + arg.name + suffix
            if i == len(self.args) - 1:
                opSourceCode += "\n"
            else:
                opSourceCode += ",\n"

            if i == len(self.args) - 1:
                functionCall += arg.name
            else:
                functionCall += arg.name + ", "
        functionCall += ");\n"

        opSourceCode += "    )\n"
        opSourceCode += "{\n"
        opSourceCode += arrayResizing
        opSourceCode += functionCall
        opSourceCode += "}\n"

        return opSourceCode

    def evaluate(self):
        """Returns the source code for a stub operator that will invoke the KL operator

        Return:
        String, The source code for the stub operator.

        """
        def getRTVal(obj):
            if isinstance(obj, SceneItem):
                return obj.xfo.getRTVal().toMat44('Mat44')
            elif isinstance(obj, BaseAttribute):
                return obj.getRTVal()

        argVals = []
        for i in xrange(len(self.args)):
            arg = self.args[i]
            if arg.connectionType == 'in':
                if str(arg.dataType).endswith('[]'):
                    rtValArray = ks.rtVal(arg.dataType[:-2]+'Array')
                    rtValArray.resize(len(self.inputs[arg.name]))
                    for j in xrange(len(self.inputs[arg.name])):
                        rtValArray[j] = getRTVal(self.inputs[arg.name][j])
                    argVals.append(rtValArray)
                else:
                    argVals.append(getRTVal(self.inputs[arg.name]))
            else:
                if str(arg.dataType).endswith('[]'):
                    rtValArray = ks.rtVal(arg.dataType[:-2]+'Array')
                    rtValArray.resize(len(self.outputs[arg.name]))
                    for j in xrange(len(self.outputs[arg.name])):
                        rtValArray[j] = getRTVal(self.outputs[arg.name][j])
                    argVals.append(rtValArray)
                else:
                    argVals.append(getRTVal(self.outputs[arg.name]))

        self.solverRTVal.solve('', *argVals)

        # Now put the computed values out to the connected output objects.
        def setRTVal(obj, rtval):
            if isinstance(obj, SceneItem):
                obj.xfo.setFromMat44(Mat44(rtval))
            elif isinstance(obj, BaseAttribute):
                obj.setValue(rtval)

        for i in xrange(len(argVals)):
            arg = self.args[i]
            if arg.connectionType != 'in':
                if str(arg.dataType).endswith('[]'):
                    for j in xrange(len(argVals[i])):
                        setRTVal(self.outputs[arg.name][j], argVals[i][j])
                else:
                    setRTVal(self.outputs[arg.name], argVals[i])
