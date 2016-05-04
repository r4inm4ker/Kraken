from kraken import plugins
from kraken.core.maths import Math_degToRad
from kraken.core.maths import Vec3
from kraken.core.objects.locator import Locator

parentLoc = Locator('parent')

locator1 = Locator("locator", parent=parentLoc)

locator1.xfo.tr.x = 3
locator1.xfo.tr.y = -1
locator1.xfo.tr.z = 1

locator2 = Locator("locator2", parent=parentLoc)

locator2.xfo.sc.x = 1
locator2.xfo.sc.y = 2
locator2.xfo.sc.z = 1

locator2.xfo.tr.x = 2
locator2.xfo.tr.y = 5
locator2.xfo.tr.z = 3

locator2.xfo.ori.setFromEulerAngles(Vec3(Math_degToRad(45.0),
                                    Math_degToRad(0.0),
                                    Math_degToRad(0.0)))

constraint = locator2.constrainTo(locator1, 'Orientation', True, 'OrientationConstraint')

builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

builder.build(parentLoc)
