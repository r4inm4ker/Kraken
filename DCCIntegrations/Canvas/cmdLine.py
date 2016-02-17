import sys

args = sys.argv[1:]
if len(args) != 2:
    print "\nPlease provide the rig file to convert and the target canvas file as command line arguments."
    exit(1)

from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.core.objects.rig import Rig

guideRig = Rig()
guideRig.loadRigDefinitionFile(args[0])

rig = Rig()
rig.loadRigDefinition(guideRig.getRigBuildData())

builder = plugins.getBuilder()
builder.setOutputFilePath(args[1])

config = builder.getConfig()
config.setExplicitNaming(True)

builder.build(rig)

