from kraken.tests import arm_component
from kraken.tests import arm_rig
from kraken.tests.arm_rig import ArmRig

from kraken.core.builders import base_builder
reload(base_builder)

from kraken.core.builders.base_builder import BaseBuilder


myArm = ArmRig("myArm")

builder = BaseBuilder()
builder.build(myArm)