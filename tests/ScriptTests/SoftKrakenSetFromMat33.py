from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.core.maths.vec3 import Vec3
from kraken.core.maths.quat import Quat
from kraken.core.maths.mat33 import Mat33
from kraken.core.maths.xfo import Xfo


# Build Null through Softimage
si = Application

siXfo = XSIMath.CreateTransform()

siMat33 = XSIMath.CreateMatrix3()
siMat33.Set(0.7071067811865471, 5.551115123125783e-17, 0.7071067811865479, 0.5000000000000003, 0.7071067811865472, -0.4999999999999999, -0.5000000000000002, 0.7071067811865478, 0.4999999999999995)

siRot = XSIMath.CreateRotation()
siRot.SetFromMatrix3(siMat33)

siXfo.SetRotation(siRot)

siNull = si.ActiveProject3.ActiveScene.Root.AddNull("myNull")
siNull.Kinematics.Global.PutTransform2(None, siXfo)


# ====================================================

# Build through kraken
builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

myXfo = Xfo()

myMat33 = Mat33()
myMat33.setColumns(Vec3(0.7071067811865471, 5.551115123125783e-17, 0.70710678118654791), Vec3(0.5000000000000003, 0.7071067811865472, -0.4999999999999999), Vec3(-0.5000000000000002, 0.7071067811865478, 0.4999999999999995))

myQuat = Quat()
newQuat = myQuat.setFromMat33(myMat33)
myXfo.ori = newQuat

myLoc = Locator("myLocator")
myLoc.xfo = myXfo

builder.build(myLoc)