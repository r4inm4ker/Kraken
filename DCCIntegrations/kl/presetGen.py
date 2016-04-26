import os
import sys

os.environ['KRAKEN_DCC'] = 'KL'

args = sys.argv[1:]
if len(args) != 2:
    print "\nPlease provide the rig file to convert and the target folder as command line arguments."
    exit(1)

from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.core.objects.rig import Rig

guideRig = Rig()
guideRig.loadRigDefinitionFile(args[0])

rig = Rig()
rig.loadRigDefinition(guideRig.getRigBuildData())

builder = plugins.getBuilder()
builder.setOutputFolder(args[1])

config = builder.getConfig()

config.setMetaData('RigTitle', os.path.split(args[0])[1].partition('.')[0])
config.setMetaData('SetupDebugDrawing', True)
config.setMetaData('CollapseComponents', False)
config.setMetaData('AddCollectJointsNode', True)

builder.buildRig(rig)

