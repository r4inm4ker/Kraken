from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.traverser.traverser import Traverser

locA = Locator("locatorA")
locB = Locator("locatorB")
groupA = AttributeGroup("settings", locA)
groupB = AttributeGroup("settings", locB)
attrA = BoolAttribute('flag', True, groupA)
attrB = BoolAttribute('flag', True, groupB)
attrB.connect(attrA)

trav = Traverser()
trav.addRootItem(attrB)

def callback(**args):
    item = args.get('item', None)
    print 'Visited '+item.getDecoratedPath()

trav.traverse(itemCallback = callback)
