from kraken import plugins
from kraken.core.maths import *
from kraken.core.objects.control import Control


builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

nullControl = Control("NullControl", shape="null")
nullControl.rotatePoints(0, 45, 0)
nullControl.scalePoints(Vec3(3, 3, 3))
nullControl.translatePoints(Vec3(0, 1, 0.25))
nullControl.xfo.tr = Vec3(0.0, 1.0, 0.0)

builder.build(nullControl)
