from kraken.kraken_si.utils import *
from kraken.core.objects import elements
from kraken.krake_si.objects import elements

myChain = elements.Chain("myChain", [[0,6,0], [2,3,3], [0,0,0]], None)
myChain.build()