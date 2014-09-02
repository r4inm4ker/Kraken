from kraken import plugins
from kraken.tests.bob_rig import Rig

bobRig = Rig("char_bob")

builder = plugins.getBuilder()
builder.build(bobRig)