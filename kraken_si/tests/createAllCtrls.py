from kraken.objects import elements
from kraken.kraken_si.utils import *
from kraken.kraken_si.objects import elements

for eachItem in elements.Control.shapes.keys():
    ctrl = elements.Control(eachItem, eachItem)
    ctrl.build()