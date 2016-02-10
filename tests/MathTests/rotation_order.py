import json

from kraken.core.maths import *

print "=============="
print "Instance Test"
print "=============="
rotOrder = RotationOrder()
print "RotationOrder: " + str(rotOrder)
print "order: " + str(rotOrder.order)
print ""

print "\n========="
print "Is Tests"
print "========="
xyzRotationOrder = RotationOrder(0)
print "RotationOrder: " + str(xyzRotationOrder)
print "Order is XYZ: " + str(xyzRotationOrder.isXYZ())
print "Is in (XZY, ZYX or YXZ): " + str(xyzRotationOrder.isReversed())
print ""

yzxRotationOrder = RotationOrder(1)
print "RotationOrder: " + str(yzxRotationOrder)
print "Order is YZX: " + str(yzxRotationOrder.isYZX())
print "Is in (XZY, ZYX or YXZ): " + str(yzxRotationOrder.isReversed())
print ""

zxyRotationOrder = RotationOrder(2)
print "RotationOrder: " + str(zxyRotationOrder)
print "Order is ZXY: " + str(zxyRotationOrder.isZXY())
print "Is in (XZY, ZYX or YXZ): " + str(zxyRotationOrder.isReversed())
print ""

xzyRotationOrder = RotationOrder(3)
print "RotationOrder: " + str(xzyRotationOrder)
print "Order is XZY: " + str(xzyRotationOrder.isXZY())
print "Is in (XZY, ZYX or YXZ): " + str(xzyRotationOrder.isReversed())
print ""

zyxRotationOrder = RotationOrder(4)
print "RotationOrder: " + str(zyxRotationOrder)
print "Order is ZYX: " + str(zyxRotationOrder.isZYX())
print "Is in (XZY, ZYX or YXZ): " + str(zyxRotationOrder.isReversed())
print ""

yxzRotationOrder = RotationOrder(5)
print "RotationOrder: " + str(yxzRotationOrder)
print "Order is YXZ: " + str(yxzRotationOrder.isYXZ())
print "Is in (XZY, ZYX or YXZ): " + str(yxzRotationOrder.isReversed())
print ""

print "\n=========="
print "String Tests"
print "==========="
xyzRotationOrder = RotationOrder('YXZ')
print "RotationOrder: " + str(xyzRotationOrder)
print "Order is YXZ: " + str(xyzRotationOrder.isYXZ())
print ""


print "\n=========="
print "Set Tests"
print "=========="

utilOrder = RotationOrder()
print "RotationOrder: " + str(utilOrder)
utilOrder.setXYZ()
print "Order is XYZ: " + str(utilOrder.isXYZ())
print ""

print "RotationOrder: " + str(utilOrder)
utilOrder.setYZX()
print "Order is YZX: " + str(utilOrder.isYZX())
print ""

print "RotationOrder: " + str(utilOrder)
utilOrder.setZXY()
print "Order is ZXY: " + str(utilOrder.isZXY())
print ""

print "RotationOrder: " + str(utilOrder)
utilOrder.setXZY()
print "Order is XZY: " + str(utilOrder.isXZY())
print ""

print "RotationOrder: " + str(utilOrder)
utilOrder.setZYX()
print "Order is ZYX: " + str(utilOrder.isZYX())
print ""

print "RotationOrder: " + str(utilOrder)
utilOrder.setYXZ()
print "Order is YXZ: " + str(utilOrder.isYXZ())

print "equal:" + str(xyzRotationOrder == yzxRotationOrder)
print "not equal:" + str(xyzRotationOrder != yzxRotationOrder)