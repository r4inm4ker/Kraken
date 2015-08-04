
import os
import sys


krakenDir = os.path.dirname(os.path.realpath(__file__))
# krakenDir=os.path.abspath(os.path.join(krakenModuleDir, '..', '..'))

fabricEngineDir=os.path.normpath("D:/temp/FabricEngine-1.15.2-Windows-x86_64/")

os.environ['PATH'] = os.path.join(fabricEngineDir, 'bin') + ';' + os.environ['PATH']

PYTHON_VERSION = sys.version[:3]
sys.path.append( os.path.join(fabricEngineDir, 'Python', PYTHON_VERSION ) )

os.environ['FABRIC_EXTS_PATH'] = os.path.join(fabricEngineDir, 'Exts') + ';' + os.path.join(krakenDir, 'KLExts') + ';' + os.environ['FABRIC_EXTS_PATH']

os.environ['KRAKEN_PATHS'] = os.path.join(krakenDir, 'extraComponents')



from kraken import plugins
from kraken.core.maths import Vec3
from kraken_examples.tentacle_component import TentacleComponentGuide, TentacleComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("tentacle_build")

tentacleGuide = TentacleComponentGuide("tentacle")
tentacleGuide.loadData(
                        {
                         "name": "tentacle",
                         "location": "L",
                         "numJoints": 4,
                         "jointPositions": [
                                            Vec3(0.9811, 9.769, -1.237),
                                            Vec3(5.4488, 8.4418, -1.237),
                                            Vec3(4.0, 3.1516, -1.237),
                                            Vec3(6.841, 1.0, -1.237),
                                            Vec3(9.841, 0.0, -1.237)
                                           ]
                        })

# Save the hand guide data for persistence.
saveData = tentacleGuide.saveData()

tentacleGuideData = tentacleGuide.getRigBuildData()

tentacle = TentacleComponentRig()
tentacle.loadData(tentacleGuideData)

builder = plugins.getBuilder()
builder.build(tentacle)

Profiler.getInstance().pop()

if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    logHierarchy(tentacle)