from kraken.tests import arm_component
reload(arm_component)

from kraken.tests import arm_rig
reload(arm_rig)

from kraken.tests.arm_rig import ArmRig
from kraken.core import builders


from kraken.core.builders import si_builder
reload(si_builder)

from kraken.core.builders.si_builder import SIBuilder

myArm = ArmRig("myArm")

siBuilder = SIBuilder()
siBuilder.build(myArm)