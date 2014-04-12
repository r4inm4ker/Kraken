import json

from kraken.kraken_core import serialize
from kraken.core.objects import elements

from kraken.core.maths import mathUtils
from kraken.core.maths import vec
from kraken.core.maths import rotation
from kraken.core.maths import matrix
from kraken.core.maths import xfo
reload(mathUtils)
reload(vec)
reload(rotation)
reload(matrix)
reload(xfo)

#myXfo = xfo.Xfo()
#jsonData = json.dumps(myXfo, cls=encode.KrakenJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
#print jsonData

myNull = elements.Null("myNull")
jsonData = json.dumps(myNull, cls=encode.KrakenJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
print jsonData