import json

from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat
from kraken.core.objects.container import Container
from kraken.examples.arm_component import ArmComponentGuide, ArmComponent
from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


def buildArm(mode='guide'):

    Profiler.getInstance().push("arm_build")

    guideContainer = Container('armGuide')

    armGuide = ArmComponentGuide("arm", parent=guideContainer)
    armGuide.loadData({
            "name": "L_Arm",
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        })

    if mode == 'guide':
        builder = plugins.getBuilder()
        builder.build(guideContainer)

    elif mode == 'rig':
        synchronizer = plugins.getSynchronizer()
        synchronizer.setTarget(guideContainer)
        synchronizer.sync()

        armGuideData = armGuide.getGuideData()

        rigContainer = Container('armRig')
        arm = ArmComponent(parent=rigContainer)
        arm.loadData(armGuideData)

        builder = plugins.getBuilder()
        builder.build(rigContainer)
    else:
        LogMessage('Invalid mode set')

    Profiler.getInstance().pop()

    if __name__ == "__main__":
        print Profiler.getInstance().generateReport()
    else:
        if mode == 'guide':
            logHierarchy(armGuide)
        elif mode == 'rig':
            logHierarchy(arm)

# Run once in guide mode, then in rig mode.
# Delete Rig Hierarchy
# Move guide objects
# Run in rig mode
buildArm(mode='guide')