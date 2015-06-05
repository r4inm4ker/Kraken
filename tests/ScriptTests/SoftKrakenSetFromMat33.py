from kraken import plugins
from kraken.core.maths import Vec3
from kraken.core.maths import Quat
from kraken.core.maths import Mat33
from kraken.core.maths import Xfo
from kraken.core.objects.locator import Locator

from kraken.plugins.si_plugin.utils import *


# =============================
# Build Null through Softimage
# =============================
siXfo = XSIMath.CreateTransform()

siMat33 = XSIMath.CreateMatrix3()
siMat33.Set(0.7071, 0.0, 0.7071, 0.5, 0.7071, -0.5, -0.5, 0.7071, 0.50)

siRot = XSIMath.CreateRotation()
siRot.SetFromMatrix3(siMat33)

siXfo.SetRotation(siRot)

siNull = si.ActiveProject3.ActiveScene.Root.AddNull("myNull")
siNull.Kinematics.Global.PutTransform2(None, siXfo)


# =====================
# Build through kraken
# =====================
builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

myXfo = Xfo()

myMat33 = Mat33()
myMat33.setColumns(Vec3(0.7071, 0.0, 0.7071), Vec3(0.5, 0.7071, -0.5), Vec3(-0.5, 0.7071, 0.50))

myQuat = Quat()
newQuat = myQuat.setFromMat33(myMat33)
myXfo.ori = newQuat

myLoc = Locator("myLocator")
myLoc.xfo = myXfo

builder.build(myLoc)
