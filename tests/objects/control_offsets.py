from kraken import plugins
from kraken.core.objects.controls.null_control import NullControl

builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

nullControl = NullControl("NullControl")
nullControl.rotatePoints(0, 0, 90)
nullControl.scalePoints(Vec3(3, 3, 3))
nullControl.translatePoints(Vec3(0, 1, 0.25))
nullControl.xfo.tr = Vec3(0.0, 1.0, 0.0)

builder.build(nullControl)