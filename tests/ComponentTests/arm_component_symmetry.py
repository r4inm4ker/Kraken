from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat

from kraken_components.biped.arm_component import ArmComponentGuide, ArmComponentRig

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


Profiler.getInstance().push("arm_component_symmetry")

leftArmGuide = ArmComponentGuide('arm')
leftArmGuide.loadData({
    'name': 'Arm',
    'location': 'L',
    'bicepXfo': Xfo(Vec3(2.27, 15.295, -0.753)),
    'forearmXfo': Xfo(Vec3(5.039, 13.56, -0.859)),
    'wristXfo': Xfo(Vec3(7.1886, 12.2819, 0.4906)),
    'handXfo': Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                   ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
    'bicepFKCtrlSize': 1.75,
    'forearmFKCtrlSize': 1.5
})

# Save the arm guid data for persistence.
rightArmGuide = ArmComponentGuide('arm')
rightArmGuide.setLocation('R')

rightArmGuide.pasteData(leftArmGuide.copyData(), setLocation=False)

builder = plugins.getBuilder()
builder.build(leftArmGuide)
builder.build(rightArmGuide)


armLeft = ArmComponentRig()
armLeft.loadData(leftArmGuide.getRigBuildData())

armRight = ArmComponentRig()
armRight.loadData(rightArmGuide.getRigBuildData())

builder.build(armLeft)
builder.build(armRight)

Profiler.getInstance().pop()


if __name__ == "__main__":
    print Profiler.getInstance().generateReport()
else:
    print '==armLeft=='
    for each in armLeft.getItems().values():
        # Only log hierarchy for Layer objects as Layers in this test are added to
        # the component since there is no rig object.
        if each.isTypeOf('Layer'):
            logHierarchy(each)

    print '==armRight=='
    for each in armRight.getItems().values():
        # Only log hierarchy for Layer objects as Layers in this test are added to
        # the component since there is no rig object.
        if each.isTypeOf('Layer'):
            logHierarchy(each)
