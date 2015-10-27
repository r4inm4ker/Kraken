import os, sys



# fabricEngineDir=os.path.normpath("D:/temp/FabricEngine-2.0.0-Windows-x86_64/")
# # fabricEngineDir=os.path.normpath("D:/temp/FabricEngine-1.15.2-Windows-x86_64/")

# os.environ['PATH'] = os.path.join(fabricEngineDir, 'bin') + ';' + os.environ['PATH']
# os.environ['FABRIC_DFG_PATH'] = os.path.join(fabricEngineDir, 'Presets', 'DFG')

# PYTHON_VERSION = sys.version[:3]
# sys.path.append( os.path.join(fabricEngineDir, 'Python', PYTHON_VERSION ) )

# ##############################

# krakenDir = os.path.dirname(os.path.realpath(__file__))
# # krakenDir=os.path.abspath(os.path.join(krakenModuleDir, '..', '..'))


# os.environ['KRAKEN_PATH']  = krakenDir

# os.environ['FABRIC_EXTS_PATH'] = os.path.join(fabricEngineDir, 'Exts') + ';' + os.path.join(krakenDir, 'KLExts') + ';' + os.environ['FABRIC_EXTS_PATH']

# os.environ['KRAKEN_PATHS'] = os.path.join(krakenDir, 'extraComponents')


# os.environ['PYTHONPATH'] = os.path.join(krakenDir, 'Python') + ';' + os.environ['PYTHONPATH']


# canvasPresetsDir = os.path.join(krakenDir, 'CanvasPresets')
# os.environ['FABRIC_DFG_PATH'] = canvasPresetsDir + ';' + os.environ['FABRIC_DFG_PATH']
# ##############################


# print os.environ['FABRIC_DFG_USER_PATH']
print os.environ['FABRIC_DFG_PATH']

#addPresetDir

import FabricEngine.Core, json
client = FabricEngine.Core.createClient()
host = client.DFG.host

# host.addPresetDir('', 'Kraken', os.path.join(krakenDir, 'CanvasPresets'))

print host.getPresetDesc('Kraken')

# def getPresetDesc(path):
#     fileContents = open( host.getPresetImportPathname(path) ).read()
#     fileContents = "".join(fileContents.split('\n'))
#     fileContents = "  ".join(fileContents.split('\t'))
#     return json.loads(fileContents)

# addNode = getPresetDesc('Fabric.Core.Math.Add')
# for port in addNode['ports']:
#     print port['name']

# # turbulizeVec3Node = getPresetDesc('Fabric.Compounds.Deform.TurbulizeVec3')
# # for port in turbulizeVec3Node['ports']:
# #     print port['name'] + ":" + port['execPortType'] + ":" + port["typeSpec"]

# # print json.dumps(json.loads(str(open( host.getPresetImportPathname('Fabric.Core.Math.Add') ).read())))
# # print json.dumps(json.loads(host.getPresetDesc('Fabric.Core.Math.Add')), indent=1, sort_keys=True)


# def displayMsg(path, jsonMsg):
#   print "Notif on '" + path + "': " + jsonMsg

# binding = host.createBindingToNewGraph()
# # binding.setNotificationCallback(bindingDisplayMsg)
# rootExec = binding.getExec()
# rootView = rootExec.createView(lambda jsonMsg: displayMsg('', jsonMsg))

# binding = host.createBindingToPreset('Fabric.Core.Math.Add', [42, 45, 0])
# binding.execute()
# binding.setArgValue("lhs", client.RT.types.Float32(5.67))
# print binding.getArgValue("result")


# addInstFromPreset
client.close()
