from kraken.tests import arm_component
from kraken.tests import arm_rig

from kraken.tests.arm_rig import ArmRig

from kraken.plugins.si_plugin.builder import SIBuilder
reload(si_builder)

myArm = ArmRig("myArm")

siBuilder = SIBuilder()
siBuilder.build(myArm)