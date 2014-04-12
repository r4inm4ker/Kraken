from kraken.core.maths import vec
from kraken.core.maths import rotation
from kraken.core.maths.mathUtils import *
from kraken.core.objects import elements
from kraken.kraken_maya.objects import elements

parentNull = elements.Null("parentNull")
parentNull.visibility = False
parentNull.setGlobalTranslation(vec.Vec3(0,10,0))
parentNull.setLocalRotation(rotation.Euler(0,degToRad(10),0))

childNull = elements.Null("childNull", parentNull)
childNull.visibility = True

parentNull.build()