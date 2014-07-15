from kraken.tests import arm_component
from kraken.tests import arm_rig

from kraken.tests.arm_rig import ArmRig

from kraken.plugins.si_plugin import builder
reload(builder)

from kraken.plugins.si_plugin.builder import Builder

myArm = ArmRig("myArm")

builder = Builder()
builder.build(myArm)

# Editing happens here....

# now we can save out a preset....
json = myArm.save()

# delte the guide/go to a new scene.

builder = Builder()
builder.build(json)
