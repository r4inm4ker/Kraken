from kraken.core.maths import *
from kraken.core.maths import decodeValue


tr = Vec3(32,35,234)
sc = Vec3(2.3,2.3,2.3)
xfo = Xfo(tr=tr, sc=sc)
jsonData = xfo.jsonEncode()
print "Xfo:" + str(jsonData)

xfo2 = Xfo()
xfo2.jsonDecode(jsonData, decodeValue)
print "Xfo2:" + str(xfo2)

xfo3 = decodeValue(jsonData)
print "Xfo3:" + str(xfo2)