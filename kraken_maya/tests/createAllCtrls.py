from kraken.core.objects import elements
from kraken.kraken_maya.objects import elements

for eachItem in elements.Control.shapes.keys():
    ctrl = elements.Control(eachItem, eachItem)
    ctrl.build()