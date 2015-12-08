import json
import os

from kraken import plugins
from kraken.core.objects.rig import Rig
from kraken_examples.bob_guide_data import bob_guide_data
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("bob_build")

bobGuideRig = Rig("char_bob")
bobGuideRig.loadRigDefinition(bob_guide_data)

bobGuideRig.writeRigDefinitionFile('bob_guide.krg')

bobGuideRig2 = Rig()
bobGuideRig2.loadRigDefinitionFile('bob_guide.krg')

logHierarchy(bobGuideRig2)

os.remove('bob_guide.krg')