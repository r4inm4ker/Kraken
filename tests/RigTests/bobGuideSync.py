from kraken import plugins
from kraken.core.objects.rig import Rig
from kraken_examples.bob_guide_data import bob_guide_data
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


def buildBob(mode='guide'):

    Profiler.getInstance().push("bob_build")

    bobGuideRig = Rig("char_bob")
    bobGuideRig.loadRigDefinition(bob_guide_data)

    if mode == 'guide':
        builder = plugins.getBuilder()
        builder.build(bobGuideRig)

    elif mode == 'rig':
        synchronizer = plugins.getSynchronizer()
        synchronizer.setTarget(bobGuideRig)
        synchronizer.sync()

        bobRigData = bobGuideRig.getGuideData()
        bobRig = Rig()
        bobRig.loadRigDefinition(bobRigData)

        builder = plugins.getBuilder()
        builder.build(bobRig)

    else:
        print 'Invalid mode set'

    Profiler.getInstance().pop()

    if __name__ == "__main__":
        print Profiler.getInstance().generateReport()
    else:
        if mode == 'guide':
            logHierarchy(bobGuideRig)
        elif mode == 'rig':
            logHierarchy(bobRig)

# Run once in guide mode, then in rig mode.
# Delete Rig Hierarchy
# Move guide objects
# Run in rig mode
buildBob(mode='guide')
