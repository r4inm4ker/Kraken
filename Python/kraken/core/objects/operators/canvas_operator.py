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

    def __init__(self, name, canvasPresetPath):
        super(CanvasOperator, self).__init__(name)

        self.canvasPresetPath = canvasPresetPath

        # Note: this is a temporary solution to getting the descritption of a Canvas node.
        # I beleive that the API does provide a method to retrieve the node desc, but I couldn't find it.
        def getPresetDesc(path):

            fileContents = ""
            with open(ks.getCoreClient().DFG.host.getPresetImportPathname(path), 'r') as presetFile:
                fileContents = presetFile.read()
                fileContents = "".join(fileContents.split('\n'))
                fileContents = "".join(fileContents.split('\r'))
                fileContents = "  ".join(fileContents.split('\t'))

            return json.loads(fileContents)

        self.graphDesc = getPresetDesc(self.canvasPresetPath)

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


    def getPresetPath(self):
        """Returns the preset path within the Canvas library for the node used by this operator.

        Returns:
            str: Path of the preset files used by this operator.

        """

        return self.canvasPresetPath


    def getGraphDesc(self):
        """Returns the json description of the node used by this operator

        Returns:
            object: A json dict containing the description the operator.

        """

        return self.graphDesc


    def evaluate(self):
        """invokes the Canvas node causing the output values to be computed.

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
        binding = host.createBindingToPreset(self.canvasPresetPath, portVals)
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