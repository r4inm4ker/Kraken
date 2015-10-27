"""Kraken - objects.operators.kl_operator module.

Classes:
CanvasOperator - Splice operator object.

"""
import json
from kraken.core.maths import Mat44
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.operators.operator import Operator
from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.kraken_system import ks


class CanvasOperator(Operator):
    """Splice Operator representation."""

    # TODO: Look in to expanding the Splice operator to be able to handle more
    # than one extension / operator. Need to change extension to extensions and
    # figure out how to differentiate the solver types per operator. Maybe have
    # an attirbute array called 'klOperators' that contains sets of what we
    # currently have setup.

    def __init__(self, name, canvasPresetName):
        super(CanvasOperator, self).__init__(name)

        self.canvasPresetName = canvasPresetName

        # Load the Fabric Engine client and construct the RTVal for the Solver
        host = ks.getCoreClient().DFG.host


        def getPresetDesc(path):
            fileContents = open( host.getPresetImportPathname(path) ).read()
            fileContents = "".join(fileContents.split('\n'))
            fileContents = "  ".join(fileContents.split('\t'))
            return json.loads(fileContents)
        self.graphDesc = getPresetDesc(self.canvasPresetName)

        # Initialize the inputs and outputs based on the given args.
        for port in self.graphDesc['ports']:
            portName = port['name']
            portConnectionType = port['execPortType']
            if 'typeSpec' in port:
                portDataType = port['typeSpec']
            else:
                portDataType = '$TYPE$'

            if portConnectionType == 'In':
                if portDataType.endswith('[]'):
                    self.inputs[portName] = []
                else:
                    self.inputs[portName] = None
            else:
                if portDataType.endswith('[]'):
                    self.outputs[portName] = []
                else:
                    self.outputs[portName] = None


    def getPresetTypeName(self):
        """Returns the solver type name for this operator.

        Returns:
            str: Name of the solver type this operator uses.

        """

        return self.canvasGraphName


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


    def evaluate(self):
        """invokes the Splice operator causing the output values to be computed.

        Returns:
            bool: True if successful.

        """

        def getRTVal(obj):
            if isinstance(obj, Object3D):
                return obj.xfo.getRTVal().toMat44('Mat44')
            elif isinstance(obj, Attribute):
                return obj.getRTVal()

        portVals = []
        for port in self.graphDesc['ports']:
            portName = port['name']
            portConnectionType = port['execPortType']
            portDataType = port['typeSpec']

            if portDataType == '$TYPE$':
                return

            if portDataType == 'EvalContext':
                portVals.append(ks.constructRTVal(portDataType))
                continue
            if portName == 'time':
                portVals.append(ks.constructRTVal(portDataType))
                continue
            if portName == 'frame':
                portVals.append(ks.constructRTVal(portDataType))
                continue

            if portConnectionType == 'In':
                if str(portDataType).endswith('[]'):
                    rtValArray = ks.rtVal(portDataType[:-2]+'Array')
                    rtValArray.resize(len(self.inputs[portName]))
                    for j in xrange(len(self.inputs[portName])):
                        rtValArray[j] = getRTVal(self.inputs[portName][j])
                    portVals.append(rtValArray)
                else:
                    portVals.append(getRTVal(self.inputs[portName]))
            else:
                if str(portDataType).endswith('[]'):
                    rtValArray = ks.rtVal(portDataType[:-2]+'Array')
                    rtValArray.resize(len(self.outputs[portName]))
                    for j in xrange(len(self.outputs[portName])):
                        rtValArray[j] = getRTVal(self.outputs[portName][j])
                    portVals.append(rtValArray)
                else:
                    portVals.append(getRTVal(self.outputs[portName]))


        host = ks.getCoreClient().DFG.host
        binding = host.createBindingToPreset(self.canvasPresetName, portVals)
        binding.execute()

        # Now put the computed values out to the connected output objects.
        def setRTVal(obj, rtval):
            if isinstance(obj, Object3D):
                obj.xfo.setFromMat44(Mat44(rtval))
            elif isinstance(obj, Attribute):
                obj.setValue(rtval)

        for port in self.graphDesc['ports']:
            portName = port['name']
            portConnectionType = port['execPortType']
            portDataType = '$TYPE$'

            if portConnectionType != 'In':
                outVal = binding.getArgValue(portName)
                if portDataType.endswith('[]'):
                    for j in xrange(len(outVal)):
                        setRTVal(self.outputs[portName][j], outVal[j])
                else:
                    setRTVal(self.outputs[portName], outVal)

        return True