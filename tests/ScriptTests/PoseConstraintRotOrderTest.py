from kraken import plugins
from kraken.core.maths import RotationOrder
from kraken.core.maths import Vec3
from kraken.core.maths import Math_degToRad
from kraken.core.objects.locator import Locator

parentLoc = Locator('parent')

for i in xrange(0, 6):
    print i
    rotOrderStrMap = {
        0: 'XYZ',
        1: 'YZX',
        2: 'ZXY',
        3: 'XZY',
        4: 'ZYX',
        5: 'YXZ'
    }

    srcLoc = Locator(rotOrderStrMap[i] + '_src', parent=parentLoc)

    srcLoc.xfo.tr.x = i * 2
    srcLoc.xfo.tr.y = 0
    srcLoc.xfo.tr.z = 0

    tgtLoc = Locator(rotOrderStrMap[i] + '_tgt', parent=parentLoc)
    tgtLoc.ro = RotationOrder(i)

    tgtLoc.xfo.tr.x = i * 2
    tgtLoc.xfo.tr.y = 0
    tgtLoc.xfo.tr.z = 0

    tgtLoc.xfo.ori.setFromEulerAngles(Vec3(Math_degToRad(90.0),
                                           Math_degToRad(0.0),
                                           Math_degToRad(0.0)))

    constraint = tgtLoc.constrainTo(srcLoc, 'Pose', True, 'PoseConstraint')


builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

builder.build(parentLoc)
