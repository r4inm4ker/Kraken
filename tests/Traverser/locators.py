from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.core.traverser.traverser import Traverser

locA = Locator("locatorA")
locB = Locator("locatorB", parent = locA)
locC = Locator("locatorC", parent = locB)
locD = Locator("locatorD", parent = locB)

trav = Traverser()
trav.addRootItem(locD)
trav.addRootItem(locC)

def callback(**args):
    item = args.get('item', None)
    print 'Visited '+item.getDecoratedPath()

trav.traverse(itemCallback = callback)
