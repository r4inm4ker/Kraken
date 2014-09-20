from kraken import plugins
from kraken.tests.RigTests.bob_rig import Rig

bobRig = Rig("char_bob")

builder = plugins.getBuilder()
builder.build(bobRig)