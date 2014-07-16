from kraken.tests.bob_rig import Rig
from kraken.plugins.maya_plugin.builder import Builder

bobRig = Rig("char_bob")

builder = Builder()
builder.build(bobRig)