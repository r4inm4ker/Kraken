from kraken.core.objects.containers import *
from kraken.core.components import arm
from kraken.core import assembler
import json

assembler = assembler.Assembler()
container = Container("MyContainer")
assembler.container = container
armLCmp = arm.ArmComponent("arm_L", "L", parent=None)

container.addComponent(armLCmp)

print json.dumps(assembler.buildDef(), indent=4)