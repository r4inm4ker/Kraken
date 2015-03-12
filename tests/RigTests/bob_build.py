from kraken import plugins
from bob_rig import Rig

bobRig = Rig("char_bob")

builder = plugins.getBuilder()
builder.build(bobRig)